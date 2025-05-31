import React, { useState } from 'react';
import '../styles/Home.css';
import AgentCard from '../components/AgentCard';
import SearchBar from '../components/SearchBar';
import CaseShowcase from '../components/CaseShowcase';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import CodeAgentInput from '../components/CodeAgentInput';

const Home = () => {
  // 智能体数据 - 更新为四个专业智能体
  const agents = [
    {
      id: 'ppt_agent',
      name: 'PPT智能体',
      icon: '📊',
      description: '省时高效的专家级PPT智能体',
      isExpert: true,
      isActive: false
    },
    {
      id: 'web_agent',
      name: '网页智能体',
      icon: '🌐',
      description: '增强的网页搜索和内容分析',
      isExpert: true,
      isActive: false
    },
    {
      id: 'code_agent',
      name: '代码智能体',
      icon: '💻',
      description: '智能代码生成与分析',
      isExpert: true,
      isActive: true
    },
    {
      id: 'general_agent',
      name: '通用智能体',
      icon: '🤖',
      description: '通用智能助手',
      isExpert: true,
      isActive: false
    }
  ];

  // 案例数据
  const showcaseCases = [
    {
      id: 1,
      title: '企业年度报告PPT',
      image: '/images/case1.png',
      thumbnail: '/images/thumbnail1.png'
    },
    {
      id: 2,
      title: '响应式电商网站',
      image: '/images/case2.png',
      thumbnail: '/images/thumbnail2.png'
    },
    {
      id: 3,
      title: '数据分析可视化',
      image: '/images/case3.png',
      thumbnail: '/images/thumbnail3.png'
    }
  ];

  // 状态管理
  const [selectedAgentId, setSelectedAgentId] = useState('code_agent');
  const [queryResult, setQueryResult] = useState(null);

  // 当前选中的智能体
  const currentAgent = agents.find(agent => agent.id === selectedAgentId) || agents[2]; // 默认代码智能体

  // 处理智能体选择
  const handleAgentSelect = (id) => {
    setSelectedAgentId(id);
    setQueryResult(null); // 清除之前的查询结果
  };

  // 处理查询提交
  const handleQuerySubmit = (query, targetAgent) => {
    console.log(`向${targetAgent}提交查询:`, query);
    // 这里将来会实现与后端的实际通信
    setQueryResult({
      agent: targetAgent,
      query,
      timestamp: new Date().toISOString(),
      status: '处理中...'
    });
  };

  // 处理智能体变更（由代码智能体拆解后触发）
  const handleAgentChange = (newAgentId) => {
    console.log(`智能体自动切换: ${selectedAgentId} -> ${newAgentId}`);
    setSelectedAgentId(newAgentId);
    
    // 更新智能体激活状态
    agents.forEach(agent => {
      agent.isActive = agent.id === newAgentId;
    });
  };

  return (
    <div className="home-container">
      <Sidebar />
      
      <div className="main-content">
        <Header />
        
        <div className="agent-header">
          <div className="agent-badge">PowerAutomation 超级智能体</div>
          <h1 className="agent-title">{currentAgent.description}</h1>
        </div>
        
        <div className="input-section">
          <div className="input-header">
            <span className="agent-icon">{currentAgent.icon} {currentAgent.name}</span>
            <span className="divider">|</span>
            <span className="mode-label">{currentAgent.name}</span>
          </div>
          
          {selectedAgentId === 'code_agent' ? (
            <CodeAgentInput 
              onSubmit={handleQuerySubmit}
              onAgentChange={handleAgentChange}
            />
          ) : (
            <SearchBar 
              placeholder={`请输入您的需求，让${currentAgent.name}为您服务...`}
              onSearch={(query) => handleQuerySubmit(query, selectedAgentId)}
            />
          )}
          
          <div className="action-buttons">
            <button className="scene-button">
              <span className="icon">🔍</span>
              通用场景
              <span className="dropdown-icon">▼</span>
            </button>
            <button className="link-button">
              <span className="icon">🔗</span>
              联网
            </button>
          </div>
        </div>
        
        {queryResult && (
          <div className="query-result">
            <h3>查询结果</h3>
            <div className="result-content">
              <p><strong>处理智能体:</strong> {queryResult.agent}</p>
              <p><strong>查询内容:</strong> {queryResult.query}</p>
              <p><strong>状态:</strong> {queryResult.status}</p>
              <p><strong>时间:</strong> {queryResult.timestamp}</p>
            </div>
          </div>
        )}
        
        <div className="agents-grid">
          {agents.map(agent => (
            <AgentCard 
              key={agent.id}
              agent={agent}
              isActive={agent.id === selectedAgentId}
              onClick={() => handleAgentSelect(agent.id)}
            />
          ))}
        </div>
        
        <div className="showcase-section">
          <h2 className="showcase-title">精选案例展示</h2>
          <CaseShowcase cases={showcaseCases} />
        </div>
      </div>
    </div>
  );
};

export default Home;
