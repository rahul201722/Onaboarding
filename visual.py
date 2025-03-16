from flask import Flask, jsonify, render_template
import geopandas as gpd
import pandas as pd
import folium
import plotly.express as px
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set database credentials manually if .env is not loading
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Print values to verify they are loaded correctly
print("DB_NAME:", DB_NAME)
print("DB_USER:", DB_USER)
print("DB_HOST:", DB_HOST)

# Function to get database connection
def get_db_connection():
    try:
        print(f"🔄 Connecting to database {DB_NAME} at {DB_HOST}...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ Successfully connected to Supabase PostgreSQL!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# Load shapefile for Australian states
shapefile_path = "shapefile.shp"  # Ensure you have the correct path

def get_data():
    conn = get_db_connection()
    if conn:
        query = "SELECT * FROM incidence_and_mortality_by_state;"
        df = pd.read_sql(query, conn)
        conn.close()
        print("🔌 Connection closed.")
        return df
    return pd.DataFrame()

@app.route("/choropleth")
def choropleth():
    df = get_data()
    aus_states = gpd.read_file(shapefile_path)
    aus_states = aus_states.merge(df, left_on="name", right_on="State or Territory", how="right")
    
    m = folium.Map(location=[-25, 135], zoom_start=4)
    choropleth = folium.Choropleth(
        geo_data=aus_states,
        data=aus_states,
        columns=["State or Territory", "Mortality Count"],
        key_on="feature.properties.name",
        fill_color='YlOrRd',
        fill_opacity=0.8,
        line_opacity=0.5,
        legend_name="Total Deaths",
    ).add_to(m)
    
    return m._repr_html_()

@app.route("/plot/<state>")
def plot(state):
    df = get_data()
    state_data = df[df["State or Territory"] == state]
    if state_data.empty:
        return jsonify({"error": "State not found"})
    
    fig = px.line(state_data, x="Year", y="Mortality Rate", title=f"Mortality Rate in {state}")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

if __name__ == "__main__":
    app.run(debug=True)
