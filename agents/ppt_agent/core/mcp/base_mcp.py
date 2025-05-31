"""
MCP基类模块

定义所有模块化认知处理器(MCP)的基础接口和共享功能
"""

from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, List, Optional

class BaseMCP(ABC):
    """MCP基类，定义所有模块化认知处理器的通用接口和功能"""
    
    def __init__(self, mcp_id: str, name: str, description: str = ""):
        """
        初始化MCP
        
        参数:
            mcp_id: MCP唯一标识符
            name: MCP名称
            description: MCP描述
        """
        self.mcp_id = mcp_id
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{self.mcp_id}")
        
    @abstractmethod
    def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理输入数据并返回结果
        
        参数:
            input_data: 输入数据字典
            context: 上下文信息字典
            
        返回:
            处理结果字典
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取MCP信息
        
        返回:
            MCP信息字典
        """
        return {
            "mcp_id": self.mcp_id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }
