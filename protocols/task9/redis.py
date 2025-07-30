#!/usr/bin/env python3
"""
Task 9: Redis Caching Implementation
Problem: Write a Python script to cache restaurant details using Redis. 
If the details are not in the cache, fetch from a mock database and store them in Redis.

Instructions:
- Use the redis-py library
- Implement caching logic with expiration

Evaluation Criteria: Proper use of Redis for caching and efficient data retrieval.

Note: Make sure Redis server is running before executing this script.
Install redis-py: pip install redis
"""

import redis
import json
import time
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis Configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None  # Set if Redis requires authentication
DEFAULT_EXPIRATION = 3600  # 1 hour in seconds


class MockRestaurantDatabase:
    """
    Mock database to simulate restaurant data fetching
    """
    
    def __init__(self):
        self.restaurants = {
            'rest_001': {
                'restaurant_id': 'rest_001',
                'name': 'The Golden Spoon',
                'address': '123 Main St, Downtown, City 12345',
                'phone_number': '+1-555-0101',
                'rating': 4.8,
                'cuisine_type': 'Italian',
                'description': 'Authentic Italian cuisine with a modern twist',
                'is_active': True,
                'created_at': '2024-01-15T10:30:00',
                'updated_at': '2024-01-20T14:45:00',
                'menu_items': [
                    {
                        'item_id': 'item_001',
                        'name': 'Margherita Pizza',
                        'description': 'Classic pizza with tomato, mozzarella, and basil',
                        'price': 15.99,
                        'category': 'Pizza',
                        'is_available': True
                    },
                    {
                        'item_id': 'item_002',
                        'name': 'Pasta Carbonara',
                        'description': 'Creamy pasta with bacon and parmesan',
                        'price': 18.50,
                        'category': 'Pasta',
                        'is_available': True
                    }
                ],
                'reviews': [
                    {
                        'review_id': 'rev_001',
                        'customer_name': 'John Doe',
                        'rating': 5,
                        'comment': 'Excellent food and service!',
                        'date': '2024-01-18T19:30:00'
                    }
                ]
            },
            'rest_002': {
                'restaurant_id': 'rest_002',
                'name': 'Sushi Sensation',
                'address': '456 Oak Ave, Uptown, City 12345',
                'phone_number': '+1-555-0102',
                'rating': 4.9,
                'cuisine_type': 'Japanese',
                'description': 'Fresh sushi and traditional Japanese dishes',
                'is_active': True,
                'created_at': '2024-01-10T09:15:00',
                'updated_at': '2024-01-22T11:20:00',
                'menu_items': [
                    {
                        'item_id': 'item_003',
                        'name': 'Salmon Sashimi',
                        'description': 'Fresh salmon slices',
                        'price': 22.00,
                        'category': 'Sashimi',
                        'is_available': True
                    },
                    {
                        'item_id': 'item_004',
                        'name': 'California Roll',
                        'description': 'Crab, avocado, and cucumber roll',
                        'price': 12.50,
                        'category': 'Sushi Roll',
                        'is_available': True
                    }
                ],
                'reviews': [
                    {
                        'review_id': 'rev_002',
                        'customer_name': 'Jane Smith',
                        'rating': 5,
                        'comment': 'Best sushi in town!',
                        'date': '2024-01-20T20:15:00'
                    }
                ]
            },
            'rest_003': {
                'restaurant_id': 'rest_003',
                'name': 'Burger Barn',
                'address': '789 Pine St, Westside, City 12345',
                'phone_number': '+1-555-0103',
                'rating': 4.6,
                'cuisine_type': 'American',
                'description': 'Gourmet burgers and craft beer',
                'is_active': True,
                'created_at': '2024-01-12T12:00:00',
                'updated_at': '2024-01-19T16:30:00',
                'menu_items': [
                    {
                        'item_id': 'item_005',
                        'name': 'Classic Cheeseburger',
                        'description': 'Beef patty with cheese, lettuce, tomato',
                        'price': 14.99,
                        'category': 'Burger',
                        'is_available': True
                    },
                    {
                        'item_id': 'item_006',
                        'name': 'BBQ Bacon Burger',
                        'description': 'Beef patty with BBQ sauce and crispy bacon',
                        'price': 17.99,
                        'category': 'Burger',
                        'is_available': True
                    }
                ],
                'reviews': [
                    {
                        'review_id': 'rev_003',
                        'customer_name': 'Mike Johnson',
                        'rating': 4,
                        'comment': 'Great burgers, friendly staff',
                        'date': '2024-01-17T18:45:00'
                    }
                ]
            }
        }
        
    def get_restaurant(self, restaurant_id: str) -> Optional[Dict]:
        """Simulate database fetch with delay"""
        logger.info(f"Fetching restaurant {restaurant_id} from database...")
        
        # Simulate database query delay
        time.sleep(0.5)
        
        restaurant = self.restaurants.get(restaurant_id)
        if restaurant:
            logger.info(f"Restaurant {restaurant_id} found in database")
        else:
            logger.warning(f"Restaurant {restaurant_id} not found in database")
            
        return restaurant
        
    def get_all_restaurants(self) -> List[Dict]:
        """Get all restaurants from database"""
        logger.info("Fetching all restaurants from database...")
        time.sleep(1.0)  # Simulate longer delay for bulk operation
        return list(self.restaurants.values())
        
    def search_restaurants(self, query: str, cuisine_type: str = None, 
                         min_rating: float = 0.0) -> List[Dict]:
        """Search restaurants with filters"""
        logger.info(f"Searching restaurants with query: '{query}'")
        time.sleep(0.8)  # Simulate search delay
        
        results = []
        for restaurant in self.restaurants.values():
            # Text search in name and description
            if query.lower() in restaurant['name'].lower() or \
               query.lower() in restaurant['description'].lower():
                
                # Apply filters
                if cuisine_type and restaurant['cuisine_type'].lower() != cuisine_type.lower():
                    continue
                if restaurant['rating'] < min_rating:
                    continue
                    
                results.append(restaurant)
                
        logger.info(f"Found {len(results)} restaurants matching search criteria")
        return results


