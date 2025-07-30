#!/usr/bin/env python3
"""
Redis Cache Wrapper for HTTP Gateway
Simplified interface for Redis operations
"""

import redis
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class RestaurantCache:
    def __init__(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("Connected to Redis server")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def get_restaurant(self, restaurant_id: int) -> Optional[Dict]:
        """Get restaurant from cache"""
        if not self.redis_client:
            return None
            
        try:
            key = f"restaurant:{restaurant_id}"
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Error getting restaurant {restaurant_id}: {e}")
            return None
    
    def get_all_restaurants(self) -> List[Dict]:
        """Get all restaurants from cache"""
        if not self.redis_client:
            return []
            
        try:
            keys = self.redis_client.keys("restaurant:*")
            restaurants = []
            for key in keys:
                data = self.redis_client.get(key)
                if data:
                    restaurants.append(json.loads(data))
            return restaurants
        except Exception as e:
            logger.error(f"Error getting all restaurants: {e}")
            return []
    
    def search_restaurants(self, query: str, cuisine_type: str = None, min_rating: float = 0.0) -> List[Dict]:
        """Search restaurants in cache"""
        restaurants = self.get_all_restaurants()
        results = []
        
        for restaurant in restaurants:
            # Filter by cuisine type
            if cuisine_type and restaurant.get('cuisine_type', '').lower() != cuisine_type.lower():
                continue
                
            # Filter by minimum rating
            if restaurant.get('rating', 0) < min_rating:
                continue
                
            # Filter by query (name contains query)
            if query and query.lower() not in restaurant.get('name', '').lower():
                continue
                
            results.append(restaurant)
        
        return results
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        if not self.redis_client:
            return {"error": "Redis not connected"}
            
        try:
            info = self.redis_client.info()
            restaurant_keys = len(self.redis_client.keys("restaurant:*"))
            
            return {
                "connected_clients": info.get('connected_clients', 0),
                "used_memory": info.get('used_memory_human', '0B'),
                "total_keys": info.get('db0', {}).get('keys', 0) if 'db0' in info else 0,
                "restaurant_keys": restaurant_keys,
                "redis_version": info.get('redis_version', 'unknown')
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {"error": str(e)}
    
    def clear_cache(self) -> bool:
        """Clear all restaurant cache"""
        if not self.redis_client:
            return False
            
        try:
            keys = self.redis_client.keys("restaurant:*")
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
