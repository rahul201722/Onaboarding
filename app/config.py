"""
Configuration module for the application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    
    # Database configuration
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Shapefile path
    SHAPEFILE_PATH = os.path.join('data', 'states_provinces', 'shapefile.shp')
    
    @property
    def DATABASE_URL(self):
        """Construct database URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def validate_config(self):
        """Validate required configuration values."""
        required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
