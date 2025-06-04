#!/usr/bin/env python3
"""
多模型协同集成测试
测试Claude、Gemini等多个AI模型的协同工作能力
"""

import sys
import os
import unittest
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mcptool.adapters.ai_enhanced_intent_understanding_mcp import AIEnhancedIntentUnderstandingMCP
from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP

class TestMultiModelSynergy(unittest.TestCase):
    """多模型协同测试"""
    
    def setUp(self):
        """测试初始化"""
        self.ai_adapter = AIEnhancedIntentUnderstandingMCP()
        self.workflow_engine = IntelligentWorkflowEngineMCP()
    
    def test_claude_gemini_collaboration(self):
        """测试Claude和Gemini协同分析"""
        test_request = {
            "user_input": "分析销售数据并生成报告",
            "context": {"department": "sales", "priority": "high"}
        }
        
        # 测试AI增强意图理解
        result = self.ai_adapter.process(test_request)
        
        self.assertIsInstance(result, dict)
        self.assertIn("intent_analysis", result)
        self.assertIn("complexity_score", result)
    
    def test_multi_model_consensus(self):
        """测试多模型一致性分析"""
        test_cases = [
            "创建一个网站",
            "分析用户行为数据",
            "优化系统性能"
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                result = self.ai_adapter.process({
                    "action": "analyze_intent",
                    "user_input": case
                })
                
                self.assertIsInstance(result, dict)
                self.assertIn("claude_analysis", result)
                self.assertIn("gemini_analysis", result)

if __name__ == "__main__":
    unittest.main()

