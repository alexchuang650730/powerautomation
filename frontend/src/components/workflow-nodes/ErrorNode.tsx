import React from 'react';
import '../../styles/WorkflowNodes.css';

// 使用自定义SimpleNodeProps接口替代reactflow的NodeProps
interface SimpleNodeProps {
  node: {
    id: string;
    type: 'trigger' | 'action' | 'condition' | 'error';
    name: string;
    description: string;
    status: 'pending' | 'running' | 'success' | 'error';
    position: { x: number; y: number };
    data?: Record<string, any>;
  };
  isSelected: boolean;
  onClick: () => void;
}

const ErrorNode: React.FC<SimpleNodeProps> = ({ node, isSelected, onClick }) => {
  // 错误节点始终使用红色
  const statusColor = '#F44336';

  return (
    <div 
      className={`workflow-node workflow-node-error ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
    >
      <div className="workflow-node-header">
        <div className="workflow-node-type">{node.type}</div>
        <div className="workflow-node-status" style={{ backgroundColor: statusColor }}>
          失败
        </div>
      </div>
      
      <div className="workflow-node-name">{node.name}</div>
      <div className="workflow-node-description">{node.description}</div>
      
      {node.data && node.data.error_message && (
        <div className="workflow-node-error-message">
          错误信息: {node.data.error_message}
        </div>
      )}
      
      {node.data && node.data.error_type && (
        <div className="workflow-node-error-type">
          错误类型: {node.data.error_type}
        </div>
      )}
      
      {node.data && node.data.timestamp && (
        <div className="workflow-node-timestamp">
          {new Date(node.data.timestamp).toLocaleString('zh-CN')}
        </div>
      )}
    </div>
  );
};

export default ErrorNode;
