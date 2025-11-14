import joblib
import numpy as np
from typing import Dict, List, Any
import os

class ModelUtils:
    def __init__(self, model_path=None):
        self.model = None
        self.feature_names = []
        self.baseline_means = {}
        self.feature_importance = {}
        
        # Set default model path
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Try multiple possible locations
            possible_paths = [
                os.path.join(current_dir, 'phish_model.joblib'),  # In backend folder
                os.path.join(os.path.dirname(current_dir), 'models', 'phish_model.joblib'),  # In main models folder
                'models/phish_model.joblib'  # Relative path
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            else:
                # If no model found, use first path
                model_path = possible_paths[1]
        
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load trained model and metadata"""
        try:
            if os.path.exists(model_path):
                model_data = joblib.load(model_path)
                self.model = model_data['model']
                self.feature_names = model_data['feature_names']
                self.baseline_means = model_data['baseline_means']
                
                # Extract feature importance if available
                if hasattr(self.model, 'feature_importances_'):
                    self.feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
                else:
                    # Default importance for demo
                    self.feature_importance = {feature: 1.0 for feature in self.feature_names}
                
                print(f"✅ Model loaded successfully from {model_path}")
            else:
                print(f"⚠️  Model file not found at {model_path}, creating dummy model...")
                self._create_dummy_model()
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a dummy model for demo when no trained model exists"""
        from sklearn.ensemble import RandomForestClassifier
        print("🤖 Creating dummy model for demo...")
        
        # Simple rules-based dummy model
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        
        # Mock training on minimal data with all features
        import pandas as pd
        np.random.seed(42)
        n_features = 40  # Updated feature count
        X_dummy = np.random.rand(100, n_features)
        y_dummy = np.random.randint(0, 2, 100)
        self.model.fit(X_dummy, y_dummy)
        
        self.feature_names = [
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
            'is_suspicious_tld'  # New feature
        ]
        
        self.baseline_means = {feature: 0.5 for feature in self.feature_names}
        self.feature_importance = {feature: np.random.rand() for feature in self.feature_names}
        print("✅ Dummy model created successfully")
    
    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Make prediction and generate explanation"""
        try:
            # Check if model is loaded
            if self.model is None:
                raise Exception("Model not loaded")
            
            # Convert features to array in correct order
            feature_array = np.array([[features.get(f, 0) for f in self.feature_names]])
            
            # Get prediction probabilities
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(feature_array)[0]
                phishing_prob = probabilities[1]  # Probability of class 1 (phishing)
            else:
                # Fallback for models without predict_proba
                prediction = self.model.predict(feature_array)[0]
                phishing_prob = 0.9 if prediction == 1 else 0.1
            
            # ENHANCED BOOSTING: More sophisticated boosting based on feature combinations
            boost_score = 0.0
            
            # Critical red flags - high boosting
            if features.get('has_ip', 0) == 1:
                boost_score += 0.30  # IP address is very suspicious
            
            if features.get('typosquatting_score', 0) >= 3:
                boost_score += 0.35
            elif features.get('typosquatting_score', 0) >= 2:
                boost_score += 0.25
            
            if features.get('brand_impersonation_count', 0) >= 3:
                boost_score += 0.35
            elif features.get('brand_impersonation_count', 0) >= 2:
                boost_score += 0.25
            
            # Strong red flags - moderate boosting
            if features.get('suspicious_hosting', 0) == 1:
                boost_score += 0.25
            
            if features.get('is_url_shortener', 0) == 1:
                boost_score += 0.20
            
            if features.get('suspicious_keyword_count', 0) >= 5:
                boost_score += 0.25
            elif features.get('suspicious_keyword_count', 0) >= 3:
                boost_score += 0.15
            
            if features.get('has_https', 0) == 0:
                boost_score += 0.15
            
            if features.get('count_dashes_in_domain', 0) >= 5:
                boost_score += 0.20
            elif features.get('count_dashes_in_domain', 0) >= 3:
                boost_score += 0.10
            
            if features.get('has_port', 0) == 1:
                boost_score += 0.15
            
            if features.get('has_hex_encoding', 0) == 1:
                boost_score += 0.20
            
            if features.get('suspicious_params_count', 0) >= 4:
                boost_score += 0.20
            elif features.get('suspicious_params_count', 0) >= 2:
                boost_score += 0.10
            
            # Moderate red flags - light boosting
            if features.get('count_subdomains', 0) > 6:
                boost_score += 0.15
            elif features.get('count_subdomains', 0) > 4:
                boost_score += 0.10
            
            if features.get('url_entropy', 0) > 6.5:
                boost_score += 0.15
            elif features.get('url_entropy', 0) > 5.5:
                boost_score += 0.10
            
            if features.get('digit_ratio', 0) > 0.5:
                boost_score += 0.12
            elif features.get('digit_ratio', 0) > 0.3:
                boost_score += 0.08
            
            if features.get('char_repetition_ratio', 0) > 0.5:
                boost_score += 0.12
            elif features.get('char_repetition_ratio', 0) > 0.3:
                boost_score += 0.08
            
            if features.get('has_at_symbol', 0) == 1:
                boost_score += 0.15
            
            if features.get('url_length', 0) > 200:
                boost_score += 0.12
            elif features.get('url_length', 0) > 100:
                boost_score += 0.08
            
            if features.get('phishing_terms_count', 0) >= 4:
                boost_score += 0.15
            elif features.get('phishing_terms_count', 0) >= 2:
                boost_score += 0.10
            
            if not features.get('is_known_tld', 1):
                boost_score += 0.10
            
            if features.get('is_suspicious_tld', 0) == 1:
                boost_score += 0.15
            
            # Apply boost with cap at 0.98
            phishing_prob = min(phishing_prob + boost_score, 0.98)
            
            # ADJUSTED THRESHOLD: Better balance between precision and recall
            label = "phish" if phishing_prob > 0.60 else "safe"  # Slightly lowered from 0.65 for better recall
            
            # Generate explanations
            reasons = self._generate_reasons(features, phishing_prob)
            explainability = self._generate_explainability(features, phishing_prob)
            
            # Calculate confidence based on distance from decision boundary
            confidence = self._calculate_confidence(phishing_prob)
            
            return {
                "label": label,
                "score": float(phishing_prob),
                "reasons": reasons[:5],  # Top 5 reasons
                "explainability": explainability,
                "confidence": confidence
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                "label": "safe",
                "score": 0.0,
                "reasons": ["Error in analysis - assuming safe"],
                "explainability": [],
                "confidence": 0.0
            }
    
    def _calculate_confidence(self, score: float) -> float:
        """Calculate model confidence based on distance from decision boundary"""
        # Confidence is higher when score is further from 0.5 (decision boundary)
        distance_from_boundary = abs(score - 0.5)
        # Normalize to 0-1 range
        confidence = min(distance_from_boundary * 2, 1.0)
        return round(confidence, 3)
    
    def _generate_reasons(self, features: Dict[str, float], score: float) -> List[str]:
        """Generate human-readable reasons for the prediction with detailed explanations"""
        reasons = []
        
        # High score reasons with detailed explanations
        if score > 0.9:
            reasons.append("🚨 CRITICAL RISK: URL exhibits multiple strong phishing indicators")
        elif score > 0.75:
            reasons.append("🚨 VERY HIGH RISK: URL shows several concerning characteristics")
        elif score > 0.6:
            reasons.append("⚠️ HIGH RISK: URL shows several concerning characteristics")
        elif score > 0.45:
            reasons.append("⚠️ MODERATE-HIGH RISK: URL has suspicious features")
        elif score > 0.35:
            reasons.append("⚠️ MODERATE RISK: URL has some suspicious features")
        elif score > 0.25:
            reasons.append("⚠️ LOW-MODERATE RISK: URL has minor suspicious indicators")
        
        # Feature-based reasons with detailed explanations
        suspicious_words = features.get('suspicious_keyword_count', 0)
        if suspicious_words >= 5:
            reasons.append(f"🔤 Contains {int(suspicious_words)} highly suspicious keywords (e.g., 'login', 'secure', 'bank')")
        elif suspicious_words >= 3:
            reasons.append(f"🔤 Contains {int(suspicious_words)} suspicious keywords that mimic legitimate services")
        elif suspicious_words >= 1:
            reasons.append(f"🔤 Contains {int(suspicious_words)} keyword commonly used in phishing attempts")
        
        brand_impersonation = features.get('brand_impersonation_count', 0)
        if brand_impersonation >= 2:
            reasons.append(f"🏢 Impersonates {int(brand_impersonation)} well-known brands (e.g., PayPal, Google, Amazon)")
        elif brand_impersonation >= 1:
            reasons.append("🏢 Attempts to impersonate a well-known brand")
        
        typosquatting = features.get('typosquatting_score', 0)
        if typosquatting >= 2:
            reasons.append(f"⚠️ High typosquatting risk (score: {int(typosquatting)}) - domain similar to popular brands")
        elif typosquatting >= 1:
            reasons.append("⚠️ Possible typosquatting detected - domain name resembles known brands")
        
        if features.get('has_ip', 0) == 1:
            reasons.append("🌐 Uses IP address instead of domain name - a common phishing technique")
        
        if features.get('is_url_shortener', 0) == 1:
            reasons.append("🔗 URL shortening service detected - often used to hide phishing URLs")
        
        subdomains = features.get('count_subdomains', 0)
        if subdomains > 5:
            reasons.append(f"🔗 Excessive subdomains ({int(subdomains)}) - often used to appear legitimate")
        elif subdomains > 3:
            reasons.append(f"🔗 Many subdomains ({int(subdomains)}) - may indicate phishing attempt")
        elif subdomains > 2:
            reasons.append(f"🔗 Multiple subdomains ({int(subdomains)}) - could be suspicious")
        
        if features.get('has_https', 0) == 0:
            reasons.append("🔓 No HTTPS encryption - legitimate sites typically use HTTPS for security")
        
        if features.get('has_port', 0) == 1:
            reasons.append("🔌 Uses non-standard port - unusual for legitimate websites")
        
        digit_ratio = features.get('digit_ratio', 0)
        if digit_ratio > 0.3:
            reasons.append(f"🔢 High digit ratio ({digit_ratio:.2f}) in domain - unusual pattern")
        elif digit_ratio > 0.2:
            reasons.append(f"🔢 Moderate digit ratio ({digit_ratio:.2f}) in domain - potentially suspicious")
        
        dashes_in_domain = features.get('count_dashes_in_domain', 0)
        if dashes_in_domain > 3:
            reasons.append(f"➖ Excessive dashes ({int(dashes_in_domain)}) in domain - common phishing tactic")
        elif dashes_in_domain > 1:
            reasons.append(f"➖ Multiple dashes ({int(dashes_in_domain)}) in domain - potentially suspicious")
        
        entropy = features.get('url_entropy', 0)
        if entropy > 5.5:
            reasons.append(f"🎲 Very high URL randomness ({entropy:.1f}) - may indicate obfuscation")
        elif entropy > 5.0:
            reasons.append(f"🎲 High URL randomness ({entropy:.1f}) - may indicate obfuscation")
        elif entropy > 4.5:
            reasons.append(f"🎲 Elevated URL randomness ({entropy:.1f}) - somewhat unusual")
        
        if features.get('has_at_symbol', 0) == 1:
            reasons.append("📧 Contains '@' symbol in URL (often used to trick users about the real domain)")
        
        if features.get('has_hex_encoding', 0) == 1:
            reasons.append("🔤 Contains hexadecimal encoding - often used to obfuscate malicious URLs")
        elif features.get('has_encoded_chars', 0) == 1:
            reasons.append("🔤 Contains encoded characters (often used to obfuscate malicious URLs)")
        
        url_length = features.get('url_length', 0)
        if url_length > 150:
            reasons.append(f"📏 Very long URL ({int(url_length)} characters) - often used in phishing to obfuscate")
        elif url_length > 100:
            reasons.append(f"📏 Long URL ({int(url_length)} characters) - may indicate obfuscation")
        elif url_length > 80:
            reasons.append(f"📏 Moderately long URL ({int(url_length)} characters) - somewhat unusual")
        
        query_params = features.get('query_param_count', 0)
        suspicious_params = features.get('suspicious_params_count', 0)
        if suspicious_params >= 3:
            reasons.append(f"❓ Multiple suspicious parameters ({int(suspicious_params)}) - may carry malicious data")
        elif suspicious_params >= 1:
            reasons.append(f"❓ Suspicious parameter detected - could be used for credential theft")
        elif query_params > 10:
            reasons.append(f"❓ Excessive query parameters ({int(query_params)}) - often used to carry malicious data")
        elif query_params > 5:
            reasons.append(f"❓ Many query parameters ({int(query_params)}) - potentially suspicious")
        
        # Check for suspicious hosting
        if features.get('suspicious_hosting', 0) == 1:
            reasons.append("⚠️ Hosted on free service (e.g., trycloudflare.com) - commonly used for phishing")
        
        char_repetition = features.get('char_repetition_ratio', 0)
        if char_repetition > 0.3:
            reasons.append(f"🔁 High character repetition ({char_repetition:.2f}) - unusual pattern")
        
        phishing_terms = features.get('phishing_terms_count', 0)
        if phishing_terms >= 2:
            reasons.append(f"🎯 Contains {int(phishing_terms)} phishing-specific terms")
        elif phishing_terms >= 1:
            reasons.append("🎯 Contains phishing-related terminology")
        
        # Low score reassurances with detailed explanations
        if score < 0.15:
            if features.get('has_https', 0) == 1:
                reasons.append("🔒 Uses HTTPS encryption - indicates good security practices")
            if suspicious_words == 0:
                reasons.append("✅ No suspicious keywords detected in the URL")
            if subdomains <= 2:
                reasons.append("✅ Normal domain structure with few subdomains")
            if features.get('has_hex_encoding', 0) == 0:
                reasons.append("✅ No encoded characters detected")
            if url_length < 70:
                reasons.append("✅ Reasonable URL length for a legitimate website")
            if query_params < 3:
                reasons.append("✅ Minimal query parameters - reduces attack surface")
            if typosquatting == 0:
                reasons.append("✅ No typosquatting patterns detected")
        elif score < 0.25:
            reasons.append("✅ Overall URL characteristics align with legitimate websites")
        elif score < 0.35:
            reasons.append("⚠️ URL has some minor anomalies but may be legitimate")
        
        # Additional context-based reasons
        path_depth = features.get('path_depth', 0)
        if path_depth > 7:
            reasons.append(f"📁 Deep URL path ({int(path_depth)} levels) - sometimes used to mimic legitimate sites")
        elif path_depth > 5:
            reasons.append(f"📁 Moderately deep path ({int(path_depth)} levels) - somewhat unusual")
        
        if not features.get('is_known_tld', 1):
            reasons.append("🌐 Uses uncommon TLD - less common for legitimate sites")
        
        return reasons if reasons else ["⚠️ URL shows some suspicious characteristics based on analysis"]
    
    def _generate_explainability(self, features: Dict[str, float], score: float) -> List[Dict]:
        """Generate detailed feature impact explanations"""
        explainability = []
        
        # Calculate impact for all features
        for feature in self.feature_names:
            if feature in features:
                value = features.get(feature, 0)
                baseline = self.baseline_means.get(feature, 0.5)
                importance = self.feature_importance.get(feature, 0.1)
                
                # Calculate deviation from baseline
                deviation = value - baseline
                
                # Calculate impact (deviation * importance)
                impact = deviation * importance
                
                # Generate human-readable description
                description = self._generate_feature_description(feature, value, baseline)
                
                explainability.append({
                    "feature": feature,
                    "value": round(value, 3),
                    "baseline": round(baseline, 3),
                    "importance": round(importance, 3),
                    "deviation": round(deviation, 3),
                    "impact": round(impact, 3),
                    "description": description
                })
        
        # Sort by absolute impact
        explainability.sort(key=lambda x: abs(x['impact']), reverse=True)
        return explainability[:10]  # Top 10 features
    
    def _generate_feature_description(self, feature: str, value: float, baseline: float) -> str:
        """Generate human-readable description for a feature"""
        descriptions = {
            'url_length': f"URL length is {int(value)} characters",
            'netloc_length': f"Domain name length is {int(value)} characters",
            'domain_length': f"Main domain length is {int(value)} characters",
            'path_length': f"Path length is {int(value)} characters",
            'count_digits': f"Contains {int(value)} digits",
            'digit_ratio': f"Digit ratio is {value:.2f}",
            'count_special_chars': f"Contains {int(value)} special characters",
            'count_dashes': f"Contains {int(value)} dashes",
            'count_dashes_in_domain': f"Domain contains {int(value)} dashes",
            'count_dots': f"Contains {int(value)} dots",
            'count_underscores': f"Contains {int(value)} underscores",
            'count_at_symbols': f"Contains {int(value)} @ symbols",
            'has_ip': "Uses IP address instead of domain" if value == 1 else "Uses domain name",
            'count_subdomains': f"Has {int(value)} subdomains",
            'has_at_symbol': "Contains '@' symbol" if value == 1 else "No '@' symbol",
            'has_port': "Uses non-standard port" if value == 1 else "Uses standard port",
            'has_double_slash_in_path': "Double slash in path" if value == 1 else "No double slash in path",
            'has_encoded_chars': "Contains encoded characters" if value == 1 else "No encoded characters",
            'has_hex_encoding': "Contains hexadecimal encoding" if value == 1 else "No hexadecimal encoding",
            'domain_entropy': f"Domain randomness is {value:.2f}",
            'url_entropy': f"URL randomness is {value:.2f}",
            'path_entropy': f"Path randomness is {value:.2f}",
            'has_https': "Uses HTTPS encryption" if value == 1 else "No HTTPS encryption",
            'suspicious_keyword_count': f"Contains {int(value)} suspicious keywords",
            'brand_impersonation_count': f"Impersonates {int(value)} brands",
            'phishing_terms_count': f"Contains {int(value)} phishing terms",
            'typosquatting_score': f"Typosquatting score: {int(value)}",
            'char_repetition_ratio': f"Character repetition ratio: {value:.2f}",
            'query_param_count': f"Has {int(value)} query parameters",
            'suspicious_params_count': f"Has {int(value)} suspicious parameters",
            'average_token_length': f"Average token length is {value:.2f}",
            'max_token_length': f"Longest token is {int(value)} characters",
            'token_count': f"Has {int(value)} tokens",
            'tld': "Uses common TLD" if value == 1 else "Uses uncommon TLD",
            'tld_length': f"TLD length is {int(value)} characters",
            'is_known_tld': "Uses known TLD" if value == 1 else "Uses unknown TLD",
            'path_depth': f"Path depth is {int(value)} levels",
            'domain_age': f"Domain age score is {value:.2f}",
            'suspicious_hosting': "Hosted on suspicious free service" if value == 1 else "Not hosted on suspicious free service",
            'is_url_shortener': "URL shortening service" if value == 1 else "Not a URL shortener"
        }
        
        return descriptions.get(feature, f"Feature '{feature}' has value {value}")
    
    def _calculate_feature_impact(self, feature: str, value: float, score: float) -> float:
        """Calculate simplified feature impact (deprecated but kept for compatibility)"""
        # Simple heuristic impacts
        impact_rules = {
            'suspicious_keyword_count': value * 0.15,
            'has_https': -0.4 if value == 1 else 0.3,
            'has_ip': 0.5 if value == 1 else 0,
            'count_subdomains': (value - 2) * 0.15,
            'url_entropy': (value - 3.0) * 0.25,
            'has_at_symbol': 0.4 if value == 1 else 0,
            'suspicious_hosting': 0.3 if value == 1 else 0  # New rule for suspicious hosting
        }
        
        return impact_rules.get(feature, 0.0)