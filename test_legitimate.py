import requests

# Test legitimate URLs
legitimate_urls = [
    "https://www.google.com",
    "https://www.amazon.com",
    "https://www.paypal.com"
]

print("Testing legitimate URLs...")

for test_url in legitimate_urls:
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"url": test_url}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nURL: {test_url}")
            print(f"Score: {result['score']:.3f} ({result['score']*100:.1f}%)")
            print(f"Label: {result['label']}")
        else:
            print(f"\nError testing {test_url}: {response.status_code}")
            
    except Exception as e:
        print(f"\nException testing {test_url}: {e}")

print("\nTesting complete")