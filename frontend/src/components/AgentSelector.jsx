/**
 * 智能体选择器组件
 * 负责展示和选择四个智能体（PPT、网页、代码、通用）
 */

import React, { useState, useEffect } from 'react';
import agentRouter, { AGENT_TYPES } from '../utils/agent-router';

const AgentSelector = ({ onAgentChange }) => {
  const [selectedAgent, setSelectedAgent] = useState(agentRouter.getCurrentAgent());
  
  // 智能体信息
  const agents = [
    {
      id: AGENT_TYPES.PPT,
      name: 'PPT智能体',
      icon: '📊',
      description: '创建专业、美观的演示文稿'
    },
    {
      id: AGENT_TYPES.WEB,
      name: '网页智能体',
      icon: '🌐',
      description: '设计和开发响应式网页'
    },
    {
      id: AGENT_TYPES.CODE,
      name: '代码智能体',
      icon: '💻',
      description: '编写高质量代码和解决编程问题'
    },
    {
      id: AGENT_TYPES.GENERAL,
      name: '通用智能体',
      icon: '🤖',
      description: '处理各种通用任务和问题'
    }
  ];

  // 处理智能体选择
  const handleAgentSelect = (agentId) => {
    if (agentRouter.setCurrentAgent(agentId)) {
      setSelectedAgent(agentId);
      
      // 通知父组件
      if (onAgentChange) {
        onAgentChange(agentId);
      }
    }
  };

  // 初始化时同步当前智能体
  useEffect(() => {
    setSelectedAgent(agentRouter.getCurrentAgent());
  }, []);

  return (
    <div className="agent-selector">
      <h2 className="selector-title">选择智能体</h2>
      
      <div className="agents-grid">
        {agents.map(agent => (
          <div 
            key={agent.id}
            className={`agent-card ${selectedAgent === agent.id ? 'selected' : ''}`}
            onClick={() => handleAgentSelect(agent.id)}
          >
            <div className="agent-icon">{agent.icon}</div>
            <h3 className="agent-name">{agent.name}</h3>
            <p className="agent-description">{agent.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentSelector;
