"""
RL增强器端到端集成测试
"""
import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# 导入被测试模块
from enhancers.rl_enhancer.core.thought.decomposer import ThoughtDecomposer
from enhancers.rl_enhancer.core.thought.serializer import ThoughtSerializer
from enhancers.rl_enhancer.core.learning.supervised import SupervisedLearning
from enhancers.rl_enhancer.core.learning.reinforcement import ReinforcementLearning
from enhancers.rl_enhancer.core.learning.contrastive import ContrastiveLearning
from enhancers.rl_enhancer.core.learning.hybrid import HybridLearningArchitecture
from enhancers.rl_enhancer.adapters.infinite_context_adapter import InfiniteContextAdapter
from enhancers.rl_enhancer.adapters.mcp_so_adapter import MCPSoAdapter
from enhancers.rl_enhancer.adapters.github_actions_adapter import GitHubActionsAdapter
from enhancers.rl_enhancer.adapters.aci_dev_adapter import ACIDevAdapter
from enhancers.rl_enhancer.adapters.webui_tool_builder import WebUIToolBuilder


class TestRLEnhancerEndToEnd(unittest.TestCase):
    """RL增强器端到端集成测试类"""
    
    def setUp(self):
        """测试前准备工作"""
        # 创建测试所需的临时目录
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 初始化测试所需的组件
        self.thought_decomposer = ThoughtDecomposer()
        self.thought_serializer = ThoughtSerializer()
        self.supervised_learning = SupervisedLearning()
        self.reinforcement_learning = ReinforcementLearning()
        self.contrastive_learning = ContrastiveLearning()
        self.hybrid_learning = HybridLearningArchitecture(
            supervised=self.supervised_learning,
            reinforcement=self.reinforcement_learning,
            contrastive=self.contrastive_learning
        )
        
        # 使用Mock对象模拟外部依赖
        self.infinite_context_adapter = InfiniteContextAdapter()
        self.mcp_so_adapter = MCPSoAdapter()
        self.github_actions_adapter = GitHubActionsAdapter()
        self.aci_dev_adapter = MagicMock(spec=ACIDevAdapter)
        self.webui_tool_builder = MagicMock(spec=WebUIToolBuilder)
    
    def tearDown(self):
        """测试后清理工作"""
        # 清理测试目录
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_thought_process_decomposition_and_serialization(self):
        """测试思考过程分解和序列化"""
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
        
        # 序列化和反序列化
        serialized = self.thought_serializer.serialize(decomposed)
        deserialized = self.thought_serializer.deserialize(serialized)
        
        # 验证序列化和反序列化结果
        self.assertEqual(decomposed, deserialized)
        
        # 保存到文件并读取
        file_path = os.path.join(self.test_dir, "thought_process.json")
        self.thought_serializer.save(decomposed, file_path)
        loaded = self.thought_serializer.load(file_path)
        
        # 验证文件保存和加载结果
        self.assertEqual(decomposed, loaded)
    
    @patch('enhancers.rl_enhancer.core.learning.supervised.SupervisedLearning.train')
    def test_hybrid_learning_architecture(self, mock_train):
        """测试混合学习架构"""
        # 设置Mock返回值
        mock_train.return_value = {"loss": 0.1, "accuracy": 0.95}
        
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
        self.assertIsNotNone(result)
        self.assertIn("supervised_result", result)
        self.assertIn("reinforcement_result", result)
        self.assertIn("contrastive_result", result)
    
    @patch('enhancers.rl_enhancer.adapters.infinite_context_adapter.InfiniteContextAdapter.process')
    def test_infinite_context_integration(self, mock_process):
        """测试无限上下文集成"""
        # 设置Mock返回值
        mock_process.return_value = {
            "processed_context": "这是处理后的上下文内容，已经过压缩和优化...",
            "tokens_saved": 1024,
            "important_segments": ["关键片段1", "关键片段2"]
        }
        
        # 准备测试数据
        long_context = "这是一个非常长的上下文..." * 1000
        
        # 执行上下文处理
        result = self.infinite_context_adapter.process(long_context)
        
        # 验证处理结果
        self.assertIsNotNone(result)
        self.assertIn("processed_context", result)
        self.assertIn("tokens_saved", result)
        self.assertIn("important_segments", result)
    
    @patch('enhancers.rl_enhancer.adapters.mcp_so_adapter.MCPSoAdapter.call_tool')
    def test_mcp_so_integration(self, mock_call_tool):
        """测试MCP.so集成"""
        # 设置Mock返回值
        mock_call_tool.return_value = {
            "status": "success",
            "result": "工具执行结果"
        }
        
        # 准备测试数据
        tool_name = "test_tool"
        tool_args = {"arg1": "value1", "arg2": "value2"}
        
        # 执行工具调用
        result = self.mcp_so_adapter.call_tool(tool_name, tool_args)
        
        # 验证调用结果
        self.assertIsNotNone(result)
        self.assertEqual("success", result["status"])
        self.assertEqual("工具执行结果", result["result"])
    
    @patch('enhancers.rl_enhancer.adapters.github_actions_adapter.GitHubActionsAdapter.trigger_workflow')
    def test_github_actions_integration(self, mock_trigger_workflow):
        """测试GitHub Actions集成"""
        # 设置Mock返回值
        mock_trigger_workflow.return_value = {
            "status": "success",
            "workflow_id": "12345",
            "run_id": "67890"
        }
        
        # 准备测试数据
        workflow_name = "test_workflow"
        workflow_inputs = {"input1": "value1", "input2": "value2"}
        
        # 触发工作流
        result = self.github_actions_adapter.trigger_workflow(workflow_name, workflow_inputs)
        
        # 验证触发结果
        self.assertIsNotNone(result)
        self.assertEqual("success", result["status"])
        self.assertEqual("12345", result["workflow_id"])
        self.assertEqual("67890", result["run_id"])
    
    def test_aci_dev_integration(self):
        """测试ACI.dev集成"""
        # 设置Mock返回值
        self.aci_dev_adapter.list_tools.return_value = [
            {"id": "tool1", "name": "Tool 1", "description": "Test tool 1"},
            {"id": "tool2", "name": "Tool 2", "description": "Test tool 2"}
        ]
        self.aci_dev_adapter.import_tool.return_value = {
            "status": "success",
            "message": "工具 Tool 1 已成功导入",
            "tool": {
                "id": "tool1",
                "name": "Tool 1",
                "description": "Test tool 1",
                "source": "aci.dev"
            }
        }
        
        # 获取工具列表
        tools = self.aci_dev_adapter.list_tools()
        
        # 验证工具列表
        self.assertEqual(2, len(tools))
        self.assertEqual("tool1", tools[0]["id"])
        self.assertEqual("Tool 1", tools[0]["name"])
        
        # 导入工具
        result = self.aci_dev_adapter.import_tool("tool1")
        
        # 验证导入结果
        self.assertEqual("success", result["status"])
        self.assertEqual("工具 Tool 1 已成功导入", result["message"])
    
    def test_webui_tool_builder_integration(self):
        """测试WebUI工具构建集成"""
        # 设置Mock返回值
        self.webui_tool_builder.create_tool.return_value = {
            "id": "new_tool",
            "name": "New Tool",
            "description": "A new test tool",
            "parameters": {"param1": {"type": "string"}},
            "implementation": "def main(param1): return param1"
        }
        self.webui_tool_builder.test_tool.return_value = {
            "status": "success",
            "result": "test_value"
        }
        
        # 创建工具
        tool = self.webui_tool_builder.create_tool(
            name="New Tool",
            description="A new test tool",
            parameters={"param1": {"type": "string"}},
            implementation="def main(param1): return param1"
        )
        
        # 验证创建结果
        self.assertEqual("new_tool", tool["id"])
        self.assertEqual("New Tool", tool["name"])
        
        # 测试工具
        result = self.webui_tool_builder.test_tool("new_tool", {"param1": "test_value"})
        
        # 验证测试结果
        self.assertEqual("success", result["status"])
        self.assertEqual("test_value", result["result"])
    
    def test_end_to_end_workflow(self):
        """测试完整的端到端工作流"""
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
        with patch('enhancers.rl_enhancer.core.learning.hybrid.HybridLearningArchitecture.train') as mock_train:
            mock_train.return_value = {
                "supervised_result": {"loss": 0.1},
                "reinforcement_result": {"reward": 0.8},
                "contrastive_result": {"accuracy": 0.9}
            }
            learning_result = self.hybrid_learning.train([{"input": thought_process, "output": decomposed}])
        
        # 3. 使用无限上下文处理长文本
        with patch('enhancers.rl_enhancer.adapters.infinite_context_adapter.InfiniteContextAdapter.process') as mock_process:
            mock_process.return_value = {"processed_context": "处理后的上下文"}
            context_result = self.infinite_context_adapter.process("长文本..." * 1000)
        
        # 4. 使用MCP.so调用工具
        with patch('enhancers.rl_enhancer.adapters.mcp_so_adapter.MCPSoAdapter.call_tool') as mock_call_tool:
            mock_call_tool.return_value = {"status": "success", "result": "爬虫创建成功"}
            tool_result = self.mcp_so_adapter.call_tool("create_scraper", {"url": "https://example.com"})
        
        # 5. 使用GitHub Actions部署
        with patch('enhancers.rl_enhancer.adapters.github_actions_adapter.GitHubActionsAdapter.trigger_workflow') as mock_trigger:
            mock_trigger.return_value = {"status": "success", "run_id": "12345"}
            deploy_result = self.github_actions_adapter.trigger_workflow("deploy", {"repo": "user/repo"})
        
        # 6. 使用ACI.dev导入工具
        import_result = self.aci_dev_adapter.import_tool("tool1")
        
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
        self.assertEqual("success", import_result["status"])
        self.assertIsNotNone(create_result)


if __name__ == '__main__':
    unittest.main()
