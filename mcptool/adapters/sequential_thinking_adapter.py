"""
Sequential Thinking适配器模块

提供Sequential Thinking能力的MCP适配器实现
"""

from typing import Dict, Any, List, Optional
import logging
from .base_mcp import BaseMCP

class SequentialThinkingAdapter(BaseMCP):
    """Sequential Thinking适配器，提供思维链和任务分解能力"""
    
    def __init__(self):
        """初始化Sequential Thinking适配器"""
        super().__init__(name="SequentialThinking")
    
    def decompose_task(self, task_description: str) -> List[Dict[str, Any]]:
        """
        分解任务为步骤序列
        
        Args:
            task_description: 任务描述
            
        Returns:
            分解后的任务步骤列表
        """
        self.logger.info(f"分解任务: {task_description}")
        
        # 简单实现，实际应用中应该有更复杂的逻辑
        steps = [
            {
                "step_id": 1,
                "description": f"分析任务: {task_description}",
                "status": "pending"
            },
            {
                "step_id": 2,
                "description": "收集必要信息",
                "status": "pending"
            },
            {
                "step_id": 3,
                "description": "执行核心操作",
                "status": "pending"
            },
            {
                "step_id": 4,
                "description": "验证结果",
                "status": "pending"
            },
            {
                "step_id": 5,
                "description": "总结并完成任务",
                "status": "pending"
            }
        ]
        
        return steps
    
    def create_todo_md(self, steps: List[Dict[str, Any]]) -> str:
        """
        创建todo.md文件内容
        
        Args:
            steps: 任务步骤列表
            
        Returns:
            todo.md文件内容
        """
        self.logger.info("创建todo.md")
        
        lines = ["# 任务计划\n"]
        
        for step in steps:
            status_mark = "[ ]" if step["status"] == "pending" else "[x]"
            lines.append(f"- {status_mark} {step['description']}")
        
        return "\n".join(lines)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果字典
        """
        if not self.validate_input(input_data):
            return {
                "status": "error",
                "message": "输入数据无效"
            }
        
        task_type = input_data.get("task_type", "decompose")
        
        if task_type == "decompose":
            task_description = input_data.get("task_description", "")
            steps = self.decompose_task(task_description)
            todo_md = self.create_todo_md(steps)
            
            return {
                "status": "success",
                "steps": steps,
                "todo_md": todo_md
            }
        else:
            return {
                "status": "error",
                "message": f"不支持的任务类型: {task_type}"
            }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        验证输入数据是否有效
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            数据是否有效
        """
        if "task_type" not in input_data:
            self.logger.error("缺少task_type字段")
            return False
            
        task_type = input_data["task_type"]
        
        if task_type == "decompose" and "task_description" not in input_data:
            self.logger.error("分解任务缺少task_description字段")
            return False
        
        return True
    
    def get_capabilities(self) -> List[str]:
        """
        获取适配器能力列表
        
        Returns:
            能力描述列表
        """
        return [
            "任务分解",
            "思维链生成",
            "todo.md创建"
        ]
