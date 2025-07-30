#!/usr/bin/env python3
"""
Task 8: gRPC Service Implementation
Problem: Create a simple gRPC service in Python that defines a RestaurantService 
with a method GetRestaurant that takes a RestaurantID and returns restaurant details.

Instructions:
- Define the service in a .proto file
- Implement the server and client in Python

Evaluation Criteria: Correct service definition, server implementation, and client interaction.

Note: Before running this script, you need to generate the gRPC code:
1. Install grpcio-tools: pip install grpcio grpcio-tools
2. Generate Python code: python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. restaurant.proto
"""

import grpc
import logging
import threading
import time
import uuid
from concurrent import futures
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    # Import generated gRPC code
    import restaurant_pb2
    import restaurant_pb2_grpc
except ImportError as e:
    logger.error("Failed to import generated gRPC code. Please run:")
    logger.error("python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. restaurant.proto")
    logger.error(f"Error: {e}")
    exit(1)


class RestaurantDatabase:
    """
    Mock database for restaurant data
    """
    
    def __init__(self):
        self.restaurants: Dict[str, Dict] = {}
        self._initialize_sample_data()
        
    def _initialize_sample_data(self):
        """Initialize with sample restaurant data"""
        sample_restaurants = [
            {
                'restaurant_id': 'rest_001',
                'name': 'The Golden Spoon',
                'address': '123 Main St, Downtown, City 12345',
                'phone_number': '+1-555-0101',
                'rating': 4.8,
                'cuisine_type': 'Italian',
                'description': 'Authentic Italian cuisine with a modern twist',
                'is_active': True,
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
                ]
            },
            {
                'restaurant_id': 'rest_002',
                'name': 'Sushi Sensation',
                'address': '456 Oak Ave, Uptown, City 12345',
                'phone_number': '+1-555-0102',
                'rating': 4.9,
                'cuisine_type': 'Japanese',
                'description': 'Fresh sushi and traditional Japanese dishes',
                'is_active': True,
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
                ]
            },
            {
                'restaurant_id': 'rest_003',
                'name': 'Burger Barn',
                'address': '789 Pine St, Westside, City 12345',
                'phone_number': '+1-555-0103',
                'rating': 4.6,
                'cuisine_type': 'American',
                'description': 'Gourmet burgers and craft beer',
                'is_active': True,
                'menu_items': [
                    {
                        'item_id': 'item_005',
                        'name': 'Classic Cheeseburger',
                        'description': 'Beef patty with cheese, lettuce, tomato',
                        'price': 14.99,
                        'category': 'Burger',
                        'is_available': True
                    }
                ]
            }
        ]
        
        for restaurant in sample_restaurants:
            restaurant['created_at'] = datetime.now().isoformat()
            restaurant['updated_at'] = datetime.now().isoformat()
            self.restaurants[restaurant['restaurant_id']] = restaurant
            
    def get_restaurant(self, restaurant_id: str) -> Optional[Dict]:
        """Get restaurant by ID"""
        return self.restaurants.get(restaurant_id)
        
    def get_restaurants(self, limit: int = 10, offset: int = 0, 
                      city: str = None, min_rating: float = 0.0) -> List[Dict]:
        """Get multiple restaurants with filtering"""
        restaurants = list(self.restaurants.values())
        
        # Apply filters
        if city:
            restaurants = [r for r in restaurants if city.lower() in r['address'].lower()]
        if min_rating > 0:
            restaurants = [r for r in restaurants if r['rating'] >= min_rating]
            
        # Apply pagination
        return restaurants[offset:offset + limit]
        
    def add_restaurant(self, restaurant_data: Dict) -> str:
        """Add new restaurant"""
        restaurant_id = f"rest_{uuid.uuid4().hex[:8]}"
        restaurant_data['restaurant_id'] = restaurant_id
        restaurant_data['created_at'] = datetime.now().isoformat()
        restaurant_data['updated_at'] = datetime.now().isoformat()
        restaurant_data['is_active'] = True
        restaurant_data['menu_items'] = restaurant_data.get('menu_items', [])
        
        self.restaurants[restaurant_id] = restaurant_data
        return restaurant_id
        
    def update_restaurant(self, restaurant_id: str, restaurant_data: Dict) -> bool:
        """Update existing restaurant"""
        if restaurant_id not in self.restaurants:
            return False
            
        restaurant_data['restaurant_id'] = restaurant_id
        restaurant_data['updated_at'] = datetime.now().isoformat()
        restaurant_data['created_at'] = self.restaurants[restaurant_id]['created_at']
        
        self.restaurants[restaurant_id].update(restaurant_data)
        return True
        
    def delete_restaurant(self, restaurant_id: str) -> bool:
        """Delete restaurant"""
        if restaurant_id in self.restaurants:
            del self.restaurants[restaurant_id]
            return True
        return False
        
    def get_total_count(self) -> int:
        """Get total number of restaurants"""
        return len(self.restaurants)


