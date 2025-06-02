#!/usr/bin/env python3
"""
PPT Agent 意图路由集成模块
负责将PPT相关意图从通用智能体路由到PPT智能体
"""

import logging
from typing import Dict, Any
from ..general_agent.intent_router import IntentRouter
from .ppt_agent_features import PptAgentFeatures

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ppt_agent_router')

class PptAgentRouter:
    """
    PPT智能体路由器类
    负责处理PPT相关意图的路由和特性校验
    """
    
    def __init__(self):
        """初始化PPT智能体路由器"""
        self.intent_router = IntentRouter()
        self.ppt_features = PptAgentFeatures()
        logger.info("PPT智能体路由器初始化完成")
        
    def validate_features(self) -> bool:
        """
        通过SuperMemory API验证PPT智能体六大特性定义
        确保特性定义完整且未被修改
        
        返回:
            bool: 验证成功返回True，否则返回False
        """
        # 实际应用中应调用SuperMemory API进行验证
        # 此处为模拟实现
        features = self.ppt_features.get_features()
        
        # 检查六大特性是否完整
        required_features = ["platform", "ui_layout", "prompt_template", 
                            "thinking_content_generation", "content", "memory"]
        
        for feature in required_features:
            if feature not in features:
                logger.error(f"PPT智能体特性验证失败: 缺少{feature}特性")
                return False
                
        # 检查SuperMemory集成是否存在
        if "super_memory_integration" not in features["memory"]:
            logger.error("PPT智能体特性验证失败: 缺少SuperMemory集成")
            return False
            
        logger.info("PPT智能体六大特性验证成功")
        return True
        
    def should_route_to_ppt_agent(self, user_input: str, context: Dict[str, Any] = None) -> bool:
        """
        判断是否应将请求路由到PPT智能体
        
        参数:
            user_input: 用户输入的文本
            context: 上下文信息 (可选)
            
        返回:
            bool: 如果应路由到PPT智能体则返回True，否则返回False
        """
        # 如果上下文中已指定使用PPT智能体，直接返回True
        if context and context.get("current_agent") == "ppt":
            return True
            
        # 检查是否有PPT相关意图
        agent_type, confidence = self.intent_router.analyze_intent(user_input)
        
        # 如果直接识别为PPT意图且置信度高，返回True
        if agent_type == "ppt" and confidence > 0.6:
            logger.info(f"直接识别为PPT意图，置信度: {confidence:.2f}")
            return True
            
        # 如果在通用上下文中检测到PPT相关意图，返回True
        if self.intent_router.check_ppt_intent_in_general_context(user_input):
            logger.info("在通用上下文中检测到PPT相关意图")
            return True
            
        return False
        
    def route_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理用户请求，决定是否路由到PPT智能体
        
        参数:
            user_input: 用户输入的文本
            context: 上下文信息 (可选)
            
        返回:
            dict: 包含路由信息的字典
        """
        if context is None:
            context = {}
            
        # 首先验证PPT智能体六大特性
        if not self.validate_features():
            logger.warning("PPT智能体特性验证失败，使用通用智能体处理请求")
            return {
                "agent_type": "general",
                "reason": "ppt_agent_validation_failed",
                "user_input": user_input
            }
            
        # 判断是否应路由到PPT智能体
        if self.should_route_to_ppt_agent(user_input, context):
            logger.info("请求已路由至PPT智能体")
            return {
                "agent_type": "ppt",
                "user_input": user_input,
                "timestamp": context.get("timestamp", None),
                "session_id": context.get("session_id", None)
            }
        else:
            # 使用通用路由器决定路由目标
            return self.intent_router.route_to_agent(user_input, context)

# 示例用法
if __name__ == "__main__":
    router = PptAgentRouter()
    
    # 测试不同类型的输入
    test_inputs = [
        "帮我制作一个公司介绍的PPT",
        "我需要将这个数据可视化成幻灯片",
        "如何在PPT中添加动画效果？",
        "帮我写一个Python函数计算斐波那契数列",
        "我想设计一个响应式网站",
        "请帮我分析这份报告，并制作成PPT演示文稿"
    ]
    
    for input_text in test_inputs:
        result = router.route_request(input_text)
        print(f"输入: '{input_text}'")
        print(f"路由结果: {result['agent_type']}")
        print("-" * 50)
