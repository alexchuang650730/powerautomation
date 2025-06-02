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

const TriggerNode: React.FC<SimpleNodeProps> = ({ node, isSelected, onClick }) => {
  // 根据节点状态设置颜色
  let statusColor = '#9e9e9e'; // 默认灰色
  if (node.status === 'success') statusColor = '#4CAF50';
  else if (node.status === 'error') statusColor = '#F44336';
  else if (node.status === 'running') statusColor = '#FFC107';

  // 状态文本映射
  const statusText = {
    'success': '成功',
    'error': '失败',
    'running': '运行中',
    'pending': '等待中'
  }[node.status] || node.status;

  return (
    <div 
      className={`workflow-node workflow-node-trigger ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
    >
      <div className="workflow-node-header">
        <div className="workflow-node-type">{node.type}</div>
        <div className="workflow-node-status" style={{ backgroundColor: statusColor }}>
          {statusText}
        </div>
      </div>
      
      <div className="workflow-node-name">{node.name}</div>
      <div className="workflow-node-description">{node.description}</div>
      
      {node.data && node.data.timestamp && (
        <div className="workflow-node-timestamp">
          {new Date(node.data.timestamp).toLocaleString('zh-CN')}
        </div>
      )}
    </div>
  );
};

export default TriggerNode;
