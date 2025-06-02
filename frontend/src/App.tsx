import React, { useState, useEffect } from 'react';
import './App.css';
import InputBox from './components/input-area/InputBox';
import AgentCard from './components/agent-cards/AgentCard';
import WorkNodeTimeline from './components/work-node-timeline/WorkNodeTimeline';
import N8nWorkflowVisualizer from './components/N8nWorkflowVisualizer';

type AgentType = 'code' | 'ppt' | 'web' | 'general';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
  files?: string[];
}

const App: React.FC = () => {
  const [selectedAgent, setSelectedAgent] = useState<AgentType>('general');
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  // 模拟消息处理
  const handleSendMessage = (message: string, files?: File[]) => {
    // 添加用户消息
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      text: message,
      isUser: true,
      timestamp: new Date().toLocaleTimeString(),
      files: files?.map(file => file.name)
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // 模拟智能体响应
    setTimeout(() => {
      const agentMessage: Message = {
        id: `msg_${Date.now()}`,
        text: `您选择了${getAgentName(selectedAgent)}，正在处理您的请求...`,
        isUser: false,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, agentMessage]);
    }, 1000);
  };

  const getAgentName = (type: AgentType): string => {
    switch (type) {
      case 'code':
        return '代码智能体';
      case 'ppt':
        return 'PPT智能体';
      case 'web':
        return '网页智能体';
      case 'general':
        return '通用智能体';
      default:
        return '智能体';
    }
  };

  const handleWorkNodeSelect = (node: any) => {
    setSelectedNode(node.id);
    // 这里可以添加更多处理逻辑，如显示节点详情等
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="logo">PowerAutomation</div>
        <nav className="nav-menu">
          <div className="nav-item active">首页</div>
          <div className="nav-item">智能体</div>
          <div className="nav-item">工作节点</div>
          <div className="nav-item">工作流</div>
          <div className="nav-item">设置</div>
          <div className="nav-item">帮助</div>
        </nav>
      </div>
      
      <div className="main-content">
        <header className="header">
          <h1>PowerAutomation</h1>
          <div className="user-controls">
            <button className="search-button">🔍</button>
            <button className="notifications-button">🔔</button>
            <button className="user-profile">👤</button>
          </div>
        </header>
        
        {/* 输入框区域 - 新增 */}
        <div className="input-area">
          <InputBox onSend={handleSendMessage} agentType={selectedAgent} />
        </div>
        
        {/* 智能体卡片区域 */}
        <div className="agent-cards">
          <AgentCard 
            type="code" 
            name="代码智能体" 
            description="处理代码相关任务，包括代码生成、调试和优化" 
            isSelected={selectedAgent === 'code'}
            onClick={() => setSelectedAgent('code')}
          />
          <AgentCard 
            type="ppt" 
            name="PPT智能体" 
            description="创建和编辑演示文稿，支持多种主题和布局" 
            isSelected={selectedAgent === 'ppt'}
            onClick={() => setSelectedAgent('ppt')}
          />
          <AgentCard 
            type="web" 
            name="网页智能体" 
            description="网页设计与开发，支持响应式布局和交互功能" 
            isSelected={selectedAgent === 'web'}
            onClick={() => setSelectedAgent('web')}
          />
          <AgentCard 
            type="general" 
            name="通用智能体" 
            description="通用智能助手，可处理各种任务和问题" 
            isSelected={selectedAgent === 'general'}
            onClick={() => setSelectedAgent('general')}
          />
        </div>
        
        {/* 工作节点与工作流整合区域 - 新增 */}
        <div className="workflow-integration">
          {/* 工作节点时间线 */}
          <div className="work-node-section">
            <WorkNodeTimeline onNodeSelect={handleWorkNodeSelect} />
          </div>
          
          {/* 工作流可视化 */}
          <div className="workflow-section">
            <N8nWorkflowVisualizer />
          </div>
        </div>
        
        {/* 消息历史区域 */}
        <div className="messages-container">
          {messages.map((msg) => (
            <div key={msg.id} className={`message ${msg.isUser ? 'user' : 'agent'}`}>
              <div className="message-header">
                <span className="message-sender">{msg.isUser ? '您' : getAgentName(selectedAgent)}</span>
                <span className="message-time">{msg.timestamp}</span>
              </div>
              <div className="message-content">{msg.text}</div>
              {msg.files && msg.files.length > 0 && (
                <div className="message-files">
                  <div className="files-header">附件:</div>
                  {msg.files.map((file, index) => (
                    <div key={index} className="file-item">{file}</div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
