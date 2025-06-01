"""
WebAgentB适配器单元测试
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from mcptool.enhancers.webagent_adapter import WebAgentBAdapter

class TestWebAgentBAdapter(unittest.TestCase):
    """WebAgentB适配器单元测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 使用mock替代真实的Playwright适配器
        self.playwright_patcher = patch('agents.ppt_agent.core.mcp.playwright_adapter.PlaywrightAdapter')
        self.mock_playwright = self.playwright_patcher.start()
        
        # 初始化WebAgentB适配器
        self.webagent = WebAgentBAdapter()
        
        # 设置mock返回值
        self.mock_playwright.return_value.search_information.return_value = [
            {
                "title": "测试结果1",
                "url": "https://example.com/result1",
                "snippet": "这是测试结果1的摘要"
            },
            {
                "title": "测试结果2",
                "url": "https://example.com/result2",
                "snippet": "这是测试结果2的摘要"
            }
        ]
        
        self.mock_playwright.return_value.extract_page_content.return_value = "这是测试页面的原始内容"
    
    def tearDown(self):
        """测试后清理"""
        self.playwright_patcher.stop()
    
    def test_initialization(self):
        """测试初始化"""
        self.assertTrue(hasattr(self.webagent, 'playwright'))
        self.assertTrue(hasattr(self.webagent, 'available'))
        self.assertTrue(self.webagent.available)
    
    def test_enhanced_search(self):
        """测试增强搜索功能"""
        results = self.webagent.enhanced_search("测试查询", depth=1)
        
        # 验证结果数量
        self.assertEqual(len(results), 2)
        
        # 验证结果内容
        self.assertEqual(results[0]["title"], "测试结果1")
        self.assertEqual(results[0]["url"], "https://example.com/result1")
        self.assertEqual(results[0]["snippet"], "这是测试结果1的摘要")
        
        # 验证增强内容
        self.assertIn("semantic_analysis", results[0])
        self.assertIn("key_concepts", results[0]["semantic_analysis"])
        self.assertIn("sentiment", results[0]["semantic_analysis"])
        self.assertIn("relevance_score", results[0]["semantic_analysis"])
    
    def test_semantic_extract(self):
        """测试语义化提取功能"""
        content = self.webagent.semantic_extract("https://example.com/test")
        
        # 验证原始内容
        self.assertEqual(content["raw_content"], "这是测试页面的原始内容")
        
        # 验证结构化内容
        self.assertIn("structured_content", content)
        self.assertIn("title", content["structured_content"])
        self.assertIn("main_points", content["structured_content"])
        self.assertIn("entities", content["structured_content"])
        self.assertIn("code_snippets", content["structured_content"])
    
    def test_interactive_task(self):
        """测试交互式任务功能"""
        result = self.webagent.interactive_task(
            "https://example.com/form", 
            "填写表单并提交"
        )
        
        # 验证任务结果
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["url"], "https://example.com/form")
        self.assertEqual(result["task_description"], "填写表单并提交")
        self.assertIn("steps_executed", result)
        self.assertIn("screenshots", result)
    
    def test_unavailable_webagent(self):
        """测试WebAgentB不可用的情况"""
        # 设置WebAgentB为不可用
        self.webagent.available = False
        
        # 测试增强搜索
        results = self.webagent.enhanced_search("测试查询")
        self.assertEqual(len(results), 2)
        self.assertNotIn("semantic_analysis", results[0])
        
        # 测试语义化提取
        content = self.webagent.semantic_extract("https://example.com/test")
        self.assertEqual(content["raw_content"], "这是测试页面的原始内容")
        self.assertNotIn("structured_content", content)
        
        # 测试交互式任务
        result = self.webagent.interactive_task(
            "https://example.com/form", 
            "填写表单并提交"
        )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["message"], "WebAgentB不可用")
    
    def test_integration_with_agent_features(self):
        """测试与智能体特性的集成"""
        # 模拟GeneralAgentFeatures
        mock_features = MagicMock()
        
        # 执行语义化提取
        content = self.webagent.semantic_extract("https://example.com/test")
        
        # 更新内容特性
        mock_features.update_content_feature(content["structured_content"])
        
        # 验证更新调用
        mock_features.update_content_feature.assert_called_once()
        
        # 执行增强搜索
        results = self.webagent.enhanced_search("测试查询")
        
        # 构建思维过程
        thinking_process = {
            "search_query": "测试查询",
            "search_results": results,
            "analysis": "基于搜索结果的分析...",
            "conclusions": ["结论1", "结论2"]
        }
        
        # 更新思维特性
        mock_features.update_thinking_feature(thinking_process)
        
        # 验证更新调用
        mock_features.update_thinking_feature.assert_called_once()

if __name__ == '__main__':
    unittest.main()
