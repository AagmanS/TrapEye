import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import os
import warnings
from collections import Counter
import math
import string
import re
warnings.filterwarnings('ignore')

class URLFeatureExtractor:
    """Standalone feature extractor for training"""
    def __init__(self):
        # Enhanced suspicious keywords with more specific phishing terms
        self.suspicious_keywords = [
            'login', 'secure', 'account', 'verify', 'update', 'signin', 
            'bank', 'confirm', 'reset', 'password', 'security', 'authenticate',
            'validation', 'ebay', 'signin', 'verification', 'suspend', 'unlock',
            'activate', 'reactivate', 'revalidate', 'renew', 'upgrade', 'limited',
            'expires', 'alert', 'warning', 'urgent', 'immediate', 'critical'
        ]
        
        # Brand impersonation keywords - more comprehensive list
        self.brand_impersonation_keywords = [
            'paypal', 'google', 'apple', 'amazon', 'netflix', 'facebook',
            'twitter', 'instagram', 'microsoft', 'wellsfargo', 'chase', 
            'citibank', 'bankofamerica', 'hsbc', 'barclays', 'office365',
            'adobe', 'dropbox', 'linkedin', 'yahoo', 'ebay', 'alibaba',
            'walmart', 'target', 'costco', 'visa', 'mastercard', 'americanexpress'
        ]
        
        # Popular brands for typosquatting detection - expanded list
        self.popular_brands = [
            'google', 'facebook', 'amazon', 'paypal', 'microsoft', 'apple',
            'netflix', 'instagram', 'linkedin', 'twitter', 'chase', 'wellsfargo',
            'bankofamerica', 'citibank', 'ebay', 'yahoo', 'adobe', 'dropbox',
            'alibaba', 'walmart', 'target', 'costco', 'visa', 'mastercard'
        ]
        
        # URL shortening services - expanded list
        self.url_shorteners = [
            'bit.ly', 'goo.gl', 'tinyurl.com', 'ow.ly', 't.co', 'is.gd',
            'buff.ly', 'adf.ly', 'bit.do', 'short.link', 'tiny.cc', 'cutt.ly',
            'bl.ink', 'rebrand.ly', 'shorturl.at', 'rb.gy'
        ]
        
        # Phishing terms - more specific terms
        self.phishing_terms = [
            'cgi-bin', 'cmd', 'execute', 'admin', 'signin', 'verification', 'suspend',
            'unlock', 'activate', 'reactivate', 'revalidate', 'renew'
        ]
        
        # Suspicious TLDs often used in phishing
        self.suspicious_tlds = [
            'tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top', 'club', 'info', 'site',
            'online', 'space', 'tech', 'host', 'press', 'website', 'work', 'life'
        ]
        
        # Suspicious free hosting services
        self.suspicious_hosting_services = [
            'trycloudflare.com', 'pages.dev', 'netlify.app', 'vercel.app',
            'github.io', 'herokuapp.com', 'firebaseapp.com', 'surge.sh',
            'netlify.com', 'vercel.com', 'glitch.me', '000webhostapp.com',
            'weebly.com', 'wixsite.com', 'yolasite.com', 'freehosting.com'
        ]
    
    def extract_features(self, url):
        """Extract all features from URL"""
        features = {}
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Basic URL features
        features['url_length'] = len(url)
        features['has_https'] = 1 if url.startswith('https') else 0
        
        # Parse URL components
        try:
            if '://' in url:
                scheme, rest = url.split('://', 1)
            else:
                scheme = ''
                rest = url
            
            if '/' in rest:
                netloc, path = rest.split('/', 1)
                path = '/' + path
            else:
                netloc = rest
                path = ''
                
            if '?' in path:
                path, query = path.split('?', 1)
            else:
                query = ''
                
        except:
            netloc = ''
            path = ''
            query = ''
        
        # Network location features
        features['netloc_length'] = len(netloc)
        features['domain_length'] = self._get_domain_length(netloc)
        features['has_ip'] = 1 if self._contains_ip(netloc) else 0
        features['count_subdomains'] = self._count_subdomains(netloc)
        features['has_at_symbol'] = 1 if '@' in url else 0
        features['has_port'] = self._has_port(url)
        features['domain_age'] = 0.5  # Placeholder
        features['suspicious_hosting'] = self._check_suspicious_hosting(netloc)
        features['is_url_shortener'] = self._is_url_shortener(netloc)
        features['is_suspicious_tld'] = self._is_suspicious_tld(netloc)
        
        # Path features
        features['path_length'] = len(path)
        features['has_double_slash_in_path'] = 1 if '//' in path else 0
        features['has_encoded_chars'] = 1 if '%' in url else 0
        features['path_depth'] = self._count_path_depth(path)
        
        # Character analysis
        features['count_digits'] = sum(c.isdigit() for c in url)
        features['digit_ratio'] = sum(c.isdigit() for c in netloc) / max(len(netloc), 1)
        features['count_special_chars'] = self._count_special_chars(url)
        features['count_dashes'] = url.count('-')
        features['count_dashes_in_domain'] = netloc.count('-')
        features['count_dots'] = url.count('.')
        features['count_underscores'] = url.count('_')
        features['count_at_symbols'] = url.count('@')
        features['has_hex_encoding'] = 1 if self._has_hex_encoding(url) else 0
        
        # Entropy calculations
        features['domain_entropy'] = self._calculate_entropy(netloc)
        features['url_entropy'] = self._calculate_entropy(url)
        features['path_entropy'] = self._calculate_entropy(path)
        
        # Suspicious elements
        features['suspicious_keyword_count'] = self._count_suspicious_keywords(url)
        features['brand_impersonation_count'] = self._count_brand_impersonation(url)
        features['phishing_terms_count'] = self._count_phishing_terms(url)
        features['typosquatting_score'] = self._detect_typosquatting(netloc)
        features['char_repetition_ratio'] = self._calculate_char_repetition(netloc)
        
        # Query parameters
        features['query_param_count'] = query.count('&') + 1 if '&' in query else (1 if query else 0)
        features['suspicious_params_count'] = self._count_suspicious_params(query)
        
        # Token analysis
        features['average_token_length'] = self._average_token_length(url)
        features['max_token_length'] = self._max_token_length(url)
        features['token_count'] = self._count_tokens(url)
        
        # TLD and domain analysis
        features['tld'] = self._encode_tld(netloc)
        features['tld_length'] = self._get_tld_length(netloc)
        features['is_known_tld'] = self._is_known_tld(netloc)
        
        return features
    
    def _contains_ip(self, netloc):
        """Check if netloc contains IP address"""
        parts = netloc.split('.')
        if len(parts) == 4:
            try:
                return all(0 <= int(part) <= 255 for part in parts)
            except:
                return False
        return False
    
    def _count_subdomains(self, netloc):
        """Count number of subdomains"""
        parts = netloc.split('.')
        if len(parts) > 2:
            return len(parts) - 2
        return 0
    
    def _count_special_chars(self, text):
        """Count special characters (excluding dots, slashes, colons)"""
        special_chars = "!@#$%^&*()_+-=[]{}|;',?~`"
        return sum(1 for c in text if c in special_chars)
    
    def _calculate_entropy(self, text):
        """Calculate Shannon entropy"""
        if len(text) <= 1:
            return 0
        try:
            counts = Counter(text)
            probs = [float(count) / len(text) for count in counts.values()]
            return -sum(p * math.log2(p) for p in probs if p > 0)
        except:
            return 0
    
    def _count_suspicious_keywords(self, url):
        """Count suspicious keywords in URL"""
        url_lower = url.lower()
        count = 0
        for keyword in self.suspicious_keywords:
            if keyword in url_lower:
                count += 1
        return count
    
    def _average_token_length(self, url):
        """Calculate average token length"""
        tokens = url.replace('.', ' ').replace('/', ' ').replace('?', ' ').replace('&', ' ').replace('=', ' ').split()
        if not tokens:
            return 0
        return sum(len(token) for token in tokens) / len(tokens)
    
    def _encode_tld(self, netloc):
        """Simple TLD encoding (1 for common, 0 for others)"""
        common_tlds = ['.com', '.org', '.net', '.edu', '.gov']
        netloc_lower = netloc.lower()
        return 1 if any(netloc_lower.endswith(tld) for tld in common_tlds) else 0
    
    def _get_domain_length(self, netloc):
        """Get the length of the main domain"""
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        parts = netloc.split('.')
        if len(parts) >= 2:
            return len(parts[-2]) + len(parts[-1]) + 1
        return len(netloc)
    
    def _has_port(self, url):
        """Check if URL has explicit port"""
        # Simple check for :port pattern
        pattern = r'://[^/]+:(\d+)'
        return 1 if re.search(pattern, url) else 0
    
    def _is_url_shortener(self, netloc):
        """Check if domain is a URL shortener"""
        for shortener in self.url_shorteners:
            if shortener in netloc.lower():
                return 1
        return 0
    
    def _has_hex_encoding(self, url):
        """Check for hexadecimal encoding"""
        return 1 if re.search(r'%[0-9a-fA-F]{2}', url) else 0
    
    def _count_brand_impersonation(self, url):
        """Count brand impersonation attempts"""
        url_lower = url.lower()
        count = 0
        for keyword in self.brand_impersonation_keywords:
            if keyword in url_lower:
                count += 1
        return count
    
    def _count_phishing_terms(self, url):
        """Count phishing-related terms"""
        url_lower = url.lower()
        count = 0
        for term in self.phishing_terms:
            if term in url_lower:
                count += 1
        return count
    
    def _detect_typosquatting(self, netloc):
        """Detect potential typosquatting"""
        netloc_lower = netloc.lower()
        domain_parts = netloc_lower.split('.')
        
        if len(domain_parts) >= 2:
            main_domain = domain_parts[-2]
        else:
            main_domain = netloc_lower
        
        score = 0
        for brand in self.popular_brands:
            if brand in main_domain and brand != main_domain:
                score += 1
            elif self._levenshtein_distance(brand, main_domain) <= 2 and len(brand) > 4:
                score += 1
        
        return min(score, 3)
    
    def _levenshtein_distance(self, s1, s2):
        """Calculate Levenshtein distance"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _calculate_char_repetition(self, text):
        """Calculate character repetition ratio"""
        if len(text) <= 1:
            return 0
        repetitions = 0
        for i in range(len(text) - 1):
            if text[i] == text[i + 1]:
                repetitions += 1
        return repetitions / max(len(text) - 1, 1)
    
    def _count_suspicious_params(self, query):
        """Count suspicious query parameters"""
        if not query:
            return 0
        suspicious = ['id', 'key', 'token', 'password', 'username', 'email', 'session']
        query_lower = query.lower()
        count = 0
        for param in suspicious:
            if param in query_lower:
                count += 1
        return count
    
    def _max_token_length(self, url):
        """Find maximum token length"""
        tokens = re.split(r'[./?=&_-]', url)
        tokens = [t for t in tokens if t]
        return max(len(token) for token in tokens) if tokens else 0
    
    def _count_tokens(self, url):
        """Count number of tokens"""
        tokens = re.split(r'[./?=&_-]', url)
        tokens = [t for t in tokens if t]
        return len(tokens)
    
    def _get_tld_length(self, netloc):
        """Get TLD length"""
        parts = netloc.split('.')
        return len(parts[-1]) if len(parts) > 1 else 3
    
    def _is_known_tld(self, netloc):
        """Check if TLD is known"""
        known_tlds = ['com', 'org', 'net', 'edu', 'gov', 'uk', 'ca', 'de', 'fr', 'io']
        parts = netloc.split('.')
        if len(parts) > 1:
            return 1 if parts[-1].lower() in known_tlds else 0
        return 1
    
    def _is_suspicious_tld(self, netloc):
        """Check if TLD is suspicious"""
        parts = netloc.split('.')
        if len(parts) > 1:
            tld = parts[-1].lower()
            return 1 if tld in self.suspicious_tlds else 0
        return 0
    
    def _check_suspicious_hosting(self, netloc):
        """Check if domain is hosted on suspicious free hosting service"""
        netloc_lower = netloc.lower()
        for service in self.suspicious_hosting_services:
            if service in netloc_lower:
                return 1
        return 0
    
    def _count_path_depth(self, path):
        """Count path depth"""
        if not path or path == '/':
            return 0
        path = path.strip('/')
        return path.count('/') + 1 if path else 0

class PhishingDetectorTrainer:
    def __init__(self):
        self.model = None
        self.feature_names = []
        self.baseline_means = {}
        self.feature_extractor = URLFeatureExtractor()
        
    def create_synthetic_dataset(self, n_samples=2000):
        """Create a realistic demo dataset with comprehensive phishing patterns"""
        np.random.seed(42)
        
        data = []
        print("Generating synthetic dataset with enhanced phishing patterns...")
        
        for i in range(n_samples):
            if i % 200 == 0:
                print(f"Generated {i}/{n_samples} samples...")
                
            # Benign URLs (60%)
            if i < n_samples * 0.6:
                url = self._generate_benign_url()
                label = 0
            # Phishing URLs (40%)
            else:
                url = self._generate_phishing_url()
                label = 1
            
            features = self.feature_extractor.extract_features(url)
            features['label'] = label
            
            # Convert features to list in correct order
            feature_list = [features.get(col, 0) for col in [
                'url_length', 'netloc_length', 'domain_length', 'path_length', 
                'count_digits', 'digit_ratio', 'count_special_chars', 'count_dashes',
                'count_dashes_in_domain', 'count_dots', 'count_underscores', 
                'count_at_symbols', 'has_ip', 'count_subdomains', 'has_at_symbol',
                'has_port', 'has_double_slash_in_path', 'has_encoded_chars', 
                'has_hex_encoding', 'domain_entropy', 'url_entropy', 'path_entropy',
                'has_https', 'suspicious_keyword_count', 'brand_impersonation_count',
                'phishing_terms_count', 'typosquatting_score', 'char_repetition_ratio',
                'query_param_count', 'suspicious_params_count', 'average_token_length',
                'max_token_length', 'token_count', 'tld', 'tld_length', 'is_known_tld',
                'path_depth', 'domain_age', 'suspicious_hosting', 'is_url_shortener',
                'label'
            ]]
            data.append(feature_list)
        
        columns = [
            'url_length', 'netloc_length', 'domain_length', 'path_length', 
            'count_digits', 'digit_ratio', 'count_special_chars', 'count_dashes',
            'count_dashes_in_domain', 'count_dots', 'count_underscores', 
            'count_at_symbols', 'has_ip', 'count_subdomains', 'has_at_symbol',
            'has_port', 'has_double_slash_in_path', 'has_encoded_chars', 
            'has_hex_encoding', 'domain_entropy', 'url_entropy', 'path_entropy',
            'has_https', 'suspicious_keyword_count', 'brand_impersonation_count',
            'phishing_terms_count', 'typosquatting_score', 'char_repetition_ratio',
            'query_param_count', 'suspicious_params_count', 'average_token_length',
            'max_token_length', 'token_count', 'tld', 'tld_length', 'is_known_tld',
            'path_depth', 'domain_age', 'suspicious_hosting', 'is_url_shortener',
            'label'
        ]
        
        return pd.DataFrame(data, columns=columns)
    
    def _generate_benign_url(self):
        """Generate realistic benign URL"""
        # Legitimate domains
        domains = [
            "github.com", "stackoverflow.com", "wikipedia.org", "microsoft.com",
            "python.org", "google.com", "amazon.com", "linkedin.com",
            "medium.com", "reddit.com", "youtube.com", "twitter.com"
        ]
        domain = np.random.choice(domains)
        
        # Use HTTPS most of the time
        scheme = "https" if np.random.random() < 0.9 else "http"
        url = f"{scheme}://{domain}/"
        
        # Add path 80% of time
        if np.random.random() < 0.8:
            paths = ["docs", "articles", "help", "support", "download", "api", "blog", "about"]
            path = np.random.choice(paths)
            url += f"{path}/"
            
            # Add sub-path
            if np.random.random() < 0.6:
                subpaths = ["tutorial", "guide", "reference", "getting-started", "examples"]
                url += f"{np.random.choice(subpaths)}/"
            
            # Add page
            if np.random.random() < 0.5:
                url += f"page{np.random.randint(1, 100)}.html"
        
        # Add query params occasionally
        if np.random.random() < 0.3:
            url += f"?page={np.random.randint(1, 50)}&sort=date"
        
        return url
    
    def _generate_phishing_url(self):
        """Generate realistic phishing URL with various attack patterns"""
        attack_type = np.random.choice([
            'brand_impersonation', 'typosquatting', 'subdomain_attack', 
            'ip_based', 'suspicious_tld', 'url_shortener_like', 'free_hosting'
        ])
        
        if attack_type == 'brand_impersonation':
            # Brand name + suspicious keywords
            brands = ['paypal', 'amazon', 'microsoft', 'apple', 'netflix', 'facebook']
            keywords = ['login', 'secure', 'verify', 'account', 'update', 'confirm']
            brand = np.random.choice(brands)
            keyword = np.random.choice(keywords)
            
            # Mix brand and keyword with dashes
            domain = f"{brand}-{keyword}-{np.random.choice(['secure', 'online', 'portal'])}"
            tld = np.random.choice(['.com', '.net', '.tk', '.ml', '.ga'])
            url = f"http://{domain}{tld}/"
            
        elif attack_type == 'typosquatting':
            # Slight misspellings of popular brands
            typos = [
                ('google', ['gooogle', 'googel', 'gogle', 'go0gle']),
                ('paypal', ['paypai', 'paypa1', 'paypall', 'paipal']),
                ('amazon', ['arnazon', 'amazcn', 'amaz0n', 'amaozn']),
                ('microsoft', ['microsft', 'micros0ft', 'microsofte', 'rnicrosoft'])
            ]
            idx = np.random.randint(0, len(typos))
            brand, variations = typos[idx]
            domain = np.random.choice(variations)
            url = f"https://{domain}.com/login/"
            
        elif attack_type == 'subdomain_attack':
            # Legitimate-looking brand in subdomain
            brands = ['paypal', 'amazon', 'apple', 'microsoft', 'netflix']
            brand = np.random.choice(brands)
            fake_domains = ['secure-login', 'verify-account', 'update-info', 'portal-auth']
            fake = np.random.choice(fake_domains)
            url = f"http://{brand}.{fake}.com/signin/?session={np.random.randint(1000, 9999)}"
            
        elif attack_type == 'ip_based':
            # IP address instead of domain
            ip = f"{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}"
            url = f"http://{ip}/login/verify.php?id={np.random.randint(1000, 9999)}"
            
        elif attack_type == 'suspicious_tld':
            # Suspicious TLDs with multiple dashes
            keywords = ['secure', 'banking', 'verify', 'account', 'login']
            domain = '-'.join(np.random.choice(keywords, size=3, replace=False))
            tld = np.random.choice(['.tk', '.ml', '.ga', '.cf', '.gq'])
            url = f"http://{domain}{tld}/auth/login.php"
            
        elif attack_type == 'url_shortener_like':
            # Short, random-looking domain
            chars = string.ascii_lowercase + string.digits
            domain = ''.join(np.random.choice(list(chars), size=6))
            url = f"http://{domain}.com/r/{np.random.randint(10000, 99999)}"
            
        else:  # free_hosting
            # Free hosting services
            keywords = ['login', 'verify', 'secure', 'account']
            subdomain = '-'.join(np.random.choice(keywords, size=2))
            hosting = np.random.choice(['pages.dev', 'netlify.app', 'vercel.app', 'github.io'])
            url = f"https://{subdomain}.{hosting}/signin/"
        
        # Add suspicious query params 70% of time
        if np.random.random() < 0.7 and '?' not in url:
            params = ['token', 'session', 'id', 'key', 'user']
            param = np.random.choice(params)
            url += f"?{param}={np.random.randint(1000, 99999)}"
        
        # Add encoded characters occasionally
        if np.random.random() < 0.2:
            url += "%20verify%20account"
        
        return url
    
    def load_data(self, csv_path=None):
        """Load data from CSV or generate synthetic"""
        if csv_path and os.path.exists(csv_path):
            print(f"Loading data from {csv_path}")
            df = pd.read_csv(csv_path)
        else:
            print("No dataset provided, generating synthetic data for demo...")
            df = self.create_synthetic_dataset(800)  # Smaller for quick demo
        
        # Store baseline means for explainability
        self.feature_names = [col for col in df.columns if col != 'label']
        for feature in self.feature_names:
            self.baseline_means[feature] = df[df['label'] == 0][feature].mean()
        
        print(f"Dataset shape: {df.shape}")
        print(f"Class distribution:\n{df['label'].value_counts()}")
        return df
    
    def train(self, df):
        """Train the Random Forest model with enhanced features"""
        X = df[self.feature_names]
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model with optimized hyperparameters for better performance
        self.model = RandomForestClassifier(
            n_estimators=200,      # Increased for better performance
            max_depth=20,          # Increased to capture complex patterns
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',   # Good for high-dimensional data
            random_state=42,
            class_weight='balanced',
            n_jobs=-1,             # Use all CPU cores
            bootstrap=True,
            oob_score=True         # Enable out-of-bag score estimation
        )
        
        print("Training model with enhanced features...")
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        print(f"Number of features: {len(self.feature_names)}")
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        print("\n" + "="*50)
        print("MODEL EVALUATION RESULTS")
        print("="*50)
        print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
        print(f"Out-of-Bag Score: {self.model.oob_score_:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['benign', 'phishing']))
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        print(f"\nTrue Negatives: {cm[0][0]} | False Positives: {cm[0][1]}")
        print(f"False Negatives: {cm[1][0]} | True Positives: {cm[1][1]}")
        
        return X_test, y_test, y_pred, y_pred_proba
    
    def save_model(self, path='models/phish_model.joblib'):
        """Save model and metadata"""
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'baseline_means': self.baseline_means
        }
        joblib.dump(model_data, path)
        print(f"\n✅ Model saved to {path}")

def main():
    print("🚀 Starting Phishing Detector Training...")
    trainer = PhishingDetectorTrainer()
    
    # Generate synthetic data (no external dependencies)
    df = trainer.load_data()
    
    # Train model
    X_test, y_test, y_pred, y_pred_proba = trainer.train(df)
    
    # Save model
    trainer.save_model()
    
    # Print final metrics
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*50)
    print("FINAL MODEL PERFORMANCE")
    print("="*50)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Show feature importance
    print("\nTop 10 Most Important Features:")
    feature_imp = pd.DataFrame({
        'feature': trainer.feature_names,
        'importance': trainer.model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_imp.head(10))

if __name__ == "__main__":
    main()