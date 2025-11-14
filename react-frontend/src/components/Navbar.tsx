import * as React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Navbar.css';

const Navbar: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="navbar-brand"
      >
        <img src="/logo.png" alt="Trap Eye Logo" className="navbar-logo" />
        <Link to="/">Trap Eye</Link>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="nav-links"
      >
        <Link 
          to="/" 
          className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
        >
          Home
        </Link>
        <Link 
          to="/analyzer" 
          className={`nav-link ${location.pathname === '/analyzer' ? 'active' : ''}`}
        >
          URL Analyzer
        </Link>
        <Link 
          to="/cybersecurity" 
          className={`nav-link ${location.pathname === '/cybersecurity' ? 'active' : ''}`}
        >
          Cybersecurity Info
        </Link>
        
      </motion.div>
    </nav>
  );
};

export default Navbar;