class RestaurantServiceImpl(restaurant_pb2_grpc.RestaurantServiceServicer):
    """
    gRPC Restaurant Service Implementation
    """
    
    def __init__(self):
        self.db = RestaurantDatabase()
        logger.info("RestaurantService initialized with sample data")
        
    def _dict_to_restaurant_pb(self, restaurant_dict: Dict) -> restaurant_pb2.Restaurant:
        """Convert dictionary to Restaurant protobuf message"""
        menu_items = []
        for item in restaurant_dict.get('menu_items', []):
            menu_item = restaurant_pb2.MenuItem(
                item_id=item['item_id'],
                name=item['name'],
                description=item['description'],
                price=item['price'],
                category=item['category'],
                is_available=item['is_available']
            )
            menu_items.append(menu_item)
            
        return restaurant_pb2.Restaurant(
            restaurant_id=restaurant_dict['restaurant_id'],
            name=restaurant_dict['name'],
            address=restaurant_dict['address'],
            phone_number=restaurant_dict['phone_number'],
            rating=restaurant_dict['rating'],
            cuisine_type=restaurant_dict['cuisine_type'],
            description=restaurant_dict['description'],
            created_at=restaurant_dict['created_at'],
            updated_at=restaurant_dict['updated_at'],
            is_active=restaurant_dict['is_active'],
            menu_items=menu_items
        )
        
    def GetRestaurant(self, request, context):
        """Get restaurant details by ID"""
        logger.info(f"GetRestaurant called with ID: {request.restaurant_id}")
        
        try:
            restaurant_data = self.db.get_restaurant(request.restaurant_id)
            
            if restaurant_data:
                restaurant_pb = self._dict_to_restaurant_pb(restaurant_data)
                return restaurant_pb2.RestaurantResponse(
                    success=True,
                    message=f"Restaurant {request.restaurant_id} found successfully",
                    restaurant=restaurant_pb
                )
            else:
                return restaurant_pb2.RestaurantResponse(
                    success=False,
                    message=f"Restaurant {request.restaurant_id} not found"
                )
                
        except Exception as e:
            logger.error(f"Error in GetRestaurant: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            return restaurant_pb2.RestaurantResponse(
                success=False,
                message=f"Error retrieving restaurant: {str(e)}"
            )
            
    def GetRestaurants(self, request, context):
        """Get multiple restaurants with filtering"""
        logger.info(f"GetRestaurants called with limit: {request.limit}, offset: {request.offset}")
        
        try:
            restaurants_data = self.db.get_restaurants(
                limit=request.limit or 10,
                offset=request.offset or 0,
                city=request.city if request.city else None,
                min_rating=request.min_rating or 0.0
            )
            
            restaurants_pb = [self._dict_to_restaurant_pb(r) for r in restaurants_data]
            total_count = self.db.get_total_count()
            
            return restaurant_pb2.RestaurantsResponse(
                success=True,
                message=f"Found {len(restaurants_pb)} restaurants",
                restaurants=restaurants_pb,
                total_count=total_count
            )
            
        except Exception as e:
            logger.error(f"Error in GetRestaurants: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            return restaurant_pb2.RestaurantsResponse(
                success=False,
                message=f"Error retrieving restaurants: {str(e)}",
                restaurants=[],
                total_count=0
            )
            
    def AddRestaurant(self, request, context):
        """Add a new restaurant"""
        logger.info(f"AddRestaurant called for: {request.name}")
        
        try:
            restaurant_data = {
                'name': request.name,
                'address': request.address,
                'phone_number': request.phone_number,
                'rating': request.rating,
                'cuisine_type': request.cuisine_type,
                'description': request.description
            }
            
            restaurant_id = self.db.add_restaurant(restaurant_data)
            restaurant_data = self.db.get_restaurant(restaurant_id)
            restaurant_pb = self._dict_to_restaurant_pb(restaurant_data)
            
            return restaurant_pb2.RestaurantResponse(
                success=True,
                message=f"Restaurant {restaurant_id} added successfully",
                restaurant=restaurant_pb
            )
            
        except Exception as e:
            logger.error(f"Error in AddRestaurant: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            return restaurant_pb2.RestaurantResponse(
                success=False,
                message=f"Error adding restaurant: {str(e)}"
            )
            
    def UpdateRestaurant(self, request, context):
        """Update restaurant details"""
        logger.info(f"UpdateRestaurant called for ID: {request.restaurant_id}")
        
        try:
            restaurant_data = {
                'name': request.name,
                'address': request.address,
                'phone_number': request.phone_number,
                'rating': request.rating,
                'cuisine_type': request.cuisine_type,
                'description': request.description
            }
            
            success = self.db.update_restaurant(request.restaurant_id, restaurant_data)
            
            if success:
                updated_restaurant = self.db.get_restaurant(request.restaurant_id)
                restaurant_pb = self._dict_to_restaurant_pb(updated_restaurant)
                
                return restaurant_pb2.RestaurantResponse(
                    success=True,
                    message=f"Restaurant {request.restaurant_id} updated successfully",
                    restaurant=restaurant_pb
                )
            else:
                return restaurant_pb2.RestaurantResponse(
                    success=False,
                    message=f"Restaurant {request.restaurant_id} not found"
                )
                
        except Exception as e:
            logger.error(f"Error in UpdateRestaurant: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            return restaurant_pb2.RestaurantResponse(
                success=False,
                message=f"Error updating restaurant: {str(e)}"
            )
            
    def DeleteRestaurant(self, request, context):
        """Delete a restaurant"""
        logger.info(f"DeleteRestaurant called for ID: {request.restaurant_id}")
        
        try:
            success = self.db.delete_restaurant(request.restaurant_id)
            
            if success:
                return restaurant_pb2.DeleteRestaurantResponse(
                    success=True,
                    message=f"Restaurant {request.restaurant_id} deleted successfully",
                    deleted_restaurant_id=request.restaurant_id
                )
            else:
                return restaurant_pb2.DeleteRestaurantResponse(
                    success=False,
                    message=f"Restaurant {request.restaurant_id} not found",
                    deleted_restaurant_id=""
                )
                
        except Exception as e:
            logger.error(f"Error in DeleteRestaurant: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error: {str(e)}")
            return restaurant_pb2.DeleteRestaurantResponse(
                success=False,
                message=f"Error deleting restaurant: {str(e)}",
                deleted_restaurant_id=""
            )


