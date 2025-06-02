import React from 'react';
import '../styles/Sidebar.css';

interface SidebarProps {
  activeMenu: string;
  onMenuSelect: (menuId: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeMenu, onMenuSelect }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-menu">
        <div 
          className={`sidebar-item ${activeMenu === 'dashboard' ? 'active' : ''}`}
          onClick={() => onMenuSelect('dashboard')}
        >
          <div className="sidebar-icon">🏠</div>
          <div className="sidebar-text">仪表盘</div>
        </div>
        <div 
          className={`sidebar-item ${activeMenu === 'agents' ? 'active' : ''}`}
          onClick={() => onMenuSelect('agents')}
        >
          <div className="sidebar-icon">🔄</div>
          <div className="sidebar-text">智能体</div>
        </div>
        <div 
          className={`sidebar-item ${activeMenu === 'workflows' ? 'active' : ''}`}
          onClick={() => onMenuSelect('workflows')}
        >
          <div className="sidebar-icon">📋</div>
          <div className="sidebar-text">工作流节点及工作流</div>
        </div>
        <div 
          className={`sidebar-item sidebar-bottom ${activeMenu === 'settings' ? 'active' : ''}`}
          onClick={() => onMenuSelect('settings')}
        >
          <div className="sidebar-icon">⚙️</div>
          <div className="sidebar-text">设置</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