class RestaurantRedisCache:
    """
    Redis-based caching system for restaurant data
    """
    
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, 
                 db: int = REDIS_DB, password: str = REDIS_PASSWORD):
        self.redis_client = None
        self.db = MockRestaurantDatabase()
        self.default_expiration = DEFAULT_EXPIRATION
        
        # Connect to Redis
        self.connect(host, port, db, password)
        
    def connect(self, host: str, port: int, db: int, password: str = None):
        """Connect to Redis server"""
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis server at {host}:{port}")
            
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            logger.warning("Falling back to database-only mode")
            self.redis_client = None
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            self.redis_client = None
            
    def _generate_cache_key(self, prefix: str, identifier: str, **kwargs) -> str:
        """Generate a consistent cache key"""
        key_parts = [prefix, identifier]
        
        # Add additional parameters for complex keys
        if kwargs:
            sorted_params = sorted(kwargs.items())
            param_string = '_'.join([f"{k}:{v}" for k, v in sorted_params])
            key_parts.append(param_string)
            
        return ':'.join(key_parts)
        
    def _serialize_data(self, data: Any) -> str:
        """Serialize data for Redis storage"""
        return json.dumps(data, default=str, ensure_ascii=False)
        
    def _deserialize_data(self, data: str) -> Any:
        """Deserialize data from Redis"""
        return json.loads(data)
        
    def get_restaurant(self, restaurant_id: str, use_cache: bool = True) -> Optional[Dict]:
        """Get restaurant details with caching"""
        cache_key = self._generate_cache_key('restaurant', restaurant_id)
        
        # Try to get from cache first
        if use_cache and self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    logger.info(f"Restaurant {restaurant_id} found in cache")
                    return self._deserialize_data(cached_data)
                else:
                    logger.info(f"Restaurant {restaurant_id} not found in cache")
            except Exception as e:
                logger.error(f"Error reading from cache: {e}")
                
        # Fetch from database
        restaurant_data = self.db.get_restaurant(restaurant_id)
        
        # Store in cache if data found and Redis is available
        if restaurant_data and self.redis_client:
            try:
                serialized_data = self._serialize_data(restaurant_data)
                self.redis_client.setex(
                    cache_key, 
                    self.default_expiration, 
                    serialized_data
                )
                logger.info(f"Restaurant {restaurant_id} cached for {self.default_expiration} seconds")
            except Exception as e:
                logger.error(f"Error writing to cache: {e}")
                
        return restaurant_data
        
    def get_all_restaurants(self, use_cache: bool = True) -> List[Dict]:
        """Get all restaurants with caching"""
        cache_key = self._generate_cache_key('restaurants', 'all')
        
        # Try cache first
        if use_cache and self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    logger.info("All restaurants found in cache")
                    return self._deserialize_data(cached_data)
            except Exception as e:
                logger.error(f"Error reading from cache: {e}")
                
        # Fetch from database
        restaurants_data = self.db.get_all_restaurants()
        
        # Cache the results
        if restaurants_data and self.redis_client:
            try:
                serialized_data = self._serialize_data(restaurants_data)
                self.redis_client.setex(
                    cache_key,
                    self.default_expiration // 2,  # Shorter expiration for bulk data
                    serialized_data
                )
                logger.info(f"All restaurants cached for {self.default_expiration // 2} seconds")
            except Exception as e:
                logger.error(f"Error writing to cache: {e}")
                
        return restaurants_data
        
    def search_restaurants(self, query: str, cuisine_type: str = None, 
                         min_rating: float = 0.0, use_cache: bool = True) -> List[Dict]:
        """Search restaurants with caching"""
        # Create cache key based on search parameters
        cache_key = self._generate_cache_key(
            'search', 
            hashlib.md5(query.encode()).hexdigest()[:8],
            cuisine=cuisine_type or 'any',
            min_rating=min_rating
        )
        
        # Try cache first
        if use_cache and self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    logger.info(f"Search results found in cache for query: '{query}'")
                    return self._deserialize_data(cached_data)
            except Exception as e:
                logger.error(f"Error reading search cache: {e}")
                
        # Perform search
        search_results = self.db.search_restaurants(query, cuisine_type, min_rating)
        
        # Cache search results with shorter expiration
        if self.redis_client:
            try:
                serialized_data = self._serialize_data(search_results)
                self.redis_client.setex(
                    cache_key,
                    self.default_expiration // 4,  # Even shorter for search results
                    serialized_data
                )
                logger.info(f"Search results cached for {self.default_expiration // 4} seconds")
            except Exception as e:
                logger.error(f"Error caching search results: {e}")
                
        return search_results
        
    def invalidate_restaurant_cache(self, restaurant_id: str) -> bool:
        """Invalidate cache for a specific restaurant"""
        if not self.redis_client:
            return False
            
        try:
            cache_key = self._generate_cache_key('restaurant', restaurant_id)
            deleted = self.redis_client.delete(cache_key)
            
            # Also invalidate related caches
            self.redis_client.delete(self._generate_cache_key('restaurants', 'all'))
            
            # Clear search caches (pattern-based deletion)
            search_pattern = self._generate_cache_key('search', '*')
            search_keys = self.redis_client.keys(search_pattern)
            if search_keys:
                self.redis_client.delete(*search_keys)
                
            logger.info(f"Invalidated cache for restaurant {restaurant_id}")
            return deleted > 0
            
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
            return False
            
    def clear_all_cache(self) -> bool:
        """Clear all restaurant-related cache"""
        if not self.redis_client:
            return False
            
        try:
            # Get all restaurant-related keys
            patterns = [
                self._generate_cache_key('restaurant', '*'),
                self._generate_cache_key('restaurants', '*'),
                self._generate_cache_key('search', '*')
            ]
            
            deleted_count = 0
            for pattern in patterns:
                keys = self.redis_client.keys(pattern)
                if keys:
                    deleted_count += self.redis_client.delete(*keys)
                    
            logger.info(f"Cleared {deleted_count} cache entries")
            return deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
            
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.redis_client:
            return {'status': 'Redis not available'}
            
        try:
            info = self.redis_client.info()
            
            # Count restaurant-related keys
            restaurant_keys = len(self.redis_client.keys(self._generate_cache_key('restaurant', '*')))
            search_keys = len(self.redis_client.keys(self._generate_cache_key('search', '*')))
            all_keys = len(self.redis_client.keys(self._generate_cache_key('restaurants', '*')))
            
            return {
                'status': 'Connected',
                'redis_version': info.get('redis_version'),
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_keys': info.get('db0', {}).get('keys', 0),
                'restaurant_cache_keys': restaurant_keys,
                'search_cache_keys': search_keys,
                'bulk_cache_keys': all_keys,
                'cache_hit_ratio': self._calculate_hit_ratio()
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {'status': f'Error: {str(e)}'}
            
    def _calculate_hit_ratio(self) -> str:
        """Calculate cache hit ratio (simplified)"""
        try:
            info = self.redis_client.info()
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            
            if total > 0:
                ratio = (hits / total) * 100
                return f"{ratio:.2f}%"
            else:
                return "N/A"
        except:
            return "N/A"
            
    def set_expiration(self, seconds: int):
        """Set default cache expiration time"""
        self.default_expiration = seconds
        logger.info(f"Cache expiration set to {seconds} seconds")
        
    def close(self):
        """Close Redis connection"""
        if self.redis_client:
            self.redis_client.close()
            logger.info("Redis connection closed")


def demo_cache_operations():
    """Demonstrate Redis caching operations"""
    logger.info("=== Redis Caching Demo ===")
    
    # Initialize cache system
    cache = RestaurantRedisCache()
    
    try:
        # Demo 1: Get restaurant with caching
        logger.info("\n1. Testing restaurant retrieval with caching:")
        
        # First call - should fetch from database and cache
        start_time = time.time()
        restaurant1 = cache.get_restaurant('rest_001')
        first_call_time = time.time() - start_time
        
        if restaurant1:
            logger.info(f"First call took {first_call_time:.3f} seconds")
            logger.info(f"Restaurant: {restaurant1['name']} - {restaurant1['rating']} stars")
            
        # Second call - should come from cache (faster)
        start_time = time.time()
        restaurant2 = cache.get_restaurant('rest_001')
        second_call_time = time.time() - start_time
        
        if restaurant2:
            logger.info(f"Second call took {second_call_time:.3f} seconds")
            logger.info(f"Speed improvement: {(first_call_time / second_call_time):.1f}x faster")
            
        # Demo 2: Search with caching
        logger.info("\n2. Testing search with caching:")
        
        start_time = time.time()
        search_results1 = cache.search_restaurants('pizza', min_rating=4.0)
        first_search_time = time.time() - start_time
        
        logger.info(f"First search took {first_search_time:.3f} seconds")
        logger.info(f"Found {len(search_results1)} restaurants")
        
        start_time = time.time()
        search_results2 = cache.search_restaurants('pizza', min_rating=4.0)
        second_search_time = time.time() - start_time
        
        logger.info(f"Second search took {second_search_time:.3f} seconds")
        if second_search_time > 0:
            logger.info(f"Search speed improvement: {(first_search_time / second_search_time):.1f}x faster")
            
        # Demo 3: Cache statistics
        logger.info("\n3. Cache statistics:")
        stats = cache.get_cache_stats()
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
            
        # Demo 4: Cache invalidation
        logger.info("\n4. Testing cache invalidation:")
        cache.invalidate_restaurant_cache('rest_001')
        
        # This should fetch from database again
        start_time = time.time()
        restaurant3 = cache.get_restaurant('rest_001')
        third_call_time = time.time() - start_time
        logger.info(f"After invalidation, call took {third_call_time:.3f} seconds")
        
        # Demo 5: Bulk operations
        logger.info("\n5. Testing bulk operations:")
        
        start_time = time.time()
        all_restaurants1 = cache.get_all_restaurants()
        first_bulk_time = time.time() - start_time
        
        logger.info(f"First bulk fetch took {first_bulk_time:.3f} seconds")
        logger.info(f"Retrieved {len(all_restaurants1)} restaurants")
        
        start_time = time.time()
        all_restaurants2 = cache.get_all_restaurants()
        second_bulk_time = time.time() - start_time
        
        logger.info(f"Second bulk fetch took {second_bulk_time:.3f} seconds")
        if second_bulk_time > 0:
            logger.info(f"Bulk speed improvement: {(first_bulk_time / second_bulk_time):.1f}x faster")
            
    except Exception as e:
        logger.error(f"Demo error: {e}")
    finally:
        cache.close()


def benchmark_cache_performance():
    """Benchmark cache vs database performance"""
    logger.info("\n=== Performance Benchmark ===")
    
    cache = RestaurantRedisCache()
    
    try:
        restaurant_ids = ['rest_001', 'rest_002', 'rest_003']
        iterations = 10
        
        # Benchmark without cache
        logger.info(f"\nBenchmarking {iterations} iterations without cache:")
        start_time = time.time()
        for _ in range(iterations):
            for restaurant_id in restaurant_ids:
                cache.get_restaurant(restaurant_id, use_cache=False)
        no_cache_time = time.time() - start_time
        logger.info(f"Total time without cache: {no_cache_time:.3f} seconds")
        
        # Clear cache and benchmark with cache
        cache.clear_all_cache()
        logger.info(f"\nBenchmarking {iterations} iterations with cache:")
        start_time = time.time()
        for _ in range(iterations):
            for restaurant_id in restaurant_ids:
                cache.get_restaurant(restaurant_id, use_cache=True)
        with_cache_time = time.time() - start_time
        logger.info(f"Total time with cache: {with_cache_time:.3f} seconds")
        
        # Calculate improvement
        if with_cache_time > 0:
            improvement = no_cache_time / with_cache_time
            logger.info(f"\nPerformance improvement: {improvement:.1f}x faster with cache")
            logger.info(f"Time saved: {no_cache_time - with_cache_time:.3f} seconds")
            
    except Exception as e:
        logger.error(f"Benchmark error: {e}")
    finally:
        cache.close()


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python redis.py [demo|benchmark|stats|clear]")
        print("  demo      - Run caching demonstration")
        print("  benchmark - Run performance benchmark")
        print("  stats     - Show cache statistics")
        print("  clear     - Clear all cache")
        return
        
    mode = sys.argv[1].lower()
    
    if mode == "demo":
        demo_cache_operations()
    elif mode == "benchmark":
        benchmark_cache_performance()
    elif mode == "stats":
        cache = RestaurantRedisCache()
        try:
            stats = cache.get_cache_stats()
            print("\n=== Cache Statistics ===")
            for key, value in stats.items():
                print(f"{key}: {value}")
        finally:
            cache.close()
    elif mode == "clear":
        cache = RestaurantRedisCache()
        try:
            if cache.clear_all_cache():
                print("Cache cleared successfully")
            else:
                print("Failed to clear cache")
        finally:
            cache.close()
    else:
        print(f"Unknown mode: {mode}")
        print("Valid modes: demo, benchmark, stats, clear")


if __name__ == "__main__":
    main()