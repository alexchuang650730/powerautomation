import React from 'react';
import '../styles/WorkflowNodes.css';
import { SimpleNodeProps } from './TriggerNode';

const ActionNode: React.FC<SimpleNodeProps> = ({ id, data, selected, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(id);
    }
  };

  return (
    <div 
      className={`workflow-node workflow-node-action ${selected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="workflow-node-header">
        <span className="workflow-node-type">动作</span>
        {data.status && (
          <span className="workflow-node-status" style={{ backgroundColor: '#4CAF50' }}>
            {data.status}
          </span>
        )}
      </div>
      <div className="workflow-node-name">{data.name}</div>
      {data.description && (
        <div className="workflow-node-description">{data.description}</div>
      )}
      {data.timestamp && (
        <div className="workflow-node-timestamp">执行时间: {data.timestamp}</div>
      )}
    </div>
  );
};

export default ActionNode;
