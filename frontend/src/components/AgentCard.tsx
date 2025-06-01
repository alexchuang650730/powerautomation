import React from 'react';
import '../styles/AgentCard.css';
import pptIcon from '../assets/images/ppt_icon.png';

export interface Agent {
  id: string;
  name: string;
  icon: string;
  description: string;
  isExpert: boolean;
}

interface AgentCardProps {
  agent: Agent;
  isActive: boolean;
  onClick?: (id: string) => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, isActive, onClick }) => {
  const { id, name, icon, isExpert } = agent;
  
  // 根据不同模式显示不同的图标
  const renderIcon = () => {
    if (id === 'ppt') {
      return <img src={pptIcon} alt="PPT模式" className="agent-card-custom-icon" />;
    }
    return <div className="agent-card-icon">{icon}</div>;
  };
  
  return (
    <div 
      className={`agent-card ${isActive ? 'agent-card-active' : ''} ${id}-mode`}
      onClick={() => onClick && onClick(id)}
    >
      <div className="agent-card-content">
        {renderIcon()}
        <div className="agent-card-name">{name}</div>
        {isExpert && (
          <div className="agent-card-expert-badge">专家</div>
        )}
      </div>
    </div>
  );
};

export default AgentCard;
