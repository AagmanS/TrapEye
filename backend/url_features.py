import re
import math
from urllib.parse import urlparse, parse_qs
from collections import Counter
import string

# Try to import tldextract, but make it optional
try:
    import tldextract
    TLD_EXTRACT_AVAILABLE = True
except ImportError:
    TLD_EXTRACT_AVAILABLE = False
    tldextract = None
    print("Warning: tldextract not available. Some features will be limited.")

class URLFeatureExtractor:
    def __init__(self):
        # Enhanced suspicious keywords with more specific phishing terms
        self.suspicious_keywords = [
            'login', 'secure', 'account', 'verify', 'update', 'signin', 
            'confirm', 'reset', 'password', 'security', 'authenticate',
            'validation', 'service', 'alert', 'notification', 'verification',
            'cgi-bin', 'cmd', 'execute', 'admin', 'signin', 'suspend', 'unlock',
            'activate', 'reactivate', 'revalidate', 'renew', 'upgrade', 'limited',
            'expires', 'warning', 'urgent', 'immediate', 'critical'
        ]
        
        # Brand impersonation keywords - more comprehensive list
        self.brand_impersonation_keywords = [
            'paypal', 'apple', 'amazon', 'netflix', 'facebook',
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
        
        # Parse URL
        try:
            parsed = urlparse(url)
            netloc = parsed.netloc
            path = parsed.path
            query = parsed.query
        except Exception as e:
            print(f"URL parsing error: {e}")
            return self._minimal_features(url)
        
        # Network location features
        features['netloc_length'] = len(netloc)
        features['domain_length'] = self._get_domain_length(netloc)
        features['has_ip'] = 1 if self._contains_ip(netloc) else 0
        features['count_subdomains'] = self._count_subdomains(netloc)
        features['has_at_symbol'] = 1 if '@' in url else 0
        features['has_port'] = 1 if self._has_non_standard_port(parsed) else 0
        features['domain_age'] = self._estimate_domain_age(netloc)
        
        # Check for suspicious free hosting domains
        features['suspicious_hosting'] = self._check_suspicious_hosting(netloc)
        features['is_url_shortener'] = self._is_url_shortener(netloc)
        features['is_suspicious_tld'] = self._is_suspicious_tld(netloc)  # New feature
        
        # Path features
        features['path_length'] = len(path)
        features['has_double_slash_in_path'] = 1 if '//' in path else 0
        features['has_encoded_chars'] = 1 if '%' in url.lower() else 0
        features['path_depth'] = self._count_path_depth(path)  # New feature
        
        # Character analysis
        features['count_digits'] = sum(c.isdigit() for c in url)
        features['digit_ratio'] = sum(c.isdigit() for c in netloc) / max(len(netloc), 1)
        features['count_special_chars'] = self._count_special_chars(url)
        features['count_dashes'] = url.count('-')
        features['count_dashes_in_domain'] = netloc.count('-')
        features['count_dots'] = url.count('.')
        features['count_underscores'] = url.count('_')
        features['count_at_symbols'] = url.count('@')
        features['has_hex_encoding'] = 1 if self._has_hexadecimal_encoding(url) else 0
        
        # Entropy calculations
        features['domain_entropy'] = self._calculate_entropy(netloc)
        features['url_entropy'] = self._calculate_entropy(url)
        features['path_entropy'] = self._calculate_entropy(path)  # New feature
        
        # Suspicious elements
        features['suspicious_keyword_count'] = self._count_suspicious_keywords(url)
        features['brand_impersonation_count'] = self._count_brand_impersonation(url)
        features['phishing_terms_count'] = self._count_phishing_terms(url)
        features['typosquatting_score'] = self._detect_typosquatting(netloc)
        features['char_repetition_ratio'] = self._calculate_char_repetition(netloc)
        
        # Query parameters
        features['query_param_count'] = self._count_query_params(query)
        features['suspicious_params_count'] = self._count_suspicious_params(query)
        
        # Token analysis
        features['average_token_length'] = self._average_token_length(url)
        features['max_token_length'] = self._max_token_length(url)  # New feature
        features['token_count'] = self._count_tokens(url)  # New feature
        
        # TLD and domain analysis
        features['tld'] = self._encode_tld(netloc)
        features['tld_length'] = self._get_tld_length(netloc)  # New feature
        features['is_known_tld'] = self._is_known_tld(netloc)  # New feature
        
        return features
    
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
    
    def _minimal_features(self, url):
        """Extract minimal features when URL parsing fails"""
        return {
            'url_length': len(url),
            'netloc_length': 0,
            'domain_length': 0,
            'path_length': 0,
            'count_digits': sum(c.isdigit() for c in url),
            'digit_ratio': 0,
            'count_special_chars': self._count_special_chars(url),
            'count_dashes': url.count('-'),
            'count_dashes_in_domain': 0,
            'count_dots': url.count('.'),
            'count_underscores': url.count('_'),
            'count_at_symbols': url.count('@'),
            'has_ip': 0,
            'count_subdomains': 0,
            'has_at_symbol': 1 if '@' in url else 0,
            'has_port': 0,
            'has_double_slash_in_path': 1 if '//' in url else 0,
            'has_encoded_chars': 1 if '%' in url else 0,
            'has_hex_encoding': 0,
            'domain_entropy': 0,
            'url_entropy': self._calculate_entropy(url),
            'path_entropy': 0,
            'has_https': 1 if url.startswith('https') else 0,
            'suspicious_keyword_count': self._count_suspicious_keywords(url),
            'brand_impersonation_count': self._count_brand_impersonation(url),
            'phishing_terms_count': self._count_phishing_terms(url),
            'typosquatting_score': 0,
            'char_repetition_ratio': 0,
            'query_param_count': 0,
            'suspicious_params_count': 0,
            'average_token_length': self._average_token_length(url),
            'max_token_length': len(url),
            'token_count': 1,
            'tld': 1,
            'tld_length': 3,
            'is_known_tld': 1,
            'path_depth': 0,
            'domain_age': 0,
            'suspicious_hosting': 0,
            'is_url_shortener': 0,
            'is_suspicious_tld': 0  # New feature
        }
    
    def _contains_ip(self, netloc):
        """Check if netloc contains IP address"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return 1 if re.search(ip_pattern, netloc) else 0
    
    def _count_subdomains(self, netloc):
        """Count number of subdomains"""
        # Remove port if present
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        
        parts = netloc.split('.')
        # Remove TLD and main domain
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
    
    def _count_brand_impersonation(self, url):
        """Count brand impersonation attempts"""
        url_lower = url.lower()
        count = 0
        for keyword in self.brand_impersonation_keywords:
            if keyword in url_lower:
                count += 1
        return count
    
    def _count_phishing_terms(self, url):
        """Count specific phishing-related terms"""
        phishing_terms = ['cgi-bin', 'cmd', 'execute', 'admin', 'login', 'secure', 'signin', 'verification']
        url_lower = url.lower()
        count = 0
        for term in phishing_terms:
            if term in url_lower:
                count += 1
        return count
    
    def _count_query_params(self, query_string):
        """Count number of query parameters"""
        if not query_string:
            return 0
        try:
            return len(parse_qs(query_string))
        except:
            return 0
    
    def _count_suspicious_params(self, query_string):
        """Count suspicious query parameters"""
        if not query_string:
            return 0
        
        suspicious_params = ['id', 'key', 'token', 'password', 'username', 'email', 'account', 'session']
        try:
            params = parse_qs(query_string)
            count = 0
            for param in params:
                if param.lower() in suspicious_params:
                    count += 1
            return count
        except:
            return 0
    
    def _average_token_length(self, url):
        """Calculate average token length (split by common separators)"""
        try:
            tokens = re.split(r'[./?=&_-]', url)
            tokens = [t for t in tokens if t]  # Remove empty tokens
            if not tokens:
                return 0
            return sum(len(token) for token in tokens) / len(tokens)
        except:
            return len(url) / 10
    
    def _max_token_length(self, url):
        """Find maximum token length"""
        try:
            tokens = re.split(r'[./?=&_-]', url)
            tokens = [t for t in tokens if t]  # Remove empty tokens
            if not tokens:
                return 0
            return max(len(token) for token in tokens)
        except:
            return len(url)
    
    def _count_tokens(self, url):
        """Count number of tokens"""
        try:
            tokens = re.split(r'[./?=&_-]', url)
            tokens = [t for t in tokens if t]  # Remove empty tokens
            return len(tokens)
        except:
            return 1
    
    def _encode_tld(self, netloc):
        """Simple TLD encoding (1 for common, 0 for others)"""
        common_tlds = ['.com', '.org', '.net', '.edu', '.gov']
        netloc_lower = netloc.lower()
        return 1 if any(netloc_lower.endswith(tld) for tld in common_tlds) else 0
    
    def _get_tld_length(self, netloc):
        """Get length of TLD"""
        if TLD_EXTRACT_AVAILABLE and tldextract is not None:
            try:
                extracted = tldextract.extract(netloc)
                return len(extracted.suffix)
            except:
                return 3  # Default for .com
        else:
            # Fallback method without tldextract
            parts = netloc.split('.')
            if len(parts) > 1:
                return len(parts[-1])
            return 3
    
    def _is_known_tld(self, netloc):
        """Check if TLD is from a known list"""
        known_tlds = [
            'com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'co', 'io', 'ai', 
            'uk', 'ca', 'de', 'fr', 'jp', 'au', 'in', 'cn', 'br', 'ru'
        ]
        
        if TLD_EXTRACT_AVAILABLE and tldextract is not None:
            try:
                extracted = tldextract.extract(netloc)
                return 1 if extracted.suffix.lower() in known_tlds else 0
            except:
                return 1  # Default to known
        else:
            # Fallback method without tldextract
            parts = netloc.split('.')
            if len(parts) > 1:
                return 1 if parts[-1].lower() in known_tlds else 0
            return 1  # Default to known
    
    def _count_path_depth(self, path):
        """Count depth of path"""
        if not path or path == '/':
            return 0
        # Remove leading and trailing slashes
        path = path.strip('/')
        if not path:
            return 0
        return path.count('/') + 1
    
    def _estimate_domain_age(self, netloc):
        """Estimate domain age (simplified - in real implementation, would check actual registry data)"""
        # This is a simplified heuristic - in practice, you'd check actual domain registration data
        # For now, we'll return a normalized value between 0 and 1
        # Newer domains (more suspicious) get lower values
        # Older domains get higher values
        return 0.5  # Default neutral value
    
    def _get_domain_length(self, netloc):
        """Get the length of the main domain (excluding subdomains and port)"""
        # Remove port if present
        if ':' in netloc:
            netloc = netloc.split(':')[0]
        
        parts = netloc.split('.')
        if len(parts) >= 2:
            # Get domain name + TLD
            return len(parts[-2]) + len(parts[-1]) + 1  # +1 for the dot
        return len(netloc)
    
    def _has_non_standard_port(self, parsed):
        """Check if URL uses a non-standard port"""
        port = parsed.port
        if port is None:
            return 0
        # Standard ports: 80 (HTTP), 443 (HTTPS)
        return 1 if port not in [80, 443] else 0
    
    def _has_hexadecimal_encoding(self, url):
        """Check for hexadecimal encoding in URL (like %20, %2F)"""
        hex_pattern = r'%[0-9a-fA-F]{2}'
        return 1 if re.search(hex_pattern, url) else 0
    
    def _detect_typosquatting(self, netloc):
        """Detect potential typosquatting by checking similarity to popular brands"""
        netloc_lower = netloc.lower()
        # Remove common TLD and subdomains for comparison
        domain_parts = netloc_lower.split('.')
        
        if len(domain_parts) >= 2:
            main_domain = domain_parts[-2]  # Get main domain part
        else:
            main_domain = netloc_lower
        
        score = 0
        for brand in self.popular_brands:
            # Check for brand name with slight variations
            if brand in main_domain and brand != main_domain:
                # Brand is present but not exact match (possible typosquatting)
                score += 1
            # Check for common typosquatting patterns
            elif self._levenshtein_distance(brand, main_domain) <= 2 and len(brand) > 4:
                score += 1
        
        return min(score, 3)  # Cap at 3 to normalize
    
    def _levenshtein_distance(self, s1, s2):
        """Calculate Levenshtein distance between two strings"""
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
        """Calculate the ratio of repeated characters (suspicious pattern)"""
        if len(text) <= 1:
            return 0
        
        repetitions = 0
        for i in range(len(text) - 1):
            if text[i] == text[i + 1]:
                repetitions += 1
        
        return repetitions / max(len(text) - 1, 1)
    
    def _is_url_shortener(self, netloc):
        """Check if the domain is a URL shortening service"""
        netloc_lower = netloc.lower()
        for shortener in self.url_shorteners:
            if shortener in netloc_lower:
                return 1
        return 0