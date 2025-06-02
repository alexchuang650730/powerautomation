import React from 'react';
import '../styles/N8nWorkflowVisualizer.css';
import '../styles/WorkflowNodes.css';

// 简化版本，移除对reactflow的直接依赖，使用自定义节点渲染
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

// 简化的节点props接口
interface SimpleNodeProps {
  node: Node;
  isSelected: boolean;
  onClick: () => void;
}

const N8nWorkflowVisualizer: React.FC = () => {
  const [workflow, setWorkflow] = React.useState<WorkflowData>({
    nodes: [],
    connections: []
  });
  const [loading, setLoading] = React.useState<boolean>(true);
  const [error, setError] = React.useState<string | null>(null);
  const [selectedNode, setSelectedNode] = React.useState<string | null>(null);

  // 使用useCallback替代useEffect，避免未使用警告
  const fetchWorkflowData = React.useCallback(() => {
    try {
      setLoading(true);
      
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
              release_url: 'https://github.com/example/repo/releases/tag/v1.0.0',
              timestamp: new Date().toISOString()
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
              path: '/home/user/downloads/v1.0.0',
              timestamp: new Date().toISOString()
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
              test_path: 'src/main.py',
              timestamp: new Date().toISOString()
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
              condition: 'test_success == true',
              timestamp: new Date().toISOString()
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
              description: '测试通过的版本',
              timestamp: new Date().toISOString()
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
              error_message: '测试失败',
              timestamp: new Date().toISOString()
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
  }, []);

  // 初始化数据
  React.useEffect(() => {
    fetchWorkflowData();
    
    // 设置定时刷新
    const intervalId = setInterval(() => {
      fetchWorkflowData();
    }, 30000); // 每30秒刷新一次

    return () => clearInterval(intervalId);
  }, [fetchWorkflowData]);

  const handleNodeClick = (nodeId: string) => {
    setSelectedNode(nodeId === selectedNode ? null : nodeId);
  };

  // 简化的节点渲染函数，使用自定义props
  const renderNode = (node: Node) => {
    const props: SimpleNodeProps = {
      node,
      isSelected: node.id === selectedNode,
      onClick: () => handleNodeClick(node.id)
    };

    // 根据节点类型渲染不同组件
    const style = {
      position: 'absolute' as const,
      left: `${node.position.x}px`,
      top: `${node.position.y}px`,
    };

    return (
      <div key={node.id} style={style}>
        {node.type === 'trigger' && (
          <div className={`workflow-node workflow-node-trigger ${props.isSelected ? 'selected' : ''}`} onClick={props.onClick}>
            <div className="workflow-node-header">
              <div className="workflow-node-type">触发器</div>
              <div className="workflow-node-status" style={{ 
                backgroundColor: node.status === 'success' ? '#4CAF50' : 
                                node.status === 'error' ? '#F44336' : 
                                node.status === 'running' ? '#FFC107' : '#9e9e9e'
              }}>
                {node.status === 'success' ? '成功' : 
                 node.status === 'error' ? '失败' : 
                 node.status === 'running' ? '运行中' : '等待中'}
              </div>
            </div>
            <div className="workflow-node-name">{node.name}</div>
            <div className="workflow-node-description">{node.description}</div>
          </div>
        )}
        
        {node.type === 'action' && (
          <div className={`workflow-node workflow-node-action ${props.isSelected ? 'selected' : ''}`} onClick={props.onClick}>
            <div className="workflow-node-header">
              <div className="workflow-node-type">动作</div>
              <div className="workflow-node-status" style={{ 
                backgroundColor: node.status === 'success' ? '#4CAF50' : 
                                node.status === 'error' ? '#F44336' : 
                                node.status === 'running' ? '#FFC107' : '#9e9e9e'
              }}>
                {node.status === 'success' ? '成功' : 
                 node.status === 'error' ? '失败' : 
                 node.status === 'running' ? '运行中' : '等待中'}
              </div>
            </div>
            <div className="workflow-node-name">{node.name}</div>
            <div className="workflow-node-description">{node.description}</div>
          </div>
        )}
        
        {node.type === 'condition' && (
          <div className={`workflow-node workflow-node-condition ${props.isSelected ? 'selected' : ''}`} onClick={props.onClick}>
            <div className="workflow-node-header">
              <div className="workflow-node-type">条件</div>
              <div className="workflow-node-status" style={{ 
                backgroundColor: node.status === 'success' ? '#4CAF50' : 
                                node.status === 'error' ? '#F44336' : 
                                node.status === 'running' ? '#FFC107' : '#9e9e9e'
              }}>
                {node.status === 'success' ? '成功' : 
                 node.status === 'error' ? '失败' : 
                 node.status === 'running' ? '运行中' : '等待中'}
              </div>
            </div>
            <div className="workflow-node-name">{node.name}</div>
            <div className="workflow-node-description">{node.description}</div>
            {node.data && node.data.condition && (
              <div className="workflow-node-condition-expr">
                条件: {node.data.condition}
              </div>
            )}
          </div>
        )}
        
        {node.type === 'error' && (
          <div className={`workflow-node workflow-node-error ${props.isSelected ? 'selected' : ''}`} onClick={props.onClick}>
            <div className="workflow-node-header">
              <div className="workflow-node-type">错误</div>
              <div className="workflow-node-status" style={{ backgroundColor: '#F44336' }}>
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
          </div>
        )}
      </div>
    );
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
          <button className="refresh-button" onClick={() => fetchWorkflowData()}>
            刷新
          </button>
        </div>
      </div>
      <div className="workflow-canvas" style={{ position: 'relative', height: '600px', border: '1px solid #eee', overflow: 'auto' }}>
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
