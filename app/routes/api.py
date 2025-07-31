"""
API routes for the cancer data visualization application.
"""
from flask import Blueprint, jsonify, request
from app.services.data import DataService
from app.services.visualization import VisualizationService
import logging

logger = logging.getLogger(__name__)

def create_api_routes(data_service: DataService, viz_service: VisualizationService) -> Blueprint:
    """Create and configure API routes."""
    
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    
    @api_bp.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'message': 'Cancer Data API is running'
        })
    
    @api_bp.route('/locations', methods=['GET'])
    def get_locations():
        """Get all locations."""
        try:
            locations = data_service.get_locations()
            return jsonify({
                'success': True,
                'data': locations,
                'count': len(locations)
            })
        except Exception as e:
            logger.error(f"Error in get_locations: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api_bp.route('/states', methods=['GET'])
    def get_states():
        """Get list of states/territories."""
        try:
            states = data_service.get_states_list()
            return jsonify({
                'success': True,
                'data': states,
                'count': len(states)
            })
        except Exception as e:
            logger.error(f"Error in get_states: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api_bp.route('/cancer-types', methods=['GET'])
    def get_cancer_types():
        """Get list of cancer types."""
        try:
            cancer_types = data_service.get_cancer_types()
            return jsonify({
                'success': True,
                'data': cancer_types,
                'count': len(cancer_types)
            })
        except Exception as e:
            logger.error(f"Error in get_cancer_types: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api_bp.route('/years', methods=['GET'])
    def get_years():
        """Get years range."""
        try:
            years_range = data_service.get_years_range()
            return jsonify({
                'success': True,
                'data': years_range
            })
        except Exception as e:
            logger.error(f"Error in get_years: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api_bp.route('/data', methods=['GET'])
    def get_cancer_data():
        """Get cancer data with optional filters."""
        try:
            # Get query parameters
            state = request.args.get('state')
            year = request.args.get('year', type=int)
            cancer_type = request.args.get('cancer_type')
            
            # Fetch data
            data = data_service.get_cancer_data(
                state=state,
                year=year,
                cancer_type=cancer_type
            )
            
            if data.empty:
                return jsonify({
                    'success': True,
                    'data': [],
                    'count': 0,
                    'message': 'No data found for the specified filters'
                })
            
            # Convert DataFrame to JSON
            data_json = data.to_dict('records')
            
            return jsonify({
                'success': True,
                'data': data_json,
                'count': len(data_json),
                'filters': {
                    'state': state,
                    'year': year,
                    'cancer_type': cancer_type
                }
            })
            
        except Exception as e:
            logger.error(f"Error in get_cancer_data: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api_bp.route('/summary/<state>', methods=['GET'])
    def get_state_summary(state: str):
        """Get summary statistics for a specific state."""
        try:
            data = data_service.get_cancer_data(state=state)
            
            if data.empty:
                return jsonify({
                    'success': False,
                    'error': f'No data found for state: {state}'
                }), 404
            
            # Calculate summary statistics
            summary = {
                'state': state,
                'total_records': len(data),
                'years_covered': {
                    'min': int(data['year'].min()),
                    'max': int(data['year'].max())
                },
                'cancer_types_count': data['cancer_type'].nunique(),
                'total_mortality': {
                    'count': int(data['mortality_count'].sum()),
                    'avg_rate': float(data['mortality_rate'].mean())
                },
                'total_incidence': {
                    'count': int(data['incidence_count'].sum()),
                    'avg_rate': float(data['incidence_rate'].mean())
                }
            }
            
            return jsonify({
                'success': True,
                'data': summary
            })
            
        except Exception as e:
            logger.error(f"Error in get_state_summary: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return api_bp
