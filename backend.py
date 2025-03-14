import json
import os
import psycopg2
import pandas as pd
import geopandas as gpd
import plotly.express as px
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/locations")
def get_locations():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        cur = conn.cursor()
        cur.execute("SELECT * FROM location")
        columns = [desc[0] for desc in cur.description]  # Get column names
        locations = cur.fetchall()
        
        # Convert to list of dictionaries for JSON serialization
        locations_json = [dict(zip(columns, row)) for row in locations]
        
        cur.close()
        conn.close()

        return jsonify(locations_json)

    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(port=5000)