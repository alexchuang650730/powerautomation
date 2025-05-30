import React from 'react';
import '../styles/Home.css';
import AgentCard from '../components/AgentCard';
import SearchBar from '../components/SearchBar';
import CaseShowcase from '../components/CaseShowcase';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';

const Home = () => {
  // 智能体数据
  const agents = [
    {
      id: 'doc',
      name: '文档模式',
      icon: '📄',
      description: '智能文档处理',
      isExpert: true,
      isActive: false
    },
    {
      id: 'ppt',
      name: 'PPT模式',
      icon: '📊',
      description: '省时高效的专家级PPT智能体',
      isExpert: true,
      isActive: true
    },
    {
      id: 'sheet',
      name: '表格模式',
      icon: '📈',
      description: '智能表格处理',
      isExpert: true,
      isActive: false
    },
    {
      id: 'web',
      name: '网页模式',
      icon: '🌐',
      description: '增强的网页搜索和内容分析',
      isExpert: true,
      isActive: false
    },
    {
      id: 'podcast',
      name: '播客模式',
      icon: '🎙️',
      description: '智能音频内容生成',
      isExpert: true,
      isActive: false
    },
    {
      id: 'general',
      name: '通用模式',
      icon: '🔍',
      description: '通用智能助手',
      isExpert: true,
      isActive: false
    }
  ];

  // PPT案例数据
  const pptCases = [
    {
      id: 1,
      title: '分析中国乙女游戏的魅力',
      image: '/images/case1.png',
      thumbnail: '/images/thumbnail1.png'
    },
    {
      id: 2,
      title: '虚拟偶像市场分析与营收',
      image: '/images/case2.png',
      thumbnail: '/images/thumbnail2.png'
    },
    {
      id: 3,
      title: '甲元智的中国之行总结',
      image: '/images/case3.png',
      thumbnail: '/images/thumbnail3.png'
    }
  ];

  // 当前选中的智能体
  const currentAgent = agents.find(agent => agent.isActive) || agents[1]; // 默认PPT模式

  return (
    <div className="home-container">
      <Sidebar />
      
      <div className="main-content">
        <Header />
        
        <div className="agent-header">
          <div className="agent-badge">天工超级智能体</div>
          <h1 className="agent-title">{currentAgent.description}</h1>
        </div>
        
        <div className="input-section">
          <div className="input-header">
            <span className="agent-icon">{currentAgent.icon} {currentAgent.name}</span>
            <span className="divider">|</span>
            <span className="mode-label">PPT模式</span>
          </div>
          
          <SearchBar 
            placeholder="请输入PPT的主题和需求，或上传文件，让PPT智能体帮你制作" 
          />
          
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
        
        <div className="agents-grid">
          {agents.map(agent => (
            <AgentCard 
              key={agent.id}
              agent={agent}
              isActive={agent.id === currentAgent.id}
            />
          ))}
        </div>
        
        <div className="showcase-section">
          <h2 className="showcase-title">PPT 用户案例展示</h2>
          <CaseShowcase cases={pptCases} />
        </div>
      </div>
    </div>
  );
};

export default Home;
