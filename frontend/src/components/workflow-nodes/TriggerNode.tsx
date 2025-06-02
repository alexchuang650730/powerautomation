import React from 'react';
import '../styles/WorkflowNodes.css';

export interface SimpleNodeProps {
  id: string;
  data: {
    name: string;
    description?: string;
    status?: string;
    timestamp?: string;
    type: string;
  };
  selected?: boolean;
  onClick?: (id: string) => void;
}

const TriggerNode: React.FC<SimpleNodeProps> = ({ id, data, selected, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(id);
    }
  };

  return (
    <div 
      className={`workflow-node workflow-node-trigger ${selected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="workflow-node-header">
        <span className="workflow-node-type">触发器</span>
        {data.status && (
          <span className="workflow-node-status" style={{ backgroundColor: '#2196F3' }}>
            {data.status}
          </span>
        )}
      </div>
      <div className="workflow-node-name">{data.name}</div>
      {data.description && (
        <div className="workflow-node-description">{data.description}</div>
      )}
      {data.timestamp && (
        <div className="workflow-node-timestamp">上次触发: {data.timestamp}</div>
      )}
    </div>
  );
};

export default TriggerNode;
