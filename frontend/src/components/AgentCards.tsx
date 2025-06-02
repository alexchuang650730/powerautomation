import React from 'react';
import '../styles/AgentCards.css';

interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
}

interface AgentCardsProps {
  agents: Agent[];
  selectedAgentId: string;
  onSelect: (agentId: string) => void;
}

const AgentCards: React.FC<AgentCardsProps> = ({ agents, selectedAgentId, onSelect }) => {
  return (
    <div className="agent-cards">
      {agents.map((agent) => (
        <div 
          key={agent.id}
          className={`agent-card ${agent.id === selectedAgentId ? 'selected' : ''}`}
          onClick={() => onSelect(agent.id)}
        >
          <div className="agent-header">
            <div className="agent-icon">{agent.icon}</div>
            <div className="agent-name">{agent.name}</div>
            {agent.id === 'ppt' && (
              <div className="mode-label">PPT模式</div>
            )}
          </div>
          <div className="agent-description">{agent.description}</div>
          
          {agent.id === selectedAgentId && agent.id === 'ppt' && (
            <div className="mode-description">
              <h4>任务说明:</h4>
              <p>任务完成或暂停后，30分钟内没有发起新对话，系统会自动终止该任务。</p>
              <p>任务进行将消耗积分,任务越复杂积分消耗越多。</p>
              <p>专家级智能体将交付更专业的成果，需等待10-25min</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default AgentCards;
