# 重新设计：统一工具注册表 + 智能路由 + MCP统一执行

## 🎯 **核心设计理念**

### 📋 **设计原则**
1. **统一注册表** - 一个中央化的工具注册表，记录所有平台的工具
2. **智能路由** - 基于工具特性、成本、性能的智能选择算法
3. **MCP统一执行** - 通过标准MCP协议执行所有平台的工具
4. **透明切换** - 用户无感知的平台切换体验

### 🏗️ **重新设计的架构图**
```
                    用户请求
                       ↓
                MCPBrainstorm
                (意图理解)
                       ↓
                 复杂度分析
                       ↓
            [简单任务]     [复杂任务]
               ↓              ↓
         直接工具查询    MCPPlanner规划
               ↓              ↓
           InfiniteContext (上下文增强)
                       ↓
              ┌─────────────────────┐
              │   统一工具注册表      │
              │ ┌─────────────────┐ │
              │ │ ACI.dev 工具    │ │
              │ │ MCP.so 工具     │ │
              │ │ Zapier 工具     │ │
              │ └─────────────────┘ │
              └─────────────────────┘
                       ↓
                 工具发现与匹配
                       ↓
                 智能路由决策
                       ↓
              选择最优工具+平台
                       ↓
                MCP统一执行引擎
                       ↓
        ┌─────────────┬─────────────┬─────────────┐
        ↓             ↓             ↓             ↓
   ACI.dev MCP   MCP.so MCP   Zapier MCP   本地MCP
     客户端        客户端        适配器       工具
        ↓             ↓             ↓             ↓
        └─────────────┴─────────────┴─────────────┘
                       ↓
                   执行结果
                       ↓
                   返回用户
```

## 🗂️ **统一工具注册表设计**

### 📊 **工具注册表数据结构**
```python
class UnifiedToolRegistry:
    """统一工具注册表"""
    
    def __init__(self):
        self.tools_db = {}  # 工具数据库
        self.platform_clients = {
            "aci.dev": ACIDevMCPClient(),
            "mcp.so": MCPSoMCPClient(), 
            "zapier": ZapierMCPAdapter()
        }
        
    def register_tool(self, tool_info):
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
            "platform": tool_info["platform"],  # "aci.dev", "mcp.so", "zapier"
            "platform_tool_id": tool_info["platform_tool_id"],
            "mcp_endpoint": tool_info["mcp_endpoint"],
            
            # 功能特性
            "capabilities": tool_info["capabilities"],
            "input_schema": tool_info["input_schema"],
            "output_schema": tool_info["output_schema"],
            "supported_formats": tool_info.get("supported_formats", []),
            
            # 性能指标
            "performance_metrics": {
                "avg_response_time": tool_info.get("avg_response_time", 1000),  # ms
                "success_rate": tool_info.get("success_rate", 0.95),
                "throughput": tool_info.get("throughput", 100),  # requests/min
                "reliability_score": tool_info.get("reliability_score", 0.9)
            },
            
            # 成本信息
            "cost_model": {
                "type": tool_info.get("cost_type", "free"),  # free, per_call, subscription
                "cost_per_call": tool_info.get("cost_per_call", 0.0),
                "monthly_limit": tool_info.get("monthly_limit", -1),  # -1 = unlimited
                "currency": tool_info.get("currency", "USD")
            },
            
            # 使用限制
            "limitations": {
                "rate_limit": tool_info.get("rate_limit", 1000),  # calls/hour
                "data_size_limit": tool_info.get("data_size_limit", 10),  # MB
                "concurrent_limit": tool_info.get("concurrent_limit", 10),
                "geographic_restrictions": tool_info.get("geo_restrictions", [])
            },
            
            # 质量评分
            "quality_scores": {
                "user_rating": tool_info.get("user_rating", 4.0),  # 1-5
                "documentation_quality": tool_info.get("doc_quality", 0.8),
                "community_support": tool_info.get("community_support", 0.7),
                "update_frequency": tool_info.get("update_frequency", 0.8)
            },
            
            # 元数据
            "metadata": {
                "created_at": tool_info.get("created_at"),
                "updated_at": tool_info.get("updated_at"),
                "tags": tool_info.get("tags", []),
                "author": tool_info.get("author", ""),
                "license": tool_info.get("license", ""),
                "homepage": tool_info.get("homepage", "")
            }
        }
        
        self.tools_db[tool_id] = unified_tool
        return tool_id

# 示例工具注册
registry = UnifiedToolRegistry()

# ACI.dev工具示例
aci_tool = {
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
}

# MCP.so工具示例  
mcpso_tool = {
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
}

# Zapier工具示例
zapier_tool = {
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

# 注册工具
registry.register_tool(aci_tool)
registry.register_tool(mcpso_tool)
registry.register_tool(zapier_tool)
```

