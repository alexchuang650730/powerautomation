"""
网页智能体模块 - Web Agent

提供网页抓取、内容分析、数据提取和自动化操作功能，作为PowerAutomation平台的网页处理组件。
通过MCP规划器和MCP头脑风暴器调用开发工具模块和已有工具。
"""

import os
import json
from ..base.base_agent import BaseAgent
from ...agents.ppt_agent.core.mcp.mcp_planner import MCPPlanner
from ...agents.ppt_agent.core.mcp.mcp_brainstorm import MCPBrainstorm
from ...development_tools.thought_action_recorder import ThoughtActionRecorder

class WebAgent(BaseAgent):
    def __init__(self, agent_id: str = None):
        """
        初始化网页智能体
        
        参数:
            agent_id: 智能体ID，如果不提供则自动生成
        """
        super().__init__(
            agent_id=agent_id,
            name="网页智能体",
            description="高效的网页抓取与自动化操作智能体"
        )
        
        # 初始化MCP规划器和头脑风暴器
        self.mcp_planner = MCPPlanner()
        self.mcp_brainstorm = MCPBrainstorm()
        
        # 初始化思考与操作记录器
        self.recorder = ThoughtActionRecorder()
        
        # 初始化会话ID
        self.session_id = None
    
    def get_capabilities(self):
        """
        获取网页智能体能力列表
        
        返回:
            能力描述列表
        """
        return [
            "网页内容抓取",
            "数据提取与结构化",
            "网页自动化操作",
            "内容分析与摘要",
            "多页面导航与数据聚合"
        ]
    
    def process(self, input_data):
        """
        处理输入数据并返回结果
        
        参数:
            input_data: 输入数据字典
            
        返回:
            处理结果字典
        """
        task_type = input_data.get("task_type", "")
        
        if task_type == "extract_data":
            url = input_data.get("url", "")
            extraction_query = input_data.get("extraction_query", "")
            return self.extract_data(url, extraction_query)
            
        elif task_type == "automate_task":
            url = input_data.get("url", "")
            task = input_data.get("task", "")
            return self.automate_task(url, task)
            
        elif task_type == "analyze_content":
            url = input_data.get("url", "")
            analysis_type = input_data.get("analysis_type", "general")
            analysis_query = input_data.get("analysis_query", "")
            return self.analyze_content(url, analysis_type, analysis_query)
            
        else:
            return {"status": "error", "message": f"不支持的任务类型: {task_type}"}
    
    def _start_session(self):
        """启动新的会话"""
        self.session_id = self.recorder.start_session("web_agent")
        return self.session_id
    
    def _record_thought(self, thought):
        """记录思考过程"""
        if self.session_id:
            self.recorder.record_thought(self.session_id, thought)
    
    def _record_action(self, action, params=None, result=None):
        """记录执行的操作"""
        if self.session_id:
            self.recorder.record_action(self.session_id, action, params, result)
    
    def extract_data(self, url, extraction_query=None):
        """
        从指定网页提取数据
        
        参数:
        - url: 网页URL
        - extraction_query: 提取指令
        
        返回:
        - 提取的数据
        """
        self._start_session()
        self._record_thought(f"准备从网页 {url} 提取数据")
        
        # 使用MCP规划器解析提取指令
        self._record_thought("使用MCP规划器解析提取指令")
        parsed_query = self.mcp_planner.plan({
            "type": "extraction_query",
            "url": url,
            "query": extraction_query
        })
        
        # 如果MCP规划器无法处理，尝试使用MCP头脑风暴器
        if not parsed_query.get("success"):
            self._record_thought("MCP规划器无法处理，尝试使用MCP头脑风暴器")
            parsed_query = self.mcp_brainstorm.generate({
                "type": "extraction_query",
                "url": url,
                "query": extraction_query
            })
        
        # 使用MCP规划器确定最佳提取策略
        self._record_thought("使用MCP规划器确定最佳提取策略")
        extraction_strategy = self.mcp_planner.plan({
            "type": "extraction_strategy",
            "url": url,
            "parsed_query": parsed_query
        })
        
        # 使用MCP规划器执行提取操作
        self._record_thought("使用MCP规划器执行提取操作")
        extraction_result = self.mcp_planner.plan({
            "type": "extraction_execution",
            "url": url,
            "strategy": extraction_strategy
        })
        
        # 记录操作和结果
        self._record_action("extract_data", {
            "url": url,
            "extraction_strategy": extraction_strategy
        }, extraction_result)
        
        return extraction_result.get("data", {
            "type": "extraction",
            "data": [
                {"title": "示例数据1", "content": "这是示例内容1"},
                {"title": "示例数据2", "content": "这是示例内容2"}
            ]
        })
    
    def automate_task(self, url, task):
        """
        在指定网页执行自动化任务
        
        参数:
        - url: 网页URL
        - task: 自动化任务描述
        
        返回:
        - 执行结果
        """
        self._start_session()
        self._record_thought(f"准备在网页 {url} 执行自动化任务: {task}")
        
        # 使用MCP规划器解析任务
        self._record_thought("使用MCP规划器解析任务")
        parsed_task = self.mcp_planner.plan({
            "type": "automation_task",
            "url": url,
            "task": task
        })
        
        # 使用MCP规划器生成操作步骤
        self._record_thought("使用MCP规划器生成操作步骤")
        operation_steps = self.mcp_planner.plan({
            "type": "automation_steps",
            "url": url,
            "parsed_task": parsed_task
        })
        
        # 使用MCP规划器执行自动化操作
        self._record_thought("使用MCP规划器执行自动化操作")
        automation_result = self.mcp_planner.plan({
            "type": "automation_execution",
            "url": url,
            "steps": operation_steps
        })
        
        # 记录操作和结果
        self._record_action("automate_task", {
            "url": url,
            "operation_steps": operation_steps
        }, automation_result)
        
        return automation_result.get("data", {
            "type": "automation",
            "steps": [
                f"打开网页: {url}",
                "执行操作1",
                "执行操作2",
                "操作完成"
            ],
            "status": "success"
        })
    
    def analyze_content(self, url, analysis_type="general", analysis_query=""):
        """
        分析指定网页的内容
        
        参数:
        - url: 网页URL
        - analysis_type: 分析类型
        - analysis_query: 分析要求
        
        返回:
        - 分析结果
        """
        self._start_session()
        self._record_thought(f"准备分析网页 {url} 的内容，类型: {analysis_type}，要求: {analysis_query}")
        
        # 使用MCP规划器解析分析要求
        self._record_thought("使用MCP规划器解析分析要求")
        parsed_query = self.mcp_planner.plan({
            "type": "analysis_query",
            "url": url,
            "analysis_type": analysis_type,
            "query": analysis_query
        })
        
        # 使用MCP规划器确定最佳分析策略
        self._record_thought("使用MCP规划器确定最佳分析策略")
        analysis_strategy = self.mcp_planner.plan({
            "type": "analysis_strategy",
            "url": url,
            "parsed_query": parsed_query
        })
        
        # 使用MCP规划器执行内容分析
        self._record_thought("使用MCP规划器执行内容分析")
        analysis_result = self.mcp_planner.plan({
            "type": "analysis_execution",
            "url": url,
            "strategy": analysis_strategy
        })
        
        # 记录操作和结果
        self._record_action("analyze_content", {
            "url": url,
            "analysis_strategy": analysis_strategy
        }, analysis_result)
        
        return analysis_result.get("data", {
            "type": "analysis",
            "summary": "这是网页内容的分析摘要",
            "keyPoints": [
                "关键点1",
                "关键点2",
                "关键点3"
            ]
        })
