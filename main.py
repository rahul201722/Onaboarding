"""
Main application entry point.
"""
import os
from app import create_app

# Create application instance
app = create_app()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Cancer Data Visualization Server...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🐛 Debug: {debug}")
    print(f"🌐 URL: http://{host}:{port}")
    
    app.run(host=host, port=port, debug=debug)