### 🔍 **工具发现与搜索**
```python
class ToolDiscoveryEngine:
    """工具发现引擎"""
    
    def __init__(self, registry: UnifiedToolRegistry):
        self.registry = registry
        
    def search_tools(self, query: str, filters: Dict = None) -> List[Dict]:
        """搜索工具"""
        filters = filters or {}
        
        # 1. 文本匹配
        text_matches = self._text_search(query)
        
        # 2. 应用过滤器
        filtered_tools = self._apply_filters(text_matches, filters)
        
        # 3. 相关性排序
        ranked_tools = self._rank_by_relevance(filtered_tools, query)
        
        return ranked_tools
    
    def _text_search(self, query: str) -> List[Dict]:
        """文本搜索"""
        query_lower = query.lower()
        matches = []
        
        for tool_id, tool in self.registry.tools_db.items():
            score = 0.0
            
            # 名称匹配 (权重: 40%)
            if query_lower in tool["name"].lower():
                score += 0.4
            
            # 描述匹配 (权重: 30%)
            if query_lower in tool["description"].lower():
                score += 0.3
                
            # 类别匹配 (权重: 20%)
            if query_lower in tool["category"].lower():
                score += 0.2
                
            # 能力匹配 (权重: 10%)
            for capability in tool["capabilities"]:
                if query_lower in capability.lower():
                    score += 0.1
                    break
            
            if score > 0:
                tool_copy = tool.copy()
                tool_copy["relevance_score"] = score
                matches.append(tool_copy)
        
        return matches
    
    def _apply_filters(self, tools: List[Dict], filters: Dict) -> List[Dict]:
        """应用过滤器"""
        filtered = tools
        
        # 平台过滤
        if "platforms" in filters:
            filtered = [t for t in filtered if t["platform"] in filters["platforms"]]
        
        # 类别过滤
        if "categories" in filters:
            filtered = [t for t in filtered if t["category"] in filters["categories"]]
        
        # 成本过滤
        if "max_cost" in filters:
            filtered = [t for t in filtered 
                       if t["cost_model"]["cost_per_call"] <= filters["max_cost"]]
        
        # 性能过滤
        if "min_success_rate" in filters:
            filtered = [t for t in filtered 
                       if t["performance_metrics"]["success_rate"] >= filters["min_success_rate"]]
        
        return filtered
    
    def _rank_by_relevance(self, tools: List[Dict], query: str) -> List[Dict]:
        """按相关性排序"""
        return sorted(tools, key=lambda x: x.get("relevance_score", 0), reverse=True)
```

## 🧠 **智能路由决策引擎**

