#!/usr/bin/env python3
"""
Test script for the Restaurant API
This script demonstrates the functionality of the Django REST API endpoints
"""

import requests
import json
from decimal import Decimal

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_restaurant_api():
    """Test the Restaurant API endpoints"""
    
    print("🧪 Testing Restaurant API Endpoints")
    print("=" * 50)
    
    # Test 1: Create restaurants
    print("\n1. Creating sample restaurants...")
    
    restaurants_data = [
        {
            "name": "Pizza Palace",
            "address": "123 Main St, Downtown",
            "phone_number": "+1-555-0123",
            "rating": 4.5
        },
        {
            "name": "Burger Barn",
            "address": "456 Oak Ave, Midtown",
            "phone_number": "+1-555-0456",
            "rating": 4.2
        },
        {
            "name": "Sushi Spot",
            "address": "789 Pine Rd, Uptown",
            "phone_number": "+1-555-0789",
            "rating": 4.8
        }
    ]
    
    created_restaurants = []
    
    for restaurant_data in restaurants_data:
        try:
            response = requests.post(f"{BASE_URL}/restaurants/", json=restaurant_data)
            if response.status_code == 201:
                result = response.json()
                created_restaurants.append(result['data'])
                print(f"✅ Created: {restaurant_data['name']} (ID: {result['data']['id']})")
            else:
                print(f"❌ Failed to create {restaurant_data['name']}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error creating {restaurant_data['name']}: {e}")
    
    # Test 2: List all restaurants
    print(f"\n2. Listing all restaurants...")
    try:
        response = requests.get(f"{BASE_URL}/restaurants/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result['count']} restaurants:")
            for restaurant in result['data']:
                print(f"   - {restaurant['name']} (Rating: {restaurant['rating']}⭐)")
        else:
            print(f"❌ Failed to list restaurants: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error listing restaurants: {e}")
    
    # Test 3: Get specific restaurant details
    if created_restaurants:
        restaurant_id = created_restaurants[0]['id']
        print(f"\n3. Getting details for restaurant ID {restaurant_id}...")
        try:
            response = requests.get(f"{BASE_URL}/restaurants/{restaurant_id}/")
            if response.status_code == 200:
                result = response.json()
                restaurant = result['data']
                print(f"✅ Restaurant Details:")
                print(f"   Name: {restaurant['name']}")
                print(f"   Address: {restaurant['address']}")
                print(f"   Phone: {restaurant['phone_number']}")
                print(f"   Rating: {restaurant['rating']}⭐")
            else:
                print(f"❌ Failed to get restaurant details: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error getting restaurant details: {e}")
    
    # Test 4: Update restaurant
    if created_restaurants:
        restaurant_id = created_restaurants[0]['id']
        print(f"\n4. Updating restaurant ID {restaurant_id}...")
        update_data = {
            "name": "Pizza Palace Supreme",
            "address": "123 Main St, Downtown (Updated)",
            "phone_number": "+1-555-0123",
            "rating": 4.7
        }
        try:
            response = requests.put(f"{BASE_URL}/restaurants/{restaurant_id}/", json=update_data)
            if response.status_code == 200:
                result = response.json()
                # Django REST framework returns the object directly for updates
                restaurant_name = result.get('name', result.get('data', {}).get('name', 'Unknown'))
                print(f"✅ Updated restaurant: {restaurant_name}")
            else:
                print(f"❌ Failed to update restaurant: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error updating restaurant: {e}")
    
    # Test 5: Get restaurant statistics
    print(f"\n5. Getting restaurant statistics...")
    try:
        response = requests.get(f"{BASE_URL}/restaurants/stats/")
        if response.status_code == 200:
            result = response.json()
            stats = result['stats']
            print(f"✅ Restaurant Statistics:")
            print(f"   Total Restaurants: {stats['total_restaurants']}")
            print(f"   Average Rating: {stats['average_rating']}⭐")
            if stats['highest_rated']:
                print(f"   Highest Rated: {stats['highest_rated']['name']} ({stats['highest_rated']['rating']}⭐)")
            if stats['lowest_rated']:
                print(f"   Lowest Rated: {stats['lowest_rated']['name']} ({stats['lowest_rated']['rating']}⭐)")
        else:
            print(f"❌ Failed to get statistics: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error getting statistics: {e}")
    
    # Test 6: Error handling - Invalid data
    print(f"\n6. Testing error handling with invalid data...")
    invalid_data = {
        "name": "",  # Empty name should fail
        "address": "Test Address",
        "phone_number": "123",
        "rating": 6.0  # Rating > 5.0 should fail
    }
    try:
        response = requests.post(f"{BASE_URL}/restaurants/", json=invalid_data)
        if response.status_code == 400:
            result = response.json()
            print(f"✅ Validation correctly failed:")
            print(f"   Errors: {result['errors']}")
        else:
            print(f"❌ Expected validation error, got: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error testing validation: {e}")
    
    print(f"\n🎉 API Testing Complete!")
    print("=" * 50)

def test_data_processing():
    """Test the data processing function from Task 2"""
    
    print("\n🧪 Testing Data Processing Function")
    print("=" * 50)
    
    # Import the function from task2
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'task2'))
    
    try:
        from data import calculate_total_revenue, get_order_summary
        
        # Test cases
        test_cases = [
            {
                "name": "Normal Orders",
                "orders": [
                    {'item_name': 'Pizza', 'quantity': 2, 'price_per_item': 15.99},
                    {'item_name': 'Burger', 'quantity': 1, 'price_per_item': 8.50},
                    {'item_name': 'Soda', 'quantity': 3, 'price_per_item': 2.99}
                ],
                "expected": 49.45
            },
            {
                "name": "Empty Orders",
                "orders": [],
                "expected": 0.0
            },
            {
                "name": "Single Order",
                "orders": [{'item_name': 'Coffee', 'quantity': 1, 'price_per_item': 3.50}],
                "expected": 3.50
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing {test_case['name']}:")
            try:
                result = calculate_total_revenue(test_case['orders'])
                if result == test_case['expected']:
                    print(f"✅ Expected: ${test_case['expected']}, Got: ${result}")
                else:
                    print(f"❌ Expected: ${test_case['expected']}, Got: ${result}")
                
                # Get summary for non-empty orders
                if test_case['orders']:
                    summary = get_order_summary(test_case['orders'])
                    print(f"   Summary: {summary['total_orders']} orders, {summary['total_items']} items")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n🎉 Data Processing Testing Complete!")
        
    except ImportError as e:
        print(f"❌ Could not import data processing functions: {e}")

if __name__ == "__main__":
    print("🚀 Starting Backend Development Tests")
    print("=" * 60)
    
    # Test the Django API
    test_restaurant_api()
    
    # Test the data processing function
    test_data_processing()
    
    print(f"\n✨ All tests completed!")
