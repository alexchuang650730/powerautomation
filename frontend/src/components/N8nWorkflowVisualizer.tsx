import React, { useState, useEffect, useRef } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Controls,
  Background,
  MiniMap,
  Node,
  Edge,
  NodeTypes,
  EdgeTypes,
  Connection,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import '../styles/N8nWorkflowVisualizer.css';

// 自定义节点类型
import TriggerNode from './workflow-nodes/TriggerNode';
import ActionNode from './workflow-nodes/ActionNode';
import ConditionNode from './workflow-nodes/ConditionNode';
import ErrorNode from './workflow-nodes/ErrorNode';

// 工作流节点数据接口
interface WorkflowNode {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  status: string;
  data?: any;
  savepoint_id?: string;
}

// 工作流连接数据接口
interface WorkflowConnection {
  source: string;
  target: string;
  type: string;
}

// 组件属性接口
interface N8nWorkflowVisualizerProps {
  workflowNodes?: WorkflowNode[];
  workflowConnections?: WorkflowConnection[];
  refreshInterval?: number;
  readOnly?: boolean;
  height?: string;
}

// 节点类型映射
const nodeTypes: NodeTypes = {
  triggerNode: TriggerNode,
  actionNode: ActionNode,
  conditionNode: ConditionNode,
  errorNode: ErrorNode
};

// 默认节点样式
const getNodeStyle = (type: string, status: string) => {
  const baseStyle = {
    padding: 10,
    borderRadius: 5,
    minWidth: 150,
    boxShadow: '0 1px 4px rgba(0, 0, 0, 0.16)'
  };

  // 根据节点类型设置颜色
  switch (type.toLowerCase()) {
    case 'trigger':
    case '触发器':
    case '下载release':
      return { ...baseStyle, background: '#61b8ff' };
    case 'action':
    case '动作':
    case '部署成功':
    case '创建保存点':
      return { ...baseStyle, background: '#27ae60' };
    case 'condition':
    case '条件':
      return { ...baseStyle, background: '#ff9800' };
    case 'error':
    case '错误':
    case '部署失败':
    case '上传代码失败':
      return { ...baseStyle, background: '#e74c3c' };
    default:
      return { ...baseStyle, background: '#95a5a6' };
  }
};

// 默认边样式
const getEdgeStyle = (type: string) => {
  switch (type.toLowerCase()) {
    case 'success':
      return {
        stroke: '#27ae60',
        strokeWidth: 2,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#27ae60'
        }
      };
    case 'error':
      return {
        stroke: '#e74c3c',
        strokeWidth: 2,
        strokeDasharray: '5,5',
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#e74c3c'
        }
      };
    case 'conditional':
      return {
        stroke: '#ff9800',
        strokeWidth: 2,
        strokeDasharray: '3,3',
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#ff9800'
        }
      };
    default:
      return {
        stroke: '#95a5a6',
        strokeWidth: 2,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#95a5a6'
        }
      };
  }
};

// 将工作流节点转换为ReactFlow节点
const convertToReactFlowNodes = (workflowNodes: WorkflowNode[]): Node[] => {
  return workflowNodes.map((node, index) => {
    // 根据节点类型确定ReactFlow节点类型
    let nodeType = 'actionNode';
    switch (node.type.toLowerCase()) {
      case 'trigger':
      case '触发器':
      case '下载release':
        nodeType = 'triggerNode';
        break;
      case 'condition':
      case '条件':
        nodeType = 'conditionNode';
        break;
      case 'error':
      case '错误':
      case '部署失败':
      case '上传代码失败':
        nodeType = 'errorNode';
        break;
      default:
        nodeType = 'actionNode';
    }

    // 创建ReactFlow节点
    return {
      id: node.id,
      type: nodeType,
      position: { x: 100 + (index % 3) * 250, y: 100 + Math.floor(index / 3) * 150 },
      data: {
        label: node.description,
        type: node.type,
        status: node.status,
        timestamp: node.timestamp,
        ...node.data
      },
      style: getNodeStyle(node.type, node.status)
    };
  });
};

// 将工作流连接转换为ReactFlow边
const convertToReactFlowEdges = (workflowConnections: WorkflowConnection[]): Edge[] => {
  return workflowConnections.map((connection, index) => {
    return {
      id: `edge-${index}`,
      source: connection.source,
      target: connection.target,
      type: 'default',
      style: getEdgeStyle(connection.type),
      animated: connection.type.toLowerCase() === 'running'
    };
  });
};

