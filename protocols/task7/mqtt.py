#!/usr/bin/env python3
"""
Task 7: MQTT Protocol Implementation
Problem: Write a Python script to publish and subscribe to an MQTT topic. The topic is restaurant/orders.

Instructions:
- Use the paho-mqtt library
- Implement the publisher and subscriber functions
- Proper message handling

Evaluation Criteria: Correct use of the MQTT protocol and proper message handling.
"""

import paho.mqtt.client as mqtt
import json
import time
import threading
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = "localhost"  # Change to your MQTT broker address
MQTT_PORT = 1883
MQTT_TOPIC = "restaurant/orders"
MQTT_KEEPALIVE = 60

class MQTTRestaurantOrderSystem:
    """
    MQTT-based Restaurant Order System
    Handles publishing and subscribing to restaurant orders
    """
    
    def __init__(self, client_id: Optional[str] = None):
        self.client_id = client_id or f"restaurant_client_{uuid.uuid4().hex[:8]}"
        self.client = mqtt.Client(client_id=self.client_id)
        self.is_connected = False
        self.setup_callbacks()
        
    def setup_callbacks(self):
        """Setup MQTT client callbacks"""
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_log = self.on_log
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server"""
        if rc == 0:
            self.is_connected = True
            logger.info(f"Connected to MQTT broker with result code {rc}")
            # Subscribe to the restaurant orders topic upon successful connection
            client.subscribe(MQTT_TOPIC)
            logger.info(f"Subscribed to topic: {MQTT_TOPIC}")
        else:
            self.is_connected = False
            logger.error(f"Failed to connect to MQTT broker with result code {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the server"""
        self.is_connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker (rc: {rc})")
        else:
            logger.info("Disconnected from MQTT broker")
            
    def on_message(self, client, userdata, msg):
        """Callback for when a PUBLISH message is received from the server"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            logger.info(f"Received message on topic '{topic}': {payload}")
            
            # Parse the JSON message
            order_data = json.loads(payload)
            self.process_order(order_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            
    def on_publish(self, client, userdata, mid):
        """Callback for when a message is published"""
        logger.info(f"Message published successfully (mid: {mid})")
        
    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback for when the client subscribes to a topic"""
        logger.info(f"Subscribed successfully (mid: {mid}, QoS: {granted_qos})")
        
    def on_log(self, client, userdata, level, buf):
        """Callback for MQTT client logging"""
        logger.debug(f"MQTT Log: {buf}")
        
    def connect(self, broker: str = MQTT_BROKER, port: int = MQTT_PORT) -> bool:
        """Connect to MQTT broker"""
        try:
            logger.info(f"Connecting to MQTT broker at {broker}:{port}")
            self.client.connect(broker, port, MQTT_KEEPALIVE)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
            
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.is_connected:
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")
            
    def publish_order(self, order_data: Dict[str, Any]) -> bool:
        """Publish a restaurant order to the MQTT topic"""
        try:
            # Add timestamp and order ID if not present
            if 'order_id' not in order_data:
                order_data['order_id'] = str(uuid.uuid4())
            if 'timestamp' not in order_data:
                order_data['timestamp'] = datetime.now().isoformat()
                
            # Convert to JSON
            message = json.dumps(order_data, indent=2)
            
            # Publish the message
            result = self.client.publish(MQTT_TOPIC, message, qos=1)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Order published successfully: {order_data.get('order_id')}")
                return True
            else:
                logger.error(f"Failed to publish order (rc: {result.rc})")
                return False
                
        except Exception as e:
            logger.error(f"Error publishing order: {e}")
            return False
            
    def process_order(self, order_data: Dict[str, Any]):
        """Process received restaurant order"""
        try:
            order_id = order_data.get('order_id', 'Unknown')
            restaurant_name = order_data.get('restaurant_name', 'Unknown Restaurant')
            customer_name = order_data.get('customer_name', 'Unknown Customer')
            items = order_data.get('items', [])
            total_amount = order_data.get('total_amount', 0.0)
            
            logger.info(f"Processing Order {order_id}:")
            logger.info(f"  Restaurant: {restaurant_name}")
            logger.info(f"  Customer: {customer_name}")
            logger.info(f"  Items: {len(items)}")
            logger.info(f"  Total: ${total_amount:.2f}")
            
            # Simulate order processing
            self.simulate_order_processing(order_data)
            
        except Exception as e:
            logger.error(f"Error processing order: {e}")
            
    def simulate_order_processing(self, order_data: Dict[str, Any]):
        """Simulate restaurant order processing workflow"""
        order_id = order_data.get('order_id')
        
        # Simulate different order statuses
        statuses = ['received', 'preparing', 'ready', 'delivered']
        
        for status in statuses:
            time.sleep(1)  # Simulate processing time
            
            status_update = {
                'order_id': order_id,
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'message': f"Order {order_id} is now {status}"
            }
            
            # Publish status update
            status_topic = f"{MQTT_TOPIC}/status"
            self.client.publish(status_topic, json.dumps(status_update), qos=1)
            logger.info(f"Order {order_id} status updated: {status}")
            
    def start_loop(self):
        """Start the MQTT client loop"""
        self.client.loop_start()
        
    def stop_loop(self):
        """Stop the MQTT client loop"""
        self.client.loop_stop()
        
    def run_forever(self):
        """Run the MQTT client loop forever"""
        self.client.loop_forever()


