import React, { useState } from 'react';
import '../styles/N8nWorkflowVisualizer.css';
import TriggerNode from './workflow-nodes/TriggerNode';
import ActionNode from './workflow-nodes/ActionNode';
import ConditionNode from './workflow-nodes/ConditionNode';
import ErrorNode from './workflow-nodes/ErrorNode';

// 定义工作流节点类型
export type NodeType = 'trigger' | 'action' | 'condition' | 'error';

// 定义工作流节点数据结构
export interface WorkflowNode {
  id: string;
  type: NodeType;
  position: { x: number; y: number };
  data: {
    name: string;
    description?: string;
    status?: string;
    timestamp?: string;
    type: string;
    condition?: string;
    errorType?: string;
    errorMessage?: string;
  };
}

// 定义工作流连接数据结构
export interface WorkflowConnection {
  id: string;
  source: string;
  target: string;
  label?: string;
}

// 定义组件Props
interface N8nWorkflowVisualizerProps {
  nodes: WorkflowNode[];
  connections: WorkflowConnection[];
}

const N8nWorkflowVisualizer: React.FC<N8nWorkflowVisualizerProps> = ({ nodes, connections }) => {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  // 处理节点点击事件
  const handleNodeClick = (id: string) => {
    setSelectedNodeId(id === selectedNodeId ? null : id);
  };

  // 渲染节点
  const renderNode = (node: WorkflowNode) => {
    const isSelected = node.id === selectedNodeId;
    const style = {
      position: 'absolute' as 'absolute',
      left: `${node.position.x}px`,
      top: `${node.position.y}px`,
      zIndex: isSelected ? 10 : 1,
    };

    switch (node.type) {
      case 'trigger':
        return (
          <div key={node.id} style={style}>
            <TriggerNode
              id={node.id}
              data={node.data}
              selected={isSelected}
              onClick={handleNodeClick}
            />
          </div>
        );
      case 'action':
        return (
          <div key={node.id} style={style}>
            <ActionNode
              id={node.id}
              data={node.data}
              selected={isSelected}
              onClick={handleNodeClick}
            />
          </div>
        );
      case 'condition':
        return (
          <div key={node.id} style={style}>
            <ConditionNode
              id={node.id}
              data={node.data}
              selected={isSelected}
              onClick={handleNodeClick}
            />
          </div>
        );
      case 'error':
        return (
          <div key={node.id} style={style}>
            <ErrorNode
              id={node.id}
              data={node.data}
              selected={isSelected}
              onClick={handleNodeClick}
            />
          </div>
        );
      default:
        return null;
    }
  };

  // 渲染连接线
  const renderConnections = () => {
    return connections.map((connection) => {
      const sourceNode = nodes.find((node) => node.id === connection.source);
      const targetNode = nodes.find((node) => node.id === connection.target);

      if (!sourceNode || !targetNode) return null;

      // 计算连接线的起点和终点
      const sourceX = sourceNode.position.x + 100; // 假设节点宽度为200px，取中点
      const sourceY = sourceNode.position.y + 50; // 假设节点高度，取中点
      const targetX = targetNode.position.x + 100;
      const targetY = targetNode.position.y + 50;

      // 计算控制点，创建曲线
      const controlPointX1 = sourceX + (targetX - sourceX) * 0.25;
      const controlPointY1 = sourceY;
      const controlPointX2 = sourceX + (targetX - sourceX) * 0.75;
      const controlPointY2 = targetY;

      // 创建SVG路径
      const path = `M ${sourceX},${sourceY} C ${controlPointX1},${controlPointY1} ${controlPointX2},${controlPointY2} ${targetX},${targetY}`;

      // 计算标签位置
      const labelX = sourceX + (targetX - sourceX) * 0.5;
      const labelY = sourceY + (targetY - sourceY) * 0.5 - 10;

      return (
        <g key={connection.id} className="workflow-connection">
          <path
            d={path}
            stroke="#999"
            strokeWidth="2"
            fill="none"
            markerEnd="url(#arrowhead)"
          />
          {connection.label && (
            <text
              x={labelX}
              y={labelY}
              textAnchor="middle"
              className="connection-label"
            >
              {connection.label}
            </text>
          )}
        </g>
      );
    });
  };

  return (
    <div className="n8n-workflow-visualizer">
      <svg className="connections-layer">
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="10"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#999" />
          </marker>
        </defs>
        {renderConnections()}
      </svg>
      <div className="nodes-layer">
        {nodes.map((node) => renderNode(node))}
      </div>
    </div>
  );
};

export default N8nWorkflowVisualizer;
