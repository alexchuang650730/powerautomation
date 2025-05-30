"""
PPT智能体模块 - PPT Agent

提供PPT生成、思维导图转换和模板优化功能，作为PowerAutomation平台的PPT处理组件。
通过MCP规划器和MCP头脑风暴器调用开发工具模块和已有工具。
"""

import os
import json
from datetime import datetime
from .core.mcp.mcp_planner import MCPPlanner
from .core.mcp.mcp_brainstorm import MCPBrainstorm
from ...development_tools.thought_action_recorder import ThoughtActionRecorder

class PPTAgent:
    def __init__(self):
        # 初始化MCP规划器和头脑风暴器
        self.mcp_planner = MCPPlanner()
        self.mcp_brainstorm = MCPBrainstorm()
        
        # 初始化思考与操作记录器
        self.recorder = ThoughtActionRecorder()
        
        # 初始化会话ID
        self.session_id = None
    
    def _start_session(self):
        """启动新的会话"""
        self.session_id = self.recorder.start_session("ppt_agent")
        return self.session_id
    
    def _record_thought(self, thought):
        """记录思考过程"""
        if self.session_id:
            self.recorder.record_thought(self.session_id, thought)
    
    def _record_action(self, action, params=None, result=None):
        """记录执行的操作"""
        if self.session_id:
            self.recorder.record_action(self.session_id, action, params, result)
    
    def generate_ppt(self, topic, content=None, style=None, template=None):
        """
        生成PPT演示文稿
        
        参数:
        - topic: 主题
        - content: 内容（可选）
        - style: 样式（可选）
        - template: 模板（可选）
        
        返回:
        - 生成的PPT文件路径
        """
        self._start_session()
        self._record_thought(f"准备生成PPT，主题: {topic}")
        
        # 使用MCP规划器解析PPT需求
        self._record_thought("使用MCP规划器解析PPT需求")
        parsed_request = self.mcp_planner.plan({
            "type": "ppt_request_parsing",
            "topic": topic,
            "content": content,
            "style": style,
            "template": template
        })
        
        # 如果MCP规划器无法处理，尝试使用MCP头脑风暴器
        if not parsed_request.get("success"):
            self._record_thought("MCP规划器无法处理，尝试使用MCP头脑风暴器")
            parsed_request = self.mcp_brainstorm.generate({
                "type": "ppt_request_parsing",
                "topic": topic,
                "content": content,
                "style": style,
                "template": template
            })
        
        # 使用MCP规划器生成PPT内容结构
        self._record_thought("使用MCP规划器生成PPT内容结构")
        ppt_structure = self.mcp_planner.plan({
            "type": "ppt_structure_generation",
            "parsed_request": parsed_request
        })
        
        # 使用MCP规划器生成PPT
        self._record_thought("使用MCP规划器生成PPT")
        ppt_result = self.mcp_planner.plan({
            "type": "ppt_generation",
            "structure": ppt_structure,
            "style": style,
            "template": template
        })
        
        # 记录操作和结果
        self._record_action("generate_ppt", {
            "topic": topic,
            "style": style,
            "template": template
        }, ppt_result)
        
        return ppt_result.get("file_path", f"/tmp/generated_ppt_{datetime.now().timestamp()}.pptx")
    
    def mindmap_to_ppt(self, mindmap_data, style=None, template=None):
        """
        将思维导图转换为PPT
        
        参数:
        - mindmap_data: 思维导图数据
        - style: 样式（可选）
        - template: 模板（可选）
        
        返回:
        - 生成的PPT文件路径
        """
        self._start_session()
        self._record_thought("准备将思维导图转换为PPT")
        
        # 使用MCP规划器解析思维导图
        self._record_thought("使用MCP规划器解析思维导图")
        parsed_mindmap = self.mcp_planner.plan({
            "type": "mindmap_parsing",
            "mindmap_data": mindmap_data
        })
        
        # 使用MCP规划器生成PPT结构
        self._record_thought("使用MCP规划器生成PPT结构")
        ppt_structure = self.mcp_planner.plan({
            "type": "mindmap_to_ppt_structure",
            "parsed_mindmap": parsed_mindmap,
            "style": style,
            "template": template
        })
        
        # 使用MCP规划器生成PPT
        self._record_thought("使用MCP规划器生成PPT")
        ppt_result = self.mcp_planner.plan({
            "type": "ppt_generation",
            "structure": ppt_structure,
            "style": style,
            "template": template
        })
        
        # 记录操作和结果
        self._record_action("mindmap_to_ppt", {
            "mindmap_nodes": len(mindmap_data.get("nodes", [])),
            "style": style,
            "template": template
        }, ppt_result)
        
        return ppt_result.get("file_path", f"/tmp/mindmap_ppt_{datetime.now().timestamp()}.pptx")
    
    def generate_mindmap(self, topic, content=None):
        """
        生成思维导图
        
        参数:
        - topic: 主题
        - content: 内容（可选）
        
        返回:
        - 生成的思维导图数据
        """
        self._start_session()
        self._record_thought(f"准备生成思维导图，主题: {topic}")
        
        # 使用MCP规划器解析思维导图需求
        self._record_thought("使用MCP规划器解析思维导图需求")
        parsed_request = self.mcp_planner.plan({
            "type": "mindmap_request_parsing",
            "topic": topic,
            "content": content
        })
        
        # 使用MCP规划器生成思维导图
        self._record_thought("使用MCP规划器生成思维导图")
        mindmap_result = self.mcp_planner.plan({
            "type": "mindmap_generation",
            "parsed_request": parsed_request
        })
        
        # 记录操作和结果
        self._record_action("generate_mindmap", {
            "topic": topic
        }, mindmap_result)
        
        return mindmap_result.get("data", {
            "topic": topic,
            "nodes": [
                {"id": "root", "text": topic, "parent": ""},
                {"id": "node1", "text": "主要内容1", "parent": "root"},
                {"id": "node2", "text": "主要内容2", "parent": "root"},
                {"id": "node3", "text": "主要内容3", "parent": "root"},
                {"id": "node1.1", "text": "子内容1.1", "parent": "node1"},
                {"id": "node1.2", "text": "子内容1.2", "parent": "node1"},
                {"id": "node2.1", "text": "子内容2.1", "parent": "node2"}
            ]
        })
    
    def edit_mindmap(self, mindmap_data, changes):
        """
        编辑思维导图
        
        参数:
        - mindmap_data: 思维导图数据
        - changes: 变更内容
        
        返回:
        - 更新后的思维导图数据
        """
        self._start_session()
        self._record_thought("准备编辑思维导图")
        
        # 使用MCP规划器解析编辑请求
        self._record_thought("使用MCP规划器解析编辑请求")
        parsed_request = self.mcp_planner.plan({
            "type": "mindmap_edit_parsing",
            "mindmap_data": mindmap_data,
            "changes": changes
        })
        
        # 使用MCP规划器执行编辑操作
        self._record_thought("使用MCP规划器执行编辑操作")
        edit_result = self.mcp_planner.plan({
            "type": "mindmap_edit_execution",
            "parsed_request": parsed_request
        })
        
        # 记录操作和结果
        self._record_action("edit_mindmap", {
            "changes": changes
        }, edit_result)
        
        return edit_result.get("data", {
            "topic": mindmap_data.get("topic", "更新后的主题"),
            "nodes": mindmap_data.get("nodes", [])
        })