### ⚡ **路由决策算法**
```python
class IntelligentRoutingEngine:
    """智能路由决策引擎"""
    
    def __init__(self, registry: UnifiedToolRegistry):
        self.registry = registry
        self.discovery_engine = ToolDiscoveryEngine(registry)
        
        # 决策权重配置
        self.decision_weights = {
            "performance": 0.3,      # 性能权重
            "cost": 0.25,           # 成本权重  
            "quality": 0.25,        # 质量权重
            "availability": 0.2     # 可用性权重
        }
    
    def select_optimal_tool(self, user_request: str, context: Dict = None) -> Dict:
        """选择最优工具"""
        context = context or {}
        
        # 1. 工具发现
        candidate_tools = self.discovery_engine.search_tools(
            user_request, 
            filters=context.get("filters", {})
        )
        
        if not candidate_tools:
            return {"success": False, "error": "未找到匹配的工具"}
        
        # 2. 多维度评分
        scored_tools = []
        for tool in candidate_tools:
            score = self._calculate_comprehensive_score(tool, context)
            tool["comprehensive_score"] = score
            scored_tools.append(tool)
        
        # 3. 选择最优工具
        best_tool = max(scored_tools, key=lambda x: x["comprehensive_score"])
        
        # 4. 生成决策解释
        decision_explanation = self._generate_decision_explanation(
            best_tool, scored_tools[:3], context
        )
        
        return {
            "success": True,
            "selected_tool": best_tool,
            "alternatives": scored_tools[1:4],  # 前3个备选
            "decision_explanation": decision_explanation,
            "routing_metadata": {
                "total_candidates": len(candidate_tools),
                "decision_time": "< 100ms",
                "confidence_score": best_tool["comprehensive_score"]
            }
        }
    
    def _calculate_comprehensive_score(self, tool: Dict, context: Dict) -> float:
        """计算综合评分"""
        scores = {}
        
        # 1. 性能评分
        scores["performance"] = self._calculate_performance_score(tool)
        
        # 2. 成本评分
        scores["cost"] = self._calculate_cost_score(tool, context)
        
        # 3. 质量评分
        scores["quality"] = self._calculate_quality_score(tool)
        
        # 4. 可用性评分
        scores["availability"] = self._calculate_availability_score(tool, context)
        
        # 5. 加权综合评分
        comprehensive_score = sum(
            scores[dimension] * self.decision_weights[dimension]
            for dimension in scores
        )
        
        # 6. 相关性加成
        relevance_bonus = tool.get("relevance_score", 0) * 0.1
        
        return min(comprehensive_score + relevance_bonus, 1.0)
    
    def _calculate_performance_score(self, tool: Dict) -> float:
        """计算性能评分"""
        metrics = tool["performance_metrics"]
        
        # 响应时间评分 (越低越好)
        response_time_score = max(0, 1 - (metrics["avg_response_time"] / 5000))  # 5s为基准
        
        # 成功率评分
        success_rate_score = metrics["success_rate"]
        
        # 吞吐量评分
        throughput_score = min(metrics["throughput"] / 1000, 1.0)  # 1000 req/min为满分
        
        # 可靠性评分
        reliability_score = metrics["reliability_score"]
        
        return (response_time_score * 0.3 + success_rate_score * 0.3 + 
                throughput_score * 0.2 + reliability_score * 0.2)
    
    def _calculate_cost_score(self, tool: Dict, context: Dict) -> float:
        """计算成本评分"""
        cost_model = tool["cost_model"]
        user_budget = context.get("budget", {"max_cost_per_call": 0.01})
        
        if cost_model["type"] == "free":
            return 1.0
        elif cost_model["type"] == "per_call":
            cost_ratio = cost_model["cost_per_call"] / user_budget["max_cost_per_call"]
            return max(0, 1 - cost_ratio)
        elif cost_model["type"] == "subscription":
            # 基于月度限制计算单次成本
            if cost_model["monthly_limit"] > 0:
                estimated_cost_per_call = 10 / cost_model["monthly_limit"]  # 假设月费$10
                cost_ratio = estimated_cost_per_call / user_budget["max_cost_per_call"]
                return max(0, 1 - cost_ratio)
            else:
                return 0.8  # 无限制订阅给予较高分数
        
        return 0.5  # 未知成本模型
    
    def _calculate_quality_score(self, tool: Dict) -> float:
        """计算质量评分"""
        quality = tool["quality_scores"]
        
        # 用户评分 (1-5 转换为 0-1)
        user_rating_score = (quality["user_rating"] - 1) / 4
        
        # 文档质量
        doc_quality_score = quality["documentation_quality"]
        
        # 社区支持
        community_score = quality["community_support"]
        
        # 更新频率
        update_score = quality["update_frequency"]
        
        return (user_rating_score * 0.4 + doc_quality_score * 0.2 + 
                community_score * 0.2 + update_score * 0.2)
    
    def _calculate_availability_score(self, tool: Dict, context: Dict) -> float:
        """计算可用性评分"""
        limitations = tool["limitations"]
        user_requirements = context.get("requirements", {})
        
        score = 1.0
        
        # 速率限制检查
        required_rate = user_requirements.get("required_rate", 100)  # calls/hour
        if limitations["rate_limit"] < required_rate:
            score *= 0.5
        
        # 数据大小限制检查
        required_data_size = user_requirements.get("data_size", 1)  # MB
        if limitations["data_size_limit"] < required_data_size:
            score *= 0.7
        
        # 并发限制检查
        required_concurrent = user_requirements.get("concurrent_requests", 1)
        if limitations["concurrent_limit"] < required_concurrent:
            score *= 0.8
        
        # 地理限制检查
        user_location = user_requirements.get("location", "")
        if (user_location and limitations["geographic_restrictions"] and 
            user_location in limitations["geographic_restrictions"]):
            score *= 0.3
        
        return score
    
    def _generate_decision_explanation(self, selected_tool: Dict, 
                                     alternatives: List[Dict], context: Dict) -> Dict:
        """生成决策解释"""
        return {
            "selected_tool": {
                "name": selected_tool["name"],
                "platform": selected_tool["platform"],
                "score": selected_tool["comprehensive_score"],
                "key_advantages": self._identify_key_advantages(selected_tool)
            },
            "decision_factors": {
                "primary_factor": self._identify_primary_factor(selected_tool),
                "performance_rank": self._get_performance_rank(selected_tool, alternatives),
                "cost_efficiency": self._get_cost_efficiency(selected_tool),
                "quality_rating": selected_tool["quality_scores"]["user_rating"]
            },
            "alternatives_summary": [
                {
                    "name": alt["name"],
                    "platform": alt["platform"], 
                    "score": alt["comprehensive_score"],
                    "why_not_selected": self._explain_why_not_selected(alt, selected_tool)
                }
                for alt in alternatives
            ]
        }
    
    def _identify_key_advantages(self, tool: Dict) -> List[str]:
        """识别关键优势"""
        advantages = []
        
        if tool["cost_model"]["type"] == "free":
            advantages.append("免费使用")
        
        if tool["performance_metrics"]["success_rate"] > 0.95:
            advantages.append("高可靠性")
        
        if tool["performance_metrics"]["avg_response_time"] < 500:
            advantages.append("快速响应")
        
        if tool["quality_scores"]["user_rating"] > 4.0:
            advantages.append("用户好评")
        
        return advantages
    
    def _identify_primary_factor(self, tool: Dict) -> str:
        """识别主要决策因素"""
        scores = {
            "performance": self._calculate_performance_score(tool),
            "cost": self._calculate_cost_score(tool, {}),
            "quality": self._calculate_quality_score(tool),
            "availability": self._calculate_availability_score(tool, {})
        }
        
        return max(scores, key=scores.get)
    
    def _get_performance_rank(self, tool: Dict, alternatives: List[Dict]) -> int:
        """获取性能排名"""
        all_tools = [tool] + alternatives
        sorted_tools = sorted(all_tools, 
                            key=lambda x: x["performance_metrics"]["success_rate"], 
                            reverse=True)
        
        return sorted_tools.index(tool) + 1
    
    def _get_cost_efficiency(self, tool: Dict) -> str:
        """获取成本效率描述"""
        cost_model = tool["cost_model"]
        
        if cost_model["type"] == "free":
            return "免费"
        elif cost_model["cost_per_call"] < 0.001:
            return "极低成本"
        elif cost_model["cost_per_call"] < 0.01:
            return "低成本"
        else:
            return "标准成本"
    
    def _explain_why_not_selected(self, alternative: Dict, selected: Dict) -> str:
        """解释为什么没有选择备选方案"""
        if alternative["comprehensive_score"] < selected["comprehensive_score"]:
            score_diff = selected["comprehensive_score"] - alternative["comprehensive_score"]
            if score_diff > 0.2:
                return "综合评分显著较低"
            else:
                return "综合评分略低"
        
        return "其他因素考虑"
```

