"""
工作流驱动器 - 主动驱动核心Agent组件
版本: 1.0.0
更新日期: 2025-06-01
"""

import os
import sys
import json
import time
import logging
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Callable

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 导入核心Agent组件
from agents.general_agent.general_agent_features import get_instance as get_features
from development_tools.agent_problem_solver import AgentProblemSolver
from development_tools.release_manager import ReleaseManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("workflow_driver.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("WorkflowDriver")

class WorkflowDriver:
    """
    工作流驱动器类
    负责主动驱动ReleaseManager、TestAndIssueCollector、ThoughtActionRecorder、agentProblemSolver等核心组件
    """
    
    def __init__(self, project_root: str):
        """
        初始化工作流驱动器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = project_root
        self.features = get_features()
        
        # 初始化核心组件
        self.agent_problem_solver = AgentProblemSolver(project_root)
        self.release_manager = ReleaseManager(project_root)
        
        # 初始化工作流节点和连接
        self.workflow_nodes = []
        self.workflow_connections = []
        
        # 初始化事件监听器
        self.event_listeners = {}
        
        # 初始化工作流状态
        self.workflow_status = {
            "is_running": False,
            "current_node": None,
            "start_time": None,
            "last_update_time": None
        }
        
        # 初始化工作流线程
        self.workflow_thread = None
        
        logger.info(f"WorkflowDriver初始化完成，项目根目录: {project_root}")
    
    def register_event_listener(self, event_type: str, callback: Callable):
        """
        注册事件监听器
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        
        self.event_listeners[event_type].append(callback)
        logger.info(f"已注册事件监听器: {event_type}")
    
    def trigger_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        触发事件
        
        Args:
            event_type: 事件类型
            event_data: 事件数据
        """
        if event_type in self.event_listeners:
            for callback in self.event_listeners[event_type]:
                try:
                    callback(event_data)
                except Exception as e:
                    logger.error(f"事件处理异常: {str(e)}")
        
        logger.info(f"已触发事件: {event_type}")
    
    def create_workflow_node(self, node_type: str, name: str, description: str, data: Dict[str, Any] = None) -> str:
        """
        创建工作流节点
        
        Args:
            node_type: 节点类型 (trigger, action, condition, error)
            name: 节点名称
            description: 节点描述
            data: 节点数据
            
        Returns:
            节点ID
        """
        node_id = f"node_{len(self.workflow_nodes) + 1}"
        timestamp = datetime.now().isoformat()
        
        node = {
            "id": node_id,
            "type": node_type,
            "name": name,
            "description": description,
            "timestamp": timestamp,
            "status": "pending",
            "data": data or {}
        }
        
        self.workflow_nodes.append(node)
        
        # 触发节点创建事件
        self.trigger_event("node_created", {"node": node})
        
        logger.info(f"已创建工作流节点: {node_id} ({name})")
        return node_id
    
    def create_workflow_connection(self, source_id: str, target_id: str, connection_type: str = "success") -> str:
        """
        创建工作流连接
        
        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            connection_type: 连接类型 (success, error, conditional)
            
        Returns:
            连接ID
        """
        connection_id = f"conn_{len(self.workflow_connections) + 1}"
        
        connection = {
            "id": connection_id,
            "source": source_id,
            "target": target_id,
            "type": connection_type
        }
        
        self.workflow_connections.append(connection)
        
        # 触发连接创建事件
        self.trigger_event("connection_created", {"connection": connection})
        
        logger.info(f"已创建工作流连接: {connection_id} ({source_id} -> {target_id})")
        return connection_id
    
    def update_node_status(self, node_id: str, status: str, data: Dict[str, Any] = None):
        """
        更新节点状态
        
        Args:
            node_id: 节点ID
            status: 节点状态 (pending, running, success, failed)
            data: 节点数据更新
        """
        for node in self.workflow_nodes:
            if node["id"] == node_id:
                node["status"] = status
                node["last_update_time"] = datetime.now().isoformat()
                
                if data:
                    node["data"].update(data)
                
                # 触发节点更新事件
                self.trigger_event("node_updated", {"node": node})
                
                logger.info(f"已更新节点状态: {node_id} -> {status}")
                
                # 更新工作流状态
                if status == "running":
                    self.workflow_status["current_node"] = node_id
                
                return
        
        logger.warning(f"未找到节点: {node_id}")
    
    def get_workflow_data(self) -> Dict[str, Any]:
        """
        获取工作流数据
        
        Returns:
            工作流数据
        """
        return {
            "nodes": self.workflow_nodes,
            "connections": self.workflow_connections,
            "status": self.workflow_status
        }
    
    def start_github_release_workflow(self, release_version: str, release_url: str):
        """
        启动GitHub Release工作流
        
        Args:
            release_version: 版本号
            release_url: 版本URL
        """
        if self.workflow_status["is_running"]:
            logger.warning("工作流已在运行中，无法启动新工作流")
            return
        
        # 更新工作流状态
        self.workflow_status["is_running"] = True
        self.workflow_status["start_time"] = datetime.now().isoformat()
        self.workflow_status["last_update_time"] = datetime.now().isoformat()
        
        # 创建触发器节点
        trigger_node_id = self.create_workflow_node(
            "trigger",
            "GitHub Release",
            f"检测到新版本: {release_version}",
            {
                "release_version": release_version,
                "release_url": release_url
            }
        )
        
        # 更新触发器节点状态
        self.update_node_status(trigger_node_id, "success")
        
        # 启动工作流线程
        self.workflow_thread = threading.Thread(
            target=self._run_github_release_workflow,
            args=(trigger_node_id, release_version, release_url)
        )
        self.workflow_thread.daemon = True
        self.workflow_thread.start()
        
        logger.info(f"已启动GitHub Release工作流: {release_version}")
    
    def _run_github_release_workflow(self, trigger_node_id: str, release_version: str, release_url: str):
        """
        运行GitHub Release工作流
        
        Args:
            trigger_node_id: 触发器节点ID
            release_version: 版本号
            release_url: 版本URL
        """
        try:
            # 1. 下载代码节点
            download_node_id = self.create_workflow_node(
                "action",
                "下载代码",
                f"下载{release_version}代码到本地",
                {
                    "release_version": release_version,
                    "release_url": release_url
                }
            )
            self.create_workflow_connection(trigger_node_id, download_node_id)
            self.update_node_status(download_node_id, "running")
            
            # 调用ReleaseManager下载代码
            download_result = self.release_manager.download_release(release_url)
            
            if download_result["success"]:
                self.update_node_status(download_node_id, "success", {
                    "local_path": download_result["local_path"],
                    "file_count": download_result["file_count"]
                })
                
                local_path = download_result["local_path"]
                
                # 2. 运行测试节点
                test_node_id = self.create_workflow_node(
                    "action",
                    "运行测试",
                    "执行自动化测试",
                    {
                        "release_version": release_version
                    }
                )
                self.create_workflow_connection(download_node_id, test_node_id)
                self.update_node_status(test_node_id, "running")
                
                # 调用TestAndIssueCollector运行测试
                test_result = self._run_tests(local_path)
                
                if test_result["success"]:
                    self.update_node_status(test_node_id, "success", {
                        "test_count": test_result["test_count"],
                        "pass_rate": test_result["pass_rate"]
                    })
                    
                    # 3. 测试通过条件节点
                    condition_node_id = self.create_workflow_node(
                        "condition",
                        "测试通过?",
                        "检查测试结果",
                        {
                            "condition": "pass_rate >= 95.0",
                            "result": test_result["pass_rate"] >= 95.0
                        }
                    )
                    self.create_workflow_connection(test_node_id, condition_node_id)
                    self.update_node_status(condition_node_id, "success")
                    
                    if test_result["pass_rate"] >= 95.0:
                        # 4. 创建保存点节点
                        savepoint_node_id = self.create_workflow_node(
                            "action",
                            "创建保存点",
                            "创建代码保存点",
                            {
                                "release_version": release_version
                            }
                        )
                        self.create_workflow_connection(condition_node_id, savepoint_node_id, "true")
                        self.update_node_status(savepoint_node_id, "running")
                        
                        # 调用AgentProblemSolver创建保存点
                        savepoint_description = f"Release {release_version} 测试通过"
                        savepoint_result = self.agent_problem_solver.create_savepoint(savepoint_description)
                        
                        self.update_node_status(savepoint_node_id, "success", {
                            "savepoint_id": savepoint_result["id"],
                            "description": savepoint_description
                        })
                        
                        # 5. 部署代码节点
                        deploy_node_id = self.create_workflow_node(
                            "action",
                            "部署代码",
                            "部署到生产环境",
                            {
                                "release_version": release_version
                            }
                        )
                        self.create_workflow_connection(savepoint_node_id, deploy_node_id)
                        self.update_node_status(deploy_node_id, "running")
                        
                        # 调用ReleaseManager部署代码
                        deploy_result = self.release_manager.deploy_to_production(local_path)
                        
                        if deploy_result["success"]:
                            self.update_node_status(deploy_node_id, "success", {
                                "environment": "production",
                                "deploy_id": deploy_result["deploy_id"]
                            })
                            
                            # 6. 记录部署结果节点
                            record_node_id = self.create_workflow_node(
                                "action",
                                "记录部署结果",
                                "记录部署结果到ThoughtActionRecorder",
                                {
                                    "release_version": release_version,
                                    "deploy_id": deploy_result["deploy_id"]
                                }
                            )
                            self.create_workflow_connection(deploy_node_id, record_node_id)
                            self.update_node_status(record_node_id, "running")
                            
                            # 调用ThoughtActionRecorder记录部署结果
                            record_result = self._record_deployment(release_version, deploy_result)
                            
                            self.update_node_status(record_node_id, "success", {
                                "record_id": record_result["record_id"]
                            })
                        else:
                            self.update_node_status(deploy_node_id, "failed", {
                                "error": deploy_result["error"]
                            })
                            
                            # 创建部署失败错误节点
                            error_node_id = self.create_workflow_node(
                                "error",
                                "部署失败",
                                f"部署{release_version}失败",
                                {
                                    "error": deploy_result["error"]
                                }
                            )
                            self.create_workflow_connection(deploy_node_id, error_node_id, "error")
                            self.update_node_status(error_node_id, "failed")
                    else:
                        # 测试未通过，创建回滚节点
                        rollback_node_id = self.create_workflow_node(
                            "action",
                            "回滚版本",
                            "回滚到上一个稳定版本",
                            {
                                "reason": f"测试通过率低于阈值: {test_result['pass_rate']}%"
                            }
                        )
                        self.create_workflow_connection(condition_node_id, rollback_node_id, "false")
                        self.update_node_status(rollback_node_id, "running")
                        
                        # 调用AgentProblemSolver执行回滚
                        rollback_result = self.agent_problem_solver.rollback_to_savepoint()
                        
                        if rollback_result["status"] == "success":
                            self.update_node_status(rollback_node_id, "success", {
                                "savepoint_id": rollback_result["savepoint"]["id"]
                            })
                        else:
                            self.update_node_status(rollback_node_id, "failed", {
                                "error": rollback_result["error"]
                            })
                else:
                    self.update_node_status(test_node_id, "failed", {
                        "error": test_result["error"]
                    })
                    
                    # 创建测试失败错误节点
                    error_node_id = self.create_workflow_node(
                        "error",
                        "测试失败",
                        "自动化测试执行失败",
                        {
                            "error": test_result["error"]
                        }
                    )
                    self.create_workflow_connection(test_node_id, error_node_id, "error")
                    self.update_node_status(error_node_id, "failed")
            else:
                self.update_node_status(download_node_id, "failed", {
                    "error": download_result["error"]
                })
                
                # 创建下载失败错误节点
                error_node_id = self.create_workflow_node(
                    "error",
                    "下载失败",
                    f"下载{release_version}代码失败",
                    {
                        "error": download_result["error"]
                    }
                )
                self.create_workflow_connection(download_node_id, error_node_id, "error")
                self.update_node_status(error_node_id, "failed")
        except Exception as e:
            logger.error(f"工作流执行异常: {str(e)}")
            
            # 创建工作流异常错误节点
            error_node_id = self.create_workflow_node(
                "error",
                "工作流异常",
                "工作流执行过程中发生异常",
                {
                    "error": str(e)
                }
            )
            self.update_node_status(error_node_id, "failed")
        finally:
            # 更新工作流状态
            self.workflow_status["is_running"] = False
            self.workflow_status["last_update_time"] = datetime.now().isoformat()
            
            logger.info("工作流执行完成")
    
    def _run_tests(self, local_path: str) -> Dict[str, Any]:
        """
        运行测试（模拟）
        
        Args:
            local_path: 本地代码路径
            
        Returns:
            测试结果
        """
        logger.info(f"运行测试: {local_path}")
        
        # 模拟测试执行
        time.sleep(2)
        
        # 模拟测试结果
        return {
            "success": True,
            "test_count": 120,
            "pass_count": 115,
            "fail_count": 5,
            "pass_rate": 95.8
        }
    
    def _record_deployment(self, release_version: str, deploy_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录部署结果（模拟）
        
        Args:
            release_version: 版本号
            deploy_result: 部署结果
            
        Returns:
            记录结果
        """
        logger.info(f"记录部署结果: {release_version}")
        
        # 模拟记录部署结果
        time.sleep(1)
        
        # 模拟记录结果
        return {
            "success": True,
            "record_id": f"record_{int(time.time())}"
        }
    
    def stop_workflow(self):
        """
        停止工作流
        """
        if not self.workflow_status["is_running"]:
            logger.warning("工作流未在运行中")
            return
        
        # 更新工作流状态
        self.workflow_status["is_running"] = False
        self.workflow_status["last_update_time"] = datetime.now().isoformat()
        
        logger.info("工作流已停止")


# 工厂函数，获取WorkflowDriver实例
_instance = None

def get_instance(project_root: str = None) -> WorkflowDriver:
    """
    获取WorkflowDriver实例（单例模式）
    
    Args:
        project_root: 项目根目录路径，仅在首次调用时需要提供
        
    Returns:
        WorkflowDriver实例
    """
    global _instance
    
    if _instance is None:
        if project_root is None:
            raise ValueError("首次调用必须提供project_root参数")
        
        _instance = WorkflowDriver(project_root)
    
    return _instance


# 使用示例
if __name__ == "__main__":
    # 获取WorkflowDriver实例
    driver = get_instance("/path/to/project")
    
    # 启动GitHub Release工作流
    driver.start_github_release_workflow("v1.0.0", "https://github.com/example/repo/releases/tag/v1.0.0")
    
    # 等待工作流完成
    while driver.workflow_status["is_running"]:
        time.sleep(1)
    
    # 获取工作流数据
    workflow_data = driver.get_workflow_data()
    print(f"工作流节点数: {len(workflow_data['nodes'])}")
    print(f"工作流连接数: {len(workflow_data['connections'])}")
