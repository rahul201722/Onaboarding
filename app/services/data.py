"""
Data service module for handling cancer data operations.
"""
import pandas as pd
import geopandas as gpd
import logging
from typing import Optional, List, Dict, Any
from app.services.database import DatabaseService
from app.services.cache import CacheService
from app.config import Config

logger = logging.getLogger(__name__)

class DataService:
    """Service class for data operations."""
    
    def __init__(self, db_service: DatabaseService, config: Config, cache_service: Optional[CacheService] = None):
        self.db_service = db_service
        self.config = config
        self.cache_service = cache_service or CacheService(config.CACHE_DEFAULT_TIMEOUT)
        self._shapefile_cache = None
    
    @property
    def get_cancer_data(self):
        """Return cached version of get_cancer_data method."""
        return self.cache_service.cache_dataframe(self._get_cancer_data_impl)
    
    def _get_cancer_data_impl(self, 
                             state: Optional[str] = None, 
                             year: Optional[int] = None,
                             cancer_type: Optional[str] = None) -> pd.DataFrame:
        """Get cancer incidence and mortality data with optional filters."""
        
        base_query = """
        SELECT 
            "Cancer group/site" as cancer_type,
            "Year" as year,
            "Sex" as sex,
            "State or Territory" as state,
            "Mortality Count" as mortality_count,
            "Mortality Rate" as mortality_rate,
            "Incidence Rate" as incidence_rate,
            "Incidence Count" as incidence_count
        FROM incidence_and_mortality_by_state
        WHERE 1=1
        """
        
        conditions = []
        params = []
        
        if state:
            conditions.append(' AND "State or Territory" = %s')
            params.append(state)
        
        if year:
            conditions.append(' AND "Year" = %s')
            params.append(year)
            
        if cancer_type:
            conditions.append(' AND "Cancer group/site" = %s')
            params.append(cancer_type)
        
        query = base_query + ''.join(conditions) + ' ORDER BY "Year", "State or Territory"'
        
        try:
            return self.db_service.get_dataframe(query, tuple(params) if params else None)
        except Exception as e:
            logger.error(f"Error fetching cancer data: {e}")
            return pd.DataFrame()
    
    def get_locations(self) -> List[Dict[str, Any]]:
        """Get all locations from the location table."""
        try:
            query = "SELECT * FROM location"
            return self.db_service.execute_query(query)
        except Exception as e:
            logger.error(f"Error fetching locations: {e}")
            return []
    
    def get_states_list(self) -> List[str]:
        """Get list of unique states/territories."""
        try:
            query = 'SELECT DISTINCT "State or Territory" as state FROM incidence_and_mortality_by_state ORDER BY state'
            result = self.db_service.execute_query(query)
            return [row['state'] for row in result if row['state'] != 'Australia']
        except Exception as e:
            logger.error(f"Error fetching states list: {e}")
            return []
    
    def get_cancer_types(self) -> List[str]:
        """Get list of unique cancer types."""
        try:
            query = 'SELECT DISTINCT "Cancer group/site" as cancer_type FROM incidence_and_mortality_by_state ORDER BY cancer_type'
            result = self.db_service.execute_query(query)
            return [row['cancer_type'] for row in result]
        except Exception as e:
            logger.error(f"Error fetching cancer types: {e}")
            return []
    
    def get_years_range(self) -> Dict[str, int]:
        """Get the range of years in the dataset."""
        try:
            query = 'SELECT MIN("Year") as min_year, MAX("Year") as max_year FROM incidence_and_mortality_by_state'
            result = self.db_service.execute_query(query)
            if result:
                return result[0]
            return {'min_year': 2007, 'max_year': 2021}
        except Exception as e:
            logger.error(f"Error fetching years range: {e}")
            return {'min_year': 2007, 'max_year': 2021}
    
    def get_shapefile_data(self) -> Optional[gpd.GeoDataFrame]:
        """Load and cache shapefile data."""
        if self._shapefile_cache is None:
            try:
                logger.info(f"Loading shapefile from {self.config.SHAPEFILE_PATH}")
                self._shapefile_cache = gpd.read_file(self.config.SHAPEFILE_PATH)
                logger.info("Shapefile loaded successfully")
            except Exception as e:
                logger.error(f"Error loading shapefile: {e}")
                return None
        return self._shapefile_cache
    
    def get_merged_geo_data(self, metric: str = 'mortality_count') -> Optional[gpd.GeoDataFrame]:
        """Get cancer data merged with geographical data."""
        try:
            # Get latest year data
            df = self.get_cancer_data()
            if df.empty:
                return None
            
            # Get the most recent year
            latest_year = df['year'].max()
            latest_data = df[df['year'] == latest_year]
            
            # Group by state and sum the metric
            state_data = latest_data.groupby('state')[metric].sum().reset_index()
            
            # Load shapefile
            gdf = self.get_shapefile_data()
            if gdf is None:
                return None
            
            # Merge with geographical data
            merged = gdf.merge(state_data, left_on='name', right_on='state', how='left')
            return merged
            
        except Exception as e:
            logger.error(f"Error creating merged geo data: {e}")
            return None
