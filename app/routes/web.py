"""
Web routes for the cancer data visualization application.
"""
from flask import Blueprint, render_template, request
from app.services.data import DataService
from app.services.visualization import VisualizationService
import logging

logger = logging.getLogger(__name__)

def create_web_routes(data_service: DataService, viz_service: VisualizationService) -> Blueprint:
    """Create and configure web routes."""
    
    web_bp = Blueprint('web', __name__)
    
    @web_bp.route('/')
    def index():
        """Main dashboard page."""
        try:
            # Get basic data for dropdowns
            states = data_service.get_states_list()
            cancer_types = data_service.get_cancer_types()
            years_range = data_service.get_years_range()
            
            return render_template('dashboard.html',
                                 states=states,
                                 cancer_types=cancer_types,
                                 years_range=years_range)
        except Exception as e:
            logger.error(f"Error loading dashboard: {e}")
            return render_template('error.html', error=str(e)), 500
    
    @web_bp.route('/choropleth')
    def choropleth():
        """Choropleth map visualization."""
        try:
            metric = request.args.get('metric', 'mortality_count')
            
            # Get merged geographical data
            gdf = data_service.get_merged_geo_data(metric=metric)
            
            if gdf is None:
                return "<p>Error: Could not load geographical data</p>", 500
            
            # Create choropleth map
            map_html = viz_service.create_choropleth_map(
                gdf, 
                metric, 
                f"Cancer {metric.replace('_', ' ').title()} by State"
            )
            
            return map_html
            
        except Exception as e:
            logger.error(f"Error creating choropleth: {e}")
            return f"<p>Error creating choropleth map: {e}</p>", 500
    
    @web_bp.route('/plot/<state>')
    def plot_state(state: str):
        """Time series plot for a specific state."""
        try:
            metric = request.args.get('metric', 'mortality_rate')
            cancer_type = request.args.get('cancer_type')
            
            # Get data for the state
            data = data_service.get_cancer_data(state=state, cancer_type=cancer_type)
            
            if data.empty:
                return f"<p>No data found for {state}</p>", 404
            
            # Group by year and calculate mean
            if cancer_type:
                plot_data = data.groupby('year')[metric].mean().reset_index()
                title = f"{metric.replace('_', ' ').title()} in {state} - {cancer_type}"
            else:
                plot_data = data.groupby('year')[metric].mean().reset_index()
                title = f"Average {metric.replace('_', ' ').title()} in {state}"
            
            # Create line plot
            plot_html = viz_service.create_line_plot(
                plot_data,
                'year',
                metric,
                title=title
            )
            
            return plot_html
            
        except Exception as e:
            logger.error(f"Error creating plot for {state}: {e}")
            return f"<p>Error creating plot: {e}</p>", 500
    
    @web_bp.route('/comparison')
    def comparison():
        """Comparison visualization between states/cancer types."""
        try:
            states = request.args.getlist('states')
            cancer_type = request.args.get('cancer_type')
            metric = request.args.get('metric', 'mortality_rate')
            year = request.args.get('year', type=int)
            
            if not states:
                return "<p>Please select at least one state for comparison</p>", 400
            
            # Get data for selected states
            all_data = []
            for state in states:
                data = data_service.get_cancer_data(
                    state=state,
                    cancer_type=cancer_type,
                    year=year
                )
                all_data.append(data)
            
            if not all_data or all(df.empty for df in all_data):
                return "<p>No data found for selected criteria</p>", 404
            
            # Combine all data
            import pandas as pd
            combined_data = pd.concat(all_data, ignore_index=True)
            
            if year:
                # Bar chart for specific year
                grouped_data = combined_data.groupby('state')[metric].mean().reset_index()
                title = f"{metric.replace('_', ' ').title()} Comparison ({year})"
                chart_html = viz_service.create_bar_chart(
                    grouped_data,
                    'state',
                    metric,
                    title=title
                )
            else:
                # Line chart over time
                grouped_data = combined_data.groupby(['year', 'state'])[metric].mean().reset_index()
                title = f"{metric.replace('_', ' ').title()} Comparison Over Time"
                chart_html = viz_service.create_line_plot(
                    grouped_data,
                    'year',
                    metric,
                    color_column='state',
                    title=title
                )
            
            return chart_html
            
        except Exception as e:
            logger.error(f"Error creating comparison: {e}")
            return f"<p>Error creating comparison: {e}</p>", 500
    
    @web_bp.route('/heatmap')
    def heatmap():
        """Heatmap visualization."""
        try:
            metric = request.args.get('metric', 'mortality_rate')
            cancer_type = request.args.get('cancer_type')
            
            # Get data
            data = data_service.get_cancer_data(cancer_type=cancer_type)
            
            if data.empty:
                return "<p>No data available for heatmap</p>", 404
            
            # Create heatmap
            title = f"{metric.replace('_', ' ').title()} Heatmap"
            if cancer_type:
                title += f" - {cancer_type}"
            
            heatmap_html = viz_service.create_heatmap(
                data,
                'year',
                'state',
                metric,
                title=title
            )
            
            return heatmap_html
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return f"<p>Error creating heatmap: {e}</p>", 500
    
    return web_bp
