import React, { useState } from 'react';
import '../styles/WebAgent.css';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import SearchBar from '../components/SearchBar';

const WebAgent = () => {
  const [url, setUrl] = useState('');
  const [task, setTask] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [activeTab, setActiveTab] = useState('extract'); // 'extract', 'automate', 'analyze'

  // 模拟提交处理
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url) return;

    setIsProcessing(true);
    
    // 模拟API调用
    setTimeout(() => {
      // 根据不同的任务类型返回不同的结果
      let mockResult;
      
      if (activeTab === 'extract') {
        mockResult = {
          type: 'extraction',
          data: [
            { title: '产品1', price: '¥299', rating: '4.8/5' },
            { title: '产品2', price: '¥199', rating: '4.5/5' },
            { title: '产品3', price: '¥399', rating: '4.9/5' }
          ]
        };
      } else if (activeTab === 'automate') {
        mockResult = {
          type: 'automation',
          steps: [
            '打开网页: ' + url,
            '找到登录表单',
            '填写用户名和密码',
            '点击登录按钮',
            '导航到用户中心',
            '操作完成'
          ]
        };
      } else {
        mockResult = {
          type: 'analysis',
          summary: '这是一个电子商务网站，主要销售电子产品。网站结构清晰，导航简单，产品分类合理。',
          keyPoints: [
            '网站有5个主要类别',
            '共有约200个产品',
            '提供多种支付方式',
            '有用户评论系统'
          ]
        };
      }
      
      setResults(mockResult);
      setIsProcessing(false);
    }, 2000);
  };

  // 渲染结果区域
  const renderResults = () => {
    if (!results) return null;

    if (results.type === 'extraction') {
      return (
        <div className="results-container">
          <h3>提取的数据</h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>产品名称</th>
                <th>价格</th>
                <th>评分</th>
              </tr>
            </thead>
            <tbody>
              {results.data.map((item, index) => (
                <tr key={index}>
                  <td>{item.title}</td>
                  <td>{item.price}</td>
                  <td>{item.rating}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="action-buttons">
            <button className="export-button">导出为CSV</button>
            <button className="export-button">导出为JSON</button>
          </div>
        </div>
      );
    }

    if (results.type === 'automation') {
      return (
        <div className="results-container">
          <h3>自动化操作步骤</h3>
          <div className="steps-container">
            {results.steps.map((step, index) => (
              <div key={index} className="step-item">
                <div className="step-number">{index + 1}</div>
                <div className="step-text">{step}</div>
              </div>
            ))}
          </div>
          <div className="action-buttons">
            <button className="action-button">保存为脚本</button>
            <button className="action-button">重新执行</button>
          </div>
        </div>
      );
    }

    if (results.type === 'analysis') {
      return (
        <div className="results-container">
          <h3>网页分析结果</h3>
          <div className="analysis-summary">
            <h4>摘要</h4>
            <p>{results.summary}</p>
          </div>
          <div className="analysis-points">
            <h4>关键点</h4>
            <ul>
              {results.keyPoints.map((point, index) => (
                <li key={index}>{point}</li>
              ))}
            </ul>
          </div>
          <div className="action-buttons">
            <button className="action-button">生成报告</button>
            <button className="action-button">深入分析</button>
          </div>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="web-agent-container">
      <Sidebar />
      
      <div className="main-content">
        <Header />
        
        <div className="agent-header">
          <div className="agent-badge">天工超级智能体</div>
          <h1 className="agent-title">增强的网页搜索和内容分析</h1>
        </div>
        
        <div className="web-agent-tabs">
          <div 
            className={`tab ${activeTab === 'extract' ? 'active' : ''}`}
            onClick={() => setActiveTab('extract')}
          >
            <span className="tab-icon">📊</span>
            数据提取
          </div>
          <div 
            className={`tab ${activeTab === 'automate' ? 'active' : ''}`}
            onClick={() => setActiveTab('automate')}
          >
            <span className="tab-icon">🤖</span>
            网页自动化
          </div>
          <div 
            className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyze')}
          >
            <span className="tab-icon">🔍</span>
            内容分析
          </div>
        </div>
        
        <form className="web-agent-form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label>网页URL</label>
            <input 
              type="url" 
              placeholder="输入网页地址 (例如: https://example.com)" 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>
          
          <div className="input-group">
            <label>
              {activeTab === 'extract' ? '提取指令' : 
               activeTab === 'automate' ? '自动化任务' : '分析要求'}
            </label>
            <textarea 
              placeholder={
                activeTab === 'extract' ? '描述需要提取的数据 (例如: 提取所有产品的名称、价格和评分)' : 
                activeTab === 'automate' ? '描述需要自动执行的任务 (例如: 登录账户并查看订单历史)' : 
                '描述需要分析的内容 (例如: 分析网站结构和主要内容类别)'
              }
              value={task}
              onChange={(e) => setTask(e.target.value)}
            />
          </div>
          
          <div className="action-buttons">
            <button 
              type="submit" 
              className="submit-button"
              disabled={isProcessing}
            >
              {isProcessing ? '处理中...' : 
               activeTab === 'extract' ? '开始提取' : 
               activeTab === 'automate' ? '开始自动化' : '开始分析'}
            </button>
            <button type="button" className="clear-button">
              清除
            </button>
          </div>
        </form>
        
        {isProcessing && (
          <div className="processing-indicator">
            <div className="spinner"></div>
            <p>正在处理您的请求，请稍候...</p>
          </div>
        )}
        
        {renderResults()}
      </div>
    </div>
  );
};

export default WebAgent;
