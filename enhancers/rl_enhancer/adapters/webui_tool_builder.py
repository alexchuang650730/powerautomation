"""
WebUI工具构建模块，用于在Web界面中构建和管理工具
"""
import os
import json
import uuid
from typing import Dict, List, Any, Optional, Callable

class WebUIToolBuilder:
    """
    WebUI工具构建器，提供在Web界面中构建和管理工具的能力
    """
    
    def __init__(self, tools_dir: str = None):
        """
        初始化WebUI工具构建器
        
        Args:
            tools_dir: 工具存储目录，如果为None则使用默认目录
        """
        self.tools_dir = tools_dir or os.path.join(os.path.dirname(__file__), "../tools")
        os.makedirs(self.tools_dir, exist_ok=True)
        
        # 工具模板
        self.tool_templates = {
            "api_call": {
                "name": "API调用工具",
                "description": "调用外部API的工具模板",
                "parameters": {
                    "url": {"type": "string", "description": "API URL"},
                    "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]},
                    "headers": {"type": "object", "description": "请求头"},
                    "body": {"type": "object", "description": "请求体"}
                }
            },
            "data_processing": {
                "name": "数据处理工具",
                "description": "处理和转换数据的工具模板",
                "parameters": {
                    "input_data": {"type": "object", "description": "输入数据"},
                    "operation": {"type": "string", "description": "操作类型"},
                    "options": {"type": "object", "description": "操作选项"}
                }
            },
            "file_operation": {
                "name": "文件操作工具",
                "description": "处理文件的工具模板",
                "parameters": {
                    "file_path": {"type": "string", "description": "文件路径"},
                    "operation": {"type": "string", "enum": ["read", "write", "append", "delete"]},
                    "content": {"type": "string", "description": "文件内容"}
                }
            }
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        获取所有已创建的工具
        
        Returns:
            工具列表
        """
        tools = []
        for filename in os.listdir(self.tools_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.tools_dir, filename), "r") as f:
                    tool = json.load(f)
                    tools.append(tool)
        return tools
    
    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定ID的工具
        
        Args:
            tool_id: 工具ID
            
        Returns:
            工具信息，如果不存在则返回None
        """
        tool_path = os.path.join(self.tools_dir, f"{tool_id}.json")
        if os.path.exists(tool_path):
            with open(tool_path, "r") as f:
                return json.load(f)
        return None
    
    def create_tool(self, name: str, description: str, parameters: Dict[str, Any], 
                   implementation: str, template_id: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新工具
        
        Args:
            name: 工具名称
            description: 工具描述
            parameters: 工具参数定义
            implementation: 工具实现代码
            template_id: 可选的模板ID
            
        Returns:
            创建的工具信息
        """
        tool_id = str(uuid.uuid4())
        
        # 如果指定了模板，使用模板初始化
        if template_id and template_id in self.tool_templates:
            template = self.tool_templates[template_id]
            # 合并模板和用户提供的参数
            parameters = {**template["parameters"], **parameters}
        
        tool = {
            "id": tool_id,
            "name": name,
            "description": description,
            "parameters": parameters,
            "implementation": implementation,
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now())
        }
        
        # 保存工具定义
        with open(os.path.join(self.tools_dir, f"{tool_id}.json"), "w") as f:
            json.dump(tool, f, indent=2)
        
        return tool
    
    def update_tool(self, tool_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        更新工具
        
        Args:
            tool_id: 工具ID
            updates: 要更新的字段
            
        Returns:
            更新后的工具信息，如果工具不存在则返回None
        """
        tool = self.get_tool(tool_id)
        if not tool:
            return None
        
        # 更新字段
        for key, value in updates.items():
            if key in tool and key != "id":  # 不允许更新ID
                tool[key] = value
        
        tool["updated_at"] = str(datetime.datetime.now())
        
        # 保存更新后的工具
        with open(os.path.join(self.tools_dir, f"{tool_id}.json"), "w") as f:
            json.dump(tool, f, indent=2)
        
        return tool
    
    def delete_tool(self, tool_id: str) -> bool:
        """
        删除工具
        
        Args:
            tool_id: 工具ID
            
        Returns:
            是否成功删除
        """
        tool_path = os.path.join(self.tools_dir, f"{tool_id}.json")
        if os.path.exists(tool_path):
            os.remove(tool_path)
            return True
        return False
    
    def get_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有可用的工具模板
        
        Returns:
            工具模板字典
        """
        return self.tool_templates
    
    def test_tool(self, tool_id: str, test_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        测试工具
        
        Args:
            tool_id: 工具ID
            test_parameters: 测试参数
            
        Returns:
            测试结果
        """
        tool = self.get_tool(tool_id)
        if not tool:
            return {"status": "error", "message": f"工具 {tool_id} 不存在"}
        
        try:
            # 在安全的环境中执行工具代码
            # 实际实现中应使用更安全的方式，如沙箱执行
            exec_globals = {}
            exec(tool["implementation"], exec_globals)
            
            # 获取工具的主函数
            if "main" not in exec_globals:
                return {"status": "error", "message": "工具实现中缺少main函数"}
            
            main_func = exec_globals["main"]
            
            # 执行工具
            result = main_func(**test_parameters)
            
            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"工具执行失败: {str(e)}"
            }
    
    def export_tool(self, tool_id: str, export_format: str = "json") -> Dict[str, Any]:
        """
        导出工具
        
        Args:
            tool_id: 工具ID
            export_format: 导出格式，支持json和python
            
        Returns:
            导出结果
        """
        tool = self.get_tool(tool_id)
        if not tool:
            return {"status": "error", "message": f"工具 {tool_id} 不存在"}
        
        if export_format == "json":
            return {
                "status": "success",
                "format": "json",
                "content": json.dumps(tool, indent=2)
            }
        elif export_format == "python":
            # 生成Python模块代码
            code = f"""
# {tool['name']}
# {tool['description']}

{tool['implementation']}

# 使用示例:
# result = main(
#     # 在此处填入参数
# )
"""
            return {
                "status": "success",
                "format": "python",
                "content": code
            }
        else:
            return {"status": "error", "message": f"不支持的导出格式: {export_format}"}
    
    def import_tool(self, tool_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        导入工具
        
        Args:
            tool_data: 工具数据
            
        Returns:
            导入结果
        """
        # 验证必要字段
        required_fields = ["name", "description", "parameters", "implementation"]
        for field in required_fields:
            if field not in tool_data:
                return {"status": "error", "message": f"工具数据缺少必要字段: {field}"}
        
        # 生成新ID
        tool_id = str(uuid.uuid4())
        
        tool = {
            "id": tool_id,
            "name": tool_data["name"],
            "description": tool_data["description"],
            "parameters": tool_data["parameters"],
            "implementation": tool_data["implementation"],
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now())
        }
        
        # 保存工具
        with open(os.path.join(self.tools_dir, f"{tool_id}.json"), "w") as f:
            json.dump(tool, f, indent=2)
        
        return {
            "status": "success",
            "message": f"工具 {tool['name']} 已成功导入",
            "tool": tool
        }
