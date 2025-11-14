import requests

# Test the specific URL
test_url = "https://nodes-televisions-rankings-briefly.trycloudflare.com"

try:
    response = requests.post(
        "http://localhost:8000/predict",
        json={"url": test_url}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"URL: {test_url}")
        print(f"Score: {result['score']:.3f} ({result['score']*100:.1f}%)")
        print(f"Label: {result['label']}")
        print("\nReasons:")
        for i, reason in enumerate(result['reasons'], 1):
            print(f"{i}. {reason}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Exception: {e}")
