#!/usr/bin/env python3
"""Simple API test script for user creation and authentication."""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Create user
    print("=" * 50)
    print("1. CREATE USER")
    print("=" * 50)
    
    user_data = {
        "name": "Mario García",
        "email": "mario@example.com",
        "password": "securepass123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 201:
        print("Error: User creation failed!")
        return
    
    user_id = response.json()["id"]
    print(f"\n✓ User created with ID: {user_id}")
    
    # 2. Login
    print("\n" + "=" * 50)
    print("2. LOGIN")
    print("=" * 50)
    
    login_data = {
        "email": "mario@example.com",
        "password": "securepass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 200:
        print("Error: Login failed!")
        return
    
    token = response.json()["access_token"]
    print(f"\n✓ Login successful. Token: {token[:20]}...")
    
    # 3. List users with authentication
    print("\n" + "=" * 50)
    print("3. LIST USERS (with token)")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✓ Retrieved {len(response.json())} users")
    
    # 4. Get specific user
    print("\n" + "=" * 50)
    print("4. GET USER BY ID")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print(f"\n✓ User retrieved: {response.json()['name']} ({response.json()['email']})")
    
    # 5. Test invalid password
    print("\n" + "=" * 50)
    print("5. LOGIN WITH INVALID PASSWORD (should fail)")
    print("=" * 50)
    
    bad_login = {
        "email": "mario@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=bad_login)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("\n✓ Invalid password correctly rejected")

if __name__ == "__main__":
    test_flow()
