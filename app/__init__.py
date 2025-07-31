"""
Main application factory and initialization.
"""
import logging
import os
from flask import Flask
from flask_cors import CORS
from app.config import config
from app.services.database import DatabaseService
from app.services.data import DataService
from app.services.visualization import VisualizationService
from app.routes.api import create_api_routes
from app.routes.web import create_web_routes

def setup_logging(app: Flask):
    """Setup application logging."""
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )

def create_app(config_name: str = None) -> Flask:
    """Application factory pattern."""
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Setup logging
    setup_logging(app)
    
    # Enable CORS
    CORS(app)
    
    # Initialize services
    try:
        app_config = config[config_name]()
        db_service = DatabaseService(app_config)
        data_service = DataService(db_service, app_config)
        viz_service = VisualizationService()
        
        # Test database connection on startup
        if not db_service.test_connection():
            app.logger.error("Failed to connect to database on startup")
        else:
            app.logger.info("Database connection successful")
        
        # Register blueprints
        api_bp = create_api_routes(data_service, viz_service)
        web_bp = create_web_routes(data_service, viz_service)
        
        app.register_blueprint(api_bp)
        app.register_blueprint(web_bp)
        
        # Store services in app context for access in routes
        app.db_service = db_service
        app.data_service = data_service
        app.viz_service = viz_service
        
        app.logger.info(f"Application created successfully with config: {config_name}")
        
    except Exception as e:
        app.logger.error(f"Failed to initialize application: {e}")
        raise
    
    return app
