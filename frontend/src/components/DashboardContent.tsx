import React from 'react';
import '../styles/DashboardContent.css';

interface DashboardContentProps {
  agentType: string;
}

const DashboardContent: React.FC<DashboardContentProps> = ({ agentType }) => {
  // 根据不同智能体类型渲染不同内容
  const renderAgentSpecificContent = () => {
    switch (agentType) {
      case 'general':
        return (
          <>
            <div className="dashboard-section">
              <h3 className="subsection-title">通用智能体六大特性</h3>
              <div className="feature-cards">
                <div className="feature-card">
                  <div className="feature-icon">🌐</div>
                  <h4>1. 平台特性</h4>
                  <ul>
                    <li>多平台集成能力：支持与GitHub、CI/CD平台、本地开发环境的无缝集成</li>
                    <li>跨环境兼容性：在Windows、macOS和Linux环境下保持一致的功能表现</li>
                    <li>API接口标准化：提供统一的REST API接口，支持第三方系统调用</li>
                  </ul>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">🖥️</div>
                  <h4>2. UI布局特性</h4>
                  <ul>
                    <li>两栏式布局：左侧展示任务进度和ThoughtActionRecorder思考过程，右侧展示代码和画面回放</li>
                    <li>实时状态反馈：通过视觉元素直观展示测试状态和进度</li>
                    <li>响应式设计：自适应不同屏幕尺寸，确保在桌面和移动设备上的良好体验</li>
                    <li>主题定制：支持明暗主题切换和企业级视觉风格定制</li>
                  </ul>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">💬</div>
                  <h4>3. 提示词特性</h4>
                  <ul>
                    <li>上下文感知提示：根据测试阶段和问题类型生成针对性提示</li>
                    <li>多语言支持：支持中英文等多语言提示和报告生成</li>
                    <li>技术术语识别：准确识别并解释测试和开发领域的专业术语</li>
                  </ul>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">🧠</div>
                  <h4>4. 思维特性</h4>
                  <ul>
                    <li>测试策略规划：自动分析代码结构，制定最优测试策略</li>
                    <li>问题根因分析：通过调用Manus能力，深入分析测试失败原因</li>
                    <li>修复方案生成：基于历史数据和最佳实践，提供针对性修复建议</li>
                    <li>优先级排序：智能评估问题严重性，合理安排修复顺序</li>
                  </ul>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">📄</div>
                  <h4>5. 内容特性</h4>
                  <ul>
                    <li>测试报告生成：自动生成结构化、可视化的测试报告</li>
                    <li>GitHub集成：将测试结果自动提交到GitHub，支持Issue创建和更新</li>
                    <li>代码注释生成：为测试用例和修复代码生成清晰的注释</li>
                    <li>文档更新：自动更新README和相关文档，反映最新测试状态</li>
                  </ul>
                </div>
                
                <div className="feature-card">
                  <div className="feature-icon">💾</div>
                  <h4>6. 记忆特性</h4>
                  <ul>
                    <li>测试历史追踪：记录并分析历史测试结果，识别趋势和模式</li>
                    <li>知识库构建：积累常见问题和解决方案，形成项目专属知识库</li>
                    <li>ReleaseManager能力：监控GitHub release事件，自动下载代码到指定路径，支持SSH密钥认证，处理代码上传和推送</li>
                    <li>持续学习：通过每次测试和修复过程不断优化测试策略和问题解决方法</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div className="dashboard-section">
              <h3 className="subsection-title">通用智能体五大核心治理原则</h3>
              <div className="governance-cards">
                <div className="governance-card">
                  <h4>1. 结构保护原则</h4>
                  <p>所有扩展基于原有文件结构，未修改现有结构</p>
                </div>
                
                <div className="governance-card">
                  <h4>2. 兼容性原则</h4>
                  <p>新功能与现有功能保持向后兼容</p>
                </div>
                
                <div className="governance-card">
                  <h4>3. 空间利用原则</h4>
                  <p>UI扩展只在空白区域进行，不影响原有控件</p>
                </div>
                
                <div className="governance-card">
                  <h4>4. 模块化原则</h4>
                  <p>所有新功能作为独立模块添加，不修改现有代码逻辑</p>
                </div>
                
                <div className="governance-card">
                  <h4>5. 一致性原则</h4>
                  <p>保持与现有代码风格和架构的一致性</p>
                </div>
              </div>
            </div>
          </>
        );
      case 'code':
        return (
          <>
            <div className="dashboard-section">
              <h3 className="subsection-title">代码智能体特性</h3>
              <p className="placeholder-text">代码智能体的特性内容将在此显示</p>
            </div>
          </>
        );
      case 'ppt':
        return (
          <>
            <div className="dashboard-section">
              <h3 className="subsection-title">PPT智能体特性</h3>
              <p className="placeholder-text">PPT智能体的特性内容将在此显示</p>
            </div>
          </>
        );
      case 'web':
        return (
          <>
            <div className="dashboard-section">
              <h3 className="subsection-title">网页智能体特性</h3>
              <p className="placeholder-text">网页智能体的特性内容将在此显示</p>
            </div>
          </>
        );
      default:
        return (
          <div className="dashboard-section">
            <p className="placeholder-text">请选择智能体类型查看详细信息</p>
          </div>
        );
    }
  };

  return (
    <div className="dashboard-content">
      <h2 className="section-title">智能体能力与治理</h2>
      {renderAgentSpecificContent()}
    </div>
  );
};

export default DashboardContent;
