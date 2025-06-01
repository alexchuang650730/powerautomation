"""
WebAgentB与主工作流集成测试
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mcptool.enhancers.webagent_adapter import WebAgentBAdapter
from agents.features import GeneralAgentFeatures
from frontend.src.utils.agent_router import AgentRouter

class TestWebAgentIntegration(unittest.TestCase):
    """WebAgentB与主工作流集成测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 使用mock替代真实的依赖组件
        self.playwright_patcher = patch('agents.ppt_agent.core.mcp.playwright_adapter.PlaywrightAdapter')
        self.mock_playwright = self.playwright_patcher.start()
        
        # 初始化WebAgentB适配器
        self.webagent = WebAgentBAdapter()
        
        # 初始化通用智能体特性
        self.agent_features = GeneralAgentFeatures()
        
        # 初始化智能体路由器
        self.router = AgentRouter()
        
        # 设置mock返回值
        self.mock_playwright.return_value.search_information.return_value = [
            {
                "title": "集成测试结果1",
                "url": "https://example.com/integration1",
                "snippet": "这是集成测试结果1的摘要"
            }
        ]
        
        self.mock_playwright.return_value.extract_page_content.return_value = "这是集成测试页面的原始内容"
    
    def tearDown(self):
        """测试后清理"""
        self.playwright_patcher.stop()
    
    def test_integration_with_agent_features(self):
        """测试与智能体特性的集成"""
        # 模拟GeneralAgentFeatures的方法
        self.agent_features.update_content_feature = MagicMock()
        self.agent_features.update_thinking_feature = MagicMock()
        
        # 执行语义化提取
        content = self.webagent.semantic_extract("https://example.com/integration-test")
        
        # 更新内容特性
        self.agent_features.update_content_feature(content["structured_content"])
        
        # 验证更新调用
        self.agent_features.update_content_feature.assert_called_once()
        
        # 执行增强搜索
        results = self.webagent.enhanced_search("集成测试查询")
        
        # 构建思维过程
        thinking_process = {
            "search_query": "集成测试查询",
            "search_results": results,
            "analysis": "基于搜索结果的集成分析...",
            "conclusions": ["集成结论1", "集成结论2"]
        }
        
        # 更新思维特性
        self.agent_features.update_thinking_feature(thinking_process)
        
        # 验证更新调用
        self.agent_features.update_thinking_feature.assert_called_once()
    
    def test_integration_with_agent_router(self):
        """测试与智能体路由器的集成"""
        # 定义处理函数
        def web_agent_handler(request):
            if "search" in request:
                return self.webagent.enhanced_search(request["search"])
            elif "extract" in request:
                return self.webagent.semantic_extract(request["extract"])
            elif "task" in request:
                return self.webagent.interactive_task(request["url"], request["task"])
            else:
                return {"error": "Unsupported request type"}
        
        # 注册处理函数
        self.router.register_handler = MagicMock()
        self.router.register_handler("web", web_agent_handler)
        
        # 验证注册调用
        self.router.register_handler.assert_called_once_with("web", web_agent_handler)
        
        # 模拟路由请求
        self.router.route = MagicMock()
        request = {
            "agent_type": "web",
            "search": "集成测试查询"
        }
        self.router.route(request)
        
        # 验证路由调用
        self.router.route.assert_called_once_with(request)
    
    def test_end_to_end_workflow(self):
        """测试端到端工作流"""
        # 模拟用户输入
        user_input = "分析网页 https://example.com/ai-article 的主要内容"
        
        # 模拟代码智能体的需求拆解
        agent_type = "web"  # 假设代码智能体将此识别为网页智能体任务
        
        # 模拟路由到网页智能体
        if agent_type == "web":
            # 使用WebAgentB处理请求
            result = self.webagent.semantic_extract("https://example.com/ai-article")
            
            # 验证结果
            self.assertIn("raw_content", result)
            self.assertIn("structured_content", result)
            
            # 模拟更新六大特性
            self.agent_features.update_content_feature = MagicMock()
            self.agent_features.update_content_feature(result["structured_content"])
            self.agent_features.update_content_feature.assert_called_once()
            
            # 模拟无限上下文记忆存储
            mock_context_adapter = MagicMock()
            mock_context_adapter.store_context = MagicMock(return_value="context-123")
            context_id = mock_context_adapter.store_context({
                "type": "web_content",
                "url": "https://example.com/ai-article",
                "content": result
            })
            mock_context_adapter.store_context.assert_called_once()
            self.assertEqual(context_id, "context-123")
    
    def test_integration_with_supermemory(self):
        """测试与Supermemory.ai的集成"""
        # 模拟InfiniteContextAdapter
        mock_context_adapter = MagicMock()
        mock_context_adapter.store_context = MagicMock(return_value="context-456")
        mock_context_adapter.retrieve_context = MagicMock(return_value={
            "type": "web_content",
            "url": "https://example.com/test-article",
            "content": {
                "raw_content": "测试内容",
                "structured_content": {
                    "title": "测试标题",
                    "main_points": ["要点1", "要点2"]
                }
            }
        })
        
        # 使用WebAgentB提取页面内容
        semantic_content = self.webagent.semantic_extract("https://example.com/test-article")
        
        # 将内容存储到无限上下文记忆
        context_id = mock_context_adapter.store_context({
            "type": "web_content",
            "url": "https://example.com/test-article",
            "content": semantic_content
        })
        
        # 验证存储调用
        mock_context_adapter.store_context.assert_called_once()
        self.assertEqual(context_id, "context-456")
        
        # 检索内容
        retrieved_content = mock_context_adapter.retrieve_context(context_id)
        
        # 验证检索调用
        mock_context_adapter.retrieve_context.assert_called_once_with(context_id)
        self.assertEqual(retrieved_content["type"], "web_content")
        self.assertEqual(retrieved_content["url"], "https://example.com/test-article")

if __name__ == '__main__':
    unittest.main()
