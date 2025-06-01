"""
基础MCP适配器模块

提供MCP适配器的基类实现
"""

from typing import Dict, Any, List, Optional
import logging


class BaseMCP:
    """MCP适配器基类，所有MCP适配器都应继承此类"""
    
    def __init__(self, name: str = "BaseMCP"):
        """
        初始化基础MCP适配器
        
        Args:
            name: 适配器名称
        """
        self.name = name
        self.logger = logging.getLogger(f"MCP.{name}")
        self.logger.info(f"初始化MCP适配器: {name}")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果字典
        """
        self.logger.warning("BaseMCP.process()被调用，这是一个应该被子类覆盖的方法")
        return {
            "status": "error",
            "message": "BaseMCP.process()是一个抽象方法，应该被子类覆盖"
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        验证输入数据是否有效
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            数据是否有效
        """
        self.logger.warning("BaseMCP.validate_input()被调用，这是一个应该被子类覆盖的方法")
        return True
    
    def get_capabilities(self) -> List[str]:
        """
        获取适配器能力列表
        
        Returns:
            能力描述列表
        """
        return ["基础MCP适配功能"]
