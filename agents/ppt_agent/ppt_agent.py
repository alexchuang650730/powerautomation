"""
PPT智能体集成模块

整合六大MCP模块，提供统一的PPT智能体接口
"""

import logging
from typing import Dict, Any, List, Optional

from .core.mcp.base_mcp import BaseMCP
from .core.mcp.prompt_optimization_mcp import PromptOptimizationMCP
from .core.mcp.feature_optimization_mcp import FeatureOptimizationMCP
from .core.mcp.ui_journey_optimization_mcp import UIJourneyOptimizationMCP
from .core.mcp.content_template_optimization_mcp import ContentTemplateOptimizationMCP
from .core.mcp.context_matching_optimization_mcp import ContextMatchingOptimizationMCP
from .core.mcp.project_memory_optimization_mcp import ProjectMemoryOptimizationMCP

class PPTAgent:
    """PPT智能体，整合六大MCP模块，提供统一的接口"""
    
    def __init__(self):
        """初始化PPT智能体"""
        self.logger = logging.getLogger(__name__)
        
        # 初始化六大MCP模块
        self.prompt_mcp = PromptOptimizationMCP()
        self.feature_mcp = FeatureOptimizationMCP()
        self.ui_journey_mcp = UIJourneyOptimizationMCP()
        self.content_template_mcp = ContentTemplateOptimizationMCP()
        self.context_matching_mcp = ContextMatchingOptimizationMCP()
        self.project_memory_mcp = ProjectMemoryOptimizationMCP()
        
        # MCP模块映射
        self.mcp_mapping = {
            "prompt": self.prompt_mcp,
            "feature": self.feature_mcp,
            "ui_journey": self.ui_journey_mcp,
            "content_template": self.content_template_mcp,
            "context_matching": self.context_matching_mcp,
            "project_memory": self.project_memory_mcp
        }
        
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理PPT智能体请求
        
        参数:
            input_data: 输入数据字典，必须包含mcp_type字段
            context: 上下文信息字典
            
        返回:
            处理结果字典
        """
        mcp_type = input_data.get("mcp_type")
        
        if not mcp_type:
            return {"status": "error", "message": "缺少mcp_type参数"}
        
        if mcp_type not in self.mcp_mapping:
            return {"status": "error", "message": f"不支持的MCP类型: {mcp_type}"}
        
        # 获取对应的MCP模块
        mcp = self.mcp_mapping[mcp_type]
        
        # 调用MCP模块处理请求
        try:
            result = mcp.process(input_data, context)
            return result
        except Exception as e:
            self.logger.error(f"MCP处理异常: {str(e)}")
            return {"status": "error", "message": f"MCP处理异常: {str(e)}"}
    
    def generate_ppt(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        生成PPT的便捷方法，整合多个MCP模块
        
        参数:
            input_data: 输入数据字典
            context: 上下文信息字典
            
        返回:
            PPT生成结果字典
        """
        # 1. 分析上下文
        context_input = {
            "mcp_type": "context_matching",
            "context_action": "analyze_context",
            "content": input_data.get("content", ""),
            "context_type": input_data.get("context_type", "general")
        }
        context_result = self.process(context_input, context)
        
        if context_result.get("status") != "success":
            return context_result
        
        context_features = context_result.get("context_features", {})
        
        # 2. 获取适合的模板
        template_input = {
            "mcp_type": "content_template",
            "template_action": "get_template",
            "template_type": input_data.get("template_type", "general"),
            "industry": context_features.get("industry", "general")
        }
        template_result = self.process(template_input, context)
        
        if template_result.get("status") != "success":
            return template_result
        
        template = template_result.get("template", {})
        
        # 3. 生成优化的提示词
        prompt_input = {
            "mcp_type": "prompt",
            "prompt_type": "content_generation",
            "title": input_data.get("title", ""),
            "topic": input_data.get("topic", ""),
            "audience": input_data.get("audience", "通用"),
            "purpose": context_features.get("purpose", "informative"),
            "length": "high" if context_features.get("complexity") == "high" else "medium"
        }
        prompt_result = self.process(prompt_input, context)
        
        if prompt_result.get("status") != "success":
            return prompt_result
        
        # 4. 使用特性优化MCP生成PPT
        feature_input = {
            "mcp_type": "feature",
            "feature_action": "generate_ppt",
            "title": input_data.get("title", ""),
            "content": input_data.get("content", ""),
            "template_id": template.get("id", ""),
            "prompt": prompt_result.get("prompt", ""),
            "output_path": input_data.get("output_path", "")
        }
        feature_result = self.process(feature_input, context)
        
        if feature_result.get("status") != "success":
            return feature_result
        
        # 5. 保存项目记忆
        if input_data.get("save_memory", True):
            memory_input = {
                "mcp_type": "project_memory",
                "memory_action": "store",
                "project_id": input_data.get("project_id", ""),
                "memory_type": "ppt_project",
                "memory_data": {
                    "title": input_data.get("title", ""),
                    "content": input_data.get("content", ""),
                    "template_id": template.get("id", ""),
                    "context_features": context_features,
                    "output_path": feature_result.get("output_path", "")
                }
            }
            self.process(memory_input, context)
        
        # 返回最终结果
        return {
            "status": "success",
            "output_path": feature_result.get("output_path", ""),
            "template_used": template.get("name", ""),
            "slide_count": feature_result.get("slide_count", 0),
            "context_features": context_features
        }
    
    def get_all_mcps(self) -> List[Dict[str, Any]]:
        """
        获取所有MCP模块的信息
        
        返回:
            MCP模块信息列表
        """
        mcp_info = []
        for mcp_type, mcp in self.mcp_mapping.items():
            mcp_info.append({
                "type": mcp_type,
                "id": mcp.mcp_id,
                "name": mcp.name,
                "description": mcp.description
            })
        return mcp_info