def create_sample_order() -> Dict[str, Any]:
    """Create a sample restaurant order for testing"""
    return {
        'order_id': str(uuid.uuid4()),
        'restaurant_name': 'The Golden Spoon',
        'restaurant_id': 'rest_001',
        'customer_name': 'John Doe',
        'customer_phone': '+1-555-0123',
        'delivery_address': '123 Main St, City, State 12345',
        'items': [
            {
                'name': 'Margherita Pizza',
                'quantity': 2,
                'price': 15.99,
                'notes': 'Extra cheese'
            },
            {
                'name': 'Caesar Salad',
                'quantity': 1,
                'price': 8.99,
                'notes': 'Dressing on the side'
            },
            {
                'name': 'Coca Cola',
                'quantity': 2,
                'price': 2.50,
                'notes': ''
            }
        ],
        'total_amount': 43.47,
        'payment_method': 'credit_card',
        'special_instructions': 'Ring doorbell twice',
        'timestamp': datetime.now().isoformat()
    }


def publisher_demo():
    """Demonstrate MQTT publisher functionality"""
    logger.info("Starting MQTT Publisher Demo")
    
    # Create publisher client
    publisher = MQTTRestaurantOrderSystem("restaurant_publisher")
    
    # Connect to broker
    if not publisher.connect():
        logger.error("Failed to connect publisher to MQTT broker")
        return
        
    publisher.start_loop()
    
    try:
        # Wait for connection
        time.sleep(2)
        
        # Publish sample orders
        for i in range(3):
            order = create_sample_order()
            order['customer_name'] = f"Customer {i+1}"
            
            logger.info(f"Publishing order {i+1}...")
            publisher.publish_order(order)
            time.sleep(3)  # Wait between orders
            
    except KeyboardInterrupt:
        logger.info("Publisher interrupted by user")
    finally:
        publisher.stop_loop()
        publisher.disconnect()
        

def subscriber_demo():
    """Demonstrate MQTT subscriber functionality"""
    logger.info("Starting MQTT Subscriber Demo")
    
    # Create subscriber client
    subscriber = MQTTRestaurantOrderSystem("restaurant_subscriber")
    
    # Connect to broker
    if not subscriber.connect():
        logger.error("Failed to connect subscriber to MQTT broker")
        return
        
    try:
        logger.info("Subscriber is listening for orders. Press Ctrl+C to stop.")
        subscriber.run_forever()
    except KeyboardInterrupt:
        logger.info("Subscriber interrupted by user")
    finally:
        subscriber.disconnect()


def main():
    """Main function to demonstrate MQTT functionality"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mqtt.py [publisher|subscriber|both]")
        print("  publisher  - Run as publisher only")
        print("  subscriber - Run as subscriber only")
        print("  both       - Run both publisher and subscriber")
        return
        
    mode = sys.argv[1].lower()
    
    if mode == "publisher":
        publisher_demo()
    elif mode == "subscriber":
        subscriber_demo()
    elif mode == "both":
        # Run subscriber in a separate thread
        subscriber_thread = threading.Thread(target=subscriber_demo, daemon=True)
        subscriber_thread.start()
        
        # Wait a moment for subscriber to start
        time.sleep(3)
        
        # Run publisher in main thread
        publisher_demo()
    else:
        print(f"Unknown mode: {mode}")
        print("Valid modes: publisher, subscriber, both")


if __name__ == "__main__":
    main()