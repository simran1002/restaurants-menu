#!/usr/bin/env python3
"""
Quick test for Django Restaurant API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("Testing Django Restaurant API...")
    
    # Test 1: Create a restaurant
    print("\n1. Creating a restaurant...")
    restaurant_data = {
        "name": "Test Restaurant",
        "address": "123 Test St",
        "phone_number": "+1-555-0123",
        "rating": 4.5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/restaurants/", json=restaurant_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Created restaurant: {result}")
            restaurant_id = result['data']['id']
        else:
            print(f"❌ Failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: List restaurants
    print("\n2. Listing restaurants...")
    try:
        response = requests.get(f"{BASE_URL}/restaurants/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {result['count']} restaurants")
            for restaurant in result['data']:
                print(f"   - {restaurant['name']} (Rating: {restaurant['rating']})")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ API Test Complete!")

if __name__ == "__main__":
    test_api()
