"""
代码智能体入口模块

提供代码智能体的主要功能和接口，整合原manus相关功能
"""

from ..development_tools.agent_problem_solver import AgentProblemSolver
from .core.mcp.feature_optimization_mcp import FeatureOptimizationMCP
from .core.mcp.ui_journey_optimization_mcp import UIJourneyOptimizationMCP
from .core.mcp.prompt_optimization_mcp import PromptOptimizationMCP
from .core.mcp.content_template_optimization_mcp import ContentTemplateOptimizationMCP
from .core.mcp.context_matching_optimization_mcp import ContextMatchingOptimizationMCP
from .core.mcp.project_memory_optimization_mcp import ProjectMemoryOptimizationMCP

class CodeAgent:
    """
    代码智能体类
    
    整合原manus相关功能，专注于代码开发
    集成六大MCP模块，提供统一接口
    """
    
    def __init__(self, config=None):
        """
        初始化代码智能体
        
        Args:
            config: 配置参数字典
        """
        self.config = config or {}
        self.problem_solver = AgentProblemSolver(self.config)
        
        # 初始化六大MCP模块
        self.prompt_mcp = PromptOptimizationMCP(self)
        self.feature_mcp = FeatureOptimizationMCP(self)
        self.ui_journey_mcp = UIJourneyOptimizationMCP(self)
        self.content_template_mcp = ContentTemplateOptimizationMCP(self)
        self.context_matching_mcp = ContextMatchingOptimizationMCP(self)
        self.project_memory_mcp = ProjectMemoryOptimizationMCP(self)
        
    def generate_code(self, requirements, language=None, context=None):
        """
        生成代码的主要方法
        
        Args:
            requirements: 代码需求描述
            language: 编程语言
            context: 上下文信息
            
        Returns:
            生成的代码
        """
        # 使用提示词优化MCP处理需求
        optimized_prompt = self.prompt_mcp.optimize(requirements, context)
        
        # 使用特性优化MCP生成代码
        code_result = self.feature_mcp.generate_code(optimized_prompt, language)
        
        # 使用上下文匹配优化MCP确保代码与上下文一致
        code_result = self.context_matching_mcp.match_context(code_result, context)
        
        # 记录到项目级记忆
        self.project_memory_mcp.save_memory(requirements, code_result)
        
        return code_result
    
    def refactor_code(self, code, requirements=None):
        """
        重构代码
        
        Args:
            code: 原始代码
            requirements: 重构需求
            
        Returns:
            重构后的代码
        """
        return self.feature_mcp.refactor_code(code, requirements)
    
    def debug_code(self, code, error_message=None):
        """
        调试代码
        
        Args:
            code: 待调试代码
            error_message: 错误信息
            
        Returns:
            修复后的代码
        """
        return self.feature_mcp.debug_code(code, error_message)
    
    def explain_code(self, code):
        """
        解释代码
        
        Args:
            code: 待解释代码
            
        Returns:
            代码解释
        """
        return self.feature_mcp.explain_code(code)
