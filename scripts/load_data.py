"""
Script to load CSV data into the database.
"""
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv_to_database():
    """Load the CSV data into the database."""
    
    try:
        # Initialize configuration
        config = Config()
        config.validate_config()
        
        # Create database connection
        engine = create_engine(config.DATABASE_URL)
        
        # Load CSV data
        csv_path = 'data/incidence_mortality_state.csv'
        logger.info(f"Loading data from {csv_path}")
        
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} rows from CSV")
        
        # Clean column names (replace spaces with underscores, make lowercase)
        df.columns = df.columns.str.replace(' ', '_').str.replace('/', '_').str.lower()
        
        # Create table and load data
        table_name = 'incidence_and_mortality_by_state'
        
        with engine.connect() as conn:
            # Drop table if exists
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            logger.info(f"Dropped existing table {table_name}")
            
            # Load data to database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            logger.info(f"Created table {table_name} with {len(df)} rows")
            
            # Create location table with unique states
            states_df = df[['state_or_territory']].drop_duplicates().reset_index(drop=True)
            states_df.columns = ['name']
            states_df['id'] = range(1, len(states_df) + 1)
            
            conn.execute(text("DROP TABLE IF EXISTS location"))
            states_df.to_sql('location', conn, if_exists='replace', index=False)
            logger.info(f"Created location table with {len(states_df)} states")
            
            # Verify data
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.fetchone()[0]
            logger.info(f"Verification: {count} rows in {table_name}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM location"))
            count = result.fetchone()[0]
            logger.info(f"Verification: {count} rows in location")
        
        logger.info("Data loading completed successfully!")
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

if __name__ == "__main__":
    load_csv_to_database()
