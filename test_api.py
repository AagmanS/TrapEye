"""Quick API test for the enhanced phishing detection backend"""
import requests
import json

BASE_URL = "http://localhost:8002"

def test_api():
    print("🧪 Testing Enhanced Phishing Detection API")
    print("="*60)
    
    # Test 1: Health Check
    print("\n1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test 2: Phishing URL
    print("\n2. Testing Phishing URL")
    phishing_url = "http://paypal-secure-login-verify.com/signin/?session=12345"
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"url": phishing_url}
    )
    print(f"URL: {phishing_url}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Label: {result['label']}")
    print(f"Score: {result['score']:.2%}")
    print(f"Reasons: {result['reasons'][:3]}")
    
    # Test 3: Legitimate URL
    print("\n3. Testing Legitimate URL")
    legit_url = "https://github.com/python/cpython"
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"url": legit_url}
    )
    print(f"URL: {legit_url}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Label: {result['label']}")
    print(f"Score: {result['score']:.2%}")
    print(f"Reasons: {result['reasons'][:3]}")
    
    # Test 4: Typosquatting Attack
    print("\n4. Testing Typosquatting Attack")
    typo_url = "https://gooogle.com/login/"
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"url": typo_url}
    )
    print(f"URL: {typo_url}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Label: {result['label']}")
    print(f"Score: {result['score']:.2%}")
    print(f"Reasons: {result['reasons'][:3]}")
    
    # Test 5: IP-based Attack
    print("\n5. Testing IP-based Attack")
    ip_url = "http://192.168.1.100/banking/login.php"
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"url": ip_url}
    )
    print(f"URL: {ip_url}")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Label: {result['label']}")
    print(f"Score: {result['score']:.2%}")
    print(f"Reasons: {result['reasons'][:3]}")
    
    print("\n" + "="*60)
    print("✅ API Test Complete!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure backend is running on port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")
