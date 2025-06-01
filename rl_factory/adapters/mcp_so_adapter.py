"""
mcp.so适配器，用于与mcp.so库进行交互
"""
import os
import ctypes
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import numpy as np


class MCPSoAdapter:
    """mcp.so适配器，用于与mcp.so库进行交互"""
    
    def __init__(self, lib_path: str = "/path/to/mcp.so"):
        """
        初始化mcp.so适配器
        
        Args:
            lib_path: mcp.so库路径
        """
        # 加载动态库
        try:
            self.lib = ctypes.CDLL(lib_path)
            self._setup_function_signatures()
            self.initialized = True
        except Exception as e:
            print(f"Failed to load mcp.so: {e}")
            self.initialized = False
    
    def _setup_function_signatures(self):
        """设置函数签名"""
        # 初始化MCP
        self.lib.mcp_initialize.argtypes = [ctypes.c_char_p]
        self.lib.mcp_initialize.restype = ctypes.c_int
        
        # 执行MCP工具
        self.lib.mcp_execute_tool.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.mcp_execute_tool.restype = ctypes.c_char_p
        
        # 获取MCP工具列表
        self.lib.mcp_get_tools.argtypes = []
        self.lib.mcp_get_tools.restype = ctypes.c_char_p
        
        # 释放MCP资源
        self.lib.mcp_finalize.argtypes = []
        self.lib.mcp_finalize.restype = ctypes.c_int
    
    def initialize(self, config_path: str) -> bool:
        """
        初始化MCP
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            是否成功初始化
        """
        if not self.initialized:
            return False
        
        result = self.lib.mcp_initialize(config_path.encode('utf-8'))
        return result == 0
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行MCP工具
        
        Args:
            tool_name: 工具名称
            params: 工具参数
            
        Returns:
            执行结果
        """
        if not self.initialized:
            return {"error": "MCP not initialized"}
        
        # 将参数转换为JSON字符串
        params_json = json.dumps(params).encode('utf-8')
        
        # 执行工具
        result_ptr = self.lib.mcp_execute_tool(tool_name.encode('utf-8'), params_json)
        
        # 将结果转换为Python对象
        result_json = ctypes.string_at(result_ptr).decode('utf-8')
        result = json.loads(result_json)
        
        return result
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        获取MCP工具列表
        
        Returns:
            工具列表
        """
        if not self.initialized:
            return []
        
        # 获取工具列表
        tools_ptr = self.lib.mcp_get_tools()
        
        # 将结果转换为Python对象
        tools_json = ctypes.string_at(tools_ptr).decode('utf-8')
        tools = json.loads(tools_json)
        
        return tools
    
    def finalize(self) -> bool:
        """
        释放MCP资源
        
        Returns:
            是否成功释放
        """
        if not self.initialized:
            return False
        
        result = self.lib.mcp_finalize()
        return result == 0
    
    def __del__(self):
        """析构函数，确保资源被释放"""
        if hasattr(self, 'initialized') and self.initialized:
            self.finalize()


class MCPToolWrapper:
    """MCP工具包装器，提供更友好的接口"""
    
    def __init__(self, adapter: MCPSoAdapter):
        """
        初始化MCP工具包装器
        
        Args:
            adapter: MCP适配器
        """
        self.adapter = adapter
        self.tools = {}
        self._load_tools()
    
    def _load_tools(self):
        """加载工具列表"""
        tools = self.adapter.get_tools()
        
        for tool in tools:
            tool_name = tool.get("name", "")
            if tool_name:
                self.tools[tool_name] = tool
    
    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        执行工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            执行结果
        """
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        # 获取工具定义
        tool_def = self.tools[tool_name]
        
        # 验证参数
        required_params = []
        for param in tool_def.get("parameters", []):
            if param.get("required", False):
                required_params.append(param["name"])
        
        # 检查必需参数
        for param in required_params:
            if param not in kwargs:
                return {"error": f"Missing required parameter: {param}"}
        
        # 执行工具
        return self.adapter.execute_tool(tool_name, kwargs)
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        获取工具信息
        
        Args:
            tool_name: 工具名称
            
        Returns:
            工具信息
        """
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """
        列出所有工具
        
        Returns:
            工具名称列表
        """
        return list(self.tools.keys())


if __name__ == "__main__":
    # 示例用法（注意：实际运行需要正确的mcp.so路径）
    # 创建适配器
    adapter = MCPSoAdapter("/path/to/mcp.so")
    
    # 初始化
    if adapter.initialized:
        success = adapter.initialize("/path/to/config.json")
        if success:
            print("MCP initialized successfully")
            
            # 获取工具列表
            tools = adapter.get_tools()
            print(f"Available tools: {len(tools)}")
            
            # 创建工具包装器
            wrapper = MCPToolWrapper(adapter)
            
            # 列出工具
            tool_names = wrapper.list_tools()
            print(f"Tool names: {tool_names}")
            
            # 执行工具（示例）
            if "example_tool" in tool_names:
                result = wrapper.execute("example_tool", param1="value1", param2="value2")
                print(f"Tool execution result: {result}")
            
            # 释放资源
            adapter.finalize()
        else:
            print("Failed to initialize MCP")
    else:
        print("Failed to load MCP library")
