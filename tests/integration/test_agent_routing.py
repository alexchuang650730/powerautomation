"""
集成测试：多智能体路由与六特性存储
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from frontend.src.utils.agent_router import AgentRouter
from frontend.src.utils.agent_decomposer import AgentDecomposer
from agents.features.agent_features import GeneralAgentFeatures

class TestAgentRouting(unittest.TestCase):
    """测试多智能体路由功能"""
    
    def setUp(self):
        """测试前准备"""
        self.router = AgentRouter()
        self.decomposer = AgentDecomposer()
    
    @patch('frontend.src.utils.agent_router.requests.post')
    def test_code_query_routing(self, mock_post):
        """测试代码相关查询路由到代码智能体"""
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'agent': 'code',
            'response': '这是代码智能体的响应'
        }
        mock_post.return_value = mock_response
        
        # 测试代码相关查询
        query = "帮我写一个Python函数计算斐波那契数列"
        result = self.router.route_query(query)
        
        # 验证结果
        self.assertEqual(result['agent'], 'code')
        self.assertTrue(result['success'])
        self.assertEqual(result['response'], '这是代码智能体的响应')
        
        # 验证调用了正确的API
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('/api/code_agent', kwargs['url'])
    
    @patch('frontend.src.utils.agent_router.requests.post')
    def test_general_query_routing(self, mock_post):
        """测试通用查询路由到通用智能体"""
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'agent': 'general',
            'response': '这是通用智能体的响应'
        }
        mock_post.return_value = mock_response
        
        # 测试通用查询
        query = "今天天气怎么样？"
        result = self.router.route_query(query)
        
        # 验证结果
        self.assertEqual(result['agent'], 'general')
        self.assertTrue(result['success'])
        self.assertEqual(result['response'], '这是通用智能体的响应')
        
        # 验证调用了正确的API
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('/api/general_agent', kwargs['url'])
    
    def test_query_decomposition(self):
        """测试查询分解功能"""
        # 测试代码相关查询
        query = "帮我写一个Python函数计算斐波那契数列"
        agent_type = self.decomposer.decompose_query(query)
        self.assertEqual(agent_type, 'code')
        
        # 测试PPT相关查询
        query = "创建一个关于气候变化的PPT演示文稿"
        agent_type = self.decomposer.decompose_query(query)
        self.assertEqual(agent_type, 'ppt')
        
        # 测试网页相关查询
        query = "设计一个电子商务网站的首页"
        agent_type = self.decomposer.decompose_query(query)
        self.assertEqual(agent_type, 'web')
        
        # 测试通用查询
        query = "今天天气怎么样？"
        agent_type = self.decomposer.decompose_query(query)
        self.assertEqual(agent_type, 'general')


class TestFeatureStorage(unittest.TestCase):
    """测试六特性存储功能"""
    
    def setUp(self):
        """测试前准备"""
        self.features = GeneralAgentFeatures()
        self.decomposer = AgentDecomposer()
    
    def test_feature_extraction(self):
        """测试特性提取功能"""
        # 测试平台特性提取
        query = "优化PowerAutomation的平台特性"
        feature_type, feature_value = self.decomposer.extract_feature_update(query)
        self.assertEqual(feature_type, 'platform_feature')
        self.assertIn('PowerAutomation', feature_value)
        
        # 测试UI布局特性提取
        query = "改进PowerAutomation的UI布局，使用两栏设计"
        feature_type, feature_value = self.decomposer.extract_feature_update(query)
        self.assertEqual(feature_type, 'ui_layout')
        self.assertIn('两栏', feature_value)
        
        # 测试提示词特性提取
        query = "优化PowerAutomation的提示词特性，使其更接近Skywork.ai"
        feature_type, feature_value = self.decomposer.extract_feature_update(query)
        self.assertEqual(feature_type, 'prompt')
        self.assertIn('Skywork.ai', feature_value)
    
    def test_feature_update(self):
        """测试特性更新功能"""
        # 更新平台特性
        self.features.update_feature('platform_feature', 'PowerAutomation自动化平台')
        self.assertEqual(self.features.platform_feature, 'PowerAutomation自动化平台')
        
        # 更新UI布局特性
        self.features.update_feature('ui_layout', '两栏布局，左侧为导航栏，右侧为主内容区')
        self.assertEqual(self.features.ui_layout, '两栏布局，左侧为导航栏，右侧为主内容区')
        
        # 更新提示词特性
        self.features.update_feature('prompt', '类似Skywork.ai的提示词设计')
        self.assertEqual(self.features.prompt, '类似Skywork.ai的提示词设计')
        
        # 更新思维特性
        self.features.update_feature('thinking', '系统思考过程和决策逻辑')
        self.assertEqual(self.features.thinking, '系统思考过程和决策逻辑')
        
        # 更新内容特性
        self.features.update_feature('content', '处理用户输入，生成相应内容')
        self.assertEqual(self.features.content, '处理用户输入，生成相应内容')
        
        # 更新记忆特性
        self.features.update_feature('memory', '无限上下文记忆能力')
        self.assertEqual(self.features.memory, '无限上下文记忆能力')


if __name__ == '__main__':
    unittest.main()
