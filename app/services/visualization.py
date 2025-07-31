"""
Visualization service module for creating charts and maps.
"""
import plotly.express as px
import plotly.graph_objects as go
import folium
import pandas as pd
import geopandas as gpd
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class VisualizationService:
    """Service class for creating visualizations."""
    
    @staticmethod
    def create_choropleth_map(gdf: gpd.GeoDataFrame, 
                             metric_column: str,
                             title: str = "Cancer Data by State") -> str:
        """Create a choropleth map using Folium."""
        try:
            # Create base map centered on Australia
            m = folium.Map(location=[-25, 135], zoom_start=4)
            
            # Add choropleth layer
            choropleth = folium.Choropleth(
                geo_data=gdf,
                data=gdf,
                columns=["name", metric_column],
                key_on="feature.properties.name",
                fill_color='YlOrRd',
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=title,
                nan_fill_color="lightgray"
            ).add_to(m)
            
            # Add tooltips
            for idx, row in gdf.iterrows():
                if pd.notna(row[metric_column]):
                    folium.Marker(
                        location=[row.geometry.centroid.y, row.geometry.centroid.x],
                        popup=f"{row['name']}: {row[metric_column]:.1f}",
                        icon=folium.Icon(color='blue', size='small')
                    ).add_to(m)
            
            return m._repr_html_()
            
        except Exception as e:
            logger.error(f"Error creating choropleth map: {e}")
            return f"<p>Error creating map: {e}</p>"
    
    @staticmethod
    def create_line_plot(df: pd.DataFrame,
                        x_column: str,
                        y_column: str,
                        color_column: Optional[str] = None,
                        title: str = "Time Series Plot") -> str:
        """Create a line plot using Plotly."""
        try:
            if df.empty:
                return "<p>No data available for visualization</p>"
            
            fig = px.line(
                df,
                x=x_column,
                y=y_column,
                color=color_column,
                title=title,
                labels={
                    x_column: x_column.replace('_', ' ').title(),
                    y_column: y_column.replace('_', ' ').title()
                }
            )
            
            fig.update_layout(
                title_x=0.5,
                template="plotly_white",
                hovermode='x unified'
            )
            
            return fig.to_html(full_html=False, include_plotlyjs='cdn')
            
        except Exception as e:
            logger.error(f"Error creating line plot: {e}")
            return f"<p>Error creating plot: {e}</p>"
    
    @staticmethod
    def create_bar_chart(df: pd.DataFrame,
                        x_column: str,
                        y_column: str,
                        title: str = "Bar Chart") -> str:
        """Create a bar chart using Plotly."""
        try:
            if df.empty:
                return "<p>No data available for visualization</p>"
            
            fig = px.bar(
                df,
                x=x_column,
                y=y_column,
                title=title,
                labels={
                    x_column: x_column.replace('_', ' ').title(),
                    y_column: y_column.replace('_', ' ').title()
                }
            )
            
            fig.update_layout(
                title_x=0.5,
                template="plotly_white",
                xaxis_tickangle=-45
            )
            
            return fig.to_html(full_html=False, include_plotlyjs='cdn')
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {e}")
            return f"<p>Error creating chart: {e}</p>"
    
    @staticmethod
    def create_heatmap(df: pd.DataFrame,
                      x_column: str,
                      y_column: str,
                      z_column: str,
                      title: str = "Heatmap") -> str:
        """Create a heatmap using Plotly."""
        try:
            if df.empty:
                return "<p>No data available for visualization</p>"
            
            # Pivot the data for heatmap
            pivot_df = df.pivot_table(
                values=z_column,
                index=y_column,
                columns=x_column,
                aggfunc='mean'
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale='Viridis'
            ))
            
            fig.update_layout(
                title=title,
                title_x=0.5,
                template="plotly_white"
            )
            
            return fig.to_html(full_html=False, include_plotlyjs='cdn')
            
        except Exception as e:
            logger.error(f"Error creating heatmap: {e}")
            return f"<p>Error creating heatmap: {e}</p>"
