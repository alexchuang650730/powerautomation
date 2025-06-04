"""
统一智能工具引擎MCP适配器 - 完善版
整合ACI.dev、MCP.so和Zapier三个云端平台的统一工具引擎
"""

import json
import logging
import asyncio
import time
import os
import requests
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import sys

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from mcptool.adapters.base_mcp import BaseMCP

logger = logging.getLogger(__name__)

class UnifiedToolRegistry:
    """统一工具注册表"""
    
    def __init__(self):
        self.tools_db = {}
        self.platform_clients = {}
        self.last_sync_time = None
        
    def register_tool(self, tool_info: Dict) -> str:
        """注册工具到统一注册表"""
        tool_id = f"{tool_info['platform']}:{tool_info['name']}"
        
        unified_tool = {
            # 基础信息
            "id": tool_id,
            "name": tool_info["name"],
            "description": tool_info["description"],
            "category": tool_info["category"],
            "version": tool_info.get("version", "1.0.0"),
            
            # 平台信息
            "platform": tool_info["platform"],
            "platform_tool_id": tool_info["platform_tool_id"],
            "mcp_endpoint": tool_info["mcp_endpoint"],
            
            # 功能特性
            "capabilities": tool_info["capabilities"],
            "input_schema": tool_info["input_schema"],
            "output_schema": tool_info["output_schema"],
            
            # 性能指标
            "performance_metrics": {
                "avg_response_time": tool_info.get("avg_response_time", 1000),
                "success_rate": tool_info.get("success_rate", 0.95),
                "throughput": tool_info.get("throughput", 100),
                "reliability_score": tool_info.get("reliability_score", 0.9)
            },
            
            # 成本信息
            "cost_model": {
                "type": tool_info.get("cost_type", "free"),
                "cost_per_call": tool_info.get("cost_per_call", 0.0),
                "monthly_limit": tool_info.get("monthly_limit", -1),
                "currency": tool_info.get("currency", "USD")
            },
            
            # 质量评分
            "quality_scores": {
                "user_rating": tool_info.get("user_rating", 4.0),
                "documentation_quality": tool_info.get("doc_quality", 0.8),
                "community_support": tool_info.get("community_support", 0.7),
                "update_frequency": tool_info.get("update_frequency", 0.8)
            }
        }
        
        self.tools_db[tool_id] = unified_tool
        return tool_id
    
    def search_tools(self, query: str, filters: Dict = None) -> List[Dict]:
        """搜索工具"""
        filters = filters or {}
        matches = []
        query_lower = query.lower()
        
        for tool_id, tool in self.tools_db.items():
            score = 0.0
            
            # 名称匹配
            if query_lower in tool["name"].lower():
                score += 0.4
            
            # 描述匹配
            if query_lower in tool["description"].lower():
                score += 0.3
            
            # 类别匹配
            if query_lower in tool["category"].lower():
                score += 0.2
            
            # 能力匹配
            for capability in tool["capabilities"]:
                if query_lower in capability.lower():
                    score += 0.1
                    break
            
            # 应用过滤器
            if self._apply_filters(tool, filters) and score > 0:
                tool_copy = tool.copy()
                tool_copy["relevance_score"] = score
                matches.append(tool_copy)
        
        return sorted(matches, key=lambda x: x["relevance_score"], reverse=True)
    
    def _apply_filters(self, tool: Dict, filters: Dict) -> bool:
        """应用过滤器"""
        if "platforms" in filters and tool["platform"] not in filters["platforms"]:
            return False
        
        if "categories" in filters and tool["category"] not in filters["categories"]:
            return False
        
        if "max_cost" in filters:
            if tool["cost_model"]["cost_per_call"] > filters["max_cost"]:
                return False
        
        if "min_success_rate" in filters:
            if tool["performance_metrics"]["success_rate"] < filters["min_success_rate"]:
                return False
        
        return True

