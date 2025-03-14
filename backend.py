import json
import psycopg2
import pandas as pd
import geopandas as gpd
import plotly.express as px
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

@app.route("/locations")

def get_locations():
    try:
        conn = psycopg2.connect(
            host="aws-0-ap-southeast-2.pooler.supabase.com",
            port=6543,
            database="postgres",
            user="postgres.oxsesybpzosabhxpkkto",
            password="ta28_monash"  # Replace with your actual password
        )

        cur = conn.cursor()
        cur.execute("SELECT * FROM location")
        locations = cur.fetchall()
        cur.close()
        conn.close()

        return Response(json.dumps(locations), mimetype="application/json")

    except psycopg2.Error as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")
    
if __name__ == "__main__":
    app.run(port=5000)