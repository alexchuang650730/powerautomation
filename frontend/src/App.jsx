import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import WebAgent from './pages/WebAgent';
import GeneralAgent from './pages/GeneralAgent';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/web-agent" element={<WebAgent />} />
          <Route path="/general-agent" element={<GeneralAgent />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
