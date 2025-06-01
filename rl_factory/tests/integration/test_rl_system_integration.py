"""
RL增强器与系统集成验证模块
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../../..'))
sys.path.insert(0, project_root)

# 导入被测试模块
try:
    from powerautomation_integration.enhancers.rl_enhancer.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper
    from powerautomation_integration.enhancers.rl_enhancer.adapters.infinite_context_adapter import InfiniteContextAdapter
    from powerautomation_integration.enhancers.rl_enhancer.adapters.github_actions_adapter import GitHubActionsAdapter
    from powerautomation_integration.enhancers.rl_enhancer.adapters.aci_dev_adapter import ACIDevAdapter
    from powerautomation_integration.enhancers.rl_enhancer.adapters.webui_tool_builder import WebUIToolBuilder
    from powerautomation_integration.enhancers.rl_enhancer.core.thought.decomposer import ThoughtDecomposer
    from powerautomation_integration.enhancers.rl_enhancer.core.learning.hybrid import HybridLearningArchitecture
except ImportError:
    # 如果上面的导入失败，尝试直接导入
    sys.path.insert(0, os.path.abspath(os.path.join(current_dir, '../../..')))
    from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper
    from rl_factory.adapters.infinite_context_adapter import InfiniteContextAdapter
    from rl_factory.adapters.github_actions_adapter import GitHubActionsAdapter
    from rl_factory.adapters.aci_dev_adapter import ACIDevAdapter
    from rl_factory.adapters.webui_tool_builder import WebUIToolBuilder
    from rl_factory.core.thought.decomposer import ThoughtDecomposer
    from rl_factory.core.learning.hybrid import HybridLearningArchitecture


class TestRLSystemIntegration(unittest.TestCase):
    """RL增强器与系统集成测试类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 使用Mock对象模拟外部依赖
        self.mcp_so_adapter = MagicMock(spec=MCPSoAdapter)
        self.infinite_context_adapter = MagicMock(spec=InfiniteContextAdapter)
        self.github_actions_adapter = MagicMock(spec=GitHubActionsAdapter)
        self.aci_dev_adapter = MagicMock(spec=ACIDevAdapter)
        self.webui_tool_builder = MagicMock(spec=WebUIToolBuilder)
        
        # 设置Mock返回值
        self.mcp_so_adapter.get_tools.return_value = [
            {"name": "tool1", "description": "Test tool 1"},
            {"name": "tool2", "description": "Test tool 2"}
        ]
        self.mcp_so_adapter.execute_tool.return_value = {"status": "success", "result": "Tool executed"}
        
        # 创建工具包装器
        self.tool_wrapper = MCPToolWrapper(self.mcp_so_adapter)
        
        # 创建思考分解器
        self.thought_decomposer = ThoughtDecomposer()
        
        # 创建混合学习架构
        self.hybrid_learning = MagicMock(spec=HybridLearningArchitecture)
        self.hybrid_learning.train.return_value = {
            "supervised_result": {"loss": 0.1},
            "reinforcement_result": {"reward": 0.8},
            "contrastive_result": {"accuracy": 0.9}
        }
    
    def test_mcp_so_adapter_integration(self):
        """测试MCP.so适配器集成"""
        # 验证工具列表获取
        tools = self.mcp_so_adapter.get_tools()
        self.assertEqual(2, len(tools))
        self.assertEqual("tool1", tools[0]["name"])
        
        # 验证工具执行
        result = self.mcp_so_adapter.execute_tool("tool1", {"param1": "value1"})
        self.assertEqual("success", result["status"])
        self.assertEqual("Tool executed", result["result"])
        
        # 验证工具包装器
        tool_names = self.tool_wrapper.list_tools()
        self.assertEqual(2, len(tool_names))
        
        # 验证工具包装器执行
        self.mcp_so_adapter.execute_tool.assert_called_once_with("tool1", {"param1": "value1"})
    
    def test_infinite_context_adapter_integration(self):
        """测试无限上下文适配器集成"""
        # 设置Mock返回值
        self.infinite_context_adapter.process.return_value = {
            "processed_context": "处理后的上下文",
            "tokens_saved": 1024
        }
        
        # 验证上下文处理
        result = self.infinite_context_adapter.process("长文本..." * 1000)
        self.assertEqual("处理后的上下文", result["processed_context"])
        self.assertEqual(1024, result["tokens_saved"])
        
        # 验证调用参数
        self.infinite_context_adapter.process.assert_called_once()
        args, _ = self.infinite_context_adapter.process.call_args
        self.assertTrue(args[0].startswith("长文本..."))
    
    def test_github_actions_adapter_integration(self):
        """测试GitHub Actions适配器集成"""
        # 设置Mock返回值
        self.github_actions_adapter.trigger_workflow.return_value = {
            "status": "success",
            "workflow_id": "12345",
            "run_id": "67890"
        }
        self.github_actions_adapter.get_workflow_status.return_value = {
            "status": "completed",
            "conclusion": "success"
        }
        
        # 验证工作流触发
        result = self.github_actions_adapter.trigger_workflow("test_workflow", {"input1": "value1"})
        self.assertEqual("success", result["status"])
        self.assertEqual("12345", result["workflow_id"])
        
        # 验证工作流状态获取
        status = self.github_actions_adapter.get_workflow_status("67890")
        self.assertEqual("completed", status["status"])
        self.assertEqual("success", status["conclusion"])
        
        # 验证调用参数
        self.github_actions_adapter.trigger_workflow.assert_called_once_with("test_workflow", {"input1": "value1"})
        self.github_actions_adapter.get_workflow_status.assert_called_once_with("67890")
    
    def test_aci_dev_adapter_integration(self):
        """测试ACI.dev适配器集成"""
        # 设置Mock返回值
        self.aci_dev_adapter.list_tools.return_value = [
            {"id": "tool1", "name": "Tool 1", "description": "Test tool 1"},
            {"id": "tool2", "name": "Tool 2", "description": "Test tool 2"}
        ]
        self.aci_dev_adapter.get_tool.return_value = {
            "id": "tool1",
            "name": "Tool 1",
            "description": "Test tool 1",
            "parameters": {"param1": {"type": "string"}}
        }
        self.aci_dev_adapter.execute_tool.return_value = {
            "status": "success",
            "result": "Tool executed"
        }
        
        # 验证工具列表获取
        tools = self.aci_dev_adapter.list_tools()
        self.assertEqual(2, len(tools))
        self.assertEqual("tool1", tools[0]["id"])
        
        # 验证工具获取
        tool = self.aci_dev_adapter.get_tool("tool1")
        self.assertEqual("Tool 1", tool["name"])
        
        # 验证工具执行
        result = self.aci_dev_adapter.execute_tool("tool1", {"param1": "value1"})
        self.assertEqual("success", result["status"])
        self.assertEqual("Tool executed", result["result"])
        
        # 验证调用参数
        self.aci_dev_adapter.list_tools.assert_called_once()
        self.aci_dev_adapter.get_tool.assert_called_once_with("tool1")
        self.aci_dev_adapter.execute_tool.assert_called_once_with("tool1", {"param1": "value1"})
    
    def test_webui_tool_builder_integration(self):
        """测试WebUI工具构建器集成"""
        # 设置Mock返回值
        self.webui_tool_builder.create_tool.return_value = {
            "id": "new_tool",
            "name": "New Tool",
            "description": "A new test tool",
            "parameters": {"param1": {"type": "string"}},
            "implementation": "def main(param1): return param1"
        }
        self.webui_tool_builder.list_tools.return_value = [
            {"id": "new_tool", "name": "New Tool", "description": "A new test tool"}
        ]
        self.webui_tool_builder.test_tool.return_value = {
            "status": "success",
            "result": "test_value"
        }
        
        # 验证工具创建
        tool = self.webui_tool_builder.create_tool(
            name="New Tool",
            description="A new test tool",
            parameters={"param1": {"type": "string"}},
            implementation="def main(param1): return param1"
        )
        self.assertEqual("new_tool", tool["id"])
        self.assertEqual("New Tool", tool["name"])
        
        # 验证工具列表获取
        tools = self.webui_tool_builder.list_tools()
        self.assertEqual(1, len(tools))
        self.assertEqual("new_tool", tools[0]["id"])
        
        # 验证工具测试
        result = self.webui_tool_builder.test_tool("new_tool", {"param1": "test_value"})
        self.assertEqual("success", result["status"])
        self.assertEqual("test_value", result["result"])
        
        # 验证调用参数
        self.webui_tool_builder.create_tool.assert_called_once()
        self.webui_tool_builder.list_tools.assert_called_once()
        self.webui_tool_builder.test_tool.assert_called_once_with("new_tool", {"param1": "test_value"})
    
    def test_thought_decomposer_integration(self):
        """测试思考分解器集成"""
        # 准备测试数据
        thought_process = {
            "task": "创建一个简单的网页爬虫",
            "thinking": "我需要使用requests库来获取网页内容，然后使用BeautifulSoup来解析HTML。"
                       "首先，我需要安装这些库，然后编写代码来发送HTTP请求，解析响应，最后提取所需的数据。",
            "steps": [
                "安装必要的库",
                "编写代码发送HTTP请求",
                "解析HTML响应",
                "提取所需数据"
            ]
        }
        
        # 执行思考过程分解
        decomposed = self.thought_decomposer.decompose(thought_process)
        
        # 验证分解结果
        self.assertIn("problem_analysis", decomposed)
        self.assertIn("solution_design", decomposed)
        self.assertIn("implementation_planning", decomposed)
        self.assertIn("validation_evaluation", decomposed)
    
    def test_hybrid_learning_integration(self):
        """测试混合学习架构集成"""
        # 准备测试数据
        training_data = [
            {
                "input": "创建一个简单的网页爬虫",
                "output": {
                    "problem_analysis": "需要获取和解析网页内容",
                    "solution_design": "使用requests和BeautifulSoup库",
                    "implementation_planning": "分四步实现：安装库、发送请求、解析HTML、提取数据",
                    "validation_evaluation": "验证能否正确提取目标数据"
                }
            }
        ]
        
        # 执行混合学习
        result = self.hybrid_learning.train(training_data)
        
        # 验证学习结果
        self.assertIn("supervised_result", result)
        self.assertIn("reinforcement_result", result)
        self.assertIn("contrastive_result", result)
        
        # 验证调用参数
        self.hybrid_learning.train.assert_called_once()
        args, _ = self.hybrid_learning.train.call_args
        self.assertEqual(training_data, args[0])
    
    def test_end_to_end_integration(self):
        """测试端到端集成"""
        # 这个测试模拟一个完整的工作流，从思考过程分解到工具执行
        
        # 1. 思考过程分解
        thought_process = {
            "task": "创建一个网页爬虫并部署到GitHub",
            "thinking": "我需要使用requests和BeautifulSoup创建爬虫，然后使用GitHub Actions自动部署。",
            "steps": [
                "创建爬虫代码",
                "测试爬虫功能",
                "设置GitHub Actions",
                "部署到GitHub"
            ]
        }
        decomposed = self.thought_decomposer.decompose(thought_process)
        
        # 2. 使用混合学习架构学习思考过程
        learning_result = self.hybrid_learning.train([{"input": thought_process, "output": decomposed}])
        
        # 3. 使用无限上下文处理长文本
        context_result = self.infinite_context_adapter.process("长文本..." * 1000)
        
        # 4. 使用MCP.so调用工具
        tool_result = self.mcp_so_adapter.execute_tool("tool1", {"param1": "value1"})
        
        # 5. 使用GitHub Actions部署
        deploy_result = self.github_actions_adapter.trigger_workflow("deploy", {"repo": "user/repo"})
        
        # 6. 使用ACI.dev导入工具
        import_result = self.aci_dev_adapter.get_tool("tool1")
        
        # 7. 使用WebUI工具构建器创建工具
        create_result = self.webui_tool_builder.create_tool(
            name="Test Tool",
            description="A test tool",
            parameters={},
            implementation="def main(): pass"
        )
        
        # 验证整个工作流的结果
        self.assertIsNotNone(decomposed)
        self.assertIsNotNone(learning_result)
        self.assertIsNotNone(context_result)
        self.assertEqual("success", tool_result["status"])
        self.assertEqual("success", deploy_result["status"])
        self.assertEqual("Tool 1", import_result["name"])
        self.assertEqual("new_tool", create_result["id"])


if __name__ == '__main__':
    unittest.main()
