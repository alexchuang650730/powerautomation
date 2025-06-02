import React from 'react';
import '../styles/LogView.css';

interface LogViewProps {
  agentType: string;
}

const LogView: React.FC<LogViewProps> = ({ agentType }) => {
  return (
    <div className="log-view">
      <h2 className="section-title">日志视图</h2>
      
      <div className="log-content">
        <div className="log-section">
          <h3 className="log-section-title">记忆状态</h3>
          
          {/* SuperMemory.ai记忆状态卡片 */}
          <div className="memory-status-card">
            <div className="memory-status-header">
              <span className="memory-status-title">SuperMemory.ai 记忆状态</span>
              <span className="memory-status-badge success">完整记忆成功</span>
            </div>
            
            <div className="memory-status-content">
              <div className="memory-status-item">
                <span className="status-label">触发器:</span>
                <span className="status-value">AGENT</span>
                <span className="status-badge active">活跃</span>
              </div>
              <div className="memory-status-item">
                <span className="status-label">通用智能体:</span>
                <span className="status-value">接收用户输入</span>
              </div>
              <div className="memory-status-item">
                <span className="status-label">上次触发:</span>
                <span className="status-value">2025-06-02 10:30</span>
              </div>
            </div>
            
            <a href="https://supermemory.ai/" target="_blank" className="memory-link">查看完整记忆 →</a>
          </div>
        </div>
        
        <div className="log-section">
          <h3 className="log-section-title">系统日志</h3>
          <div className="log-entries">
            <div className="log-entry">
              <span className="log-timestamp">2025-06-02 10:30:00</span>
              <span className="log-level info">INFO</span>
              <span className="log-message">通用智能体已启动，等待用户输入</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">2025-06-02 10:30:05</span>
              <span className="log-level info">INFO</span>
              <span className="log-message">接收到用户输入，开始处理</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">2025-06-02 10:30:10</span>
              <span className="log-level success">SUCCESS</span>
              <span className="log-message">SuperMemory记忆检查完成，状态正常</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">2025-06-02 10:30:15</span>
              <span className="log-level info">INFO</span>
              <span className="log-message">MCP协调器开始分配任务</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">2025-06-02 10:30:20</span>
              <span className="log-level warning">WARNING</span>
              <span className="log-message">资源使用率接近阈值，考虑优化</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogView;
