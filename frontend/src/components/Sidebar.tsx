import React from 'react';
import '../styles/Sidebar.css';

interface SidebarProps {}

const Sidebar: React.FC<SidebarProps> = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-menu">
        <div className="sidebar-item active">
          <div className="sidebar-icon">🏠</div>
          <div className="sidebar-text">Dashboard</div>
        </div>
        <div className="sidebar-item">
          <div className="sidebar-icon">🔄</div>
          <div className="sidebar-text">Agents</div>
        </div>
        <div className="sidebar-item">
          <div className="sidebar-icon">📋</div>
          <div className="sidebar-text">Work nodes&flows</div>
        </div>
        <div className="sidebar-item sidebar-bottom">
          <div className="sidebar-icon">⚙️</div>
          <div className="sidebar-text">Settings</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