class IntelligentRoutingEngine:
    """智能路由决策引擎"""
    
    def __init__(self, registry: UnifiedToolRegistry):
        self.registry = registry
        self.decision_weights = {
            "performance": 0.3,
            "cost": 0.25,
            "quality": 0.25,
            "availability": 0.2
        }
    
    def select_optimal_tool(self, user_request: str, context: Dict = None) -> Dict:
        """选择最优工具"""
        context = context or {}
        
        # 工具发现
        candidate_tools = self.registry.search_tools(
            user_request, 
            filters=context.get("filters", {})
        )
        
        if not candidate_tools:
            return {"success": False, "error": "未找到匹配的工具"}
        
        # 多维度评分
        scored_tools = []
        for tool in candidate_tools:
            score = self._calculate_comprehensive_score(tool, context)
            tool["comprehensive_score"] = score
            scored_tools.append(tool)
        
        # 选择最优工具
        best_tool = max(scored_tools, key=lambda x: x["comprehensive_score"])
        
        return {
            "success": True,
            "selected_tool": best_tool,
            "alternatives": scored_tools[1:4],
            "decision_explanation": self._generate_decision_explanation(best_tool, context)
        }
    
    def _calculate_comprehensive_score(self, tool: Dict, context: Dict) -> float:
        """计算综合评分"""
        performance_score = self._calculate_performance_score(tool)
        cost_score = self._calculate_cost_score(tool, context)
        quality_score = self._calculate_quality_score(tool)
        availability_score = self._calculate_availability_score(tool, context)
        
        comprehensive_score = (
            performance_score * self.decision_weights["performance"] +
            cost_score * self.decision_weights["cost"] +
            quality_score * self.decision_weights["quality"] +
            availability_score * self.decision_weights["availability"]
        )
        
        # 相关性加成
        relevance_bonus = tool.get("relevance_score", 0) * 0.1
        
        return min(comprehensive_score + relevance_bonus, 1.0)
    
    def _calculate_performance_score(self, tool: Dict) -> float:
        """计算性能评分"""
        metrics = tool["performance_metrics"]
        
        response_time_score = max(0, 1 - (metrics["avg_response_time"] / 5000))
        success_rate_score = metrics["success_rate"]
        throughput_score = min(metrics["throughput"] / 1000, 1.0)
        reliability_score = metrics["reliability_score"]
        
        return (response_time_score * 0.3 + success_rate_score * 0.3 + 
                throughput_score * 0.2 + reliability_score * 0.2)
    
    def _calculate_cost_score(self, tool: Dict, context: Dict) -> float:
        """计算成本评分"""
        cost_model = tool["cost_model"]
        
        if cost_model["type"] == "free":
            return 1.0
        elif cost_model["type"] == "per_call":
            max_cost = context.get("budget", {}).get("max_cost_per_call", 0.01)
            cost_ratio = cost_model["cost_per_call"] / max_cost
            return max(0, 1 - cost_ratio)
        else:
            return 0.8
    
    def _calculate_quality_score(self, tool: Dict) -> float:
        """计算质量评分"""
        quality = tool["quality_scores"]
        
        user_rating_score = (quality["user_rating"] - 1) / 4
        doc_quality_score = quality["documentation_quality"]
        community_score = quality["community_support"]
        update_score = quality["update_frequency"]
        
        return (user_rating_score * 0.4 + doc_quality_score * 0.2 + 
                community_score * 0.2 + update_score * 0.2)
    
    def _calculate_availability_score(self, tool: Dict, context: Dict) -> float:
        """计算可用性评分"""
        # 简化的可用性评分
        return 0.9
    
    def _generate_decision_explanation(self, tool: Dict, context: Dict) -> Dict:
        """生成决策解释"""
        return {
            "selected_tool": {
                "name": tool["name"],
                "platform": tool["platform"],
                "score": tool["comprehensive_score"]
            },
            "key_factors": {
                "performance": self._calculate_performance_score(tool),
                "cost": self._calculate_cost_score(tool, context),
                "quality": self._calculate_quality_score(tool)
            }
        }

