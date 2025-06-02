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
    status = 'idle', 
    executionState = 'pending',
    timestamp = '', 
    type = '默认',
    errorMessage = '',
    executionTime = 0,
    memoryUsage = 0,
    cpuUsage = 0,
    logRefs = [],
    codeRefs = []
  } = data || {};

  // 根据状态确定节点样式和图标
  const getStatusStyle = () => {
    switch(status) {
      case 'running':
        return { backgroundColor: '#2196F3', icon: '⚙️' };
      case 'success':
        return { backgroundColor: '#4CAF50', icon: '✅' };
      case 'error':
        return { backgroundColor: '#F44336', icon: '❌' };
      case 'warning':
        return { backgroundColor: '#FF9800', icon: '⚠️' };
      default:
        return { backgroundColor: '#9E9E9E', icon: '⏳' };
    }
  };

  const statusStyle = getStatusStyle();

  return (
    <div 
      className={`workflow-node workflow-node-action ${selected ? 'selected' : ''} status-${status}`}
      onClick={handleClick}
      data-log-refs={logRefs.join(',')}
      data-code-refs={codeRefs.join(',')}
    >
      <div className="workflow-node-header">
        <span className="workflow-node-type">动作: {type}</span>
        <span className="workflow-node-status" style={{ backgroundColor: statusStyle.backgroundColor }}>
          <span className="status-icon">{statusStyle.icon}</span>
          {status}
        </span>
      </div>
      <div className="workflow-node-name">{name}</div>
      {description && (
        <div className="workflow-node-description">{description}</div>
      )}
      {timestamp && (
        <div className="workflow-node-timestamp">执行时间: {timestamp}</div>
      )}
      
      {/* 执行状态信息 */}
      <div className="workflow-node-execution-info">
        <div className="execution-state">状态: {executionState}</div>
        {executionTime > 0 && (
          <div className="execution-metrics">
            <span>耗时: {executionTime}ms</span>
            {memoryUsage > 0 && <span>内存: {memoryUsage}MB</span>}
            {cpuUsage > 0 && <span>CPU: {cpuUsage}%</span>}
          </div>
        )}
      </div>
      
      {/* 错误信息 */}
      {status === 'error' && errorMessage && (
        <div className="workflow-node-error">
          <span className="error-icon">🔍</span>
          <span className="error-message">{errorMessage}</span>
        </div>
      )}
      
      {/* 关联信息指示器 */}
      <div className="workflow-node-references">
        {logRefs && logRefs.length > 0 && (
          <span className="reference-indicator log-reference" title="查看相关日志">📋</span>
        )}
        {codeRefs && codeRefs.length > 0 && (
          <span className="reference-indicator code-reference" title="查看相关代码">📝</span>
        )}
      </div>
    </div>
  );
};

export default ActionNode;
