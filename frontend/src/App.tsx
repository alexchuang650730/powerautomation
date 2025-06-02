import React, { useState } from 'react';
import './App.css';
import N8nWorkflowVisualizer, { WorkflowNode, WorkflowConnection } from './components/N8nWorkflowVisualizer';
import Sidebar from './components/Sidebar';
import InputArea from './components/InputArea';
import AgentCards from './components/AgentCards';
import IntegratedWorkflowView from './components/IntegratedWorkflowView';

function App() {
  // 示例工作流节点数据
  const nodes: WorkflowNode[] = [
    {
      id: 'trigger1',
      type: 'trigger',
      position: { x: 100, y: 100 },
      data: {
        name: '新邮件触发器',
        description: '当收到新邮件时触发',
        status: '活跃',
        timestamp: '2025-06-02 10:30',
        type: 'email'
      }
    },
    {
      id: 'condition1',
      type: 'condition',
      position: { x: 100, y: 250 },
      data: {
        name: '邮件过滤器',
        description: '检查邮件是否来自重要联系人',
        status: '已评估',
        condition: 'sender IN importantContacts',
        timestamp: '2025-06-02 10:31',
        type: 'filter'
      }
    },
    {
      id: 'action1',
      type: 'action',
      position: { x: 400, y: 250 },
      data: {
        name: '标记为重要',
        description: '将邮件标记为重要并通知用户',
        status: '已执行',
        timestamp: '2025-06-02 10:32',
        type: 'mark'
      }
    },
    {
      id: 'action2',
      type: 'action',
      position: { x: 100, y: 400 },
      data: {
        name: '归档邮件',
        description: '将邮件移动到归档文件夹',
        status: '已执行',
        timestamp: '2025-06-02 10:33',
        type: 'archive'
      }
    },
    {
      id: 'error1',
      type: 'error',
      position: { x: 400, y: 400 },
      data: {
        name: '通知错误',
        description: '发送通知失败',
        status: '失败',
        errorType: 'API错误',
        errorMessage: '通知服务暂时不可用',
        timestamp: '2025-06-02 10:34',
        type: 'notification'
      }
    }
  ];

  // 示例工作流连接数据
  const connections: WorkflowConnection[] = [
    {
      id: 'conn1',
      source: 'trigger1',
      target: 'condition1',
      label: '触发'
    },
    {
      id: 'conn2',
      source: 'condition1',
      target: 'action1',
      label: '是'
    },
    {
      id: 'conn3',
      source: 'condition1',
      target: 'action2',
      label: '否'
    },
    {
      id: 'conn4',
      source: 'action1',
      target: 'error1',
      label: '失败'
    }
  ];

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

  const [selectedAgentType, setSelectedAgentType] = useState('code');
  const [inputText, setInputText] = useState('');

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

  return (
    <div className="app-container">
      <Sidebar />
      
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
          <InputArea 
            onInputChange={handleInputChange} 
            onSubmit={handleSubmit} 
            onFileUpload={handleFileUpload}
            selectedAgentType={selectedAgentType}
            selectedAgentName={agentTypes.find(agent => agent.id === selectedAgentType)?.name}
            selectedAgentIcon={agentTypes.find(agent => agent.id === selectedAgentType)?.icon}
          />
          
          {/* 上传按钮已移除 */}
          
          <AgentCards 
            agents={agentTypes} 
            selectedAgentId={selectedAgentType} 
            onSelect={handleAgentSelect} 
          />
          
          <div className="workflow-section">
            <h2 className="section-title">工作平台</h2>
            <IntegratedWorkflowView>
              <N8nWorkflowVisualizer nodes={nodes} connections={connections} />
            </IntegratedWorkflowView>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
