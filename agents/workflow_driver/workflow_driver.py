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
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# 导入核心Agent组件
from agents.general_agent.general_agent_features import get_instance as get_features
from development_tools.agent_problem_solver import AgentProblemSolver
from agents.release_manager.release_manager import ReleaseManager

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
                        savepoint_id = self.agent_problem_solver.create_savepoint(savepoint_description)
                        
                        self.update_node_status(savepoint_node_id, "success", {
                            "savepoint_id": savepoint_id,
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
                        rollback_result = self.agent_problem_solver.auto_rollback()
                        
                        if rollback_result["success"]:
                            self.update_node_status(rollback_node_id, "success", {
                                "savepoint_id": rollback_result["savepoint_id"]
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
                    f"下载{release_version}失败",
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
            self.workflow_status["current_node"] = None
            self.workflow_status["last_update_time"] = datetime.now().isoformat()
            
            # 触发工作流完成事件
            self.trigger_event("workflow_completed", {
                "workflow_data": self.get_workflow_data()
            })
            
            logger.info("GitHub Release工作流执行完成")
    
    def start_test_workflow(self, test_type: str, test_target: str):
        """
        启动测试工作流
        
        Args:
            test_type: 测试类型 (unit, integration, ui, performance)
            test_target: 测试目标
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
            "测试请求",
            f"启动{test_type}测试: {test_target}",
            {
                "test_type": test_type,
                "test_target": test_target
            }
        )
        
        # 更新触发器节点状态
        self.update_node_status(trigger_node_id, "success")
        
        # 启动工作流线程
        self.workflow_thread = threading.Thread(
            target=self._run_test_workflow,
            args=(trigger_node_id, test_type, test_target)
        )
        self.workflow_thread.daemon = True
        self.workflow_thread.start()
        
        logger.info(f"已启动测试工作流: {test_type} - {test_target}")
    
    def _run_test_workflow(self, trigger_node_id: str, test_type: str, test_target: str):
        """
        运行测试工作流
        
        Args:
            trigger_node_id: 触发器节点ID
            test_type: 测试类型
            test_target: 测试目标
        """
        try:
            # 1. 准备测试环境节点
            prepare_node_id = self.create_workflow_node(
                "action",
                "准备测试环境",
                f"准备{test_type}测试环境",
                {
                    "test_type": test_type,
                    "test_target": test_target
                }
            )
            self.create_workflow_connection(trigger_node_id, prepare_node_id)
            self.update_node_status(prepare_node_id, "running")
            
            # 模拟准备测试环境
            time.sleep(2)
            
            self.update_node_status(prepare_node_id, "success", {
                "environment": "test"
            })
            
            # 2. 运行测试节点
            test_node_id = self.create_workflow_node(
                "action",
                "运行测试",
                f"执行{test_type}测试: {test_target}",
                {
                    "test_type": test_type,
                    "test_target": test_target
                }
            )
            self.create_workflow_connection(prepare_node_id, test_node_id)
            self.update_node_status(test_node_id, "running")
            
            # 调用TestAndIssueCollector运行测试
            test_result = self._run_tests(test_target, test_type)
            
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
                            "test_type": test_type,
                            "test_target": test_target
                        }
                    )
                    self.create_workflow_connection(condition_node_id, savepoint_node_id, "true")
                    self.update_node_status(savepoint_node_id, "running")
                    
                    # 调用AgentProblemSolver创建保存点
                    savepoint_description = f"{test_type.capitalize()} 测试通过: {test_target}"
                    savepoint_id = self.agent_problem_solver.create_savepoint(savepoint_description)
                    
                    self.update_node_status(savepoint_node_id, "success", {
                        "savepoint_id": savepoint_id,
                        "description": savepoint_description
                    })
                    
                    # 5. 记录测试结果节点
                    record_node_id = self.create_workflow_node(
                        "action",
                        "记录测试结果",
                        "记录测试结果到ThoughtActionRecorder",
                        {
                            "test_type": test_type,
                            "test_target": test_target,
                            "pass_rate": test_result["pass_rate"]
                        }
                    )
                    self.create_workflow_connection(savepoint_node_id, record_node_id)
                    self.update_node_status(record_node_id, "running")
                    
                    # 调用ThoughtActionRecorder记录测试结果
                    record_result = self._record_test_result(test_type, test_target, test_result)
                    
                    self.update_node_status(record_node_id, "success", {
                        "record_id": record_result["record_id"]
                    })
                else:
                    # 测试未通过，创建问题分析节点
                    analysis_node_id = self.create_workflow_node(
                        "action",
                        "问题分析",
                        "分析测试失败原因",
                        {
                            "test_type": test_type,
                            "test_target": test_target,
                            "pass_rate": test_result["pass_rate"]
                        }
                    )
                    self.create_workflow_connection(condition_node_id, analysis_node_id, "false")
                    self.update_node_status(analysis_node_id, "running")
                    
                    # 调用AgentProblemSolver分析问题
                    analysis_result = self.agent_problem_solver.analyze_test_failures(test_result["failures"])
                    
                    self.update_node_status(analysis_node_id, "success", {
                        "root_causes": analysis_result["root_causes"],
                        "recommendations": analysis_result["recommendations"]
                    })
                    
                    # 创建GitHub Issue节点
                    issue_node_id = self.create_workflow_node(
                        "action",
                        "创建GitHub Issue",
                        "将测试失败记录到GitHub",
                        {
                            "test_type": test_type,
                            "test_target": test_target,
                            "pass_rate": test_result["pass_rate"]
                        }
                    )
                    self.create_workflow_connection(analysis_node_id, issue_node_id)
                    self.update_node_status(issue_node_id, "running")
                    
                    # 模拟创建GitHub Issue
                    time.sleep(1)
                    
                    self.update_node_status(issue_node_id, "success", {
                        "issue_number": f"#{int(time.time()) % 1000}",
                        "issue_url": f"https://github.com/example/repo/issues/{int(time.time()) % 1000}"
                    })
            else:
                self.update_node_status(test_node_id, "failed", {
                    "error": test_result["error"]
                })
                
                # 创建测试失败错误节点
                error_node_id = self.create_workflow_node(
                    "error",
                    "测试失败",
                    f"{test_type}测试执行失败",
                    {
                        "error": test_result["error"]
                    }
                )
                self.create_workflow_connection(test_node_id, error_node_id, "error")
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
            self.workflow_status["current_node"] = None
            self.workflow_status["last_update_time"] = datetime.now().isoformat()
            
            # 触发工作流完成事件
            self.trigger_event("workflow_completed", {
                "workflow_data": self.get_workflow_data()
            })
            
            logger.info("测试工作流执行完成")
    
    def start_rollback_workflow(self, savepoint_id: str = None, reason: str = None):
        """
        启动回滚工作流
        
        Args:
            savepoint_id: 保存点ID，如果为None则自动选择最近的稳定保存点
            reason: 回滚原因
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
            "回滚请求",
            f"启动版本回滚: {savepoint_id if savepoint_id else '自动选择'}",
            {
                "savepoint_id": savepoint_id,
                "reason": reason
            }
        )
        
        # 更新触发器节点状态
        self.update_node_status(trigger_node_id, "success")
        
        # 启动工作流线程
        self.workflow_thread = threading.Thread(
            target=self._run_rollback_workflow,
            args=(trigger_node_id, savepoint_id, reason)
        )
        self.workflow_thread.daemon = True
        self.workflow_thread.start()
        
        logger.info(f"已启动回滚工作流: {savepoint_id if savepoint_id else '自动选择'}")
    
    def _run_rollback_workflow(self, trigger_node_id: str, savepoint_id: str = None, reason: str = None):
        """
        运行回滚工作流
        
        Args:
            trigger_node_id: 触发器节点ID
            savepoint_id: 保存点ID
            reason: 回滚原因
        """
        try:
            if not savepoint_id:
                # 1. 查找保存点节点
                find_node_id = self.create_workflow_node(
                    "action",
                    "查找保存点",
                    "查找最近的稳定保存点",
                    {
                        "reason": reason
                    }
                )
                self.create_workflow_connection(trigger_node_id, find_node_id)
                self.update_node_status(find_node_id, "running")
                
                # 调用AgentProblemSolver查找保存点
                savepoints = self.agent_problem_solver.list_savepoints()
                
                if savepoints and len(savepoints) > 0:
                    # 选择最近的保存点
                    selected_savepoint = savepoints[0]
                    savepoint_id = selected_savepoint["id"]
                    
                    self.update_node_status(find_node_id, "success", {
                        "savepoint_id": savepoint_id,
                        "savepoint_description": selected_savepoint["description"]
                    })
                else:
                    self.update_node_status(find_node_id, "failed", {
                        "error": "未找到可用的保存点"
                    })
                    
                    # 创建查找失败错误节点
                    error_node_id = self.create_workflow_node(
                        "error",
                        "查找失败",
                        "未找到可用的保存点",
                        {
                            "error": "未找到可用的保存点"
                        }
                    )
                    self.create_workflow_connection(find_node_id, error_node_id, "error")
                    self.update_node_status(error_node_id, "failed")
                    return
            
            # 2. 执行回滚节点
            rollback_node_id = self.create_workflow_node(
                "action",
                "执行回滚",
                f"回滚到保存点: {savepoint_id}",
                {
                    "savepoint_id": savepoint_id,
                    "reason": reason
                }
            )
            
            if not savepoint_id:
                self.create_workflow_connection(find_node_id, rollback_node_id)
            else:
                self.create_workflow_connection(trigger_node_id, rollback_node_id)
                
            self.update_node_status(rollback_node_id, "running")
            
            # 调用AgentProblemSolver执行回滚
            rollback_result = self.agent_problem_solver.rollback_to_savepoint(savepoint_id)
            
            if rollback_result["success"]:
                self.update_node_status(rollback_node_id, "success", {
                    "rollback_time": datetime.now().isoformat()
                })
                
                # 3. 验证回滚节点
                verify_node_id = self.create_workflow_node(
                    "action",
                    "验证回滚",
                    "验证回滚结果",
                    {
                        "savepoint_id": savepoint_id
                    }
                )
                self.create_workflow_connection(rollback_node_id, verify_node_id)
                self.update_node_status(verify_node_id, "running")
                
                # 调用AgentProblemSolver验证回滚
                verify_result = self.agent_problem_solver.verify_rollback(savepoint_id)
                
                if verify_result["success"]:
                    self.update_node_status(verify_node_id, "success", {
                        "verification_result": verify_result["result"]
                    })
                    
                    # 4. 记录回滚结果节点
                    record_node_id = self.create_workflow_node(
                        "action",
                        "记录回滚结果",
                        "记录回滚结果到ThoughtActionRecorder",
                        {
                            "savepoint_id": savepoint_id,
                            "reason": reason
                        }
                    )
                    self.create_workflow_connection(verify_node_id, record_node_id)
                    self.update_node_status(record_node_id, "running")
                    
                    # 调用ThoughtActionRecorder记录回滚结果
                    record_result = self._record_rollback(savepoint_id, reason, rollback_result)
                    
                    self.update_node_status(record_node_id, "success", {
                        "record_id": record_result["record_id"]
                    })
                else:
                    self.update_node_status(verify_node_id, "failed", {
                        "error": verify_result["error"]
                    })
                    
                    # 创建验证失败错误节点
                    error_node_id = self.create_workflow_node(
                        "error",
                        "验证失败",
                        "回滚验证失败",
                        {
                            "error": verify_result["error"]
                        }
                    )
                    self.create_workflow_connection(verify_node_id, error_node_id, "error")
                    self.update_node_status(error_node_id, "failed")
            else:
                self.update_node_status(rollback_node_id, "failed", {
                    "error": rollback_result["error"]
                })
                
                # 创建回滚失败错误节点
                error_node_id = self.create_workflow_node(
                    "error",
                    "回滚失败",
                    f"回滚到保存点 {savepoint_id} 失败",
                    {
                        "error": rollback_result["error"]
                    }
                )
                self.create_workflow_connection(rollback_node_id, error_node_id, "error")
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
            self.workflow_status["current_node"] = None
            self.workflow_status["last_update_time"] = datetime.now().isoformat()
            
            # 触发工作流完成事件
            self.trigger_event("workflow_completed", {
                "workflow_data": self.get_workflow_data()
            })
            
            logger.info("回滚工作流执行完成")
    
    def _run_tests(self, target: str, test_type: str = "all") -> Dict[str, Any]:
        """
        运行测试
        
        Args:
            target: 测试目标
            test_type: 测试类型
            
        Returns:
            测试结果
        """
        # 模拟测试执行
        logger.info(f"执行测试: {test_type} - {target}")
        time.sleep(3)
        
        # 模拟测试结果
        if test_type == "unit":
            return {
                "success": True,
                "test_count": 50,
                "pass_count": 48,
                "pass_rate": 96.0,
                "failures": [
                    {
                        "test_name": "test_edge_case_1",
                        "message": "Expected value not equal to actual value"
                    },
                    {
                        "test_name": "test_timeout_handling",
                        "message": "Test timed out after 5 seconds"
                    }
                ]
            }
        elif test_type == "integration":
            return {
                "success": True,
                "test_count": 30,
                "pass_count": 28,
                "pass_rate": 93.3,
                "failures": [
                    {
                        "test_name": "test_api_response",
                        "message": "API returned unexpected status code"
                    },
                    {
                        "test_name": "test_database_connection",
                        "message": "Failed to connect to database"
                    }
                ]
            }
        elif test_type == "ui":
            return {
                "success": True,
                "test_count": 20,
                "pass_count": 19,
                "pass_rate": 95.0,
                "failures": [
                    {
                        "test_name": "test_responsive_layout",
                        "message": "Element not visible on mobile viewport"
                    }
                ]
            }
        elif test_type == "performance":
            return {
                "success": True,
                "test_count": 10,
                "pass_count": 10,
                "pass_rate": 100.0,
                "failures": []
            }
        else:
            return {
                "success": True,
                "test_count": 110,
                "pass_count": 105,
                "pass_rate": 95.5,
                "failures": [
                    {
                        "test_name": "test_edge_case_1",
                        "message": "Expected value not equal to actual value"
                    },
                    {
                        "test_name": "test_timeout_handling",
                        "message": "Test timed out after 5 seconds"
                    },
                    {
                        "test_name": "test_api_response",
                        "message": "API returned unexpected status code"
                    },
                    {
                        "test_name": "test_database_connection",
                        "message": "Failed to connect to database"
                    },
                    {
                        "test_name": "test_responsive_layout",
                        "message": "Element not visible on mobile viewport"
                    }
                ]
            }
    
    def _record_test_result(self, test_type: str, test_target: str, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录测试结果
        
        Args:
            test_type: 测试类型
            test_target: 测试目标
            test_result: 测试结果
            
        Returns:
            记录结果
        """
        # 模拟记录测试结果
        logger.info(f"记录测试结果: {test_type} - {test_target}")
        time.sleep(1)
        
        return {
            "success": True,
            "record_id": f"record_{int(time.time())}"
        }
    
    def _record_deployment(self, release_version: str, deploy_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录部署结果
        
        Args:
            release_version: 版本号
            deploy_result: 部署结果
            
        Returns:
            记录结果
        """
        # 模拟记录部署结果
        logger.info(f"记录部署结果: {release_version}")
        time.sleep(1)
        
        return {
            "success": True,
            "record_id": f"record_{int(time.time())}"
        }
    
    def _record_rollback(self, savepoint_id: str, reason: str, rollback_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录回滚结果
        
        Args:
            savepoint_id: 保存点ID
            reason: 回滚原因
            rollback_result: 回滚结果
            
        Returns:
            记录结果
        """
        # 模拟记录回滚结果
        logger.info(f"记录回滚结果: {savepoint_id}")
        time.sleep(1)
        
        return {
            "success": True,
            "record_id": f"record_{int(time.time())}"
        }


# 单例模式，确保全局只有一个实例
_instance = None

def get_instance(project_root: str = None):
    """获取WorkflowDriver的单例实例"""
    global _instance
    if _instance is None:
        if project_root is None:
            project_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        _instance = WorkflowDriver(project_root)
    return _instance


if __name__ == "__main__":
    # 测试工作流驱动器
    driver = get_instance()
    
    # 注册事件监听器
    def on_node_created(event_data):
        print(f"节点创建事件: {event_data['node']['id']} - {event_data['node']['name']}")
    
    def on_node_updated(event_data):
        print(f"节点更新事件: {event_data['node']['id']} - {event_data['node']['status']}")
    
    def on_workflow_completed(event_data):
        print(f"工作流完成事件: {len(event_data['workflow_data']['nodes'])} 个节点")
    
    driver.register_event_listener("node_created", on_node_created)
    driver.register_event_listener("node_updated", on_node_updated)
    driver.register_event_listener("workflow_completed", on_workflow_completed)
    
    # 启动测试工作流
    driver.start_test_workflow("unit", "src/main.py")
    
    # 等待工作流完成
    while driver.workflow_status["is_running"]:
        time.sleep(1)
    
    print("工作流执行完成")
