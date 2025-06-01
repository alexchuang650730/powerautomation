"""
ACI.dev集成适配器，用于与ACI.dev平台进行交互
"""
import os
import json
import requests
from typing import Dict, List, Any, Optional

class ACIDevAdapter:
    """
    ACI.dev集成适配器，提供与ACI.dev平台的交互能力
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化ACI.dev适配器
        
        Args:
            api_key: ACI.dev API密钥，如果为None则尝试从环境变量获取
        """
        self.api_key = api_key or os.environ.get("ACI_DEV_API_KEY")
        if not self.api_key:
            raise ValueError("ACI.dev API密钥未提供，请通过参数传入或设置ACI_DEV_API_KEY环境变量")
        
        self.base_url = "https://api.aci.dev/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        获取ACI.dev平台上可用的工具列表
        
        Returns:
            工具列表，每个工具包含id、name、description等信息
        """
        response = requests.get(f"{self.base_url}/tools", headers=self.headers)
        response.raise_for_status()
        return response.json().get("tools", [])
    
    def get_tool_details(self, tool_id: str) -> Dict[str, Any]:
        """
        获取指定工具的详细信息
        
        Args:
            tool_id: 工具ID
            
        Returns:
            工具详细信息
        """
        response = requests.get(f"{self.base_url}/tools/{tool_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def execute_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行指定工具
        
        Args:
            tool_id: 工具ID
            parameters: 工具执行参数
            
        Returns:
            工具执行结果
        """
        payload = {
            "parameters": parameters
        }
        response = requests.post(
            f"{self.base_url}/tools/{tool_id}/execute", 
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def import_tool(self, tool_id: str) -> Dict[str, Any]:
        """
        将ACI.dev平台上的工具导入到本地MCP工具池
        
        Args:
            tool_id: 工具ID
            
        Returns:
            导入结果信息
        """
        # 获取工具详情
        tool_details = self.get_tool_details(tool_id)
        
        # 转换为MCP工具格式
        mcp_tool = {
            "id": tool_details["id"],
            "name": tool_details["name"],
            "description": tool_details["description"],
            "parameters": tool_details["parameters"],
            "source": "aci.dev",
            "source_id": tool_id
        }
        
        # 保存到本地工具池
        # 实际实现中应调用MCP工具池的注册接口
        return {
            "status": "success",
            "message": f"工具 {tool_details['name']} 已成功导入",
            "tool": mcp_tool
        }
    
    def sync_tools(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        同步ACI.dev平台上的工具到本地MCP工具池
        
        Args:
            category: 可选的工具类别过滤
            
        Returns:
            同步结果信息
        """
        # 获取工具列表
        tools = self.list_tools()
        
        # 按类别过滤
        if category:
            tools = [t for t in tools if t.get("category") == category]
        
        # 导入每个工具
        imported_tools = []
        for tool in tools:
            try:
                result = self.import_tool(tool["id"])
                if result["status"] == "success":
                    imported_tools.append(result["tool"])
            except Exception as e:
                print(f"导入工具 {tool['name']} 失败: {str(e)}")
        
        return {
            "status": "success",
            "message": f"成功同步 {len(imported_tools)} 个工具",
            "tools": imported_tools
        }
