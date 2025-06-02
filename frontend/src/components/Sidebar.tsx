import React from 'react';
import '../styles/Sidebar.css';

interface SidebarProps {}

const Sidebar: React.FC<SidebarProps> = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-menu">
        <div className="sidebar-item active">
          <div className="sidebar-icon">🏠</div>
          <div className="sidebar-text">仪表盘</div>
        </div>
        <div className="sidebar-item">
          <div className="sidebar-icon">🔄</div>
          <div className="sidebar-text">智能体</div>
        </div>
        <div className="sidebar-item">
          <div className="sidebar-icon">📋</div>
          <div className="sidebar-text">工作流节点及工作流</div>
        </div>
        <div className="sidebar-item sidebar-bottom">
          <div className="sidebar-icon">⚙️</div>
          <div className="sidebar-text">设置</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
