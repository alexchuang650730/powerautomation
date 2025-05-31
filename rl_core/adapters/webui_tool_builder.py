"""
WebUI工具构建器，用于创建和管理WebUI工具
"""
import os
import json
import uuid
from typing import Dict, List, Any, Optional

class WebUIToolBuilder:
    """WebUI工具构建器类"""
    
    def __init__(self, tools_dir: str = None):
        """
        初始化WebUI工具构建器
        
        Args:
            tools_dir: 工具目录
        """
        self.tools_dir = tools_dir or os.path.join(os.getcwd(), "tools")
        
        # 确保工具目录存在
        os.makedirs(self.tools_dir, exist_ok=True)
        
        # 工具缓存
        self.tools_cache = {}
        
        # 加载现有工具
        self._load_tools()
    
    def _load_tools(self):
        """加载现有工具"""
        for filename in os.listdir(self.tools_dir):
            if filename.endswith(".json"):
                tool_path = os.path.join(self.tools_dir, filename)
                with open(tool_path, "r") as f:
                    tool = json.load(f)
                    self.tools_cache[tool["id"]] = tool
    
    def create_tool(self, name: str, description: str, parameters: Dict[str, Any], implementation: str) -> Dict[str, Any]:
        """
        创建工具
        
        Args:
            name: 工具名称
            description: 工具描述
            parameters: 工具参数
            implementation: 工具实现代码
            
        Returns:
            创建的工具
        """
        # 生成工具ID
        tool_id = str(uuid.uuid4())
        
        # 创建工具
        tool = {
            "id": tool_id,
            "name": name,
            "description": description,
            "parameters": parameters,
            "implementation": implementation
        }
        
        # 保存工具
        tool_path = os.path.join(self.tools_dir, f"{tool_id}.json")
        with open(tool_path, "w") as f:
            json.dump(tool, f, indent=2)
        
        # 更新缓存
        self.tools_cache[tool_id] = tool
        
        return tool
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        获取工具列表
        
        Returns:
            工具列表
        """
        return [
            {
                "id": tool["id"],
                "name": tool["name"],
                "description": tool["description"]
            }
            for tool in self.tools_cache.values()
        ]
    
    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """
        获取工具详情
        
        Args:
            tool_id: 工具ID
            
        Returns:
            工具详情
        """
        return self.tools_cache.get(tool_id)
    
    def update_tool(self, tool_id: str, name: str = None, description: str = None, 
                   parameters: Dict[str, Any] = None, implementation: str = None) -> Optional[Dict[str, Any]]:
        """
        更新工具
        
        Args:
            tool_id: 工具ID
            name: 工具名称
            description: 工具描述
            parameters: 工具参数
            implementation: 工具实现代码
            
        Returns:
            更新后的工具
        """
        if tool_id not in self.tools_cache:
            return None
        
        tool = self.tools_cache[tool_id]
        
        # 更新工具
        if name:
            tool["name"] = name
        if description:
            tool["description"] = description
        if parameters:
            tool["parameters"] = parameters
        if implementation:
            tool["implementation"] = implementation
        
        # 保存工具
        tool_path = os.path.join(self.tools_dir, f"{tool_id}.json")
        with open(tool_path, "w") as f:
            json.dump(tool, f, indent=2)
        
        # 更新缓存
        self.tools_cache[tool_id] = tool
        
        return tool
    
    def delete_tool(self, tool_id: str) -> bool:
        """
        删除工具
        
        Args:
            tool_id: 工具ID
            
        Returns:
            是否成功删除
        """
        if tool_id not in self.tools_cache:
            return False
        
        # 删除工具文件
        tool_path = os.path.join(self.tools_dir, f"{tool_id}.json")
        if os.path.exists(tool_path):
            os.remove(tool_path)
        
        # 从缓存中删除
        del self.tools_cache[tool_id]
        
        return True
    
    def test_tool(self, tool_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        测试工具
        
        Args:
            tool_id: 工具ID
            parameters: 工具参数
            
        Returns:
            测试结果
        """
        if tool_id not in self.tools_cache:
            return {"status": "error", "error": "工具不存在"}
        
        tool = self.tools_cache[tool_id]
        
        try:
            # 创建临时Python文件
            temp_file = os.path.join(self.tools_dir, f"{tool_id}_temp.py")
            with open(temp_file, "w") as f:
                f.write(tool["implementation"])
            
            # 导入临时模块
            import importlib.util
            spec = importlib.util.spec_from_file_location(f"tool_{tool_id}", temp_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # 执行main函数
            result = module.main(**parameters)
            
            # 删除临时文件
            os.remove(temp_file)
            
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
