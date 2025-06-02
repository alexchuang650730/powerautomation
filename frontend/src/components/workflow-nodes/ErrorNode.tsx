import React from 'react';
import '../styles/WorkflowNodes.css';
import { SimpleNodeProps } from './TriggerNode';

const ErrorNode: React.FC<SimpleNodeProps & { data: { errorType?: string, errorMessage?: string } }> = ({ 
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
      className={`workflow-node workflow-node-error ${selected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="workflow-node-header">
        <span className="workflow-node-type">错误</span>
        {data.status && (
          <span className="workflow-node-status" style={{ backgroundColor: '#F44336' }}>
            {data.status}
          </span>
        )}
      </div>
      <div className="workflow-node-name">{data.name}</div>
      {data.description && (
        <div className="workflow-node-description">{data.description}</div>
      )}
      {data.errorType && (
        <div className="workflow-node-error-type">错误类型: {data.errorType}</div>
      )}
      {data.errorMessage && (
        <div className="workflow-node-error-message">错误信息: {data.errorMessage}</div>
      )}
      {data.timestamp && (
        <div className="workflow-node-timestamp">发生时间: {data.timestamp}</div>
      )}
    </div>
  );
};

export default ErrorNode;
