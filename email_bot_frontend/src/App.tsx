import React, { useState, useEffect } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import Stats from './Stats';
import Layout from './Layout';
import StatusPage from './statusPage';
import UploadPage from './uploadPage';
import HomePage from './HomePage';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Upload, Mail, Home, BarChart2 } from 'lucide-react';

// App Component
const App = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/status" element={<StatusPage />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
