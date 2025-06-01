import React from 'react';
import '../styles/Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="logo-container">
        <div className="logo">
          <span className="logo-icon">S</span>
          <span className="logo-text">Skywork</span>
        </div>
      </div>
      
      <div className="search-container">
        <div className="sidebar-search">
          <span className="search-icon">🔍</span>
          <span className="search-text">搜索（⌘+k）</span>
        </div>
      </div>
      
      <div className="nav-container">
        <div className="nav-item active">
          <span className="nav-icon">🏠</span>
          <span className="nav-text">首页</span>
        </div>
        
        <div className="nav-item">
          <span className="nav-icon">➕</span>
          <span className="nav-text">新建项目</span>
        </div>
        
        <div className="nav-item">
          <span className="nav-icon">📁</span>
          <span className="nav-text">项目</span>
        </div>
        
        <div className="nav-item sub-item">
          <span className="nav-text">压效透的职业简历</span>
        </div>
        
        <div className="nav-item">
          <span className="nav-icon">📚</span>
          <span className="nav-text">知识库</span>
        </div>
      </div>
      
      <div className="footer-container">
        <div className="discord-link">
          <span className="discord-icon">💬</span>
          <span className="discord-text">加入discord</span>
        </div>
        
        <div className="help-button">
          <span className="help-icon">❓</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
