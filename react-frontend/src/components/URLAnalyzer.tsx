import * as React from 'react';
import { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';
import './URLAnalyzer.css';

interface AnalysisResult {
  label: string;
  score: number;
  reasons: string[];
  explainability: Array<{
    feature: string;
    value: number;
    baseline: number;
    importance: number;
    deviation: number;
    impact: number;
    description: string;
  }>;
  confidence: number;
}

const URLAnalyzer: React.FC = () => {
  const [url, setUrl] = useState<string>('');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeUrl = async () => {
    if (!url) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      // Add http:// prefix if missing
      const formattedUrl = url.startsWith('http') ? url : `http://${url}`;
      
      const response = await axios.post('http://localhost:8002/predict', {
        url: formattedUrl
      });

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Error analyzing URL');
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevel = (score: number) => {
    if (score > 0.7) return { level: 'PHISHING 🔴', className: 'high-risk', range: '0.701 - 1.000' };
    if (score > 0.3) return { level: 'SUSPICIOUS 🟡', className: 'medium-risk', range: '0.301 - 0.700' };
    return { level: 'SAFE 🟢', className: 'low-risk', range: '0.000 - 0.300' };
  };

  const getConfidenceLevel = (confidence: number) => {
    if (confidence > 0.8) return 'High';
    if (confidence > 0.5) return 'Medium';
    return 'Low';
  };

  const reportPhishing = () => {
    if (result && result.score > 0.7 && url) {
      // Open the cybercrime reporting portal with pre-filled data
      const reportUrl = `https://cybercrime.gov.in/Webform/Accept.aspx?reported_url=${encodeURIComponent(url)}&risk_score=${result.score}`;
      window.open(reportUrl, '_blank');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="analyzer-container"
    >
      <div className="analyzer-header">
        <h1>🔗 URL Analyzer</h1>
        <p>Enter a URL to check for phishing and security risks</p>
      </div>

      <div className="analyzer-form">
        <div className="input-group">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL to analyze (e.g., https://example.com)"
            className="url-input"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={analyzeUrl}
            disabled={loading}
            className="analyze-button"
          >
            {loading ? 'Analyzing...' : '🔍 Analyze URL'}
          </motion.button>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="error-message"
          >
            {error}
          </motion.div>
        )}
      </div>

      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="analysis-results"
        >
          <div className="result-header">
            <h2>Analysis Results</h2>
            <div className="score-display">
              <div className="score-value">{(result.score * 100).toFixed(1)}%</div>
              <div className={`risk-level ${getRiskLevel(result.score).className}`}>
                {getRiskLevel(result.score).level}
              </div>
              <div className="risk-range">
                Range: {getRiskLevel(result.score).range}
              </div>
            </div>
          </div>

          {/* Risk Scoring Guide */}
          <div className="risk-guide">
            <h3>📊 Risk Scoring Guide</h3>
            <div className="risk-ranges">
              <div className="risk-range-item safe">
                <span className="range-label">0.000 - 0.300</span>
                <span className="range-description">SAFE 🟢 (Legitimate sites)</span>
              </div>
              <div className="risk-range-item suspicious">
                <span className="range-label">0.301 - 0.700</span>
                <span className="range-description">SUSPICIOUS 🟡 (Warning - check carefully)</span>
              </div>
              <div className="risk-range-item phishing">
                <span className="range-label">0.701 - 1.000</span>
                <span className="range-description">PHISHING 🔴 (Avoid immediately)</span>
              </div>
            </div>
          </div>

          <div className="result-section">
            <h3>📊 Key Indicators</h3>
            <ul className="reasons-list">
              {result.reasons.map((reason, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="reason-item"
                >
                  {reason}
                </motion.li>
              ))}
            </ul>
          </div>

          <div className="result-section">
            <h3>📈 Feature Analysis</h3>
            <div className="features-grid">
              {result.explainability.slice(0, 6).map((feature, index) => {
                const impactClass = feature.impact > 0 ? 'negative' : feature.impact < 0 ? 'positive' : 'neutral';
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.05 }}
                    className="feature-card"
                  >
                    <div className="feature-name">{feature.feature}</div>
                    <div className="feature-value">Value: {feature.value}</div>
                    <div className={`feature-impact ${impactClass}`}>
                      Impact: {feature.impact > 0 ? '+' : ''}{feature.impact.toFixed(2)}
                    </div>
                    <div className="feature-description">{feature.description}</div>
                  </motion.div>
                );
              })}
            </div>
          </div>

          {/* Report Phishing Button */}
          {result.score > 0.7 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="report-section"
            >
              <h3>🚨 Report Phishing Site</h3>
              <p>This site has been identified as a high-risk phishing site. Help protect others by reporting it to the authorities.</p>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={reportPhishing}
                className="report-button"
              >
                📢 Report to Cybercrime.gov.in
              </motion.button>
            </motion.div>
          )}
        </motion.div>
      )}

      <div className="demo-section">
        <h3>🧪 Demo URLs</h3>
        <div className="demo-buttons">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              setUrl('https://google.com');
              setResult(null);
              setError(null);
            }}
            className="demo-button"
          >
            Google (Safe)
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              setUrl('http://suspicious-bank-login.com');
              setResult(null);
              setError(null);
            }}
            className="demo-button"
          >
            Suspicious URL
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              setUrl('http://192.168.1.1:8080/login');
              setResult(null);
              setError(null);
            }}
            className="demo-button"
          >
            IP Address URL
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

export default URLAnalyzer;