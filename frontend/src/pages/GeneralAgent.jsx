import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/GeneralAgent.css';

const GeneralAgent = () => {
  const [query, setQuery] = useState('');
  const [task, setTask] = useState('');
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  
  const navigate = useNavigate();

  useEffect(() => {
    // 生成会话ID
    if (!sessionId) {
      setSessionId(`session-${Date.now()}`);
    }
  }, []);

  const handleChat = async () => {
    if (!query) {
      alert('请输入问题');
      return;
    }
    
    // 添加用户消息
    const userMessage = {
      role: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    
    setLoading(true);
    try {
      const response = await axios.post('/api/general_agent/chat', {
        query,
        session_id: sessionId,
        context: { messages }
      });
      
      // 添加助手回复
      setMessages(prev => [...prev, response.data]);
      setQuery('');
    } catch (error) {
      console.error('对话失败:', error);
      // 添加错误消息
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '对话失败，请稍后重试',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteTask = async () => {
    if (!task) {
      alert('请输入任务描述');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('/api/general_agent/execute_task', {
        task,
        session_id: sessionId,
        parameters: {}
      });
      
      // 添加任务执行结果
      setMessages(prev => [...prev, {
        role: 'user',
        content: `执行任务: ${task}`,
        timestamp: new Date().toISOString()
      }, response.data]);
      setTask('');
    } catch (error) {
      console.error('执行任务失败:', error);
      // 添加错误消息
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '执行任务失败，请稍后重试',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async () => {
    if (!projectName || !projectDescription) {
      alert('请输入项目名称和描述');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('/api/general_agent/create_project', {
        project_name: projectName,
        project_description: projectDescription,
        session_id: sessionId,
        parameters: {}
      });
      
      // 添加项目创建结果
      setMessages(prev => [...prev, {
        role: 'user',
        content: `创建项目: ${projectName}\n${projectDescription}`,
        timestamp: new Date().toISOString()
      }, response.data]);
      setProjectName('');
      setProjectDescription('');
    } catch (error) {
      console.error('创建项目失败:', error);
      // 添加错误消息
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '创建项目失败，请稍后重试',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  const renderForm = () => {
    switch (activeTab) {
      case 'chat':
        return (
          <div className="form-container">
            <div className="form-group">
              <label>问题</label>
              <textarea 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="输入您的问题"
                disabled={loading}
              />
            </div>
            <button 
              className="action-button" 
              onClick={handleChat} 
              disabled={loading}
            >
              {loading ? '处理中...' : '发送'}
            </button>
          </div>
        );
      
      case 'task':
        return (
          <div className="form-container">
            <div className="form-group">
              <label>任务描述</label>
              <textarea 
                value={task} 
                onChange={(e) => setTask(e.target.value)} 
                placeholder="输入任务描述，例如: 帮我整理一份周报"
                disabled={loading}
              />
            </div>
            <button 
              className="action-button" 
              onClick={handleExecuteTask} 
              disabled={loading}
            >
              {loading ? '执行中...' : '执行任务'}
            </button>
          </div>
        );
      
      case 'project':
        return (
          <div className="form-container">
            <div className="form-group">
              <label>项目名称</label>
              <input 
                type="text" 
                value={projectName} 
                onChange={(e) => setProjectName(e.target.value)} 
                placeholder="输入项目名称"
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label>项目描述</label>
              <textarea 
                value={projectDescription} 
                onChange={(e) => setProjectDescription(e.target.value)} 
                placeholder="输入项目描述"
                disabled={loading}
              />
            </div>
            <button 
              className="action-button" 
              onClick={handleCreateProject} 
              disabled={loading}
            >
              {loading ? '创建中...' : '创建项目'}
            </button>
          </div>
        );
      
      default:
        return null;
    }
  };

  const renderMessages = () => {
    return (
      <div className="messages-container">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
          >
            <div className="message-header">
              <span className="message-role">{message.role === 'user' ? '用户' : '助手'}</span>
              <span className="message-time">
                {new Date(message.timestamp).toLocaleString()}
              </span>
            </div>
            <div className="message-content">{message.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message assistant-message">
            <div className="message-header">
              <span className="message-role">助手</span>
            </div>
            <div className="message-content loading">思考中...</div>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="general-agent-container">
      <h1>通用智能体</h1>
      <p className="description">
        通用智能体可以帮助您回答问题、执行任务和管理项目。
      </p>
      
      <div className="tabs">
        <button 
          className={activeTab === 'chat' ? 'active' : ''} 
          onClick={() => setActiveTab('chat')}
        >
          对话
        </button>
        <button 
          className={activeTab === 'task' ? 'active' : ''} 
          onClick={() => setActiveTab('task')}
        >
          任务执行
        </button>
        <button 
          className={activeTab === 'project' ? 'active' : ''} 
          onClick={() => setActiveTab('project')}
        >
          项目管理
        </button>
      </div>
      
      {renderForm()}
      {renderMessages()}
      
      <button 
        className="back-button" 
        onClick={() => navigate('/')}
      >
        返回首页
      </button>
    </div>
  );
};

export default GeneralAgent;
