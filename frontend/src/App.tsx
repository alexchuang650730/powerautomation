import React, { useState } from 'react';
import './App.css';
import N8nWorkflowVisualizer, { WorkflowNode, WorkflowConnection } from './components/N8nWorkflowVisualizer';
import Sidebar from './components/Sidebar';
import InputArea from './components/InputArea';
import AgentCards from './components/AgentCards';
import DashboardContent from './components/DashboardContent';
import WorkflowContent from './components/WorkflowContent';
import AutomationAgentDesignContent from './components/AutomationAgentDesignContent';

function App() {
  // 智能体类型
  const agentTypes = [
    {
      id: 'code',
      name: '代码智能体',
      icon: '⌨️',
      description: '专注于代码开发和调试的智能体'
    },
    {
      id: 'ppt',
      name: 'PPT 智能体',
      icon: '📊',
      description: '专注于PPT生成和编辑的智能体'
    },
    {
      id: 'web',
      name: '网页智能体',
      icon: '🌐',
      description: '专注于网页开发和设计的智能体'
    },
    {
      id: 'general',
      name: '通用智能体',
      icon: '👤',
      description: '支持多种任务处理的通用型智能体'
    }
  ];

  const [selectedAgentType, setSelectedAgentType] = useState('general');
  const [inputText, setInputText] = useState('');
  const [activeMenu, setActiveMenu] = useState('dashboard'); // 默认显示仪表盘内容

  const handleAgentSelect = (agentId: string) => {
    setSelectedAgentType(agentId);
  };

  const handleInputChange = (text: string) => {
    setInputText(text);
  };

  const handleSubmit = () => {
    console.log(`提交到${selectedAgentType}智能体: ${inputText}`);
    // 实际应用中这里会调用API发送到后端
  };

  const handleFileUpload = (files: FileList) => {
    console.log('上传文件:', files);
    // 实际应用中这里会处理文件上传
  };

  const handleMenuSelect = (menuId: string) => {
    setActiveMenu(menuId);
  };

  // 根据当前选中的菜单渲染对应内容
  const renderContent = () => {
    switch (activeMenu) {
      case 'dashboard':
        return <DashboardContent agentType={selectedAgentType} />;
      case 'agents':
        return (
          <>
            <InputArea 
              onInputChange={handleInputChange} 
              onSubmit={handleSubmit} 
              onFileUpload={handleFileUpload}
              selectedAgentType={selectedAgentType}
              selectedAgentName={agentTypes.find(agent => agent.id === selectedAgentType)?.name}
              selectedAgentIcon={agentTypes.find(agent => agent.id === selectedAgentType)?.icon}
            />
            <AgentCards 
              agents={agentTypes} 
              selectedAgentId={selectedAgentType} 
              onSelect={handleAgentSelect} 
            />
          </>
        );
      case 'workflows':
        return <WorkflowContent agentType={selectedAgentType} />;
      case 'settings':
        return (
          <div className="settings-section">
            <h2 className="section-title">设置</h2>
            <p>系统设置内容将在此显示</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="app-container">
      <Sidebar activeMenu={activeMenu} onMenuSelect={handleMenuSelect} />
      
      <div className="main-content">
        <header className="app-header">
          <h1><span className="platform-title">企业多智能体协同平台</span> PowerAutomation</h1>
          <div className="header-controls">
            <button className="menu-button">
              <span></span>
              <span></span>
              <span></span>
            </button>
          </div>
        </header>
        
        <div className="content-area">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}

export default App;
