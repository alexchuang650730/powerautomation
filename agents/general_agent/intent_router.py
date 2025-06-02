#!/usr/bin/env python3
"""
意图路由模块
负责识别用户输入中的意图，并将请求路由到合适的智能体
"""

import re
import json
import logging
from typing import Dict, Any, List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('intent_router')

class IntentRouter:
    """
    意图路由器类
    负责分析用户输入，识别意图，并路由到合适的智能体
    """
    
    def __init__(self):
        """初始化意图路由器"""
        self.agent_types = ["general", "code", "ppt", "web"]
        self.intent_patterns = self._load_intent_patterns()
        logger.info("意图路由器初始化完成")
        
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """
        加载各智能体的意图模式
        返回一个字典，键为智能体类型，值为对应的意图模式列表
        """
        # 实际应用中可从配置文件加载
        return {
            "general": [
                r".*帮我.*", 
                r".*如何.*",
                r".*能否.*",
                r".*请问.*",
                r".*我想.*"
            ],
            "code": [
                r".*代码.*",
                r".*编程.*",
                r".*函数.*",
                r".*类.*",
                r".*bug.*",
                r".*调试.*",
                r".*python.*",
                r".*java.*",
                r".*javascript.*",
                r".*html.*",
                r".*css.*",
                r".*api.*"
            ],
            "ppt": [
                r".*ppt.*",
                r".*幻灯片.*",
                r".*演示.*",
                r".*presentation.*",
                r".*slide.*",
                r".*模板.*template.*",
                r".*制作.*ppt.*",
                r".*创建.*幻灯片.*",
                r".*设计.*演示.*",
                r".*生成.*ppt.*",
                r".*转换.*ppt.*",
                r".*ppt.*转.*图片.*",
                r".*幻灯片.*转.*pdf.*"
            ],
            "web": [
                r".*网页.*",
                r".*网站.*",
                r".*html.*",
                r".*css.*",
                r".*javascript.*",
                r".*前端.*",
                r".*ui.*",
                r".*设计.*网页.*",
                r".*创建.*网站.*"
            ]
        }
    
    def analyze_intent(self, user_input: str) -> Tuple[str, float]:
        """
        分析用户输入，识别最可能的意图
        
        参数:
            user_input: 用户输入的文本
            
        返回:
            tuple: (智能体类型, 置信度)
        """
        scores = {agent_type: 0.0 for agent_type in self.agent_types}
        
        # 对每种智能体类型计算匹配分数
        for agent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    scores[agent_type] += 1.0
        
        # 找出得分最高的智能体类型
        best_agent = max(scores.items(), key=lambda x: x[1])
        agent_type, score = best_agent
        
        # 计算置信度 (简单实现，实际应用中可能需要更复杂的算法)
        total_score = sum(scores.values())
        confidence = score / total_score if total_score > 0 else 0.0
        
        # 如果最高分为0或置信度低于阈值，默认使用通用智能体
        if score == 0 or confidence < 0.4:
            return "general", 1.0
            
        logger.info(f"意图分析结果: {agent_type}, 置信度: {confidence:.2f}")
        return agent_type, confidence
    
    def route_to_agent(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        将用户请求路由到合适的智能体
        
        参数:
            user_input: 用户输入的文本
            context: 上下文信息 (可选)
            
        返回:
            dict: 包含路由信息的字典
        """
        if context is None:
            context = {}
            
        agent_type, confidence = self.analyze_intent(user_input)
        
        # 如果上下文中指定了智能体类型，且置信度不高，则使用上下文中的类型
        if "current_agent" in context and confidence < 0.7:
            agent_type = context["current_agent"]
            logger.info(f"基于上下文使用智能体: {agent_type}")
        
        # 构建路由结果
        result = {
            "agent_type": agent_type,
            "confidence": confidence,
            "user_input": user_input,
            "timestamp": context.get("timestamp", None),
            "session_id": context.get("session_id", None)
        }
        
        logger.info(f"请求已路由至: {agent_type} 智能体")
        return result
    
    def check_ppt_intent_in_general_context(self, user_input: str) -> bool:
        """
        在通用智能体上下文中检查是否有PPT相关意图
        用于实现当通用智能体遇到PPT相关意图时自动路由到PPT智能体
        
        参数:
            user_input: 用户输入的文本
            
        返回:
            bool: 如果检测到PPT相关意图则返回True，否则返回False
        """
        # 专门检查PPT相关意图
        for pattern in self.intent_patterns["ppt"]:
            if re.search(pattern, user_input, re.IGNORECASE):
                logger.info("在通用上下文中检测到PPT相关意图，建议路由到PPT智能体")
                return True
        return False

# 示例用法
if __name__ == "__main__":
    router = IntentRouter()
    
    # 测试不同类型的输入
    test_inputs = [
        "帮我写一个Python函数计算斐波那契数列",
        "请帮我制作一个公司介绍的PPT",
        "我需要一个响应式的网站首页设计",
        "如何提高工作效率？",
        "幻灯片中如何添加动画效果？",
        "我想把这个Word文档转成PPT"
    ]
    
    for input_text in test_inputs:
        result = router.route_to_agent(input_text)
        print(f"输入: '{input_text}'")
        print(f"路由结果: {result['agent_type']}, 置信度: {result['confidence']:.2f}")
        print("-" * 50)
        
    # 测试在通用上下文中检测PPT意图
    general_context = {"current_agent": "general"}
    ppt_in_general = "在我们讨论的这个问题中，我需要制作一个PPT来展示结果"
    
    result = router.route_to_agent(ppt_in_general, general_context)
    print(f"通用上下文中的PPT意图: '{ppt_in_general}'")
    print(f"路由结果: {result['agent_type']}, 置信度: {result['confidence']:.2f}")
    print(f"PPT意图检测: {router.check_ppt_intent_in_general_context(ppt_in_general)}")
