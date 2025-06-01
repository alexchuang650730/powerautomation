"""
MCP适配器模块 - MCPAdapter

提供统一的接口，支持通过mcpcoordinator/mcpbrain/mcpplanner间接调用各测试与问题定位工具
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional, Union

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mcp_adapter.log")
    ]
)
logger = logging.getLogger("MCPAdapter")

# 尝试导入MCP组件
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp'))
    from mcp_central_coordinator import MCPCentralCoordinator
    from mcp_planner import MCPPlanner
    from mcp_brainstorm import MCPBrainstorm
    logger.info("成功导入MCP组件")
    MCP_AVAILABLE = True
except ImportError as e:
    logger.error(f"无法导入MCP组件: {str(e)}")
    MCP_AVAILABLE = False


class MCPAdapter:
    """
    MCP适配器
    
    提供统一的接口，支持通过mcpcoordinator/mcpbrain/mcpplanner间接调用各测试与问题定位工具
    """
    
    def __init__(self):
        """初始化MCP适配器"""
        self.coordinator = None
        self.planner = None
        self.brainstorm = None
        
        # 初始化MCP组件
        self._initialize_mcp_components()
        
        logger.info("MCP适配器初始化完成")
    
    def _initialize_mcp_components(self) -> None:
        """初始化MCP组件"""
        if MCP_AVAILABLE:
            try:
                self.coordinator = MCPCentralCoordinator()
                self.planner = MCPPlanner()
                self.brainstorm = MCPBrainstorm()
                logger.info("MCP组件初始化成功")
            except Exception as e:
                logger.error(f"MCP组件初始化失败: {str(e)}")
        else:
            logger.warning("MCP组件不可用，将使用模拟实现")
    
    def is_mcp_available(self) -> bool:
        """
        检查MCP组件是否可用
        
        Returns:
            MCP组件是否可用
        """
        return MCP_AVAILABLE and self.coordinator is not None
    
    def execute_tool(self, tool_name: str, method_name: str = "execute", **parameters) -> Dict[str, Any]:
        """
        执行工具方法
        
        Args:
            tool_name: 工具名称
            method_name: 方法名称
            **parameters: 方法参数
            
        Returns:
            执行结果
        """
        logger.info(f"执行工具: {tool_name}.{method_name}")
        
        # 通过MCP协调器执行
        if self.is_mcp_available():
            try:
                result = self.coordinator.execute_tool(tool_name, method_name, **parameters)
                logger.info(f"通过MCP协调器执行工具成功: {tool_name}.{method_name}")
                return result
            except Exception as e:
                logger.error(f"通过MCP协调器执行工具失败: {str(e)}")
                # 如果通过协调器执行失败，尝试直接执行
                return self._direct_execute_tool(tool_name, method_name, **parameters)
        else:
            # 如果MCP组件不可用，直接执行
            return self._direct_execute_tool(tool_name, method_name, **parameters)
    
    def _direct_execute_tool(self, tool_name: str, method_name: str, **parameters) -> Dict[str, Any]:
        """
        直接执行工具方法（不通过MCP协调器）
        
        Args:
            tool_name: 工具名称
            method_name: 方法名称
            **parameters: 方法参数
            
        Returns:
            执行结果
        """
        logger.info(f"直接执行工具: {tool_name}.{method_name}")
        
        try:
            # 导入工具模块
            module_path = f"powerautomation_integration.development_tools.{tool_name}"
            module = __import__(module_path, fromlist=[tool_name])
            
            # 获取工具类
            tool_class = getattr(module, tool_name)
            
            # 实例化工具
            tool_instance = tool_class()
            
            # 获取方法
            method = getattr(tool_instance, method_name)
            
            # 执行方法
            result = method(**parameters)
            
            logger.info(f"直接执行工具成功: {tool_name}.{method_name}")
            return {"status": "success", "result": result}
        
        except Exception as e:
            logger.error(f"直接执行工具失败: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def run_test(self, test_type: str, test_parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        运行测试
        
        Args:
            test_type: 测试类型
            test_parameters: 测试参数
            
        Returns:
            测试结果
        """
        logger.info(f"运行测试: {test_type}")
        
        if test_parameters is None:
            test_parameters = {}
        
        # 通过MCP协调器运行测试
        if self.is_mcp_available():
            try:
                # 使用run_e2e_test方法
                result = self.coordinator.run_e2e_test(test_type, test_parameters)
                logger.info(f"通过MCP协调器运行测试成功: {test_type}")
                return result
            except Exception as e:
                logger.error(f"通过MCP协调器运行测试失败: {str(e)}")
                # 如果通过协调器运行失败，尝试直接运行
                return self._direct_run_test(test_type, test_parameters)
        else:
            # 如果MCP组件不可用，直接运行测试
            return self._direct_run_test(test_type, test_parameters)
    
    def _direct_run_test(self, test_type: str, test_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        直接运行测试（不通过MCP协调器）
        
        Args:
            test_type: 测试类型
            test_parameters: 测试参数
            
        Returns:
            测试结果
        """
        logger.info(f"直接运行测试: {test_type}")
        
        try:
            # 根据测试类型选择合适的测试工具
            if test_type.startswith("unit:"):
                # 单元测试
                return self._direct_execute_tool("test_and_issue_collector", "run_unit_test", test_name=test_type[5:], **test_parameters)
            elif test_type.startswith("visual:"):
                # 视觉测试
                return self._direct_execute_tool("test_and_issue_collector", "run_visual_test", test_name=test_type[7:], **test_parameters)
            elif test_type.startswith("e2e:"):
                # 端到端测试
                return self._direct_execute_tool("test_and_issue_collector", "run_e2e_test", test_name=test_type[4:], **test_parameters)
            else:
                # 默认为通用测试
                return self._direct_execute_tool("test_and_issue_collector", "run_test", test_name=test_type, **test_parameters)
        
        except Exception as e:
            logger.error(f"直接运行测试失败: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def analyze_problem(self, problem: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        分析问题
        
        Args:
            problem: 问题描述
            context: 问题上下文
            
        Returns:
            分析结果
        """
        logger.info(f"分析问题: {problem}")
        
        if context is None:
            context = {}
        
        # 通过MCP协调器分析问题
        if self.is_mcp_available():
            try:
                # 使用submit_problem方法
                result = self.coordinator.execute_tool("agent_problem_solver", "submit_problem", problem=problem, context=context)
                logger.info(f"通过MCP协调器分析问题成功")
                return result
            except Exception as e:
                logger.error(f"通过MCP协调器分析问题失败: {str(e)}")
                # 如果通过协调器分析失败，尝试直接分析
                return self._direct_analyze_problem(problem, context)
        else:
            # 如果MCP组件不可用，直接分析问题
            return self._direct_analyze_problem(problem, context)
    
    def _direct_analyze_problem(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        直接分析问题（不通过MCP协调器）
        
        Args:
            problem: 问题描述
            context: 问题上下文
            
        Returns:
            分析结果
        """
        logger.info(f"直接分析问题: {problem}")
        
        try:
            # 使用AgentProblemSolver分析问题
            return self._direct_execute_tool("agent_problem_solver", "submit_problem", problem=problem, context=context)
        
        except Exception as e:
            logger.error(f"直接分析问题失败: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def sync_with_github(self, operation: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        与GitHub同步
        
        Args:
            operation: 操作类型
            parameters: 操作参数
            
        Returns:
            同步结果
        """
        logger.info(f"与GitHub同步: {operation}")
        
        if parameters is None:
            parameters = {}
        
        # 通过MCP协调器与GitHub同步
        if self.is_mcp_available():
            try:
                result = self.coordinator.sync_with_github(operation, parameters)
                logger.info(f"通过MCP协调器与GitHub同步成功: {operation}")
                return result
            except Exception as e:
                logger.error(f"通过MCP协调器与GitHub同步失败: {str(e)}")
                # 如果通过协调器同步失败，尝试直接同步
                return self._direct_sync_with_github(operation, parameters)
        else:
            # 如果MCP组件不可用，直接与GitHub同步
            return self._direct_sync_with_github(operation, parameters)
    
    def _direct_sync_with_github(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        直接与GitHub同步（不通过MCP协调器）
        
        Args:
            operation: 操作类型
            parameters: 操作参数
            
        Returns:
            同步结果
        """
        logger.info(f"直接与GitHub同步: {operation}")
        
        try:
            # 使用ReleaseManager与GitHub同步
            if operation == "download":
                return self._direct_execute_tool("release_manager", "download_release", 
                                               repo_url=parameters.get("repo_url"), 
                                               local_path=parameters.get("local_path"))
            elif operation == "upload":
                return self._direct_execute_tool("release_manager", "upload_code", 
                                               local_path=parameters.get("local_path"), 
                                               repo_url=parameters.get("repo_url"), 
                                               commit_message=parameters.get("commit_message"))
            else:
                return {"status": "error", "reason": f"未知操作: {operation}"}
        
        except Exception as e:
            logger.error(f"直接与GitHub同步失败: {str(e)}")
            return {"status": "error", "reason": str(e)}
    
    def send_test_results_to_github(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        将测试结果发送到GitHub
        
        Args:
            test_results: 测试结果
            
        Returns:
            发送结果
        """
        logger.info("将测试结果发送到GitHub")
        
        # 通过MCP协调器发送测试结果
        if self.is_mcp_available():
            try:
                result = self.coordinator.execute_tool("github_test_reporter", "send_test_results_to_github", 
                                                     repo_owner="alexchuang650730", 
                                                     repo_name="powerautomation", 
                                                     test_results=test_results, 
                                                     token=os.environ.get("GITHUB_TOKEN"))
                logger.info("通过MCP协调器发送测试结果成功")
                return result
            except Exception as e:
                logger.error(f"通过MCP协调器发送测试结果失败: {str(e)}")
                # 如果通过协调器发送失败，尝试直接发送
                return self._direct_send_test_results_to_github(test_results)
        else:
            # 如果MCP组件不可用，直接发送测试结果
            return self._direct_send_test_results_to_github(test_results)
    
    def _direct_send_test_results_to_github(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        直接将测试结果发送到GitHub（不通过MCP协调器）
        
        Args:
            test_results: 测试结果
            
        Returns:
            发送结果
        """
        logger.info("直接将测试结果发送到GitHub")
        
        try:
            # 导入github_test_reporter模块
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
            from github_test_reporter import send_test_results_to_github
            
            # 发送测试结果
            result = send_test_results_to_github(
                repo_owner="alexchuang650730",
                repo_name="powerautomation",
                test_results=test_results,
                token=os.environ.get("GITHUB_TOKEN")
            )
            
            logger.info("直接发送测试结果成功")
            return {"status": "success", "result": result}
        
        except Exception as e:
            logger.error(f"直接发送测试结果失败: {str(e)}")
            return {"status": "error", "reason": str(e)}
