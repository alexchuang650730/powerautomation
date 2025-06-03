import React from 'react';
import '../styles/Sidebar.css';

interface SidebarProps {
  activeSection: string;
  onSectionChange: (sectionId: string) => void;
  activeAgent: string;
  onAgentChange: (agentId: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeSection, onSectionChange, activeAgent, onAgentChange }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-menu">
        <div 
          className={`sidebar-item ${activeSection === 'dashboard' ? 'active' : ''}`}
          onClick={() => onSectionChange('dashboard')}
        >
          <div className="sidebar-icon">🏠</div>
          <div className="sidebar-text">仪表盘</div>
        </div>
        <div 
          className={`sidebar-item ${activeSection === 'workflow' ? 'active' : ''}`}
          onClick={() => onSectionChange('workflow')}
        >
          <div className="sidebar-icon">🔄</div>
          <div className="sidebar-text">工作流</div>
        </div>
        <div 
          className={`sidebar-item ${activeAgent === 'general' ? 'active' : ''}`}
          onClick={() => onAgentChange('general')}
        >
          <div className="sidebar-icon">📋</div>
          <div className="sidebar-text">通用智能体</div>
        </div>
        <div 
          className={`sidebar-item sidebar-bottom ${activeSection === 'settings' ? 'active' : ''}`}
          onClick={() => onSectionChange('settings')}
        >
          <div className="sidebar-icon">⚙️</div>
          <div className="sidebar-text">设置</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
