import React from 'react';
import './Sidebar.css';

interface SidebarProps {}

const Sidebar: React.FC<SidebarProps> = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-menu">
        <div className="sidebar-item active">
          <div className="sidebar-icon">🏠</div>
          <div className="sidebar-text">dashboard</div>
        </div>
        <div className="sidebar-item">
          <div className="sidebar-icon">🔄</div>
          <div className="sidebar-text">agents</div>
        </div>
        <div className="sidebar-item">
          <div className="sidebar-icon">📋</div>
          <div className="sidebar-text">work nodes&flows</div>
        </div>
        <div className="sidebar-item sidebar-bottom">
          <div className="sidebar-icon">⚙️</div>
          <div className="sidebar-text">settings</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
