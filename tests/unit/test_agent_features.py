"""
单元测试：智能体六大特性定义模块
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.features.agent_features import (
    AgentFeatures, 
    PPTAgentFeatures, 
    WebAgentFeatures, 
    CodeAgentFeatures, 
    GeneralAgentFeatures
)

class TestAgentFeatures(unittest.TestCase):
    """测试基础AgentFeatures类"""
    
    def setUp(self):
        """测试前准备"""
        self.features = AgentFeatures()
    
    def test_init_default_values(self):
        """测试默认值初始化"""
        self.assertEqual(self.features.platform_feature, "")
        self.assertEqual(self.features.ui_layout, "")
        self.assertEqual(self.features.prompt, "")
        self.assertEqual(self.features.thinking, "")
        self.assertEqual(self.features.content, "")
        self.assertEqual(self.features.memory, "")
    
    def test_init_custom_values(self):
        """测试自定义值初始化"""
        custom_features = AgentFeatures(
            platform_feature="测试平台特性",
            ui_layout="测试UI布局",
            prompt="测试提示词",
            thinking="测试思维",
            content="测试内容",
            memory="测试记忆长度"
        )
        
        self.assertEqual(custom_features.platform_feature, "测试平台特性")
        self.assertEqual(custom_features.ui_layout, "测试UI布局")
        self.assertEqual(custom_features.prompt, "测试提示词")
        self.assertEqual(custom_features.thinking, "测试思维")
        self.assertEqual(custom_features.content, "测试内容")
        self.assertEqual(custom_features.memory, "测试记忆长度")
    
    def test_to_dict(self):
        """测试转换为字典"""
        custom_features = AgentFeatures(
            platform_feature="测试平台特性",
            ui_layout="测试UI布局",
            prompt="测试提示词",
            thinking="测试思维",
            content="测试内容",
            memory="测试记忆长度"
        )
        
        features_dict = custom_features.to_dict()
        
        self.assertEqual(features_dict["platform_feature"], "测试平台特性")
        self.assertEqual(features_dict["ui_layout"], "测试UI布局")
        self.assertEqual(features_dict["prompt"], "测试提示词")
        self.assertEqual(features_dict["thinking"], "测试思维")
        self.assertEqual(features_dict["content"], "测试内容")
        self.assertEqual(features_dict["memory"], "测试记忆长度")
    
    def test_from_dict(self):
        """测试从字典创建"""
        features_dict = {
            "platform_feature": "测试平台特性",
            "ui_layout": "测试UI布局",
            "prompt": "测试提示词",
            "thinking": "测试思维",
            "content": "测试内容",
            "memory": "测试记忆长度"
        }
        
        features = AgentFeatures.from_dict(features_dict)
        
        self.assertEqual(features.platform_feature, "测试平台特性")
        self.assertEqual(features.ui_layout, "测试UI布局")
        self.assertEqual(features.prompt, "测试提示词")
        self.assertEqual(features.thinking, "测试思维")
        self.assertEqual(features.content, "测试内容")
        self.assertEqual(features.memory, "测试记忆长度")
    
    def test_update_feature(self):
        """测试更新特性"""
        self.features.update_feature("platform_feature", "新平台特性")
        self.assertEqual(self.features.platform_feature, "新平台特性")
        
        self.features.update_feature("ui_layout", "新UI布局")
        self.assertEqual(self.features.ui_layout, "新UI布局")
        
        # 测试无效特性名
        with self.assertRaises(ValueError):
            self.features.update_feature("invalid_feature", "无效值")


class TestPPTAgentFeatures(unittest.TestCase):
    """测试PPT智能体特性"""
    
    def setUp(self):
        """测试前准备"""
        self.features = PPTAgentFeatures()
    
    def test_default_values(self):
        """测试默认值"""
        self.assertIn("PPT", self.features.platform_feature)
        self.assertIn("幻灯片", self.features.content)


class TestWebAgentFeatures(unittest.TestCase):
    """测试网页智能体特性"""
    
    def setUp(self):
        """测试前准备"""
        self.features = WebAgentFeatures()
    
    def test_default_values(self):
        """测试默认值"""
        self.assertIn("网页", self.features.platform_feature)
        self.assertIn("网站", self.features.content)


class TestCodeAgentFeatures(unittest.TestCase):
    """测试代码智能体特性"""
    
    def setUp(self):
        """测试前准备"""
        self.features = CodeAgentFeatures()
    
    def test_default_values(self):
        """测试默认值"""
        self.assertIn("代码", self.features.platform_feature)
        self.assertIn("编程", self.features.content)


class TestGeneralAgentFeatures(unittest.TestCase):
    """测试通用智能体特性"""
    
    def setUp(self):
        """测试前准备"""
        self.features = GeneralAgentFeatures()
    
    def test_default_values(self):
        """测试默认值"""
        self.assertIn("通用", self.features.platform_feature)
        self.assertIn("多种类型", self.features.content)


if __name__ == '__main__':
    unittest.main()
