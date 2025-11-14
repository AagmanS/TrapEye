import * as React from 'react';
import { motion } from 'framer-motion';
import './CybersecurityInfo.css';

const CybersecurityInfo: React.FC = () => {
  // Data for cyber laws with relevant icons
  const cyberLaws = [
    {
      id: 1,
      title: "Section 66: Computer-related offences",
      description: "Punishment for hacking with computer system",
      icon: "🔒"
    },
    {
      id: 2,
      title: "Section 66B: Receiving stolen computer resource",
      description: "Punishment for dishonestly receiving stolen computer resource",
      icon: "📱"
    },
    {
      id: 3,
      title: "Section 66C: Identity theft",
      description: "Punishment for identity theft using computer resources",
      icon: "👤"
    },
    {
      id: 4,
      title: "Section 66D: Cheating by personation",
      description: "Punishment for cheating using computer resources",
      icon: "🎭"
    },
    {
      id: 5,
      title: "Section 66E: Violation of privacy",
      description: "Punishment for violation of privacy using computer resources",
      icon: "👁️"
    },
    {
      id: 6,
      title: "Section 66F: Cyber terrorism",
      description: "Punishment for acts of cyber terrorism",
      icon: "💣"
    }
  ];

  // Data for reporting channels
  const reportingChannels = [
    {
      id: 1,
      title: "National Cyber Crime Reporting Portal",
      description: "Official portal for reporting cybercrimes in India",
      link: "https://cybercrime.gov.in",
      icon: "🌐"
    },
    {
      id: 2,
      title: "Indian Cyber Crime Coordination Centre (I4C)",
      description: "Central nodal agency for dealing with cybercrime",
      icon: "🏛️"
    },
    {
      id: 3,
      title: "Local Police Stations",
      description: "Can also register complaints for cybercrimes",
      icon: "👮"
    }
  ];

  // Data for CERT-In guidelines
  const certInGuidelines = [
    {
      id: 1,
      title: "Targeted scanning/probing",
      description: "Reporting of targeted scanning or probing of critical networks",
      icon: "📡"
    },
    {
      id: 2,
      title: "Compromise of critical systems",
      description: "Reporting compromise of critical information systems",
      icon: "💻"
    },
    {
      id: 3,
      title: "Unauthorized access",
      description: "Reporting unauthorized access to IT systems or data",
      icon: "🔓"
    },
    {
      id: 4,
      title: "Website defacement",
      description: "Reporting defacement of government or organizational websites",
      icon: "📄"
    },
    {
      id: 5,
      title: "Malicious code propagation",
      description: "Reporting propagation of malicious code or software",
      icon: "🦠"
    },
    {
      id: 6,
      title: "Identity theft and spoofing",
      description: "Reporting identity theft and spoofing activities",
      icon: "🎭"
    }
  ];

  // Data for data protection principles
  const dataProtectionPrinciples = [
    {
      id: 1,
      title: "Consent for data processing",
      description: "Clear consent required for processing personal data",
      icon: "✅"
    },
    {
      id: 2,
      title: "Right to access and correction",
      description: "Individuals have right to access and correct their data",
      icon: "📖"
    },
    {
      id: 3,
      title: "Data minimization",
      description: "Collect only necessary personal data",
      icon: "📉"
    },
    {
      id: 4,
      title: "Security safeguards",
      description: "Implement appropriate security measures for data protection",
      icon: "🛡️"
    },
    {
      id: 5,
      title: "Accountability",
      description: "Data fiduciaries must demonstrate compliance",
      icon: "📋"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="cybersecurity-container"
    >
      <div className="cybersecurity-header">
        <h1>Cybersecurity in India</h1>
        <p>Essential information about cybersecurity policies and reporting mechanisms in India</p>
      </div>

      <div className="content-section">
        {/* Indian Cyber Laws */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="info-card"
        >
          <h2>Indian Cyber Laws</h2>
          <p>
            India's primary cyber law is the Information Technology Act, 2000 (IT Act) which was amended in 2008. 
            The Act provides legal recognition for electronic transactions and addresses cybercrime and electronic 
            commerce in India.
          </p>
          
          <div className="laws-grid">
            {cyberLaws.map((law, index) => (
              <motion.div
                key={law.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="law-item"
              >
                <div className="law-icon">{law.icon}</div>
                <div className="law-content">
                  <h3>{law.title}</h3>
                  <p>{law.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Cybercrime Reporting */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="info-card"
        >
          <h2>Cybercrime Reporting</h2>
          <p>
            India has established several mechanisms for reporting cybercrimes. The primary portal for reporting 
            cybercrimes is the National Cyber Crime Reporting Portal.
          </p>
          
          <div className="channels-grid">
            {reportingChannels.map((channel, index) => (
              <motion.div
                key={channel.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 * index }}
                className="channel-item"
              >
                <div className="channel-icon">{channel.icon}</div>
                <div className="channel-content">
                  <h3>{channel.title}</h3>
                  <p>{channel.description}</p>
                  {channel.link && (
                    <a 
                      href={channel.link} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="channel-link"
                    >
                      Visit Portal →
                    </a>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* CERT-In Guidelines */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="info-card"
        >
          <h2>CERT-In Guidelines</h2>
          <p>
            The Computer Emergency Response Team of India (CERT-In) is the national nodal agency for incident 
            response and security breach reporting.
          </p>
          <p>
            Organizations must report incidents to CERT-In within 6 hours of detection.
          </p>
          
          <div className="guidelines-grid">
            {certInGuidelines.map((guideline, index) => (
              <motion.div
                key={guideline.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index }}
                className="guideline-item"
              >
                <div className="guideline-icon">{guideline.icon}</div>
                <div className="guideline-content">
                  <h3>{guideline.title}</h3>
                  <p>{guideline.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Data Protection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="info-card"
        >
          <h2>Data Protection</h2>
          <p>
            India's data protection framework is evolving with the introduction of the Digital Personal Data 
            Protection Act, 2023, which provides for processing of personal data in a manner that recognizes 
            both the right to privacy and the need for reasonable restrictions.
          </p>
          
          <div className="principles-grid">
            {dataProtectionPrinciples.map((principle, index) => (
              <motion.div
                key={principle.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="principle-item"
              >
                <div className="principle-icon">{principle.icon}</div>
                <div className="principle-content">
                  <h3>{principle.title}</h3>
                  <p>{principle.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default CybersecurityInfo;