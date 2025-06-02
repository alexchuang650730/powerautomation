import React, { useState } from 'react';
import '../styles/WorkflowContent.css';
import N8nWorkflowVisualizer, { WorkflowNode, WorkflowConnection } from './N8nWorkflowVisualizer';
import IntegratedWorkflowView from './IntegratedWorkflowView';

interface WorkflowContentProps {}

const WorkflowContent: React.FC<WorkflowContentProps> = () => {
  const [activeWorkflow, setActiveWorkflow] = useState('automation-test');
  
  // 自动化测试工作流节点数据
  const automationTestNodes: WorkflowNode[] = [
    {
      id: 'unit-test',
      type: 'trigger',
      position: { x: 100, y: 100 },
      data: {
        name: '单元测试',
        description: '测试各组件的独立功能',
        status: '活跃',
        timestamp: '2025-06-02 10:30',
        type: 'test'
      }
    },
    {
      id: 'integration-test',
      type: 'action',
      position: { x: 100, y: 250 },
      data: {
        name: '集成测试',
        description: '测试组件间的交互',
        status: '已执行',
        timestamp: '2025-06-02 10:32',
        type: 'test'
      }
    },
    {
      id: 'e2e-test',
      type: 'action',
      position: { x: 100, y: 400 },
      data: {
        name: '端到端测试',
        description: '测试完整工作流程',
        status: '已执行',
        timestamp: '2025-06-02 10:33',
        type: 'test'
      }
    }
  ];

  // 自动化测试工作流连接数据
  const automationTestConnections: WorkflowConnection[] = [
    {
      id: 'conn1',
      source: 'unit-test',
      target: 'integration-test',
      label: '通过'
    },
    {
      id: 'conn2',
      source: 'integration-test',
      target: 'e2e-test',
      label: '通过'
    }
  ];
  
  // 自动化智能体设计工作流节点数据
  const agentDesignNodes: WorkflowNode[] = [
    {
      id: 'general-agent',
      type: 'trigger',
      position: { x: 100, y: 100 },
      data: {
        name: '通用智能体',
        description: '接收用户输入',
        status: '活跃',
        timestamp: '2025-06-02 10:30',
        type: 'agent'
      }
    },
    {
      id: 'mcp-coordinator',
      type: 'action',
      position: { x: 100, y: 250 },
      data: {
        name: 'MCP协调器',
        description: '协调各子系统工作',
        status: '已执行',
        timestamp: '2025-06-02 10:32',
        type: 'coordinator'
      }
    },
    {
      id: 'mcp-planner',
      type: 'action',
      position: { x: 400, y: 350 },
      data: {
        name: 'MCP规划器',
        description: '规划问题解决方案',
        status: '已执行',
        timestamp: '2025-06-02 10:33',
        type: 'planner'
      }
    },
    {
      id: 'thought-recorder',
      type: 'action',
      position: { x: 100, y: 350 },
      data: {
        name: '思维行为记录器',
        description: '记录任务进度和历史',
        status: '已执行',
        timestamp: '2025-06-02 10:34',
        type: 'recorder'
      }
    },
    {
      id: 'release-manager',
      type: 'action',
      position: { x: 700, y: 350 },
      data: {
        name: '发布管理器',
        description: '管理代码发布和部署',
        status: '已执行',
        timestamp: '2025-06-02 10:35',
        type: 'manager'
      }
    },
    {
      id: 'problem-solver',
      type: 'action',
      position: { x: 400, y: 500 },
      data: {
        name: '问题解决器',
        description: '解决具体问题',
        status: '已执行',
        timestamp: '2025-06-02 10:36',
        type: 'solver'
      }
    },
    {
      id: 'manus-im',
      type: 'action',
      position: { x: 400, y: 650 },
      data: {
        name: 'Manus.im',
        description: '执行最终问题解决',
        status: '已执行',
        timestamp: '2025-06-02 10:37',
        type: 'executor'
      }
    }
  ];

  // 自动化智能体设计工作流连接数据
  const agentDesignConnections: WorkflowConnection[] = [
    {
      id: 'conn1',
      source: 'general-agent',
      target: 'mcp-coordinator',
      label: '输入'
    },
    {
      id: 'conn2',
      source: 'mcp-coordinator',
      target: 'mcp-planner',
      label: '规划'
    },
    {
      id: 'conn3',
      source: 'mcp-coordinator',
      target: 'thought-recorder',
      label: '记录'
    },
    {
      id: 'conn4',
      source: 'mcp-coordinator',
      target: 'release-manager',
      label: '发布'
    },
    {
      id: 'conn5',
      source: 'mcp-planner',
      target: 'problem-solver',
      label: '执行'
    },
    {
      id: 'conn6',
      source: 'problem-solver',
      target: 'manus-im',
      label: '解决'
    }
  ];

  return (
    <div className="workflow-content">
      <h2 className="section-title">工作流节点及工作流</h2>
      
      <div className="workflow-tabs">
        <button 
          className={`workflow-tab ${activeWorkflow === 'automation-test' ? 'active' : ''}`}
          onClick={() => setActiveWorkflow('automation-test')}
        >
          自动化测试工作流
        </button>
        <button 
          className={`workflow-tab ${activeWorkflow === 'agent-design' ? 'active' : ''}`}
          onClick={() => setActiveWorkflow('agent-design')}
        >
          自动化智能体设计工作流
        </button>
      </div>
      
      {activeWorkflow === 'automation-test' && (
        <div className="workflow-details">
          <div className="workflow-description">
            <h3>自动化测试工作流 (预设)</h3>
            <p>该工作流包含三个主要测试阶段，确保系统各部分功能正常运行。</p>
            <ul>
              <li><strong>单元测试</strong>：测试各组件的独立功能</li>
              <li><strong>集成测试</strong>：测试组件间的交互</li>
              <li><strong>端到端测试</strong>：测试完整工作流程</li>
            </ul>
          </div>
          <IntegratedWorkflowView>
            <N8nWorkflowVisualizer nodes={automationTestNodes} connections={automationTestConnections} />
          </IntegratedWorkflowView>
        </div>
      )}
      
      {activeWorkflow === 'agent-design' && (
        <div className="workflow-details">
          <div className="workflow-description">
            <h3>自动化智能体设计工作流</h3>
            <p>该工作流展示了通用智能体如何通过多个子系统协同工作。</p>
            <div className="submodules">
              <div className="submodule">
                <h4>2.2.1 问题解决流程</h4>
                <p>通过general agent和mcpcoordinator传给mcpplanner和mcpbrainstorm，驱动agentproblemsovler将问题传递给manus.im</p>
              </div>
              <div className="submodule">
                <h4>2.2.2 思维行为记录</h4>
                <p>通过ThoughtActionRecorder记录：</p>
                <ul>
                  <li>任务进度</li>
                  <li>用户历史回复及分析</li>
                  <li>创建及更新、取代消除动作</li>
                  <li>更新以及完成的工作</li>
                </ul>
              </div>
              <div className="submodule">
                <h4>2.2.3 发布管理</h4>
                <p>通过ReleaseManager实现：</p>
                <ul>
                  <li>检查GitHub上是否有新的release</li>
                  <li>下载release代码到指定的本地路径</li>
                  <li>支持SSH密钥认证</li>
                  <li>提供代码上传功能，自动处理提交和推送</li>
                </ul>
              </div>
              <div className="submodule">
                <h4>2.2.4 测试与问题收集</h4>
                <p>通过TestAndIssueCollector执行视觉自动化测试，收集问题并更新README文件</p>
              </div>
            </div>
          </div>
          <IntegratedWorkflowView>
            <N8nWorkflowVisualizer nodes={agentDesignNodes} connections={agentDesignConnections} />
          </IntegratedWorkflowView>
        </div>
      )}
    </div>
  );
};

export default WorkflowContent;
