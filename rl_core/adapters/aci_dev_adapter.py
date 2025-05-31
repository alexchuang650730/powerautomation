"""
ACI.dev适配器，用于与ACI.dev平台交互
"""
import os
import json
import requests
from typing import Dict, List, Any, Optional

class ACIDevAdapter:
    """ACI.dev适配器类"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.aci.dev/v1"):
        """
        初始化ACI.dev适配器
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key or os.environ.get("ACI_DEV_API_KEY")
        self.base_url = base_url
        
        if not self.api_key:
            print("警告: 未提供ACI.dev API密钥，某些功能可能不可用")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        获取工具列表
        
        Returns:
            工具列表
        """
        url = f"{self.base_url}/tools"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["tools"]
        except Exception as e:
            print(f"获取工具列表失败: {str(e)}")
            return []
    
    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """
        获取工具详情
        
        Args:
            tool_id: 工具ID
            
        Returns:
            工具详情
        """
        url = f"{self.base_url}/tools/{tool_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["tool"]
        except Exception as e:
            print(f"获取工具详情失败: {str(e)}")
            return None
    
    def execute_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具
        
        Args:
            tool_id: 工具ID
            parameters: 工具参数
            
        Returns:
            执行结果
        """
        url = f"{self.base_url}/tools/{tool_id}/execute"
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, json={"parameters": parameters})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"执行工具失败: {str(e)}")
            return {"status": "error", "error": str(e)}
