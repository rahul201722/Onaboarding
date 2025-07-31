"""
Caching service for improving application performance.
"""
import json
import logging
from typing import Any, Optional, Callable
from functools import wraps
import hashlib
import pandas as pd

logger = logging.getLogger(__name__)

class CacheService:
    """Simple in-memory cache service."""
    
    def __init__(self, default_timeout: int = 300):
        self._cache = {}
        self.default_timeout = default_timeout
        
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self._cache:
            logger.debug(f"Cache hit for key: {key}")
            return self._cache[key]
        logger.debug(f"Cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """Set value in cache."""
        self._cache[key] = value
        logger.debug(f"Cache set for key: {key}")
    
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted for key: {key}")
    
    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def cache_dataframe(self, func: Callable) -> Callable:
        """Decorator for caching DataFrame results."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{self._generate_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = self.get(cache_key)
            if cached_result is not None:
                # Convert back to DataFrame if it was serialized
                if isinstance(cached_result, str):
                    try:
                        return pd.read_json(cached_result, orient='records')
                    except:
                        pass
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            if isinstance(result, pd.DataFrame):
                # Serialize DataFrame for caching
                try:
                    serialized = result.to_json(orient='records')
                    self.set(cache_key, serialized, self.default_timeout)
                except Exception as e:
                    logger.warning(f"Failed to cache DataFrame: {e}")
            else:
                self.set(cache_key, result, self.default_timeout)
            
            return result
        return wrapper
    
    def cache_result(self, timeout: Optional[int] = None) -> Callable:
        """Decorator for caching function results."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = f"{func.__name__}:{self._generate_key(*args, **kwargs)}"
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Cache result
                cache_timeout = timeout or self.default_timeout
                self.set(cache_key, result, cache_timeout)
                
                return result
            return wrapper
        return decorator
