"""
Database service module for managing database connections and operations.
"""
import psycopg2
import pandas as pd
import logging
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from app.config import Config

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service class for database operations."""
    
    def __init__(self, config: Config):
        self.config = config
        self.config.validate_config()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            logger.info(f"Connecting to database {self.config.DB_NAME} at {self.config.DB_HOST}")
            conn = psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
            logger.info("Successfully connected to database")
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logger.info("Database connection closed")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as list of dictionaries."""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return [dict(zip(columns, row)) for row in rows]
    
    def get_dataframe(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """Execute a query and return results as pandas DataFrame."""
        with self.get_connection() as conn:
            return pd.read_sql(query, conn, params=params)
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT version()")
                    version = cur.fetchone()
                    logger.info(f"Database version: {version[0]}")
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