## 🔧 **MCP统一执行引擎**

### ⚙️ **统一执行架构**
```python
class MCPUnifiedExecutionEngine:
    """MCP统一执行引擎"""
    
    def __init__(self, registry: UnifiedToolRegistry):
        self.registry = registry
        self.routing_engine = IntelligentRoutingEngine(registry)
        
        # MCP客户端池
        self.mcp_clients = {
            "aci.dev": ACIDevMCPClient(),
            "mcp.so": MCPSoMCPClient(),
            "zapier": ZapierMCPAdapter()
        }
        
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
            # 1. 智能路由选择工具
            routing_result = self.routing_engine.select_optimal_tool(user_request, context)
            
            if not routing_result["success"]:
                return routing_result
            
            selected_tool = routing_result["selected_tool"]
            
            # 2. 准备执行参数
            execution_params = self._prepare_execution_params(
                user_request, selected_tool, context
            )
            
            # 3. 通过MCP协议执行
            execution_result = await self._execute_via_mcp(
                selected_tool, execution_params, execution_id
            )
            
            # 4. 更新统计信息
            self._update_execution_stats(selected_tool, execution_result)
            
            # 5. 返回完整结果
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
                "error": str(e),
                "error_type": "execution_error"
            }
    
    def _prepare_execution_params(self, user_request: str, tool: Dict, context: Dict) -> Dict:
        """准备执行参数"""
        # 基于工具的输入模式准备参数
        input_schema = tool["input_schema"]
        
        # 简化的参数映射逻辑
        params = {
            "request": user_request,
            "context": context,
            "tool_specific_params": self._extract_tool_specific_params(
                user_request, tool, context
            )
        }
        
        return params
    
    def _extract_tool_specific_params(self, request: str, tool: Dict, context: Dict) -> Dict:
        """提取工具特定参数"""
        # 基于工具类型和能力提取参数
        tool_params = {}
        
        # 根据工具类别设置默认参数
        category = tool["category"]
        
        if category == "productivity":
            tool_params.update({
                "priority": context.get("priority", "normal"),
                "deadline": context.get("deadline"),
                "notification": context.get("notification", True)
            })
        elif category == "data_analysis":
            tool_params.update({
                "analysis_type": context.get("analysis_type", "basic"),
                "output_format": context.get("output_format", "json"),
                "include_visualization": context.get("visualization", False)
            })
        elif category == "communication":
            tool_params.update({
                "recipients": context.get("recipients", []),
                "message_format": context.get("format", "text"),
                "urgent": context.get("urgent", False)
            })
        
        return tool_params
    
    async def _execute_via_mcp(self, tool: Dict, params: Dict, execution_id: str) -> Dict:
        """通过MCP协议执行工具"""
        platform = tool["platform"]
        mcp_client = self.mcp_clients[platform]
        
        start_time = time.time()
        
        try:
            # 构建MCP请求
            mcp_request = {
                "tool_id": tool["platform_tool_id"],
                "parameters": params,
                "execution_id": execution_id,
                "timeout": 30  # 30秒超时
            }
            
            # 执行MCP调用
            mcp_response = await mcp_client.execute_tool(mcp_request)
            
            execution_time = time.time() - start_time
            
            # 标准化响应格式
            standardized_response = self._standardize_response(
                mcp_response, tool, execution_time
            )
            
            return standardized_response
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"MCP执行失败 {execution_id}: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "platform": platform,
                "tool_id": tool["id"]
            }
    
    def _standardize_response(self, mcp_response: Dict, tool: Dict, execution_time: float) -> Dict:
        """标准化响应格式"""
        return {
            "success": mcp_response.get("success", True),
            "result": mcp_response.get("result", mcp_response),
            "execution_time": execution_time,
            "platform": tool["platform"],
            "tool_name": tool["name"],
            "tool_id": tool["id"],
            "metadata": {
                "response_size": len(str(mcp_response)),
                "execution_timestamp": time.time(),
                "mcp_version": mcp_response.get("mcp_version", "1.0")
            }
        }
    
    def _update_execution_stats(self, tool: Dict, result: Dict):
        """更新执行统计"""
        self.execution_stats["total_executions"] += 1
        self.execution_stats["platform_usage"][tool["platform"]] += 1
        
        # 更新成功率
        if result.get("success"):
            current_success = self.execution_stats.get("successful_executions", 0)
            self.execution_stats["successful_executions"] = current_success + 1
        
        total = self.execution_stats["total_executions"]
        successful = self.execution_stats.get("successful_executions", 0)
        self.execution_stats["success_rate"] = successful / total
        
        # 更新平均执行时间
        current_avg = self.execution_stats["avg_execution_time"]
        new_time = result.get("execution_time", 0)
        self.execution_stats["avg_execution_time"] = (
            (current_avg * (total - 1) + new_time) / total
        )
    
    def get_execution_statistics(self) -> Dict:
        """获取执行统计信息"""
        return {
            "statistics": self.execution_stats,
            "platform_distribution": {
                platform: count / max(self.execution_stats["total_executions"], 1)
                for platform, count in self.execution_stats["platform_usage"].items()
            },
            "registry_info": {
                "total_tools": len(self.registry.tools_db),
                "platform_breakdown": self._get_platform_breakdown()
            }
        }
    
    def _get_platform_breakdown(self) -> Dict:
        """获取平台工具分布"""
        breakdown = {"aci.dev": 0, "mcp.so": 0, "zapier": 0}
        
        for tool in self.registry.tools_db.values():
            platform = tool["platform"]
            if platform in breakdown:
                breakdown[platform] += 1
        
        return breakdown
```

