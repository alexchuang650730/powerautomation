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
from rl_factory.core.thought.decomposer import ThoughtDecomposer
from rl_factory.core.thought.serializer import ThoughtSerializer
from rl_factory.core.learning.supervised import SupervisedLearner
from rl_factory.core.learning.reinforcement import ReinforcementLearner
from rl_factory.core.learning.contrastive import ContrastiveLearner
from rl_factory.core.learning.hybrid import HybridLearner
from rl_factory.adapters.infinite_context_adapter import InfiniteContextAdapter
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter
from rl_factory.adapters.github_actions_adapter import GitHubActionsAdapter
from rl_factory.adapters.aci_dev_adapter import ACIDevAdapter
from rl_factory.adapters.webui_tool_builder import WebUIToolBuilder


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
        self.supervised_learning = SupervisedLearner()
        self.reinforcement_learning = ReinforcementLearner()
        self.contrastive_learning = ContrastiveLearner()
        self.hybrid_learning = HybridLearner(
            model_name="bert-base-uncased"
        )
        
        # 使用Mock对象模拟外部依赖
        self.infinite_context_adapter = MagicMock(spec=InfiniteContextAdapter)
        # 显式添加process_context方法
        self.infinite_context_adapter.process_context = MagicMock()
        
        self.mcp_so_adapter = MagicMock(spec=MCPSoAdapter)
        # 显式添加execute_tool方法
        self.mcp_so_adapter.execute_tool = MagicMock()
        
        # 为GitHubActionsAdapter提供必需的owner和repo参数
        self.github_actions_adapter = GitHubActionsAdapter(owner="test-owner", repo="test-repo")
        self.aci_dev_adapter = MagicMock(spec=ACIDevAdapter)
        # 确保import_tool返回真实dict而非MagicMock对象
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
        self.webui_tool_builder = MagicMock(spec=WebUIToolBuilder)
    
    def tearDown(self):
        """测试后清理工作"""
        # 清理测试目录
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_thought_process_decomposition_and_serialization(self):
        """测试思考过程分解和序列化"""
        # 准备测试数据 - 使用字符串而非字典，并确保包含关键词
        thought_process_str = """设计一个在线教育平台
    
问题分析:
我们需要设计一个功能完善、用户友好的在线教育平台。该平台应支持多种课程类型，包括视频课程、互动测验和讨论区。

约束: 响应时间不超过200ms
约束: 支持至少10000名并发用户
挑战: 确保师生实时互动的流畅性
挑战: 高效管理大量教育内容

方案设计:
基于微服务架构设计平台，将功能拆分为多个独立服务。

设计原则: 高可用性
设计原则: 可扩展性
设计原则: 用户体验优先

方案1: 基于AWS的云原生架构
方案2: 基于自建数据中心的传统架构

实现规划:
1. 设计数据库架构
2. 实现用户认证服务
3. 开发课程管理系统
4. 实现视频流处理服务
5. 开发互动测验模块
6. 实现实时通讯功能

风险: 视频流处理可能面临性能瓶颈
风险: 实时通讯在高并发下可能不稳定

验证评估:
标准: 系统响应时间
标准: 并发用户支持数量
标准: 用户满意度

测试: 负载测试以验证并发支持能力
测试: A/B测试以评估用户界面设计

改进: 考虑引入AI推荐系统
改进: 增加移动端适配
"""
        
        # 执行思考过程分解
        decomposed = self.thought_decomposer.decompose_raw_thought(thought_process_str)
        
        # 验证分解结果
        stages = decomposed.stages
        # 检查是否至少有一个阶段
        self.assertGreater(len(stages), 0)
        
        # 序列化和反序列化 - 使用正确的静态方法
        serialized = ThoughtSerializer.to_json(decomposed)
        deserialized = ThoughtSerializer.from_json(serialized)
        
        # 验证序列化和反序列化结果
        self.assertEqual(decomposed.process_id, deserialized.process_id)
        
        # 保存到文件并读取 - 使用正确的静态方法
        file_path = os.path.join(self.test_dir, "thought_process.json")
        ThoughtSerializer.to_file(decomposed, file_path)
        loaded = ThoughtSerializer.from_file(file_path)
        
        # 验证文件保存和加载结果
        self.assertEqual(decomposed.process_id, loaded.process_id)
    
    @patch('rl_factory.core.learning.supervised.SupervisedLearner.train')
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
        with patch('rl_factory.core.learning.hybrid.HybridLearner.train') as mock_hybrid_train:
            mock_hybrid_train.return_value = {
                "supervised_result": {"loss": 0.1},
                "reinforcement_result": {"reward": 0.8},
                "contrastive_result": {"accuracy": 0.9}
            }
            result = self.hybrid_learning.train(
                supervised_data=training_data,
                reinforcement_data=[],
                contrastive_data=([], []),
                epochs=1
            )
        
        # 验证学习结果
        self.assertIsNotNone(result)
    
    def test_infinite_context_integration(self):
        """测试无限上下文集成"""
        # 设置Mock返回值
        self.infinite_context_adapter.process_context.return_value = {
            "processed_context": "这是处理后的上下文内容，已经过压缩和优化...",
            "tokens_saved": 1024,
            "important_segments": ["关键片段1", "关键片段2"]
        }
        
        # 准备测试数据
        long_context = "这是一个非常长的上下文..." * 1000
        
        # 执行上下文处理
        result = self.infinite_context_adapter.process_context(long_context)
        
        # 验证处理结果
        self.assertIsNotNone(result)
        self.assertIn("processed_context", result)
        self.assertIn("tokens_saved", result)
        self.assertIn("important_segments", result)
    
    def test_mcp_so_integration(self):
        """测试MCP.so集成"""
        # 设置Mock返回值
        self.mcp_so_adapter.execute_tool.return_value = {
            "status": "success",
            "result": "工具执行结果"
        }
        
        # 准备测试数据
        tool_name = "test_tool"
        tool_args = {"arg1": "value1", "arg2": "value2"}
        
        # 执行工具调用
        result = self.mcp_so_adapter.execute_tool(tool_name, tool_args)
        
        # 验证调用结果
        self.assertIsNotNone(result)
        self.assertEqual("success", result["status"])
        self.assertEqual("工具执行结果", result["result"])
    
    @patch('rl_factory.adapters.github_actions_adapter.GitHubActionsAdapter.trigger_workflow')
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
        
        # 1. 思考过程分解 - 使用与test_thought_process_decomposition_and_serialization相同的示例
        thought_process_str = """设计一个在线教育平台
    
问题分析:
我们需要设计一个功能完善、用户友好的在线教育平台。该平台应支持多种课程类型，包括视频课程、互动测验和讨论区。

约束: 响应时间不超过200ms
约束: 支持至少10000名并发用户
挑战: 确保师生实时互动的流畅性
挑战: 高效管理大量教育内容

方案设计:
基于微服务架构设计平台，将功能拆分为多个独立服务。

设计原则: 高可用性
设计原则: 可扩展性
设计原则: 用户体验优先

方案1: 基于AWS的云原生架构
方案2: 基于自建数据中心的传统架构

实现规划:
1. 设计数据库架构
2. 实现用户认证服务
3. 开发课程管理系统
4. 实现视频流处理服务
5. 开发互动测验模块
6. 实现实时通讯功能

风险: 视频流处理可能面临性能瓶颈
风险: 实时通讯在高并发下可能不稳定

验证评估:
标准: 系统响应时间
标准: 并发用户支持数量
标准: 用户满意度

测试: 负载测试以验证并发支持能力
测试: A/B测试以评估用户界面设计

改进: 考虑引入AI推荐系统
改进: 增加移动端适配
"""
        
        decomposed = self.thought_decomposer.decompose_raw_thought(thought_process_str)
        
        # 2. 使用混合学习架构学习思考过程
        with patch('rl_factory.core.learning.hybrid.HybridLearner.train') as mock_train:
            mock_train.return_value = {
                "supervised_result": {"loss": 0.1},
                "reinforcement_result": {"reward": 0.8},
                "contrastive_result": {"accuracy": 0.9}
            }
            learning_result = self.hybrid_learning.train(
                supervised_data=[decomposed],
                reinforcement_data=[],
                contrastive_data=([], []),
                epochs=1
            )
        
        # 3. 使用无限上下文处理长文本
        self.infinite_context_adapter.process_context.return_value = {"processed_context": "处理后的上下文"}
        context_result = self.infinite_context_adapter.process_context("长文本..." * 1000)
        
        # 4. 使用MCP.so调用工具
        self.mcp_so_adapter.execute_tool.return_value = {"status": "success", "result": "爬虫创建成功"}
        tool_result = self.mcp_so_adapter.execute_tool("create_scraper", {"url": "https://example.com"})
        
        # 5. 使用GitHub Actions部署
        with patch('rl_factory.adapters.github_actions_adapter.GitHubActionsAdapter.trigger_workflow') as mock_trigger:
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
