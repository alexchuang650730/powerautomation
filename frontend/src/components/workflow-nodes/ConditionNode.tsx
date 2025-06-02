import React from 'react';
import '../styles/WorkflowNodes.css';
import { SimpleNodeProps } from './TriggerNode';

const ConditionNode: React.FC<SimpleNodeProps & { data: { condition?: string } }> = ({ 
  id, 
  data, 
  selected, 
  onClick 
}) => {
  const handleClick = () => {
    if (onClick) {
      onClick(id);
    }
  };

  return (
    <div 
      className={`workflow-node workflow-node-condition ${selected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="workflow-node-header">
        <span className="workflow-node-type">条件</span>
        {data.status && (
          <span className="workflow-node-status" style={{ backgroundColor: '#FF9800' }}>
            {data.status}
          </span>
        )}
      </div>
      <div className="workflow-node-name">{data.name}</div>
      {data.description && (
        <div className="workflow-node-description">{data.description}</div>
      )}
      {data.condition && (
        <div className="workflow-node-condition-expr">条件表达式: {data.condition}</div>
      )}
      {data.timestamp && (
        <div className="workflow-node-timestamp">评估时间: {data.timestamp}</div>
      )}
    </div>
  );
};

export default ConditionNode;
