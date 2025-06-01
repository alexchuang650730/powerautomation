import React, { useState, useEffect } from 'react';
import '../styles/N8nWorkflowVisualizer.css';
import TriggerNode from './workflow-nodes/TriggerNode';
import ActionNode from './workflow-nodes/ActionNode';
import ConditionNode from './workflow-nodes/ConditionNode';
import ErrorNode from './workflow-nodes/ErrorNode';

interface Node {
  id: string;
  type: 'trigger' | 'action' | 'condition' | 'error';
  name: string;
  description: string;
  status: 'pending' | 'running' | 'success' | 'error';
  position: { x: number; y: number };
  data?: Record<string, any>;
}

interface Connection {
  id: string;
  source: string;
  target: string;
  type: 'success' | 'error' | 'condition';
}

interface WorkflowData {
  nodes: Node[];
  connections: Connection[];
}

const N8nWorkflowVisualizer: React.FC = () => {
  const [workflow, setWorkflow] = useState<WorkflowData>({
    nodes: [],
    connections: []
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  useEffect(() => {
    // 模拟从API获取工作流数据
    const fetchWorkflowData = async () => {
      try {
        setLoading(true);
        // 实际项目中，这里应该是从API获取数据
        // const response = await fetch('/api/workflow');
        // const data = await response.json();
        
        // 模拟数据
        const mockData: WorkflowData = {
          nodes: [
            {
              id: 'node_1',
              type: 'trigger',
              name: 'GitHub Release',
              description: '检测到新版本 v1.0.0',
              status: 'success',
              position: { x: 100, y: 100 },
              data: {
                release_version: 'v1.0.0',
                release_url: 'https://github.com/example/repo/releases/tag/v1.0.0'
              }
            },
            {
              id: 'node_2',
              type: 'action',
              name: '下载代码',
              description: '从GitHub下载代码',
              status: 'success',
              position: { x: 100, y: 250 },
              data: {
                path: '/home/user/downloads/v1.0.0'
              }
            },
            {
              id: 'node_3',
              type: 'action',
              name: '运行测试',
              description: '执行单元测试',
              status: 'running',
              position: { x: 100, y: 400 },
              data: {
                test_type: 'unit',
                test_path: 'src/main.py'
              }
            },
            {
              id: 'node_4',
              type: 'condition',
              name: '测试结果',
              description: '检查测试结果',
              status: 'pending',
              position: { x: 100, y: 550 },
              data: {
                condition: 'test_success == true'
              }
            },
            {
              id: 'node_5',
              type: 'action',
              name: '创建保存点',
              description: '创建代码保存点',
              status: 'pending',
              position: { x: 300, y: 700 },
              data: {
                savepoint_id: 'sp_1234',
                description: '测试通过的版本'
              }
            },
            {
              id: 'node_6',
              type: 'error',
              name: '问题分析',
              description: '分析测试失败原因',
              status: 'pending',
              position: { x: -100, y: 700 },
              data: {
                error_type: 'test_failure',
                error_message: '测试失败'
              }
            }
          ],
          connections: [
            {
              id: 'conn_1',
              source: 'node_1',
              target: 'node_2',
              type: 'success'
            },
            {
              id: 'conn_2',
              source: 'node_2',
              target: 'node_3',
              type: 'success'
            },
            {
              id: 'conn_3',
              source: 'node_3',
              target: 'node_4',
              type: 'success'
            },
            {
              id: 'conn_4',
              source: 'node_4',
              target: 'node_5',
              type: 'success'
            },
            {
              id: 'conn_5',
              source: 'node_4',
              target: 'node_6',
              type: 'error'
            }
          ]
        };
        
        setWorkflow(mockData);
        setLoading(false);
      } catch (err) {
        setError('加载工作流数据失败');
        setLoading(false);
        console.error('Error fetching workflow data:', err);
      }
    };

    fetchWorkflowData();

    // 设置定时刷新
    const intervalId = setInterval(() => {
      fetchWorkflowData();
    }, 30000); // 每30秒刷新一次

    return () => clearInterval(intervalId);
  }, []);

  const handleNodeClick = (nodeId: string) => {
    setSelectedNode(nodeId === selectedNode ? null : nodeId);
  };

  const renderNode = (node: Node) => {
    const props = {
      key: node.id,
      node,
      isSelected: node.id === selectedNode,
      onClick: () => handleNodeClick(node.id)
    };

    switch (node.type) {
      case 'trigger':
        return <TriggerNode {...props} />;
      case 'action':
        return <ActionNode {...props} />;
      case 'condition':
        return <ConditionNode {...props} />;
      case 'error':
        return <ErrorNode {...props} />;
      default:
        return null;
    }
  };

  const renderConnection = (connection: Connection) => {
    const sourceNode = workflow.nodes.find(node => node.id === connection.source);
    const targetNode = workflow.nodes.find(node => node.id === connection.target);

    if (!sourceNode || !targetNode) return null;

    // 计算连接线的起点和终点
    const startX = sourceNode.position.x + 100; // 节点宽度的一半
    const startY = sourceNode.position.y + 50; // 节点高度
    const endX = targetNode.position.x + 100; // 节点宽度的一半
    const endY = targetNode.position.y;

    // 计算控制点，创建平滑的曲线
    const controlX1 = startX;
    const controlY1 = startY + (endY - startY) / 3;
    const controlX2 = endX;
    const controlY2 = endY - (endY - startY) / 3;

    // 根据连接类型设置颜色
    let strokeColor = '#4CAF50'; // 成功连接为绿色
    if (connection.type === 'error') {
      strokeColor = '#F44336'; // 错误连接为红色
    } else if (connection.type === 'condition') {
      strokeColor = '#2196F3'; // 条件连接为蓝色
    }

    return (
      <svg
        key={connection.id}
        className="workflow-connection"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none',
          zIndex: 1
        }}
      >
        <path
          d={`M ${startX} ${startY} C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${endX} ${endY}`}
          stroke={strokeColor}
          strokeWidth="2"
          fill="none"
          markerEnd="url(#arrowhead)"
        />
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill={strokeColor} />
          </marker>
        </defs>
      </svg>
    );
  };

  if (loading) {
    return <div className="workflow-loading">加载工作流...</div>;
  }

  if (error) {
    return <div className="workflow-error">{error}</div>;
  }

  return (
    <div className="n8n-workflow-visualizer">
      <div className="workflow-header">
        <h2>工作流可视化</h2>
        <div className="workflow-controls">
          <button className="refresh-button" onClick={() => setWorkflow({ ...workflow })}>
            刷新
          </button>
        </div>
      </div>
      <div className="workflow-canvas">
        {workflow.connections.map(renderConnection)}
        {workflow.nodes.map(renderNode)}
      </div>
      <div className="workflow-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#4CAF50' }}></span>
          <span>成功</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#F44336' }}></span>
          <span>错误</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#2196F3' }}></span>
          <span>条件</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#FFC107' }}></span>
          <span>运行中</span>
        </div>
      </div>
    </div>
  );
};

export default N8nWorkflowVisualizer;
