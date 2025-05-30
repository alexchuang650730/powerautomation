import React from 'react';
import '../styles/AgentCard.css';

const AgentCard = ({ agent, isActive, onClick }) => {
  const { id, name, icon, isExpert } = agent;
  
  return (
    <div 
      className={`agent-card ${isActive ? 'active' : ''}`}
      onClick={() => onClick && onClick(id)}
    >
      {isExpert && <div className="expert-badge">专家</div>}
      <div className="agent-icon">{icon}</div>
      <div className="agent-name">{name}</div>
    </div>
  );
};

export default AgentCard;
