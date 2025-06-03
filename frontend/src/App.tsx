import React, { useState, useEffect, createContext, useContext } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import DashboardContent from './components/DashboardContent';
import WorkflowContent from './components/WorkflowContent';
import LogView from './components/LogView';
import CodeView from './components/CodeView/CodeView';
import SavepointManager from './components/SavepointManager';
import InputArea from './components/InputArea';
import AutomationAgentDesignContent from './components/AutomationAgentDesignContent';

// 创建全局状态上下文
interface WorkflowContextType {
  selectedNodeId: string | null;
  setSelectedNodeId: (id: string | null) => void;
  activeWorkflowType: string;
  setActiveWorkflowType: (type: string) => void;
  activeSavepoint: string | null;
  setActiveSavepoint: (id: string | null) => void;
  refreshTrigger: number;
  triggerRefresh: () => void;
}

const WorkflowContext = createContext<WorkflowContextType | undefined>(undefined);

// 自定义Hook用于访问上下文
export const useWorkflowContext = () => {
  const context = useContext(WorkflowContext);
  if (!context) {
    throw new Error('useWorkflowContext must be used within a WorkflowProvider');
  }
  return context;
};

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [activeAgent, setActiveAgent] = useState('general');
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [activeWorkflowType, setActiveWorkflowType] = useState<string>('automation-test');
  const [activeSavepoint, setActiveSavepoint] = useState<string | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // 触发全局刷新的函数
  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  // 处理工作流类型切换
  const handleWorkflowTypeChange = (type: string) => {
    setActiveWorkflowType(type);
    setSelectedNodeId(null); // 切换工作流类型时重置选中节点
    setActiveSavepoint(null); // 重置活动保存点
  };

  // 渲染主内容区域
  const renderMainContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return <DashboardContent agentType={activeAgent} />;
      case 'workflow':
        return (
          <WorkflowContext.Provider value={{
            selectedNodeId,
            setSelectedNodeId,
            activeWorkflowType,
            setActiveWorkflowType,
            activeSavepoint,
            setActiveSavepoint,
            refreshTrigger,
            triggerRefresh
          }}>
            <div className="workflow-container">
              <div className="workflow-main">
                <WorkflowContent agentType={activeAgent} />
                <SavepointManager />
              </div>
              <div className="workflow-sidebar">
                <LogView agentType={activeAgent} />
                <CodeView agentType={activeAgent} />
              </div>
            </div>
          </WorkflowContext.Provider>
        );
      case 'agent':
        return (
          <WorkflowContext.Provider value={{
            selectedNodeId,
            setSelectedNodeId,
            activeWorkflowType,
            setActiveWorkflowType,
            activeSavepoint,
            setActiveSavepoint,
            refreshTrigger,
            triggerRefresh
          }}>
            <div className="agent-container">
              <AutomationAgentDesignContent agentType={activeAgent} />
            </div>
          </WorkflowContext.Provider>
        );
      case 'settings':
        return <div className="settings-container">设置页面内容</div>;
      default:
        return <div>选择一个部分查看内容</div>;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">企业多智能体协同平台</h1>
      </header>
      <main className="app-main">
        <Sidebar 
          activeSection={activeSection} 
          onSectionChange={setActiveSection}
          activeAgent={activeAgent}
          onAgentChange={setActiveAgent}
        />
        <div className="content-area">
          {renderMainContent()}
          {activeSection === 'agent' && (
            <InputArea 
              onInputChange={() => {}} 
              onSubmit={() => {}} 
              onFileUpload={() => {}}
            />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
