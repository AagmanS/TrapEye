"""Test the enhanced phishing detection model with various attack patterns"""
import sys
sys.path.append('backend')

from url_features import URLFeatureExtractor
from model_utils import ModelUtils

def test_url(url, description):
    """Test a single URL and display results"""
    print(f"\n{'='*80}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print(f"{'='*80}")
    
    # Extract features
    extractor = URLFeatureExtractor()
    features = extractor.extract_features(url)
    
    # Make prediction
    model = ModelUtils()
    result = model.predict(features)
    
    # Display results
    print(f"\n🎯 RESULT: {result['label'].upper()}")
    print(f"📊 Risk Score: {result['score']:.2%}")
    print(f"💪 Confidence: {result['confidence']:.2%}")
    
    print(f"\n📋 Top Reasons:")
    for i, reason in enumerate(result['reasons'][:7], 1):
        print(f"  {i}. {reason}")
    
    print(f"\n🔬 Top Feature Impacts:")
    for i, exp in enumerate(result['explainability'][:5], 1):
        print(f"  {i}. {exp['feature']}: {exp['description']} (impact: {exp['impact']:.3f})")

def main():
    print("🚀 Enhanced Phishing Detection Model - Comprehensive Test Suite")
    print("="*80)
    
    # Test Case 1: Brand impersonation
    test_url(
        "http://paypal-secure-login-verify.com/signin/?session=12345",
        "Brand Impersonation Attack (PayPal)"
    )
    
    # Test Case 2: Typosquatting
    test_url(
        "https://gooogle.com/login/",
        "Typosquatting Attack (Google misspelling)"
    )
    
    # Test Case 3: IP-based phishing
    test_url(
        "http://192.168.1.100/banking/login.php?user=victim",
        "IP-based Phishing Attack"
    )
    
    # Test Case 4: Subdomain attack
    test_url(
        "http://microsoft.verify-account-secure.com/office365/login",
        "Subdomain Phishing Attack (Microsoft brand in subdomain)"
    )
    
    # Test Case 5: Suspicious TLD with multiple dashes
    test_url(
        "http://secure-banking-login-verify.tk/auth/signin.php",
        "Suspicious TLD Attack (.tk domain)"
    )
    
    # Test Case 6: Free hosting service
    test_url(
        "https://paypal-login-verify.pages.dev/signin/",
        "Free Hosting Service Attack (Cloudflare Pages)"
    )
    
    # Test Case 7: URL shortener-like
    test_url(
        "http://abc123.com/r/98765",
        "URL Shortener-like Attack"
    )
    
    # Test Case 8: Hexadecimal encoding
    test_url(
        "http://bank-login.com/verify%20account%20now?token=abc123",
        "Hexadecimal Encoding Attack"
    )
    
    # Test Case 9: Non-standard port
    test_url(
        "http://secure-banking.com:8080/login/verify.php",
        "Non-standard Port Attack"
    )
    
    # Test Case 10: Multiple suspicious parameters
    test_url(
        "http://verify-account.com/login?username=user&password=pass&token=abc&session=123&key=xyz",
        "Suspicious Parameters Attack"
    )
    
    # Legitimate URLs for comparison
    print("\n\n" + "="*80)
    print("TESTING LEGITIMATE URLS FOR COMPARISON")
    print("="*80)
    
    test_url(
        "https://github.com/user/repo",
        "Legitimate URL (GitHub)"
    )
    
    test_url(
        "https://www.google.com/search?q=python",
        "Legitimate URL (Google Search)"
    )
    
    test_url(
        "https://stackoverflow.com/questions/12345/how-to-code",
        "Legitimate URL (Stack Overflow)"
    )
    
    test_url(
        "https://docs.python.org/3/library/functions.html",
        "Legitimate URL (Python Docs)"
    )
    
    print("\n\n" + "="*80)
    print("✅ TEST SUITE COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main()
