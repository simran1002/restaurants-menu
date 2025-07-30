#!/usr/bin/env python3
"""
HTTP Gateways for Protocol Testing
Provides REST endpoints to test gRPC, MQTT, and Redis services via Postman
"""

import json
import logging
import threading
import time
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Add protocol directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'task8'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'task7'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'task9'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask apps for each gateway
grpc_app = Flask('grpc_gateway')
redis_app = Flask('redis_gateway')
mqtt_app = Flask('mqtt_gateway')

# Global clients
grpc_client = None
redis_client = None
mqtt_client = None

def initialize_clients():
    """Initialize all protocol clients"""
    global grpc_client, redis_client, mqtt_client
    
    # Initialize gRPC client
    try:
        import grpc
        import restaurant_pb2
        import restaurant_pb2_grpc
        
        channel = grpc.insecure_channel('localhost:50051')
        grpc_client = restaurant_pb2_grpc.RestaurantServiceStub(channel)
        logger.info("gRPC client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize gRPC client: {e}")
    
    # Initialize Redis client
    try:
        from redis_cache import RestaurantCache
        redis_client = RestaurantCache()
        logger.info("Redis client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")
    
    # Initialize MQTT client
    try:
        import paho.mqtt.client as mqtt
        mqtt_client = mqtt.Client()
        mqtt_client.connect("localhost", 1883, 60)
        mqtt_client.loop_start()
        logger.info("MQTT client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize MQTT client: {e}")

# =============================================================================
# gRPC Gateway (Port 8001)
# =============================================================================

@grpc_app.route('/health', methods=['GET'])
def grpc_health():
    return jsonify({"status": "healthy", "service": "gRPC Gateway", "port": 8001})