## 🎯 **完整使用示例**

### 📝 **示例1：智能数据分析**
```python
# 用户请求
user_request = "分析我的销售数据并生成可视化报告"

# 执行上下文
context = {
    "budget": {"max_cost_per_call": 0.005},
    "requirements": {
        "data_size": 5,  # 5MB数据
        "required_rate": 50,  # 50 calls/hour
        "output_format": "pdf"
    },
    "filters": {
        "categories": ["data_analysis", "visualization"],
        "min_success_rate": 0.9
    }
}

# 执行请求
execution_engine = MCPUnifiedExecutionEngine(registry)
result = await execution_engine.execute_user_request(user_request, context)

# 结果示例
{
    "success": True,
    "execution_id": "exec_1704363600",
    "selected_tool": {
        "name": "advanced_data_analyzer",
        "platform": "mcp.so",
        "confidence_score": 0.87
    },
    "execution_result": {
        "success": True,
        "result": {
            "analysis_summary": "销售数据分析完成",
            "visualizations": ["chart1.png", "chart2.png"],
            "report_url": "https://reports.mcp.so/abc123.pdf"
        },
        "execution_time": 2.3,
        "platform": "mcp.so"
    },
    "routing_info": {
        "selected_tool": {
            "name": "advanced_data_analyzer",
            "platform": "mcp.so",
            "key_advantages": ["高可靠性", "专业分析", "用户好评"]
        },
        "decision_factors": {
            "primary_factor": "quality",
            "performance_rank": 2,
            "cost_efficiency": "低成本"
        }
    },
    "alternatives": [
        {
            "name": "google_sheets_analyzer",
            "platform": "aci.dev",
            "score": 0.82,
            "why_not_selected": "分析深度不足"
        }
    ]
}
```

