import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface ErrorNodeData {
  label: string;
  type: string;
  status: string;
  timestamp: string;
  error?: string;
}

const ErrorNode: React.FC<NodeProps<ErrorNodeData>> = ({ data }) => {
  return (
    <div className="workflow-node">
      <Handle type="target" position={Position.Top} />
      
      <div className="workflow-node-header">
        <div className="workflow-node-type">{data.type}</div>
        <div className={`workflow-node-status error`}>失败</div>
      </div>
      
      <div className="workflow-node-description">{data.label}</div>
      {data.error && (
        <div className="workflow-node-error">{data.error}</div>
      )}
      <div className="workflow-node-timestamp">
        {new Date(data.timestamp).toLocaleString('zh-CN')}
      </div>
    </div>
  );
};

export default ErrorNode;
