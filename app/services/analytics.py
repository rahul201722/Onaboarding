"""
Analytics service for advanced data analysis and insights.
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from app.services.data import DataService
from app.services.cache import CacheService

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service for advanced analytics and insights."""
    
    def __init__(self, data_service: DataService, cache_service: Optional[CacheService] = None):
        self.data_service = data_service
        self.cache_service = cache_service or CacheService()
    
    @property
    def calculate_trends(self):
        """Cached version of trend calculation."""
        return self.cache_service.cache_result(timeout=600)(self._calculate_trends_impl)
    
    def _calculate_trends_impl(self, 
                              state: Optional[str] = None, 
                              cancer_type: Optional[str] = None,
                              metric: str = 'mortality_rate') -> Dict[str, Any]:
        """Calculate trends for mortality/incidence rates."""
        try:
            # Get time series data
            data = self.data_service.get_cancer_data(state=state, cancer_type=cancer_type)
            
            if data.empty:
                return {'error': 'No data available'}
            
            # Group by year and calculate mean
            yearly_data = data.groupby('year')[metric].mean().reset_index()
            
            if len(yearly_data) < 2:
                return {'error': 'Insufficient data for trend analysis'}
            
            # Calculate trend statistics
            x = yearly_data['year'].values
            y = yearly_data[metric].values
            
            # Linear regression for trend
            coeffs = np.polyfit(x, y, 1)
            slope, intercept = coeffs
            
            # Calculate correlation coefficient
            correlation = np.corrcoef(x, y)[0, 1]
            
            # Calculate percentage change
            first_year_value = y[0]
            last_year_value = y[-1]
            percent_change = ((last_year_value - first_year_value) / first_year_value) * 100
            
            # Determine trend direction
            if slope > 0.1:
                trend_direction = 'increasing'
            elif slope < -0.1:
                trend_direction = 'decreasing'
            else:
                trend_direction = 'stable'
            
            return {
                'trend_direction': trend_direction,
                'slope': float(slope),
                'correlation': float(correlation),
                'percent_change': float(percent_change),
                'years_analyzed': len(yearly_data),
                'first_year': int(x[0]),
                'last_year': int(x[-1]),
                'first_value': float(first_year_value),
                'last_value': float(last_year_value),
                'mean_value': float(np.mean(y)),
                'std_value': float(np.std(y))
            }
            
        except Exception as e:
            logger.error(f"Error calculating trends: {e}")
            return {'error': str(e)}
    
    @property
    def get_top_states(self):
        """Cached version of top states analysis."""
        return self.cache_service.cache_result(timeout=600)(self._get_top_states_impl)
    
    def _get_top_states_impl(self, 
                            metric: str = 'mortality_rate',
                            cancer_type: Optional[str] = None,
                            year: Optional[int] = None,
                            limit: int = 10) -> List[Dict[str, Any]]:
        """Get top states by specified metric."""
        try:
            # Get data for latest year if no year specified
            data = self.data_service.get_cancer_data(cancer_type=cancer_type, year=year)
            
            if data.empty:
                return []
            
            if year is None:
                # Use the most recent year
                latest_year = data['year'].max()
                data = data[data['year'] == latest_year]
            
            # Group by state and calculate mean
            state_data = data.groupby('state')[metric].mean().reset_index()
            state_data = state_data.sort_values(metric, ascending=False).head(limit)
            
            return state_data.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting top states: {e}")
            return []
    
    @property
    def compare_states(self):
        """Cached version of state comparison."""
        return self.cache_service.cache_result(timeout=600)(self._compare_states_impl)
    
    def _compare_states_impl(self, 
                            states: List[str],
                            metric: str = 'mortality_rate',
                            cancer_type: Optional[str] = None) -> Dict[str, Any]:
        """Compare multiple states across different metrics."""
        try:
            comparison_data = {}
            
            for state in states:
                data = self.data_service.get_cancer_data(
                    state=state, 
                    cancer_type=cancer_type
                )
                
                if not data.empty:
                    # Calculate summary statistics
                    comparison_data[state] = {
                        'mean': float(data[metric].mean()),
                        'median': float(data[metric].median()),
                        'min': float(data[metric].min()),
                        'max': float(data[metric].max()),
                        'std': float(data[metric].std()),
                        'latest_value': float(data[data['year'] == data['year'].max()][metric].mean()),
                        'records_count': len(data)
                    }
            
            # Calculate rankings
            if comparison_data:
                ranked_by_mean = sorted(
                    comparison_data.items(), 
                    key=lambda x: x[1]['mean'], 
                    reverse=True
                )
                
                for i, (state, _) in enumerate(ranked_by_mean):
                    comparison_data[state]['rank_by_mean'] = i + 1
            
            return {
                'states_compared': states,
                'metric': metric,
                'cancer_type': cancer_type,
                'comparison_data': comparison_data,
                'summary': {
                    'highest_mean': max(comparison_data.values(), key=lambda x: x['mean'])['mean'] if comparison_data else 0,
                    'lowest_mean': min(comparison_data.values(), key=lambda x: x['mean'])['mean'] if comparison_data else 0,
                    'states_count': len(comparison_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Error comparing states: {e}")
            return {'error': str(e)}
    
    @property
    def get_outliers(self):
        """Cached version of outlier detection."""
        return self.cache_service.cache_result(timeout=600)(self._get_outliers_impl)
    
    def _get_outliers_impl(self, 
                          metric: str = 'mortality_rate',
                          threshold: float = 2.0) -> Dict[str, Any]:
        """Detect outliers in the data using z-score method."""
        try:
            # Get all data
            data = self.data_service.get_cancer_data()
            
            if data.empty:
                return {'outliers': [], 'total_records': 0}
            
            # Calculate z-scores
            mean_val = data[metric].mean()
            std_val = data[metric].std()
            
            if std_val == 0:
                return {'outliers': [], 'total_records': len(data), 'note': 'No variation in data'}
            
            data['z_score'] = np.abs((data[metric] - mean_val) / std_val)
            
            # Find outliers
            outliers = data[data['z_score'] > threshold].copy()
            outliers = outliers.sort_values('z_score', ascending=False)
            
            # Format outliers
            outlier_list = []
            for _, row in outliers.head(20).iterrows():  # Limit to top 20 outliers
                outlier_list.append({
                    'state': row['state'],
                    'year': int(row['year']),
                    'cancer_type': row['cancer_type'],
                    'value': float(row[metric]),
                    'z_score': float(row['z_score']),
                    'deviation_from_mean': float(row[metric] - mean_val)
                })
            
            return {
                'outliers': outlier_list,
                'total_outliers': len(outliers),
                'total_records': len(data),
                'threshold': threshold,
                'metric': metric,
                'dataset_mean': float(mean_val),
                'dataset_std': float(std_val)
            }
            
        except Exception as e:
            logger.error(f"Error detecting outliers: {e}")
            return {'error': str(e)}
    
    @property
    def get_correlations(self):
        """Cached version of correlation analysis."""
        return self.cache_service.cache_result(timeout=600)(self._get_correlations_impl)
    
    def _get_correlations_impl(self) -> Dict[str, Any]:
        """Calculate correlations between different metrics."""
        try:
            # Get all data
            data = self.data_service.get_cancer_data()
            
            if data.empty:
                return {'error': 'No data available'}
            
            # Select numeric columns
            numeric_cols = ['mortality_count', 'mortality_rate', 'incidence_rate', 'incidence_count']
            correlation_data = data[numeric_cols].corr()
            
            # Convert to dictionary format
            correlations = {}
            for i, col1 in enumerate(numeric_cols):
                for j, col2 in enumerate(numeric_cols):
                    if i < j:  # Only upper triangle
                        key = f"{col1}_vs_{col2}"
                        correlations[key] = {
                            'metric1': col1,
                            'metric2': col2,
                            'correlation': float(correlation_data.loc[col1, col2]),
                            'interpretation': self._interpret_correlation(correlation_data.loc[col1, col2])
                        }
            
            return {
                'correlations': correlations,
                'correlation_matrix': correlation_data.to_dict(),
                'total_records': len(data)
            }
            
        except Exception as e:
            logger.error(f"Error calculating correlations: {e}")
            return {'error': str(e)}
    
    def _interpret_correlation(self, corr_value: float) -> str:
        """Interpret correlation strength."""
        abs_corr = abs(corr_value)
        if abs_corr >= 0.8:
            strength = "very strong"
        elif abs_corr >= 0.6:
            strength = "strong"
        elif abs_corr >= 0.4:
            strength = "moderate"
        elif abs_corr >= 0.2:
            strength = "weak"
        else:
            strength = "very weak"
        
        direction = "positive" if corr_value > 0 else "negative"
        return f"{strength} {direction} correlation"
