import requests
import json

# Test URLs specifically designed to mimic phishing patterns
test_urls = [
    "https://largely-modified-mothers-utilities.trycloudflare.com/login.html",
    "https://secure-bank-login.trycloudflare.com/account/verify",
    "https://paypal-security-update.trycloudflare.com/signin",
    "https://google-verification-service.trycloudflare.com/auth",
    "https://amazon-account-verification.trycloudflare.com/login",
    "https://microsoft-office365-login.trycloudflare.com/secure",
    "https://facebook-security-alert.trycloudflare.com/confirm",
    "https://urgent-security-update.trycloudflare.com/login.php",
    "https://account-verification-service.trycloudflare.com/signin.html",
    "https://critical-security-alert.trycloudflare.com/index.php"
]

print("Testing phishing detection model...")
print("="*60)

for test_url in test_urls:
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
            if 'confidence' in result:
                print(f"Confidence: {result['confidence']:.3f}")
            else:
                print("Confidence: Not available")
            print("Top Reasons:")
            for i, reason in enumerate(result['reasons'][:3], 1):
                print(f"  {i}. {reason}")
        else:
            print(f"\nError testing {test_url}: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\nException testing {test_url}: {e}")

print("\n" + "="*60)
print("Testing complete")