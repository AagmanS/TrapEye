def get_demo_urls():
    """Return curated demo URLs for testing"""
    return {
        "benign": [
            "https://github.com/microsoft/vscode",
            "https://stackoverflow.com/questions",
            "https://docs.python.org/3/",
            "https://www.wikipedia.org",
            "https://httpbin.org/json"
        ],
        "phishing": [
            "http://login-verify-account.security-update.com",
            "http://secure-apple-id-confirm.com/validation",
            "https://amazon-payment-update.net/login.php?session=abc123",
            "http://facebook-security-check.tk/verify",
            "http://netflix-billing-update.com/account"
        ],
        "synthetic": [
            "http://user:pass@secure-login-verify.com@phishing.com",
            "https://google-account-confirm.xyz/login?token=123456",
            "http://192.168.1.1/login.php?redirect=paypal.com",
            "https://microsoft-office-verify.com/update/profile"
        ],
        "local_demo": [
            "http://localhost:8001/fake-login.html",
            "http://127.0.0.1:8001/bank-login.html"
        ]
    }