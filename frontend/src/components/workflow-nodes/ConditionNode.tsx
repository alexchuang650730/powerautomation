import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface ConditionNodeData {
  label: string;
  type: string;
  status: string;
  timestamp: string;
}

const ConditionNode: React.FC<NodeProps<ConditionNodeData>> = ({ data }) => {
  return (
    <div className="workflow-node">
      <Handle type="target" position={Position.Top} />
      <Handle type="source" position={Position.Bottom} />
      <Handle type="source" position={Position.Right} id="true" />
      <Handle type="source" position={Position.Left} id="false" />
      
      <div className="workflow-node-header">
        <div className="workflow-node-type">{data.type}</div>
        <div className={`workflow-node-status ${data.status}`}>
          {data.status === 'success' ? '成功' : 
           data.status === 'error' ? '失败' : 
           data.status === 'pending' ? '进行中' : data.status}
        </div>
      </div>
      
      <div className="workflow-node-description">{data.label}</div>
      <div className="workflow-node-timestamp">
        {new Date(data.timestamp).toLocaleString('zh-CN')}
      </div>
    </div>
  );
};

export default ConditionNode;
