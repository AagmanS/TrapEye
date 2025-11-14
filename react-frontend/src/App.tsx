import * as React from 'react';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './App.css';

// Import components
import URLAnalyzer from './components/URLAnalyzer';
import CybersecurityInfo from './components/CybersecurityInfo';
import Navbar from './components/Navbar';
import AIChat from './components/AIChat';

function Home() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="home-container"
    >
      <div className="logo-container">
        <h1 className="brand-text left">Trap</h1>
        <img src="/logo.png" alt="Trap Eye Logo" className="home-logo" />
        <h1 className="brand-text right">Eye</h1>
      </div>
      <p className="home-subtitle">
        AI-Powered Phishing Detection
      </p>
      <p className="home-description">
        Protect yourself from malicious websites with our advanced machine learning algorithms that analyze URLs in real-time.
      </p>
      
      <div className="features-grid">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="feature-card"
        >
          <div className="feature-icon">🛡️</div>
          <h3 className="feature-title">Real-time Analysis</h3>
          <p className="feature-description">
            Instantly analyze any URL for phishing and security threats with our advanced AI models.
          </p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="feature-card"
        >
          <div className="feature-icon">🔍</div>
          <h3 className="feature-title">Detailed Reports</h3>
          <p className="feature-description">
            Get comprehensive risk assessments with detailed explanations of detected threats.
          </p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="feature-card"
        >
          <div className="feature-icon">🇮🇳</div>
          <h3 className="feature-title">India-focused Security</h3>
          <p className="feature-description">
            Specialized protection against phishing threats targeting Indian users and institutions.
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="main-content"
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyzer" element={<URLAnalyzer />} />
            <Route path="/cybersecurity" element={<CybersecurityInfo />} />
          </Routes>
        </motion.div>
        
        {/* AI Chatbot */}
        <AIChat />
        
        <div className="footer">
          <p>Trap Eye - Advanced Phishing Detection System</p>
          <p>© {new Date().getFullYear()} All rights reserved</p>
        </div>
      </div>
    </Router>
  );
}

export default App;