class RestaurantGRPCServer:
    """
    gRPC Server for Restaurant Service
    """
    
    def __init__(self, port: int = 50051):
        self.port = port
        self.server = None
        
    def start(self):
        """Start the gRPC server"""
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        restaurant_pb2_grpc.add_RestaurantServiceServicer_to_server(
            RestaurantServiceImpl(), self.server
        )
        
        listen_addr = f'[::]:{self.port}'
        self.server.add_insecure_port(listen_addr)
        
        self.server.start()
        logger.info(f"gRPC Restaurant Server started on port {self.port}")
        
        try:
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Server interrupted by user")
            self.stop()
            
    def stop(self):
        """Stop the gRPC server"""
        if self.server:
            self.server.stop(0)
            logger.info("gRPC Server stopped")


class RestaurantGRPCClient:
    """
    gRPC Client for Restaurant Service
    """
    
    def __init__(self, server_address: str = 'localhost:50051'):
        self.server_address = server_address
        self.channel = None
        self.stub = None
        
    def connect(self):
        """Connect to gRPC server"""
        try:
            self.channel = grpc.insecure_channel(self.server_address)
            self.stub = restaurant_pb2_grpc.RestaurantServiceStub(self.channel)
            logger.info(f"Connected to gRPC server at {self.server_address}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to gRPC server: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from gRPC server"""
        if self.channel:
            self.channel.close()
            logger.info("Disconnected from gRPC server")
            
    def get_restaurant(self, restaurant_id: str):
        """Get restaurant by ID"""
        try:
            request = restaurant_pb2.RestaurantRequest(restaurant_id=restaurant_id)
            response = self.stub.GetRestaurant(request)
            
            if response.success:
                logger.info(f"Successfully retrieved restaurant: {response.restaurant.name}")
                return response.restaurant
            else:
                logger.warning(f"Failed to get restaurant: {response.message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"gRPC error in get_restaurant: {e}")
            return None
            
    def get_restaurants(self, limit: int = 10, offset: int = 0, 
                      city: str = None, min_rating: float = 0.0):
        """Get multiple restaurants"""
        try:
            request = restaurant_pb2.RestaurantsRequest(
                limit=limit,
                offset=offset,
                city=city or "",
                min_rating=min_rating
            )
            response = self.stub.GetRestaurants(request)
            
            if response.success:
                logger.info(f"Successfully retrieved {len(response.restaurants)} restaurants")
                return response.restaurants
            else:
                logger.warning(f"Failed to get restaurants: {response.message}")
                return []
                
        except grpc.RpcError as e:
            logger.error(f"gRPC error in get_restaurants: {e}")
            return []
            
    def add_restaurant(self, name: str, address: str, phone_number: str, 
                      rating: float, cuisine_type: str, description: str):
        """Add a new restaurant"""
        try:
            request = restaurant_pb2.AddRestaurantRequest(
                name=name,
                address=address,
                phone_number=phone_number,
                rating=rating,
                cuisine_type=cuisine_type,
                description=description
            )
            response = self.stub.AddRestaurant(request)
            
            if response.success:
                logger.info(f"Successfully added restaurant: {response.restaurant.name}")
                return response.restaurant
            else:
                logger.warning(f"Failed to add restaurant: {response.message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"gRPC error in add_restaurant: {e}")
            return None


def run_server():
    """Run the gRPC server"""
    server = RestaurantGRPCServer()
    server.start()


def run_client_demo():
    """Demonstrate gRPC client functionality"""
    client = RestaurantGRPCClient()
    
    if not client.connect():
        logger.error("Failed to connect to server")
        return
        
    try:
        # Test GetRestaurant
        logger.info("\n=== Testing GetRestaurant ===")
        restaurant = client.get_restaurant("rest_001")
        if restaurant:
            logger.info(f"Restaurant: {restaurant.name}")
            logger.info(f"Address: {restaurant.address}")
            logger.info(f"Rating: {restaurant.rating}")
            logger.info(f"Cuisine: {restaurant.cuisine_type}")
            
        # Test GetRestaurants
        logger.info("\n=== Testing GetRestaurants ===")
        restaurants = client.get_restaurants(limit=5)
        for i, restaurant in enumerate(restaurants, 1):
            logger.info(f"{i}. {restaurant.name} - {restaurant.rating} stars")
            
        # Test AddRestaurant
        logger.info("\n=== Testing AddRestaurant ===")
        new_restaurant = client.add_restaurant(
            name="Test Restaurant",
            address="123 Test St, Test City",
            phone_number="+1-555-TEST",
            rating=4.5,
            cuisine_type="Test Cuisine",
            description="A test restaurant for demonstration"
        )
        if new_restaurant:
            logger.info(f"Added restaurant: {new_restaurant.name} (ID: {new_restaurant.restaurant_id})")
            
    except Exception as e:
        logger.error(f"Client demo error: {e}")
    finally:
        client.disconnect()


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python grpc.py [server|client|generate]")
        print("  server    - Run gRPC server")
        print("  client    - Run client demo")
        print("  generate  - Generate gRPC code from proto file")
        return
        
    mode = sys.argv[1].lower()
    
    if mode == "server":
        run_server()
    elif mode == "client":
        # Wait a moment for server to start if running both
        time.sleep(2)
        run_client_demo()
    elif mode == "generate":
        import subprocess
        try:
            cmd = ["python", "-m", "grpc_tools.protoc", "-I.", "--python_out=.", "--grpc_python_out=.", "restaurant.proto"]
            subprocess.run(cmd, check=True)
            logger.info("gRPC code generated successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to generate gRPC code: {e}")
        except FileNotFoundError:
            logger.error("grpcio-tools not found. Install with: pip install grpcio-tools")
    else:
        print(f"Unknown mode: {mode}")
        print("Valid modes: server, client, generate")


if __name__ == "__main__":
    main()