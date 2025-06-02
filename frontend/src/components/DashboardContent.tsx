import React from 'react';
import '../styles/DashboardContent.css';

interface DashboardContentProps {}

const DashboardContent: React.FC<DashboardContentProps> = () => {
  return (
    <div className="dashboard-content">
      <h2 className="section-title">智能体能力与治理</h2>
      
      <div className="dashboard-section">
        <h3 className="subsection-title">智能体六大特性</h3>
        <div className="feature-cards">
          <div className="feature-card">
            <div className="feature-icon">🔄</div>
            <h4>自动化测试工作流</h4>
            <ul>
              <li>单元测试：测试各组件的独立功能</li>
              <li>集成测试：测试组件间的交互</li>
              <li>端到端测试：测试完整工作流程</li>
            </ul>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🧠</div>
            <h4>自动化智能体设计工作流</h4>
            <p>通过general agent和mcpcoordinator驱动多个子系统协同工作</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔄</div>
            <h4>自进化(RL Factory能力对齐)</h4>
            <p>通过强化学习实现智能体能力的持续优化与对齐</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">💾</div>
            <h4>记忆(SuperMemory集成与治理机制)</h4>
            <p>实现智能体的长期记忆存储与高效检索能力</p>
          </div>
        </div>
      </div>
      
      <div className="dashboard-section">
        <h3 className="subsection-title">核心治理原则</h3>
        <div className="governance-cards">
          <div className="governance-card">
            <h4>分类存储</h4>
            <p>通过ThoughtActionRecorder实现：</p>
            <ul>
              <li>任务进度</li>
              <li>用户历史回复及分析</li>
              <li>创建及更新、取代消除动作</li>
              <li>更新以及完成的工作</li>
            </ul>
          </div>
          
          <div className="governance-card">
            <h4>知识管理</h4>
            <ul>
              <li>测试历史追踪：记录并分析历史测试结果，识别趋势和模式</li>
              <li>历史数据分析：分析历史测试数据，识别趋势和模式</li>
              <li>知识库构建：积累常见问题和解决方案，形成项目专属知识库</li>
              <li>知识图谱集成：构建测试知识图谱，支持复杂关系查询和推理</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div className="dashboard-section">
        <h3 className="subsection-title">智能体协作机制</h3>
        <div className="collaboration-diagram">
          <div className="diagram-node main-node">General Agent</div>
          <div className="diagram-arrow">↓</div>
          <div className="diagram-node">MCPCoordinator</div>
          <div className="diagram-branches">
            <div className="diagram-branch">
              <div className="diagram-arrow">↙</div>
              <div className="diagram-node">MCPPlanner</div>
            </div>
            <div className="diagram-branch">
              <div className="diagram-arrow">↓</div>
              <div className="diagram-node">ThoughtActionRecorder</div>
            </div>
            <div className="diagram-branch">
              <div className="diagram-arrow">↘</div>
              <div className="diagram-node">ReleaseManager</div>
            </div>
          </div>
          <div className="diagram-arrow">↓</div>
          <div className="diagram-node">AgentProblemSolver</div>
          <div className="diagram-arrow">↓</div>
          <div className="diagram-node">Manus.im</div>
        </div>
      </div>
    </div>
  );
};

export default DashboardContent;
