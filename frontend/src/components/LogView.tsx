import React, { useState, useEffect } from 'react';
import '../styles/LogView.css';

interface LogEntry {
  timestamp: string;
  level: 'info' | 'success' | 'warning' | 'error';
  message: string;
  nodeId?: string;
  details?: string;
}

interface MemoryStatus {
  status: 'success' | 'warning' | 'error';
  statusText: string;
  trigger: {
    name: string;
    status: 'active' | 'inactive';
  };
  agent: string;
  lastTriggered: string;
}

interface LogViewProps {
  agentType: string;
  selectedNodeId?: string;
  logs?: LogEntry[];
  memoryStatus?: MemoryStatus;
}

const LogView: React.FC<LogViewProps> = ({ 
  agentType, 
  selectedNodeId,
  logs = [],
  memoryStatus = {
    status: 'success',
    statusText: '完整记忆成功',
    trigger: {
      name: 'AGENT',
      status: 'active'
    },
    agent: '接收用户输入',
    lastTriggered: '2025-06-02 10:30'
  }
}) => {
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([]);
  const [defaultLogs] = useState<LogEntry[]>([
    {
      timestamp: '2025-06-02 10:30:00',
      level: 'info',
      message: '通用智能体已启动，等待用户输入'
    },
    {
      timestamp: '2025-06-02 10:30:05',
      level: 'info',
      message: '接收到用户输入，开始处理'
    },
    {
      timestamp: '2025-06-02 10:30:10',
      level: 'success',
      message: 'SuperMemory记忆检查完成，状态正常'
    },
    {
      timestamp: '2025-06-02 10:30:15',
      level: 'info',
      message: 'MCP协调器开始分配任务'
    },
    {
      timestamp: '2025-06-02 10:30:20',
      level: 'warning',
      message: '资源使用率接近阈值，考虑优化'
    }
  ]);

  // 当选中节点变化时，过滤日志
  useEffect(() => {
    if (selectedNodeId) {
      // 如果有选中节点，过滤出与该节点相关的日志
      const nodeRelatedLogs = [...logs, ...defaultLogs].filter(
        log => log.nodeId === selectedNodeId || !log.nodeId
      );
      setFilteredLogs(nodeRelatedLogs);
    } else {
      // 如果没有选中节点，显示所有日志
      setFilteredLogs([...logs, ...defaultLogs]);
    }
  }, [selectedNodeId, logs, defaultLogs]);

  return (
    <div className="log-view">
      <h2 className="section-title">日志视图</h2>
      
      {selectedNodeId && (
        <div className="selected-node-info">
          <span className="selected-node-label">当前选中节点:</span>
          <span className="selected-node-id">{selectedNodeId}</span>
        </div>
      )}
      
      <div className="log-content">
        <div className="log-section">
          <h3 className="log-section-title">记忆状态</h3>
          
          {/* SuperMemory.ai记忆状态卡片 */}
          <div className="memory-status-card">
            <div className="memory-status-header">
              <span className="memory-status-title">SuperMemory.ai 记忆状态</span>
              <span className={`memory-status-badge ${memoryStatus.status}`}>{memoryStatus.statusText}</span>
            </div>
            
            <div className="memory-status-content">
              <div className="memory-status-item">
                <span className="status-label">触发器:</span>
                <span className="status-value">{memoryStatus.trigger.name}</span>
                <span className={`status-badge ${memoryStatus.trigger.status}`}>
                  {memoryStatus.trigger.status === 'active' ? '活跃' : '非活跃'}
                </span>
              </div>
              <div className="memory-status-item">
                <span className="status-label">通用智能体:</span>
                <span className="status-value">{memoryStatus.agent}</span>
              </div>
              <div className="memory-status-item">
                <span className="status-label">上次触发:</span>
                <span className="status-value">{memoryStatus.lastTriggered}</span>
              </div>
            </div>
            
            <a href="https://supermemory.ai/" target="_blank" className="memory-link">查看完整记忆 →</a>
          </div>
        </div>
        
        <div className="log-section">
          <h3 className="log-section-title">系统日志</h3>
          <div className="log-entries">
            {filteredLogs.map((log, index) => (
              <div key={index} className={`log-entry ${log.nodeId === selectedNodeId ? 'highlighted' : ''}`}>
                <span className="log-timestamp">{log.timestamp}</span>
                <span className={`log-level ${log.level}`}>{log.level.toUpperCase()}</span>
                <span className="log-message">{log.message}</span>
                {log.details && (
                  <div className="log-details">
                    <pre>{log.details}</pre>
                  </div>
                )}
              </div>
            ))}
            {filteredLogs.length === 0 && (
              <div className="no-logs-message">
                没有与当前节点相关的日志记录
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogView;
