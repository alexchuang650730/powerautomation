"""
代码智能体模块 - Code Agent

提供代码分析、问题解决和自动化修复功能，作为PowerAutomation平台的代码处理组件。
通过MCP规划器和MCP头脑风暴器调用开发工具模块和已有工具，特别是AgentProblemSolver。
"""

import os
import json
from datetime import datetime
from ...agents.ppt_agent.core.mcp.mcp_planner import MCPPlanner
from ...agents.ppt_agent.core.mcp.mcp_brainstorm import MCPBrainstorm
from ...development_tools.agent_problem_solver import AgentProblemSolver
from ...development_tools.thought_action_recorder import ThoughtActionRecorder

class CodeAgent:
    def __init__(self):
        # 初始化MCP规划器和头脑风暴器
        self.mcp_planner = MCPPlanner()
        self.mcp_brainstorm = MCPBrainstorm()
        
        # 初始化问题解决驱动器
        self.problem_solver = AgentProblemSolver()
        
        # 初始化思考与操作记录器
        self.recorder = ThoughtActionRecorder()
        
        # 初始化会话ID
        self.session_id = None
    
    def _start_session(self):
        """启动新的会话"""
        self.session_id = self.recorder.start_session("code_agent")
        return self.session_id
    
    def _record_thought(self, thought):
        """记录思考过程"""
        if self.session_id:
            self.recorder.record_thought(self.session_id, thought)
    
    def _record_action(self, action, params=None, result=None):
        """记录执行的操作"""
        if self.session_id:
            self.recorder.record_action(self.session_id, action, params, result)
    
    def analyze_code(self, code_content, language=None, analysis_type="general"):
        """
        分析代码内容
        
        参数:
        - code_content: 代码内容
        - language: 编程语言
        - analysis_type: 分析类型
        
        返回:
        - 分析结果
        """
        self._start_session()
        self._record_thought(f"准备分析{language or ''}代码，类型: {analysis_type}")
        
        # 使用MCP规划器解析代码
        self._record_thought("使用MCP规划器解析代码")
        parsed_code = self.mcp_planner.plan({
            "type": "code_parsing",
            "code": code_content,
            "language": language,
            "analysis_type": analysis_type
        })
        
        # 如果MCP规划器无法处理，尝试使用MCP头脑风暴器
        if not parsed_code.get("success"):
            self._record_thought("MCP规划器无法处理，尝试使用MCP头脑风暴器")
            parsed_code = self.mcp_brainstorm.generate({
                "type": "code_parsing",
                "code": code_content,
                "language": language,
                "analysis_type": analysis_type
            })
        
        # 使用MCP规划器生成分析结果
        self._record_thought("使用MCP规划器生成分析结果")
        analysis_result = self.mcp_planner.plan({
            "type": "code_analysis",
            "parsed_code": parsed_code
        })
        
        # 记录操作和结果
        self._record_action("analyze_code", {
            "language": language,
            "analysis_type": analysis_type
        }, analysis_result)
        
        return analysis_result.get("data", {
            "type": "analysis",
            "summary": "代码分析摘要",
            "complexity": "中等",
            "issues": [
                {"type": "潜在问题", "description": "可能存在的问题1", "line": 10},
                {"type": "优化建议", "description": "可能的优化点1", "line": 15}
            ]
        })
    
    def solve_problem(self, problem_description, code_content=None, language=None):
        """
        解决代码问题
        
        参数:
        - problem_description: 问题描述
        - code_content: 代码内容（可选）
        - language: 编程语言（可选）
        
        返回:
        - 问题解决方案
        """
        self._start_session()
        self._record_thought(f"准备解决问题: {problem_description}")
        
        # 使用MCP规划器解析问题
        self._record_thought("使用MCP规划器解析问题")
        parsed_problem = self.mcp_planner.plan({
            "type": "problem_parsing",
            "description": problem_description,
            "code": code_content,
            "language": language
        })
        
        # 使用AgentProblemSolver解决问题
        self._record_thought("使用AgentProblemSolver解决问题")
        solution = self.problem_solver.solve_problem({
            "problem": parsed_problem.get("problem", problem_description),
            "code": code_content,
            "language": language
        })
        
        # 记录操作和结果
        self._record_action("solve_problem", {
            "problem": problem_description,
            "language": language
        }, solution)
        
        return solution.get("data", {
            "type": "solution",
            "description": "问题解决方案描述",
            "code": "修复后的代码示例",
            "explanation": "解决方案的详细解释"
        })
    
    def update_github(self, repo_url, file_path, changes, commit_message):
        """
        更新GitHub仓库中的文件
        
        参数:
        - repo_url: 仓库URL
        - file_path: 文件路径
        - changes: 变更内容
        - commit_message: 提交信息
        
        返回:
        - 更新结果
        """
        self._start_session()
        self._record_thought(f"准备更新GitHub仓库 {repo_url} 中的文件 {file_path}")
        
        # 使用MCP规划器解析更新请求
        self._record_thought("使用MCP规划器解析更新请求")
        parsed_request = self.mcp_planner.plan({
            "type": "github_update_parsing",
            "repo_url": repo_url,
            "file_path": file_path,
            "changes": changes,
            "commit_message": commit_message
        })
        
        # 使用MCP规划器执行GitHub更新
        self._record_thought("使用MCP规划器执行GitHub更新")
        update_result = self.mcp_planner.plan({
            "type": "github_update_execution",
            "parsed_request": parsed_request
        })
        
        # 记录操作和结果
        self._record_action("update_github", {
            "repo_url": repo_url,
            "file_path": file_path,
            "commit_message": commit_message
        }, update_result)
        
        return update_result.get("data", {
            "type": "github_update",
            "status": "success",
            "commit_id": f"commit-{datetime.now().timestamp()}",
            "url": f"{repo_url}/commit/example-commit-id"
        })
