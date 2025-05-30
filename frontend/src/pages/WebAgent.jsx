import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/WebAgent.css';

const WebAgent = () => {
  const [url, setUrl] = useState('');
  const [task, setTask] = useState('');
  const [analysisType, setAnalysisType] = useState('general');
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('extract');
  
  const navigate = useNavigate();

  const handleExtractData = async () => {
    if (!url) {
      alert('请输入网页URL');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('/api/web_agent/extract_data', {
        url,
        extraction_query: query
      });
      setResult(response.data);
    } catch (error) {
      console.error('提取数据失败:', error);
      setResult({ error: '提取数据失败，请稍后重试' });
    } finally {
      setLoading(false);
    }
  };

  const handleAutomateTask = async () => {
    if (!url || !task) {
      alert('请输入网页URL和任务描述');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('/api/web_agent/automate_task', {
        url,
        task
      });
      setResult(response.data);
    } catch (error) {
      console.error('执行任务失败:', error);
      setResult({ error: '执行任务失败，请稍后重试' });
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeContent = async () => {
    if (!url) {
      alert('请输入网页URL');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('/api/web_agent/analyze_content', {
        url,
        analysis_type: analysisType,
        analysis_query: query
      });
      setResult(response.data);
    } catch (error) {
      console.error('分析内容失败:', error);
      setResult({ error: '分析内容失败，请稍后重试' });
    } finally {
      setLoading(false);
    }
  };

  const renderForm = () => {
    switch (activeTab) {
      case 'extract':
        return (
          <div className="form-container">
            <div className="form-group">
              <label>网页URL</label>
              <input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="输入网页URL，例如: https://example.com"
              />
            </div>
            <div className="form-group">
              <label>提取指令</label>
              <textarea 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="输入提取指令，例如: 提取所有产品信息"
              />
            </div>
            <button 
              className="action-button" 
              onClick={handleExtractData} 
              disabled={loading}
            >
              {loading ? '提取中...' : '提取数据'}
            </button>
          </div>
        );
      
      case 'automate':
        return (
          <div className="form-container">
            <div className="form-group">
              <label>网页URL</label>
              <input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="输入网页URL，例如: https://example.com"
              />
            </div>
            <div className="form-group">
              <label>任务描述</label>
              <textarea 
                value={task} 
                onChange={(e) => setTask(e.target.value)} 
                placeholder="输入任务描述，例如: 登录并下载报告"
              />
            </div>
            <button 
              className="action-button" 
              onClick={handleAutomateTask} 
              disabled={loading}
            >
              {loading ? '执行中...' : '执行任务'}
            </button>
          </div>
        );
      
      case 'analyze':
        return (
          <div className="form-container">
            <div className="form-group">
              <label>网页URL</label>
              <input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="输入网页URL，例如: https://example.com"
              />
            </div>
            <div className="form-group">
              <label>分析类型</label>
              <select 
                value={analysisType} 
                onChange={(e) => setAnalysisType(e.target.value)}
              >
                <option value="general">一般分析</option>
                <option value="seo">SEO分析</option>
                <option value="structure">结构分析</option>
                <option value="content">内容分析</option>
              </select>
            </div>
            <div className="form-group">
              <label>分析要求</label>
              <textarea 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="输入分析要求，例如: 分析网站的主要内容类别"
              />
            </div>
            <button 
              className="action-button" 
              onClick={handleAnalyzeContent} 
              disabled={loading}
            >
              {loading ? '分析中...' : '分析内容'}
            </button>
          </div>
        );
      
      default:
        return null;
    }
  };

  const renderResult = () => {
    if (!result) return null;
    
    if (result.error) {
      return (
        <div className="result-container error">
          <h3>错误</h3>
          <p>{result.error}</p>
        </div>
      );
    }
    
    return (
      <div className="result-container">
        <h3>结果</h3>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </div>
    );
  };

  return (
    <div className="web-agent-container">
      <h1>网页智能体</h1>
      <p className="description">
        网页智能体可以帮助您抓取网页内容、执行自动化任务和分析网页内容。
      </p>
      
      <div className="tabs">
        <button 
          className={activeTab === 'extract' ? 'active' : ''} 
          onClick={() => setActiveTab('extract')}
        >
          数据提取
        </button>
        <button 
          className={activeTab === 'automate' ? 'active' : ''} 
          onClick={() => setActiveTab('automate')}
        >
          自动化任务
        </button>
        <button 
          className={activeTab === 'analyze' ? 'active' : ''} 
          onClick={() => setActiveTab('analyze')}
        >
          内容分析
        </button>
      </div>
      
      {renderForm()}
      {renderResult()}
      
      <button 
        className="back-button" 
        onClick={() => navigate('/')}
      >
        返回首页
      </button>
    </div>
  );
};

export default WebAgent;
