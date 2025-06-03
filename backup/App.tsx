import React, { useState, createContext, useContext } from 'react';
import './App.css';

// 创建工作流上下文
export const WorkflowContext = createContext<any>(null);

// 创建自定义hook
export const useWorkflowContext = () => useContext(WorkflowContext);

function App() {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [activeWorkflowType, setActiveWorkflowType] = useState<string>('automation-test');
  
  return (
    <WorkflowContext.Provider value={{ 
      selectedNodeId, 
      setSelectedNodeId, 
      activeWorkflowType, 
      setActiveWorkflowType,
      refreshTrigger: Date.now() 
    }}>
      <div className="app">
        <h1>PowerAutomation</h1>
        <p>应用正在加载中...</p>
      </div>
    </WorkflowContext.Provider>
  );
}

export default App;
