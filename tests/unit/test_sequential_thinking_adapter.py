"""
Sequential Thinking MCP单元测试
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mcptool.enhancers.sequential_thinking_adapter import SequentialThinkingAdapter

class TestSequentialThinkingAdapter(unittest.TestCase):
    """Sequential Thinking适配器单元测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 初始化Sequential Thinking适配器
        self.sequential = SequentialThinkingAdapter()
    
    def test_initialization(self):
        """测试初始化"""
        self.assertTrue(hasattr(self.sequential, 'logger'))
    
    def test_decompose_task(self):
        """测试任务分解功能"""
        task_description = "开发一个用户认证模块"
        context = {"platform": "web", "framework": "React"}
        
        result = self.sequential.decompose_task(task_description, context)
        
        # 验证结果结构
        self.assertIn("task", result)
        self.assertIn("subtasks", result)
        self.assertIn("context", result)
        
        # 验证任务描述
        self.assertEqual(result["task"], task_description)
        
        # 验证上下文
        self.assertEqual(result["context"], context)
        
        # 验证子任务
        self.assertTrue(len(result["subtasks"]) > 0)
        
        # 验证第一个子任务
        first_subtask = result["subtasks"][0]
        self.assertIn("id", first_subtask)
        self.assertIn("description", first_subtask)
        self.assertIn("estimated_time", first_subtask)
    
    def test_create_todo_md(self):
        """测试创建todo.md功能"""
        # 创建测试数据
        decomposed_task = {
            "task": "开发一个用户认证模块",
            "subtasks": [
                {
                    "id": "analyze",
                    "description": "分析用户认证模块的需求和上下文",
                    "estimated_time": "10分钟"
                },
                {
                    "id": "design",
                    "description": "设计用户认证模块的解决方案",
                    "estimated_time": "15分钟",
                    "depends_on": ["analyze"]
                }
            ],
            "context": {"platform": "web", "framework": "React"}
        }
        
        todo_md = self.sequential.create_todo_md(decomposed_task)
        
        # 验证todo.md内容
        self.assertIn("# 任务清单", todo_md)
        self.assertIn("[ ] 分析用户认证模块的需求和上下文", todo_md)
        self.assertIn("[ ] 设计用户认证模块的解决方案", todo_md)
        self.assertIn("(id:analyze)", todo_md)
        self.assertIn("(id:design)", todo_md)
    
    def test_reflect_and_refine(self):
        """测试反思和优化功能"""
        # 创建测试数据
        plan = {
            "task_structure": {
                "task": "开发一个用户认证模块",
                "subtasks": []
            },
            "execution_plans": ["步骤1", "步骤2", "步骤3"],
            "dependencies": {"step1": [], "step2": ["step1"], "step3": ["step2"]}
        }
        
        refined_plan = self.sequential.reflect_and_refine(plan)
        
        # 验证结果结构
        self.assertIn("reflections", refined_plan)
        self.assertIn("optimizations", refined_plan)
        
        # 验证反思内容
        self.assertTrue(len(refined_plan["reflections"]) > 0)
        
        # 验证原始计划保留
        self.assertEqual(refined_plan["task_structure"], plan["task_structure"])
        self.assertEqual(refined_plan["execution_plans"], plan["execution_plans"])
        self.assertEqual(refined_plan["dependencies"], plan["dependencies"])
    
    def test_has_circular_dependency(self):
        """测试循环依赖检测功能"""
        # 创建有循环依赖的数据
        circular_dependencies = {
            "task1": ["task2"],
            "task2": ["task1"]
        }
        
        # 创建无循环依赖的数据
        normal_dependencies = {
            "task1": ["task3"],
            "task2": ["task1"],
            "task3": []
        }
        
        # 验证循环依赖检测
        self.assertTrue(self.sequential._has_circular_dependency(circular_dependencies))
        self.assertFalse(self.sequential._has_circular_dependency(normal_dependencies))
    
    def test_update_todo_status(self):
        """测试更新todo状态功能"""
        # 创建测试数据
        todo_md = "# 任务清单\n\n[ ] 分析需求 (id:analyze)\n[ ] 设计方案 (id:design)\n"
        
        # 更新状态
        updated_todo = self.sequential.update_todo_status(todo_md, "analyze", True)
        
        # 验证更新结果
        self.assertIn("[x] 分析需求 (id:analyze)", updated_todo)
        self.assertIn("[ ] 设计方案 (id:design)", updated_todo)
        
        # 再次更新状态
        updated_todo = self.sequential.update_todo_status(updated_todo, "analyze", False)
        
        # 验证更新结果
        self.assertIn("[ ] 分析需求 (id:analyze)", updated_todo)
    
    def test_integration_with_agent_features(self):
        """测试与智能体特性的集成"""
        # 模拟GeneralAgentFeatures
        mock_features = MagicMock()
        mock_features.update_thinking_feature = MagicMock()
        
        # 分解任务
        task_description = "优化网站性能"
        decomposed_task = self.sequential.decompose_task(task_description)
        
        # 构建思维过程
        thinking_process = {
            "task": task_description,
            "decomposition": decomposed_task,
            "reasoning": "通过将任务分解为多个子任务，可以更有效地解决复杂问题...",
            "conclusions": ["结论1", "结论2", "结论3"]
        }
        
        # 更新思维特性
        mock_features.update_thinking_feature(thinking_process)
        
        # 验证更新调用
        mock_features.update_thinking_feature.assert_called_once_with(thinking_process)

if __name__ == '__main__':
    unittest.main()