### 📝 **示例2：团队协作自动化**
```python
# 用户请求
user_request = "当有新的GitHub PR时，自动通知Slack团队并创建Jira任务"

# 执行上下文
context = {
    "budget": {"max_cost_per_call": 0.0},  # 希望免费
    "requirements": {
        "workflow_automation": True,
        "integration_count": 3  # GitHub + Slack + Jira
    },
    "filters": {
        "platforms": ["zapier", "aci.dev"],  # 偏好这两个平台
        "categories": ["automation", "communication", "development"]
    }
}

# 执行结果
{
    "success": True,
    "selected_tool": {
        "name": "github_slack_jira_workflow",
        "platform": "zapier",
        "confidence_score": 0.94
    },
    "routing_info": {
        "decision_factors": {
            "primary_factor": "workflow_automation",
            "key_advantages": ["免费使用", "多平台集成", "可视化配置"]
        }
    }
}
```

## 💡 **核心优势总结**

### ✅ **1. 统一管理**
- 单一工具注册表管理所有平台工具
- 标准化的工具元数据和评分体系
- 统一的搜索和发现接口

### ✅ **2. 智能决策**
- 多维度评分算法（性能、成本、质量、可用性）
- 上下文感知的工具选择
- 透明的决策解释和备选方案

### ✅ **3. 无缝执行**
- 统一的MCP协议接口
- 平台无关的执行体验
- 标准化的响应格式

### ✅ **4. 持续优化**
- 实时执行统计和性能监控
- 基于使用数据的工具推荐优化
- 动态的平台负载均衡

**这个重新设计的架构实现了真正的"统一工具注册表 + 智能路由 + MCP统一执行"，为用户提供最优的工具选择和无缝的执行体验！**