// 自动生成工作流连接
const generateWorkflowConnections = (workflowNodes: WorkflowNode[]): WorkflowConnection[] => {
  const connections: WorkflowConnection[] = [];
  
  // 按时间戳排序节点
  const sortedNodes = [...workflowNodes].sort((a, b) => {
    return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
  });
  
  // 为相邻节点创建连接
  for (let i = 0; i < sortedNodes.length - 1; i++) {
    const source = sortedNodes[i];
    const target = sortedNodes[i + 1];
    
    // 确定连接类型
    let connectionType = 'success';
    if (target.type.toLowerCase().includes('失败') || 
        target.type.toLowerCase().includes('error')) {
      connectionType = 'error';
    } else if (target.type.toLowerCase().includes('条件') || 
               target.type.toLowerCase().includes('condition')) {
      connectionType = 'conditional';
    }
    
    connections.push({
      source: source.id,
      target: target.id,
      type: connectionType
    });
  }
  
  return connections;
};

const N8nWorkflowVisualizer: React.FC<N8nWorkflowVisualizerProps> = ({
  workflowNodes = [],
  workflowConnections,
  refreshInterval = 5000,
  readOnly = false,
  height = '500px'
}) => {
  // 使用ReactFlow的状态钩子
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // 引用ReactFlow实例
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  
  // 模拟从API获取数据
  const fetchData = async () => {
    try {
      setLoading(true);
      // 实际项目中，这里应该是一个API调用
      // const response = await fetch('/api/workflow-data');
      // const data = await response.json();
      
      // 使用传入的节点或模拟数据
      const mockWorkflowNodes: WorkflowNode[] = workflowNodes.length > 0 ? workflowNodes : await getMockWorkflowNodes();
      
      // 使用传入的连接或自动生成连接
      const mockWorkflowConnections: WorkflowConnection[] = workflowConnections || generateWorkflowConnections(mockWorkflowNodes);
      
      // 转换为ReactFlow格式
      const reactFlowNodes = convertToReactFlowNodes(mockWorkflowNodes);
      const reactFlowEdges = convertToReactFlowEdges(mockWorkflowConnections);
      
      // 更新状态
      setNodes(reactFlowNodes);
      setEdges(reactFlowEdges);
      setError(null);
    } catch (err) {
      setError('获取工作流数据失败，请稍后重试');
      console.error('获取工作流数据失败:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // 模拟数据获取函数，实际项目中应替换为真实API调用
  const getMockWorkflowNodes = (): Promise<WorkflowNode[]> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 'node1',
            type: '下载release',
            description: '下载release: v1.0.0',
            timestamp: '2025-06-01T09:00:00Z',
            status: 'success'
          },
          {
            id: 'node2',
            type: '创建保存点',
            description: '创建保存点: 初始版本',
            timestamp: '2025-06-01T09:05:00Z',
            status: 'success'
          },
          {
            id: 'node3',
            type: '部署成功',
            description: '部署release: v1.0.0',
            timestamp: '2025-06-01T09:10:00Z',
            status: 'success'
          },
          {
            id: 'node4',
            type: '下载release',
            description: '下载release: v1.1.0',
            timestamp: '2025-06-01T10:00:00Z',
            status: 'success'
          },
          {
            id: 'node5',
            type: '部署失败',
            description: '部署release失败: v1.1.0',
            timestamp: '2025-06-01T10:05:00Z',
            status: 'error'
          },
          {
            id: 'node6',
            type: '回滚操作',
            description: '回滚到保存点: 初始版本',
            timestamp: '2025-06-01T10:10:00Z',
            status: 'success'
          }
        ]);
      }, 500);
    });
  };
  
  // 处理连接创建
  const onConnect = (params: Connection) => {
    if (!readOnly) {
      setEdges((eds) => addEdge({
        ...params,
        type: 'default',
        style: getEdgeStyle('success')
      }, eds));
    }
  };
  
  // 初始加载和定时刷新
  useEffect(() => {
    fetchData();
    
    if (refreshInterval > 0) {
      const intervalId = setInterval(fetchData, refreshInterval);
      return () => clearInterval(intervalId);
    }
  }, [refreshInterval, workflowNodes, workflowConnections]);
  
  if (loading && nodes.length === 0) {
    return <div className="n8n-workflow-loading">加载工作流数据...</div>;
  }
  
  if (error) {
    return <div className="n8n-workflow-error">{error}</div>;
  }
  
  return (
    <div className="n8n-workflow-visualizer" style={{ height }}>
      <ReactFlowProvider>
        <div className="reactflow-wrapper" ref={reactFlowWrapper} style={{ height: '100%' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={readOnly ? undefined : onNodesChange}
            onEdgesChange={readOnly ? undefined : onEdgesChange}
            onConnect={readOnly ? undefined : onConnect}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Controls />
            <MiniMap />
            <Background color="#f8f8f8" gap={16} />
          </ReactFlow>
        </div>
      </ReactFlowProvider>
    </div>
  );
};

export default N8nWorkflowVisualizer;
