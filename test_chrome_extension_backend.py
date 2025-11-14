#!/usr/bin/env python3
"""
Test script for Chrome Extension Backend
This script verifies that the backend API is working correctly for the Trap Eye Chrome extension.
"""

import requests
import time

def test_backend_health():
    """Test if the backend is running and healthy"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running or not accessible")
        print("   Please start the backend server with: python backend/main.py")
        return False
    except Exception as e:
        print(f"❌ Error testing backend health: {e}")
        return False

def test_phishing_detection():
    """Test phishing detection with sample URLs"""
    test_urls = [
        "https://google.com",
        "http://paypal-secure-login-verify.com/signin/",
        "https://github.com/python/cpython"
    ]
    
    print("\nTesting phishing detection:")
    for url in test_urls:
        try:
            response = requests.post(
                'http://localhost:8000/predict',
                json={"url": url},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                score = result['score']
                label = result['label']
                print(f"   {url}")
                print(f"   └── Score: {score:.2%}, Label: {label}")
            else:
                print(f"   {url} - Error: {response.status_code}")
        except Exception as e:
            print(f"   {url} - Error: {e}")

def main():
    print("🧪 Testing Trap Eye Chrome Extension Backend")
    print("=" * 50)
    
    # Test health check
    if test_backend_health():
        # Test phishing detection
        test_phishing_detection()
    
    print("\n" + "=" * 50)
    print("🔧 Troubleshooting Tips:")
    print("1. Make sure the backend is running: python backend/main.py")
    print("2. Check if port 8000 is available")
    print("3. Verify the extension is loaded in Chrome")
    print("4. Check Chrome console for extension errors")

if __name__ == "__main__":
    main()