class MCPUnifiedExecutionEngine:
    """MCP统一执行引擎"""
    
    def __init__(self, registry: UnifiedToolRegistry):
        self.registry = registry
        self.routing_engine = IntelligentRoutingEngine(registry)
        
        # 执行统计
        self.execution_stats = {
            "total_executions": 0,
            "platform_usage": {"aci.dev": 0, "mcp.so": 0, "zapier": 0},
            "success_rate": 0.0,
            "avg_execution_time": 0.0
        }
    
    async def execute_user_request(self, user_request: str, context: Dict = None) -> Dict:
        """执行用户请求"""
        context = context or {}
        execution_id = f"exec_{int(time.time())}"
        
        try:
            # 智能路由选择工具
            routing_result = self.routing_engine.select_optimal_tool(user_request, context)
            
            if not routing_result["success"]:
                return routing_result
            
            selected_tool = routing_result["selected_tool"]
            
            # 准备执行参数
            execution_params = self._prepare_execution_params(user_request, selected_tool, context)
            
            # 模拟MCP执行
            execution_result = await self._simulate_mcp_execution(
                selected_tool, execution_params, execution_id
            )
            
            # 更新统计信息
            self._update_execution_stats(selected_tool, execution_result)
            
            return {
                "success": True,
                "execution_id": execution_id,
                "selected_tool": {
                    "name": selected_tool["name"],
                    "platform": selected_tool["platform"],
                    "confidence_score": selected_tool["comprehensive_score"]
                },
                "execution_result": execution_result,
                "routing_info": routing_result["decision_explanation"],
                "alternatives": routing_result["alternatives"]
            }
            
        except Exception as e:
            logger.error(f"执行失败 {execution_id}: {e}")
            return {
                "success": False,
                "execution_id": execution_id,
                "error": str(e)
            }
    
    def _prepare_execution_params(self, user_request: str, tool: Dict, context: Dict) -> Dict:
        """准备执行参数"""
        return {
            "request": user_request,
            "context": context,
            "tool_specific_params": self._extract_tool_specific_params(user_request, tool)
        }
    
    def _extract_tool_specific_params(self, request: str, tool: Dict) -> Dict:
        """提取工具特定参数"""
        category = tool["category"]
        
        if category == "productivity":
            return {"priority": "normal", "notification": True}
        elif category == "data_analysis":
            return {"analysis_type": "basic", "output_format": "json"}
        elif category == "communication":
            return {"message_format": "text", "urgent": False}
        else:
            return {}
    
    async def _simulate_mcp_execution(self, tool: Dict, params: Dict, execution_id: str) -> Dict:
        """模拟MCP执行"""
        start_time = time.time()
        
        # 模拟执行延迟
        await asyncio.sleep(0.1)
        
        execution_time = time.time() - start_time
        
        # 模拟成功执行
        return {
            "success": True,
            "result": f"工具 {tool['name']} 执行完成",
            "execution_time": execution_time,
            "platform": tool["platform"],
            "tool_name": tool["name"],
            "metadata": {
                "execution_timestamp": time.time(),
                "mcp_version": "1.0"
            }
        }
    
    def _update_execution_stats(self, tool: Dict, result: Dict):
        """更新执行统计"""
        self.execution_stats["total_executions"] += 1
        self.execution_stats["platform_usage"][tool["platform"]] += 1
        
        if result.get("success"):
            current_success = self.execution_stats.get("successful_executions", 0)
            self.execution_stats["successful_executions"] = current_success + 1
        
        total = self.execution_stats["total_executions"]
        successful = self.execution_stats.get("successful_executions", 0)
        self.execution_stats["success_rate"] = successful / total if total > 0 else 0
    
    def get_execution_statistics(self) -> Dict:
        """获取执行统计信息"""
        return {
            "statistics": self.execution_stats,
            "platform_distribution": {
                platform: count / max(self.execution_stats["total_executions"], 1)
                for platform, count in self.execution_stats["platform_usage"].items()
            },
            "registry_info": {
                "total_tools": len(self.registry.tools_db)
            }
        }

