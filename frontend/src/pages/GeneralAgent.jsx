import React, { useState } from 'react';
import '../styles/GeneralAgent.css';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import SearchBar from '../components/SearchBar';

const GeneralAgent = () => {
  const [query, setQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [activeMode, setActiveMode] = useState('chat'); // 'chat', 'task', 'project'

  // 模拟提交处理
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    // 添加用户消息到对话
    const userMessage = {
      role: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };
    
    setConversation([...conversation, userMessage]);
    setIsProcessing(true);
    
    // 模拟API调用
    setTimeout(() => {
      // 根据不同的模式返回不同的响应
      let agentResponse;
      
      if (activeMode === 'chat') {
        agentResponse = {
          role: 'assistant',
          content: `我理解您的问题是关于"${query}"。这是一个很好的问题，让我来回答...\n\n根据最新的研究和数据，这个问题的答案是多方面的。首先，我们需要考虑...\n\n总结来说，关键点是：1) ... 2) ... 3) ...`,
          timestamp: new Date().toISOString()
        };
      } else if (activeMode === 'task') {
        agentResponse = {
          role: 'assistant',
          content: `我将帮助您完成"${query}"任务。\n\n我已经开始处理这个任务，以下是我的计划：\n\n1. 分析任务需求\n2. 收集必要信息\n3. 执行任务步骤\n4. 验证结果\n\n我现在正在执行第一步...`,
          actions: [
            { type: 'task_started', name: query, id: 'task-' + Date.now() }
          ],
          timestamp: new Date().toISOString()
        };
      } else {
        agentResponse = {
          role: 'assistant',
          content: `我将为您创建"${query}"项目。\n\n这个项目将包含以下组件：\n\n1. 需求分析文档\n2. 设计方案\n3. 实施计划\n4. 测试策略\n\n我已经开始准备项目文档，您可以在项目面板中查看进度。`,
          actions: [
            { type: 'project_created', name: query, id: 'proj-' + Date.now() }
          ],
          timestamp: new Date().toISOString()
        };
      }
      
      setConversation([...conversation, userMessage, agentResponse]);
      setQuery('');
      setIsProcessing(false);
    }, 2000);
  };

  // 渲染对话消息
  const renderMessage = (message, index) => {
    const isUser = message.role === 'user';
    
    return (
      <div 
        key={index} 
        className={`message ${isUser ? 'user-message' : 'agent-message'}`}
      >
        <div className="message-header">
          <div className="message-avatar">
            {isUser ? '👤' : '🤖'}
          </div>
          <div className="message-info">
            <div className="message-sender">{isUser ? '您' : '通用智能体'}</div>
            <div className="message-time">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>
        <div className="message-content">
          {message.content.split('\n').map((line, i) => (
            <React.Fragment key={i}>
              {line}
              <br />
            </React.Fragment>
          ))}
        </div>
        {message.actions && (
          <div className="message-actions">
            {message.actions.map((action, i) => (
              <div key={i} className="action-badge">
                {action.type === 'task_started' ? '任务已启动' : '项目已创建'}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="general-agent-container">
      <Sidebar />
      
      <div className="main-content">
        <Header />
        
        <div className="agent-header">
          <div className="agent-badge">天工超级智能体</div>
          <h1 className="agent-title">通用智能助手</h1>
        </div>
        
        <div className="mode-selector">
          <div 
            className={`mode-option ${activeMode === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveMode('chat')}
          >
            <span className="mode-icon">💬</span>
            对话模式
          </div>
          <div 
            className={`mode-option ${activeMode === 'task' ? 'active' : ''}`}
            onClick={() => setActiveMode('task')}
          >
            <span className="mode-icon">✅</span>
            任务模式
          </div>
          <div 
            className={`mode-option ${activeMode === 'project' ? 'active' : ''}`}
            onClick={() => setActiveMode('project')}
          >
            <span className="mode-icon">📂</span>
            项目模式
          </div>
        </div>
        
        <div className="conversation-container">
          {conversation.length === 0 ? (
            <div className="empty-conversation">
              <div className="empty-icon">🔍</div>
              <h3>开始与通用智能体对话</h3>
              <p>
                {activeMode === 'chat' 
                  ? '您可以询问任何问题，我会尽力回答。' 
                  : activeMode === 'task' 
                    ? '描述您需要完成的任务，我会帮您执行。' 
                    : '描述您想要创建的项目，我会为您规划和实施。'}
              </p>
            </div>
          ) : (
            <div className="messages-container">
              {conversation.map(renderMessage)}
            </div>
          )}
        </div>
        
        <form className="input-form" onSubmit={handleSubmit}>
          <div className="input-container">
            <textarea 
              placeholder={
                activeMode === 'chat' 
                  ? '输入您的问题...' 
                  : activeMode === 'task' 
                    ? '描述您需要完成的任务...' 
                    : '描述您想要创建的项目...'
              }
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={isProcessing}
              rows={3}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={isProcessing || !query.trim()}
            >
              {isProcessing ? '处理中...' : '发送'}
            </button>
          </div>
          <div className="input-options">
            <button type="button" className="option-button">
              <span className="option-icon">🔗</span>
              联网
            </button>
            <button type="button" className="option-button">
              <span className="option-icon">📎</span>
              上传文件
            </button>
            <button type="button" className="option-button">
              <span className="option-icon">🔄</span>
              调用其他智能体
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default GeneralAgent;