@grpc_app.route('/restaurant/get', methods=['POST'])
def get_restaurant():
    """Get restaurant by ID"""
    try:
        data = request.get_json()
        restaurant_id = data.get('id')
        
        if not restaurant_id:
            return jsonify({"error": "Restaurant ID is required"}), 400
        
        import restaurant_pb2
        request_msg = restaurant_pb2.RestaurantRequest(restaurant_id=restaurant_id)
        response = grpc_client.GetRestaurant(request_msg)
        
        if response.success:
            restaurant = response.restaurant
            return jsonify({
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "address": restaurant.address,
                "phone_number": restaurant.phone_number,
                "rating": restaurant.rating,
                "cuisine_type": restaurant.cuisine_type,
                "description": restaurant.description
            })
        else:
            return jsonify({"error": response.message}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grpc_app.route('/restaurant/list', methods=['POST'])
def list_restaurants():
    """List restaurants with optional filters"""
    try:
        data = request.get_json() or {}
        
        import restaurant_pb2
        request_msg = restaurant_pb2.RestaurantsRequest(
            limit=data.get('limit', 10),
            offset=data.get('offset', 0),
            city=data.get('city', ''),
            min_rating=data.get('min_rating', 0.0)
        )
        
        response = grpc_client.GetRestaurants(request_msg)
        
        if response.success:
            restaurants = []
            for restaurant in response.restaurants:
                restaurants.append({
                    "restaurant_id": restaurant.restaurant_id,
                    "name": restaurant.name,
                    "address": restaurant.address,
                    "phone_number": restaurant.phone_number,
                    "rating": restaurant.rating,
                    "cuisine_type": restaurant.cuisine_type,
                    "description": restaurant.description
                })
            
            return jsonify({
                "restaurants": restaurants, 
                "count": len(restaurants),
                "total_count": response.total_count
            })
        else:
            return jsonify({"error": response.message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grpc_app.route('/restaurant/add', methods=['POST'])
def add_restaurant():
    """Add new restaurant"""
    try:
        data = request.get_json()
        
        import restaurant_pb2
        request_msg = restaurant_pb2.AddRestaurantRequest(
            name=data.get('name', ''),
            address=data.get('address', ''),
            phone_number=data.get('phone_number', ''),
            rating=data.get('rating', 0.0),
            cuisine_type=data.get('cuisine_type', ''),
            description=data.get('description', '')
        )
        
        response = grpc_client.AddRestaurant(request_msg)
        
        if response.success:
            restaurant = response.restaurant
            return jsonify({
                "restaurant_id": restaurant.restaurant_id,
                "name": restaurant.name,
                "message": response.message
            })
        else:
            return jsonify({"error": response.message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@grpc_app.route('/restaurant/update', methods=['PUT'])
def update_restaurant():
    """Update an existing restaurant"""
    try:
        data = request.get_json()
        if not data.get('restaurant_id'):
            return jsonify({"error": "restaurant_id is required"}), 400
        
        import restaurant_pb2
        request_msg = restaurant_pb2.UpdateRestaurantRequest(
            restaurant_id=data['restaurant_id'],
            name=data.get('name', ''),
            address=data.get('address', ''),
            phone_number=data.get('phone_number', ''),
            rating=data.get('rating', 0.0),
            cuisine_type=data.get('cuisine_type', ''),
            description=data.get('description', '')
        )
        
        response = grpc_client.UpdateRestaurant(request_msg)
        
        if response.success:
            return jsonify({
                "success": True,
                "message": response.message,
                "restaurant": {
                    "restaurant_id": response.restaurant.restaurant_id,
                    "name": response.restaurant.name,
                    "address": response.restaurant.address,
                    "phone_number": response.restaurant.phone_number,
                    "rating": response.restaurant.rating,
                    "cuisine_type": response.restaurant.cuisine_type
                }
            })
        else:
            return jsonify({"error": response.message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@grpc_app.route('/restaurant/delete', methods=['DELETE'])
def delete_restaurant():
    """Delete a restaurant by ID"""
    try:
        data = request.get_json()
        if not data or 'id' not in data:
            return jsonify({"error": "Restaurant ID is required"}), 400
            
        import restaurant_pb2
        request_msg = restaurant_pb2.DeleteRestaurantRequest(restaurant_id=data['id'])
        response = grpc_client.DeleteRestaurant(request_msg)
        
        if response.success:
            return jsonify({
                "success": True,
                "message": response.message,
                "deleted_restaurant_id": response.deleted_restaurant_id
            })
        else:
            return jsonify({"error": response.message}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

# =============================================================================
# Redis Gateway (Port 8002)
# =============================================================================

@redis_app.route('/health', methods=['GET'])
def redis_health():
    return jsonify({"status": "healthy", "service": "Redis Gateway", "port": 8002})

@redis_app.route('/cache/restaurant/<int:restaurant_id>', methods=['GET'])
def get_cached_restaurant(restaurant_id):
    """Get cached restaurant by ID"""
    try:
        restaurant = redis_client.get_restaurant(restaurant_id)
        if restaurant:
            return jsonify(restaurant)
        else:
            return jsonify({"error": "Restaurant not found in cache"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@redis_app.route('/cache/restaurants/all', methods=['GET'])
def get_all_cached_restaurants():
    """Get all cached restaurants"""
    try:
        restaurants = redis_client.get_all_restaurants()
        return jsonify({"restaurants": restaurants, "count": len(restaurants)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@redis_app.route('/cache/search', methods=['POST'])
def search_cached_restaurants():
    """Search cached restaurants"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        cuisine_type = data.get('cuisine_type')
        min_rating = data.get('min_rating', 0.0)
        
        restaurants = redis_client.search_restaurants(query, cuisine_type, min_rating)
        return jsonify({"restaurants": restaurants, "count": len(restaurants)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@redis_app.route('/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = redis_client.get_cache_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@redis_app.route('/cache/clear', methods=['DELETE'])
def clear_cache():
    """Clear all cache"""
    try:
        success = redis_client.clear_cache()
        return jsonify({"success": success, "message": "Cache cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =============================================================================
# MQTT Gateway (Port 8003)
# =============================================================================

@mqtt_app.route('/health', methods=['GET'])
def mqtt_health():
    return jsonify({"status": "healthy", "service": "MQTT Gateway", "port": 8003})

@mqtt_app.route('/mqtt/publish', methods=['POST'])
def publish_message():
    """Publish MQTT message"""
    try:
        data = request.get_json()
        topic = data.get('topic', 'restaurant/orders')
        message = data.get('message', {})
        
        mqtt_client.publish(topic, json.dumps(message))
        return jsonify({"success": True, "message": "Message published", "topic": topic})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mqtt_app.route('/mqtt/status', methods=['GET'])
def mqtt_status():
    """Get MQTT connection status"""
    try:
        return jsonify({
            "connected": mqtt_client.is_connected() if mqtt_client else False,
            "broker": "localhost:1883"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_gateway(app, port, name):
    """Run a gateway on specified port"""
    logger.info(f"Starting {name} on port {port}")
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)

def main():
    """Start all HTTP gateways"""
    print("🚀 Starting HTTP Gateways for Protocol Testing")
    print("=" * 50)
    
    # Initialize clients
    initialize_clients()
    
    # Start gateways in separate threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(run_gateway, grpc_app, 8001, "gRPC Gateway")
        executor.submit(run_gateway, redis_app, 8002, "Redis Gateway") 
        executor.submit(run_gateway, mqtt_app, 8003, "MQTT Gateway")
        
        print("\n✅ All HTTP Gateways Started!")
        print("📋 Available Endpoints:")
        print("   gRPC Gateway:  http://127.0.0.1:8001")
        print("   Redis Gateway: http://127.0.0.1:8002") 
        print("   MQTT Gateway:  http://127.0.0.1:8003")
        print("\n🧪 Test with Postman:")
        print("   POST http://127.0.0.1:8001/restaurant/get")
        print("   POST http://127.0.0.1:8001/restaurant/list")
        print("   GET  http://127.0.0.1:8002/cache/stats")
        print("   POST http://127.0.0.1:8003/mqtt/publish")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down HTTP Gateways...")

if __name__ == "__main__":
    main()