class UnifiedSmartToolEngineMCP(BaseMCP):
    """统一智能工具引擎MCP适配器 - 完善版"""
    
    def __init__(self, config: Dict = None):
        super().__init__()
        self.config = config or {}
        
        # 初始化核心组件
        self.registry = UnifiedToolRegistry()
        self.execution_engine = MCPUnifiedExecutionEngine(self.registry)
        
        # 初始化示例工具
        self._initialize_sample_tools()
        
        logger.info("统一智能工具引擎MCP适配器初始化完成")
    
    def _initialize_sample_tools(self):
        """初始化示例工具"""
        sample_tools = [
            {
                "name": "google_calendar_integration",
                "description": "Google Calendar API集成工具",
                "category": "productivity",
                "platform": "aci.dev",
                "platform_tool_id": "google_calendar_v3",
                "mcp_endpoint": "https://api.aci.dev/mcp/google_calendar",
                "capabilities": ["schedule", "remind", "sync", "share"],
                "input_schema": {"type": "object", "properties": {"action": {"type": "string"}}},
                "output_schema": {"type": "object", "properties": {"result": {"type": "string"}}},
                "avg_response_time": 200,
                "success_rate": 0.98,
                "cost_type": "per_call",
                "cost_per_call": 0.001,
                "user_rating": 4.5
            },
            {
                "name": "advanced_data_analyzer",
                "description": "高级数据分析MCP工具",
                "category": "data_analysis",
                "platform": "mcp.so",
                "platform_tool_id": "data_analyzer_pro",
                "mcp_endpoint": "https://api.mcp.so/tools/data_analyzer",
                "capabilities": ["analyze", "visualize", "predict", "export"],
                "input_schema": {"type": "object", "properties": {"data": {"type": "array"}}},
                "output_schema": {"type": "object", "properties": {"analysis": {"type": "object"}}},
                "avg_response_time": 500,
                "success_rate": 0.96,
                "cost_type": "subscription",
                "monthly_limit": 1000,
                "user_rating": 4.3
            },
            {
                "name": "slack_team_notification",
                "description": "Slack团队通知自动化",
                "category": "communication",
                "platform": "zapier",
                "platform_tool_id": "slack_webhook_v2",
                "mcp_endpoint": "https://zapier-mcp-bridge.com/slack_notification",
                "capabilities": ["message", "channel", "mention", "format"],
                "input_schema": {"type": "object", "properties": {"message": {"type": "string"}}},
                "output_schema": {"type": "object", "properties": {"status": {"type": "string"}}},
                "avg_response_time": 150,
                "success_rate": 0.99,
                "cost_type": "free",
                "user_rating": 4.7
            }
        ]
        
        for tool in sample_tools:
            self.registry.register_tool(tool)
    
    def get_capabilities(self) -> List[str]:
        """获取适配器能力"""
        return [
            "unified_tool_discovery",
            "intelligent_routing",
            "multi_platform_execution",
            "performance_optimization",
            "cost_optimization",
            "quality_assurance"
        ]
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """验证输入数据"""
        if not isinstance(input_data, dict):
            return False
        
        action = input_data.get("action")
        valid_actions = [
            "execute_request",
            "discover_tools",
            "get_statistics",
            "register_tool",
            "health_check"
        ]
        
        return action in valid_actions
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        try:
            action = input_data.get("action")
            parameters = input_data.get("parameters", {})
            
            if action == "execute_request":
                return asyncio.run(self._execute_request(parameters))
            elif action == "discover_tools":
                return self._discover_tools(parameters)
            elif action == "get_statistics":
                return self._get_statistics()
            elif action == "register_tool":
                return self._register_tool(parameters)
            elif action == "health_check":
                return self._health_check()
            else:
                return {
                    "success": False,
                    "error": f"不支持的操作: {action}",
                    "available_actions": [
                        "execute_request", "discover_tools", "get_statistics",
                        "register_tool", "health_check"
                    ]
                }
                
        except Exception as e:
            logger.error(f"处理请求失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "action": input_data.get("action")
            }
    
    async def _execute_request(self, parameters: Dict) -> Dict[str, Any]:
        """执行用户请求"""
        user_request = parameters.get("request", "")
        context = parameters.get("context", {})
        
        if not user_request:
            return {
                "success": False,
                "error": "缺少必需参数: request"
            }
        
        result = await self.execution_engine.execute_user_request(user_request, context)
        return result
    
    def _discover_tools(self, parameters: Dict) -> Dict[str, Any]:
        """工具发现"""
        try:
            query = parameters.get("query", "")
            filters = parameters.get("filters", {})
            limit = parameters.get("limit", 10)
            
            tools = self.registry.search_tools(query, filters)
            
            return {
                "success": True,
                "tools": tools[:limit],
                "total_count": len(tools),
                "search_query": query,
                "filters_applied": filters
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            stats = self.execution_engine.get_execution_statistics()
            return {
                "success": True,
                "statistics": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _register_tool(self, parameters: Dict) -> Dict[str, Any]:
        """注册新工具"""
        try:
            tool_info = parameters.get("tool_info", {})
            
            if not tool_info:
                return {
                    "success": False,
                    "error": "缺少工具信息"
                }
            
            tool_id = self.registry.register_tool(tool_info)
            
            return {
                "success": True,
                "tool_id": tool_id,
                "message": "工具注册成功"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "success": True,
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0",
            "components": {
                "registry": "operational",
                "routing_engine": "operational",
                "execution_engine": "operational"
            },
            "metrics": {
                "total_tools": len(self.registry.tools_db),
                "total_executions": self.execution_engine.execution_stats["total_executions"]
            }
        }

