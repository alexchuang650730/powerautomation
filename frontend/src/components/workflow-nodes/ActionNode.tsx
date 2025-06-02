import React from 'react';
import '../../styles/WorkflowNodes.css';
import { SimpleNodeProps } from './TriggerNode';

const ActionNode: React.FC<SimpleNodeProps> = ({ id, data = {}, selected = false, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(id);
    }
  };

  // 添加默认值和空值检查
  const { 
    name = '动作', 
    description = '', 
    status = '', 
    timestamp = '', 
    type = '默认' 
  } = data || {};

  return (
    <div 
      className={`workflow-node workflow-node-action ${selected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="workflow-node-header">
        <span className="workflow-node-type">动作: {type}</span>
        {status && (
          <span className="workflow-node-status" style={{ backgroundColor: '#4CAF50' }}>
            {status}
          </span>
        )}
      </div>
      <div className="workflow-node-name">{name}</div>
      {description && (
        <div className="workflow-node-description">{description}</div>
      )}
      {timestamp && (
        <div className="workflow-node-timestamp">执行时间: {timestamp}</div>
      )}
    </div>
  );
};

export default ActionNode;
