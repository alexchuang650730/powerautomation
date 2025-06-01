import React, { useState, useEffect } from 'react';
import N8nWorkflowVisualizer from './N8nWorkflowVisualizer';
import '../styles/WorkflowIntegrationPanel.css';

// 集成面板属性接口
interface WorkflowIntegrationPanelProps {
  refreshInterval?: number;
}

const WorkflowIntegrationPanel: React.FC<WorkflowIntegrationPanelProps> = ({
  refreshInterval = 5000
}) => {
  const [workflowData, setWorkflowData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // 获取工作流数据
  const fetchWorkflowData = async () => {
    try {
      setLoading(true);
      
      // 实际项目中，这里应该是多个API调用的组合
      // 1. 获取AgentProblemSolver的工作节点数据
      // const problemSolverResponse = await fetch('/api/agent-problem-solver/web-data');
      // const problemSolverData = await problemSolverResponse.json();
      
      // 2. 获取ReleaseManager的数据
      // const releaseManagerResponse = await fetch('/api/release-manager/web-data');
      // const releaseManagerData = await releaseManagerResponse.json();
      
      // 模拟数据，实际项目中应替换为真实API调用
      const mockData = await getMockIntegratedData();
      
      // 处理数据，转换为工作流节点和连接
      const processedData = processWorkflowData(mockData);
      
      setWorkflowData(processedData);
      setError(null);
    } catch (err) {
      setError('获取工作流数据失败，请稍后重试');
      console.error('获取集成工作流数据失败:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // 模拟获取集成数据
  const getMockIntegratedData = (): Promise<any> => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          // AgentProblemSolver数据
          savepoints: [
            {
              id: 'sp_20250601121500',
              timestamp: '20250601121500',
              description: '初始版本',
              test_status: 'passed',
              deployment_status: 'success',
              project_hash: 'abc123',
              path: '/path/to/savepoint',
              created_at: '2025-06-01T12:15:00Z',
              tags: ['stable', 'release']
            },
            {
              id: 'sp_20250601131000',
              timestamp: '20250601131000',
              description: '修复UI布局问题',
              test_status: 'failed',
              deployment_status: 'pending',
              project_hash: 'def456',
              path: '/path/to/savepoint2',
              created_at: '2025-06-01T13:10:00Z',
              tags: ['bugfix']
            }
          ],
          work_nodes: [
            {
              id: 'node_20250601121500',
              savepoint_id: 'sp_20250601121500',
              type: '创建保存点',
              description: '初始版本',
              timestamp: '2025-06-01T12:15:00Z',
              status: 'success'
            },
            {
              id: 'node_20250601122000',
              savepoint_id: 'sp_20250601121500',
              type: '测试通过',
              description: '所有测试用例通过',
              timestamp: '2025-06-01T12:20:00Z',
              status: 'success'
            },
            {
              id: 'node_20250601123000',
              savepoint_id: 'sp_20250601121500',
              type: '部署成功',
              description: '部署到生产环境',
              timestamp: '2025-06-01T12:30:00Z',
              status: 'success'
            }
          ],
          rollback_history: [
            {
              id: 'rb_20250601133000',
              savepoint_id: 'sp_20250601121500',
              timestamp: '2025-06-01T13:30:00Z',
              is_auto: false,
              status: 'success',
              description: '回滚到保存点: 初始版本',
              pre_rollback_hash: 'def456',
              post_rollback_hash: 'abc123',
              hash_diff: true
            }
          ],
          
          // ReleaseManager数据
          releases: [
            {
              id: '12345',
              tag_name: 'v1.0.0',
              name: '初始版本',
              published_at: '2025-05-30T10:00:00Z',
              html_url: 'https://github.com/owner/repo/releases/tag/v1.0.0',
              downloaded: true,
              download_time: '2025-05-30T10:30:00Z',
              local_path: '/path/to/local/v1.0.0',
              extracted_path: '/path/to/local/v1.0.0/extracted'
            },
            {
              id: '12346',
              tag_name: 'v1.1.0',
              name: '功能更新',
              published_at: '2025-06-01T09:00:00Z',
              html_url: 'https://github.com/owner/repo/releases/tag/v1.1.0',
              downloaded: true,
              download_time: '2025-06-01T09:15:00Z',
              local_path: '/path/to/local/v1.1.0',
              extracted_path: '/path/to/local/v1.1.0/extracted'
            }
          ],
          deployments: [
            {
              id: 'deploy_20250530103000',
              release_id: '12345',
              tag_name: 'v1.0.0',
              target_path: '/path/to/deploy',
              deploy_time: '2025-05-30T10:30:00Z',
              status: 'success',
              savepoint_id: 'sp_20250530103000'
            },
            {
              id: 'deploy_20250601092000',
              release_id: '12346',
              tag_name: 'v1.1.0',
              target_path: '/path/to/deploy',
              deploy_time: '2025-06-01T09:20:00Z',
              status: 'failed',
              error: '部署过程中出现错误',
              savepoint_id: 'sp_20250601092000'
            }
          ]
        });
      }, 500);
    });
  };
  
  // 处理工作流数据，转换为节点和连接
  const processWorkflowData = (data: any) => {
    const workflowNodes = [];
    const workflowConnections = [];
    
    // 处理ReleaseManager的release数据
    if (data.releases) {
      for (const release of data.releases) {
        workflowNodes.push({
          id: `release_${release.id}`,
          type: '下载release',
          description: `下载release: ${release.tag_name}`,
          timestamp: release.download_time || release.published_at,
          status: release.downloaded ? 'success' : 'pending',
          data: { release_id: release.id }
        });
      }
    }
    
    // 处理ReleaseManager的deployment数据
    if (data.deployments) {
      for (const deployment of data.deployments) {
        workflowNodes.push({
          id: deployment.id,
          type: deployment.status === 'success' ? '部署成功' : '部署失败',
          description: `部署release${deployment.status === 'success' ? '' : '失败'}: ${deployment.tag_name}`,
          timestamp: deployment.deploy_time,
          status: deployment.status,
          data: { 
            release_id: deployment.release_id,
            error: deployment.error,
            savepoint_id: deployment.savepoint_id
          }
        });
        
        // 添加release到deployment的连接
        workflowConnections.push({
          source: `release_${deployment.release_id}`,
          target: deployment.id,
          type: deployment.status === 'success' ? 'success' : 'error'
        });
      }
    }
    
    // 处理AgentProblemSolver的savepoint数据
    if (data.savepoints) {
      for (const savepoint of data.savepoints) {
        workflowNodes.push({
          id: savepoint.id,
          type: '创建保存点',
          description: `创建保存点: ${savepoint.description}`,
          timestamp: savepoint.created_at,
          status: 'success',
          data: { savepoint_id: savepoint.id }
        });
        
        // 如果savepoint与deployment关联，添加连接
        for (const deployment of data.deployments || []) {
          if (deployment.savepoint_id === savepoint.id) {
            workflowConnections.push({
              source: deployment.id,
              target: savepoint.id,
              type: 'success'
            });
          }
        }
      }
    }
    
    // 处理AgentProblemSolver的work_nodes数据
    if (data.work_nodes) {
      for (const node of data.work_nodes) {
        // 避免重复添加已经处理过的节点
        if (!workflowNodes.some(n => n.id === node.id)) {
          workflowNodes.push({
            id: node.id,
            type: node.type,
            description: node.description,
            timestamp: node.timestamp,
            status: node.status,
            data: { savepoint_id: node.savepoint_id }
          });
        }
        
        // 添加savepoint到work_node的连接
        if (node.savepoint_id) {
          workflowConnections.push({
            source: node.savepoint_id,
            target: node.id,
            type: 'success'
          });
        }
      }
    }
    
    // 处理AgentProblemSolver的rollback_history数据
    if (data.rollback_history) {
      for (const rollback of data.rollback_history) {
        workflowNodes.push({
          id: rollback.id,
          type: '回滚操作',
          description: rollback.description,
          timestamp: rollback.timestamp,
          status: rollback.status,
          data: { 
            savepoint_id: rollback.savepoint_id,
            is_auto: rollback.is_auto
          }
        });
        
        // 添加savepoint到rollback的连接
        workflowConnections.push({
          source: rollback.savepoint_id,
          target: rollback.id,
          type: 'success'
        });
      }
    }
    
    return {
      workflowNodes,
      workflowConnections
    };
  };
  
  // 初始加载和定时刷新
  useEffect(() => {
    fetchWorkflowData();
    
    if (refreshInterval > 0) {
      const intervalId = setInterval(fetchWorkflowData, refreshInterval);
      return () => clearInterval(intervalId);
    }
  }, [refreshInterval]);
  
  if (loading && !workflowData) {
    return <div className="workflow-integration-loading">加载工作流数据...</div>;
  }
  
  if (error) {
    return <div className="workflow-integration-error">{error}</div>;
  }
  
  if (!workflowData) {
    return <div className="workflow-integration-empty">暂无工作流数据</div>;
  }
  
  return (
    <div className="workflow-integration-panel">
      <div className="workflow-integration-header">
        <h2>通用智能体工作流</h2>
        <div className="workflow-integration-stats">
          <div className="stat-item">
            <span className="stat-label">节点总数:</span>
            <span className="stat-value">{workflowData.workflowNodes.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">连接总数:</span>
            <span className="stat-value">{workflowData.workflowConnections.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">最后更新:</span>
            <span className="stat-value">{new Date().toLocaleString('zh-CN')}</span>
          </div>
        </div>
      </div>
      
      <div className="workflow-container">
        <N8nWorkflowVisualizer
          workflowNodes={workflowData.workflowNodes}
          workflowConnections={workflowData.workflowConnections}
          refreshInterval={0} // 由父组件控制刷新
          height="600px"
        />
      </div>
    </div>
  );
};

export default WorkflowIntegrationPanel;
