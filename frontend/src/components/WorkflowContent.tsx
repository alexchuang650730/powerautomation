import React, { useState, useEffect } from 'react';
import { useWorkflowContext } from '../App';
import N8nWorkflowVisualizer from './N8nWorkflowVisualizer';
import '../styles/WorkflowContent.css';

interface WorkflowContentProps {
  agentType?: string;
}

const WorkflowContent: React.FC<WorkflowContentProps> = ({ agentType = 'general' }) => {
  const { 
    selectedNodeId, 
    setSelectedNodeId, 
    activeWorkflowType, 
    setActiveWorkflowType,
    refreshTrigger
  } = useWorkflowContext();
  
  const [activeTab, setActiveTab] = useState<'workflow' | 'docs'>('workflow');
  const [docsUrl, setDocsUrl] = useState<string>('');

  // 自动化测试工作流节点数据
  const automationTestNodes = [
    {
      id: 'integration-test',
      type: 'action',
      name: '集成测试',
      description: '测试组件间的交互',
      status: 'success',
      position: { x: 100, y: 100 },
      metrics: {
        executionTime: '1.5s',
        memoryUsage: '85MB',
        cpuUsage: '15%'
      }
    },
    {
      id: 'e2e-test',
      type: 'action',
      name: '端到端测试',
      description: '测试完整工作流程',
      status: 'success',
      position: { x: 100, y: 250 },
      metrics: {
        executionTime: '4.2s',
        memoryUsage: '120MB',
        cpuUsage: '25%'
      }
    },
    {
      id: 'visual-test',
      type: 'action',
      name: '视觉自动化测试',
      description: '测试UI界面和视觉元素',
      status: 'error',
      position: { x: 100, y: 400 },
      metrics: {
        executionTime: '3.7s',
        memoryUsage: '180MB',
        cpuUsage: '35%'
      }
    }
  ];

  // 自动化智能体设计工作流节点数据
  const agentDesignNodes = [
    {
      id: 'general-agent',
      type: 'trigger',
      name: '通用智能体',
      description: '处理用户输入',
      status: 'success',
      position: { x: 100, y: 100 },
      metrics: {
        executionTime: '0.8s',
        memoryUsage: '100MB',
        cpuUsage: '20%'
      }
    },
    {
      id: 'mcp-coordinator',
      type: 'action',
      name: 'MCP协调器',
      description: '协调多个子系统和组件的工作',
      status: 'success',
      position: { x: 300, y: 100 },
      metrics: {
        executionTime: '1.5s',
        memoryUsage: '75MB',
        cpuUsage: '15%'
      }
    },
    {
      id: 'mcp-planner',
      type: 'action',
      name: 'MCP规划器',
      description: '创建详细的执行计划',
      status: 'success',
      position: { x: 500, y: 100 },
      metrics: {
        executionTime: '2.1s',
        memoryUsage: '110MB',
        cpuUsage: '25%'
      }
    },
    {
      id: 'thought-recorder',
      type: 'action',
      name: '思维行为记录器',
      description: '记录智能体的思考过程',
      status: 'success',
      position: { x: 300, y: 250 },
      metrics: {
        executionTime: '1.2s',
        memoryUsage: '60MB',
        cpuUsage: '10%'
      }
    },
    {
      id: 'release-manager',
      type: 'action',
      name: '发布管理器',
      description: '管理系统版本发布和更新',
      status: 'warning',
      position: { x: 500, y: 250 },
      metrics: {
        executionTime: '3.5s',
        memoryUsage: '50MB',
        cpuUsage: '12%'
      }
    },
    {
      id: 'supermemory',
      type: 'action',
      name: 'SuperMemory',
      description: '管理智能体的记忆系统',
      status: 'success',
      position: { x: 700, y: 250 },
      metrics: {
        executionTime: '0.6s',
        memoryUsage: '120MB',
        cpuUsage: '18%'
      }
    }
  ];

  // 根据工作流类型获取对应的节点数据
  const getWorkflowNodes = (type: string) => {
    switch (type) {
      case 'automation-test':
        return automationTestNodes;
      case 'agent-design':
        return agentDesignNodes;
      default:
        return [];
    }
  };

  // 设置文档URL
  useEffect(() => {
    if (activeWorkflowType === 'automation-test') {
      setDocsUrl('https://github.com/yourusername/powerautomation/blob/main/frontend/src/docs/automation_test_workflow.md');
    } else if (activeWorkflowType === 'agent-design') {
      setDocsUrl('https://github.com/yourusername/powerautomation/blob/main/frontend/src/docs/agent_design_workflow.md');
    }
  }, [activeWorkflowType]);

  // 处理节点选择
  const handleNodeSelect = (nodeId: string) => {
    setSelectedNodeId(nodeId === selectedNodeId ? null : nodeId);
  };

  // 处理工作流类型切换
  const handleWorkflowTypeChange = (type: string) => {
    setActiveWorkflowType(type);
    setSelectedNodeId(null);
  };

  return (
    <div className="workflow-content">
      <h2 className="section-title">工作流视图</h2>
      
      <div className="workflow-tabs">
        <button 
          className={`workflow-tab ${activeTab === 'workflow' ? 'active' : ''}`}
          onClick={() => setActiveTab('workflow')}
        >
          工作流
        </button>
        <button 
          className={`workflow-tab ${activeTab === 'docs' ? 'active' : ''}`}
          onClick={() => setActiveTab('docs')}
        >
          文档
        </button>
      </div>
      
      {activeTab === 'workflow' ? (
        <>
          <div className="workflow-type-selector">
            <button 
              className={`workflow-type-btn ${activeWorkflowType === 'automation-test' ? 'active' : ''}`}
              onClick={() => handleWorkflowTypeChange('automation-test')}
            >
              自动化测试工作流
            </button>
            <button 
              className={`workflow-type-btn ${activeWorkflowType === 'agent-design' ? 'active' : ''}`}
              onClick={() => handleWorkflowTypeChange('agent-design')}
            >
              自动化智能体设计工作流
            </button>
          </div>
          
          <div className="workflow-visualizer">
            <N8nWorkflowVisualizer 
              nodes={getWorkflowNodes(activeWorkflowType)}
              selectedNodeId={selectedNodeId}
              onNodeSelect={handleNodeSelect}
            />
          </div>
          
          {selectedNodeId && (
            <div className="node-details">
              <h3>节点详情</h3>
              {getWorkflowNodes(activeWorkflowType).filter(node => node.id === selectedNodeId).map(node => (
                <div key={node.id} className="node-detail-card">
                  <div className="node-header">
                    <span className="node-name">{node.name}</span>
                    <span className={`node-status ${node.status}`}>
                      {node.status === 'success' ? '成功' : 
                       node.status === 'error' ? '错误' : 
                       node.status === 'warning' ? '警告' : '待定'}
                    </span>
                  </div>
                  <div className="node-description">{node.description}</div>
                  <div className="node-metrics">
                    <div className="metric">
                      <span className="metric-label">执行时间:</span>
                      <span className="metric-value">{node.metrics.executionTime}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">内存使用:</span>
                      <span className="metric-value">{node.metrics.memoryUsage}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">CPU使用率:</span>
                      <span className="metric-value">{node.metrics.cpuUsage}</span>
                    </div>
                  </div>
                  <div className="node-actions">
                    <button className="node-action-btn">查看源代码</button>
                    <button className="node-action-btn">查看日志</button>
                    {activeWorkflowType === 'automation-test' && (
                      <a 
                        href={`https://github.com/yourusername/powerautomation/blob/main/tests/${
                          node.id === 'integration-test' ? 'integration/component_interaction.test.js' :
                          node.id === 'e2e-test' ? 'e2e/user_workflow.spec.js' :
                          'visual/component_visual.spec.js'
                        }`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="github-link"
                      >
                        在GitHub上查看
                      </a>
                    )}
                    {activeWorkflowType === 'agent-design' && (
                      <a 
                        href={`https://github.com/yourusername/powerautomation/blob/main/agents/${
                          node.id === 'general-agent' ? 'general_agent/general_agent.py' :
                          node.id === 'mcp-coordinator' ? 'mcp/mcp_coordinator.py' :
                          node.id === 'mcp-planner' ? 'mcp/mcp_planner.py' :
                          node.id === 'thought-recorder' ? 'thought_recorder/thought_recorder.py' :
                          node.id === 'release-manager' ? 'release_manager/release_manager.py' :
                          'supermemory/supermemory.py'
                        }`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="github-link"
                      >
                        在GitHub上查看
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <div className="docs-content">
          <div className="docs-actions">
            {docsUrl && (
              <a 
                href={docsUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="docs-link"
              >
                在GitHub上查看完整文档
              </a>
            )}
          </div>
          <div className="docs-frame">
            <iframe 
              src={activeWorkflowType === 'automation-test' 
                ? '/src/docs/automation_test_workflow.md'
                : '/src/docs/agent_design_workflow.md'} 
              title="文档"
              className="docs-iframe"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default WorkflowContent;
