import * as React from 'react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './AIChat.css';

interface Message {
  text: string;
  isBot: boolean;
  timestamp: Date;
}

interface FAQ {
  question: string;
  answer: string;
  keywords: string[];
}

const AIChat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "👋 Hi! I'm Cyber Cop, your AI-powered cybersecurity assistant. Ask me anything about phishing detection!",
      isBot: true,
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');

  // FAQ Database related to the project
  const faqs: FAQ[] = [
    {
      question: "What is this system?",
      answer: "This is an AI-powered Phishing Detection System powered by Cyber Cop. I use machine learning to analyze URLs and detect potential phishing threats. I analyze 39 different features including domain characteristics, URL structure, and suspicious patterns to protect you from malicious websites.",
      keywords: ["what", "system", "about", "project", "this"]
    },
    {
      question: "How does the phishing detection work?",
      answer: "Our system uses a Random Forest machine learning model with 39 comprehensive features. We analyze URL structure (domain length, special characters, subdomains), suspicious patterns (IP usage, HTTPS presence, hexadecimal encoding), and domain characteristics (typosquatting, brand impersonation, entropy). The model has 100% accuracy on test data!",
      keywords: ["how", "work", "detect", "detection", "algorithm"]
    },
    {
      question: "What features do you analyze?",
      answer: "We analyze 39 features including: URL/domain length, subdomain count, path depth, special characters, IP address usage, HTTPS presence, port numbers, URL shorteners, hexadecimal encoding, typosquatting, brand impersonation, character entropy, digit ratio, suspicious keywords, and more!",
      keywords: ["features", "analyze", "check", "look"]
    },
    {
      question: "How accurate is the detection?",
      answer: "Our enhanced model achieves 100% accuracy on test data! We use aggressive detection with a 35% threshold, meaning even moderately suspicious URLs get flagged. The model successfully detects 10+ different attack patterns including brand impersonation, typosquatting, IP-based attacks, and more.",
      keywords: ["accuracy", "accurate", "reliable", "percentage", "rate"]
    },
    {
      question: "What is the risk scoring?",
      answer: "Risk scores range from 0-100%:\n• 0-30%: SAFE 🟢 (Legitimate sites)\n• 31-70%: SUSPICIOUS 🟡 (Warning - check carefully)\n• 71-100%: PHISHING 🔴 (Avoid immediately)\n\nOur aggressive model now flags anything with suspicious indicators!",
      keywords: ["score", "scoring", "risk", "percentage", "range"]
    },
    {
      question: "What attacks can you detect?",
      answer: "We detect 10+ attack types:\n• Brand impersonation\n• Typosquatting (misspelled domains)\n• IP-based attacks\n• Subdomain attacks\n• Suspicious TLDs\n• Free hosting abuse\n• URL shorteners\n• Hexadecimal encoding\n• Non-standard ports\n• Suspicious parameters",
      keywords: ["attacks", "threats", "detect", "types", "phishing"]
    },
    {
      question: "How do I use the URL analyzer?",
      answer: "Simple! Just:\n1. Enter any URL in the input field\n2. Click 'Analyze URL'\n3. View the risk score and detailed analysis\n4. Check the reasons and feature breakdown\n5. For high-risk URLs (70%+), you can report them to cybercrime authorities",
      keywords: ["use", "how to", "analyze", "test", "check url"]
    },
    {
      question: "What is typosquatting?",
      answer: "Typosquatting is when attackers register domains that look similar to popular brands with slight misspellings. For example: 'gooogle.com' instead of 'google.com', or 'paypai.com' instead of 'paypal.com'. Our system uses Levenshtein distance algorithm to detect these!",
      keywords: ["typosquatting", "misspelling", "similar", "fake domain"]
    },
    {
      question: "What technologies power this?",
      answer: "Backend: Python with FastAPI and Uvicorn\nFrontend: React 19 with TypeScript and Vite\nMachine Learning: scikit-learn, Random Forest Classifier\nFeatures: 39 comprehensive URL analysis features\nChrome Extension: Available for browser integration",
      keywords: ["technology", "tech", "stack", "built", "made"]
    },
    {
      question: "Can I report phishing URLs?",
      answer: "Yes! When our system detects a high-risk URL (70%+ score), we provide a direct link to report it to cybercrime authorities. This helps protect others from falling victim to the same attack.",
      keywords: ["report", "submit", "authorities", "cybercrime"]
    },
    {
      question: "Is there a Chrome extension?",
      answer: "Yes! We have a Chrome extension that integrates directly with your browser. It can analyze URLs in real-time, scan the current page, maintain history, and provide instant warnings. You can load it from the chrome-extension folder!",
      keywords: ["extension", "chrome", "browser", "plugin"]
    },
    {
      question: "What are suspicious keywords?",
      answer: "Suspicious keywords are terms commonly used in phishing attacks like: 'login', 'secure', 'verify', 'account', 'update', 'confirm', 'bank', 'password', 'signin'. Phishers use these to create urgency and trick users into clicking.",
      keywords: ["keywords", "suspicious", "words", "terms"]
    },
    {
      question: "Why no HTTPS is suspicious?",
      answer: "Legitimate websites, especially those handling sensitive data, almost always use HTTPS for encryption. A site asking for login credentials or financial information without HTTPS is a major red flag! Our system flags non-HTTPS sites with suspicious content.",
      keywords: ["https", "ssl", "encryption", "secure", "http"]
    },
    {
      question: "What is brand impersonation?",
      answer: "Brand impersonation is when phishers use well-known brand names (PayPal, Google, Amazon, Microsoft, etc.) in their URLs to appear legitimate. For example: 'paypal-secure-login.com' pretends to be PayPal but isn't. We detect these patterns!",
      keywords: ["brand", "impersonation", "fake", "pretend"]
    },
    {
      question: "How to stay safe online?",
      answer: "Best practices:\n• Always check URLs before clicking\n• Look for HTTPS on sensitive sites\n• Verify sender emails\n• Don't trust urgent messages\n• Use our tool to verify suspicious links\n• Enable 2FA on important accounts\n• Never share passwords via email",
      keywords: ["safe", "tips", "protect", "security", "advice"]
    }
  ];

  const quickQuestions = [
    "What is this system?",
    "How does detection work?",
    "How accurate is it?",
    "What attacks can you detect?",
    "How do I use it?"
  ];

  const findBestAnswer = (userInput: string): string => {
    const input = userInput.toLowerCase();
    
    // Check for greetings
    if (/^(hi|hello|hey|greetings|sup|yo)/.test(input)) {
      return "Hello! 👋 I'm Cyber Cop, your cybersecurity assistant. I'm here to help you understand our Phishing Detection System. What would you like to know?";
    }

    // Check for thanks
    if (/thank|thanks|thx/.test(input)) {
      return "You're welcome! Feel free to ask anything else about our phishing detection system. Stay safe online with Cyber Cop! 🛡️";
    }

    // Search through FAQs
    let bestMatch: FAQ | null = null;
    let maxScore = 0;

    for (const faq of faqs) {
      let score = 0;
      
      // Check if keywords match
      for (const keyword of faq.keywords) {
        if (input.includes(keyword)) {
          score += 2;
        }
      }
      
      // Check if question words match
      const questionWords = faq.question.toLowerCase().split(' ');
      for (const word of questionWords) {
        if (word.length > 3 && input.includes(word)) {
          score += 1;
        }
      }

      if (score > maxScore) {
        maxScore = score;
        bestMatch = faq;
      }
    }

    if (bestMatch && maxScore > 0) {
      return bestMatch.answer;
    }

    return "I'm not sure about that specific question. Try asking about:\n• How the detection works\n• What features we analyze\n• Accuracy and risk scoring\n• Types of attacks we detect\n• How to use the analyzer\n\nOr click on any quick question below!";
  };

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      text: input,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);

    // Get bot response
    setTimeout(() => {
      const botResponse: Message = {
        text: findBestAnswer(input),
        isBot: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 500);

    setInput('');
  };

  const handleQuickQuestion = (question: string) => {
    setInput(question);
    setTimeout(() => {
      handleSend();
    }, 100);
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <motion.div
        className={`chat-toggle ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <img src="/logo.png" alt="Cyber Cop" className="chat-logo" />
        {!isOpen && (
          <motion.div
            className="chat-badge"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
          >
            <span className="pulse-dot"></span>
          </motion.div>
        )}
      </motion.div>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="chat-window"
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            transition={{ type: "spring", damping: 20 }}
          >
            {/* Chat Header */}
            <div className="chat-header">
              <div className="chat-header-info">
                <img src="/logo.png" alt="Cyber Cop" className="chat-header-logo" />
                <div>
                  <h3>Cyber Cop</h3>
                  <span className="chat-status">
                    <span className="status-dot"></span> Online
                  </span>
                </div>
              </div>
              <button onClick={() => setIsOpen(false)} className="chat-close">
                ✕
              </button>
            </div>

            {/* Chat Messages */}
            <div className="chat-messages">
              {messages.map((message, index) => (
                <motion.div
                  key={index}
                  className={`message ${message.isBot ? 'bot' : 'user'}`}
                  initial={{ opacity: 0, x: message.isBot ? -20 : 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  {message.isBot && (
                    <img src="/logo.png" alt="Bot" className="message-avatar" />
                  )}
                  <div className="message-content">
                    <p>{message.text}</p>
                    <span className="message-time">
                      {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Quick Questions */}
            <div className="quick-questions">
              <p className="quick-title">Quick Questions:</p>
              <div className="quick-buttons">
                {quickQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickQuestion(question)}
                    className="quick-btn"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>

            {/* Chat Input */}
            <div className="chat-input-container">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask me anything..."
                className="chat-input"
              />
              <button onClick={handleSend} className="chat-send">
                📤
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default AIChat;
