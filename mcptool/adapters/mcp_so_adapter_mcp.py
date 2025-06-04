#!/usr/bin/env python3
"""
MCP.so MCP适配器

此模块为mcp.so动态库提供MCP协议合规的包装，支持动态库加载、工具执行和工具列表获取。
"""

import os
import sys
import json
import ctypes
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# 添加项目路径
sys.path.append('/home/ubuntu/powerautomation')

try:
    from mcptool.adapters.base_mcp import BaseMCP
except ImportError:
    class BaseMCP:
        def __init__(self, name: str = "BaseMCP"):
            self.name = name
            self.logger = logging.getLogger(f"MCP.{name}")
        
        def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
            raise NotImplementedError("子类必须实现此方法")
        
        def validate_input(self, input_data: Dict[str, Any]) -> bool:
            return True
        
        def get_capabilities(self) -> List[str]:
            return ["基础MCP适配功能"]

# 尝试导入原始MCPSoAdapter
try:
    sys.path.append('/home/ubuntu/powerautomation/rl_factory/adapters')
    from mcp_so_adapter import MCPSoAdapter
    MCP_SO_AVAILABLE = True
except ImportError as e:
    logging.warning(f"MCPSoAdapter导入失败: {e}")
    MCP_SO_AVAILABLE = False
    
    # 创建Mock实现
    class MCPSoAdapter:
        def __init__(self, lib_path: str = "/path/to/mcp.so"):
            self.lib_path = lib_path
            self.initialized = False
            self.tools = []
            
        def initialize(self, config_path: str) -> bool:
            # Mock初始化
            self.initialized = True
            self.tools = [
                {"id": "text_processor", "name": "文本处理器", "description": "处理文本数据"},
                {"id": "data_analyzer", "name": "数据分析器", "description": "分析数据模式"},
                {"id": "code_generator", "name": "代码生成器", "description": "生成代码片段"}
            ]
            return True
            
        def get_tools(self) -> List[Dict[str, Any]]:
            return self.tools
            
        def execute_tool(self, tool_name: str, params: str) -> str:
            # Mock工具执行
            result = {
                "tool": tool_name,
                "status": "success",
                "result": f"Mock执行结果 for {tool_name}",
                "params": params,
                "timestamp": datetime.now().isoformat()
            }
            return json.dumps(result)
            
        def finalize(self) -> bool:
            self.initialized = False
            return True

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_so_adapter_mcp")

class MCPSoAdapterMCP(BaseMCP):
    """MCP.so的MCP包装器"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(name="MCPSoAdapterMCP")
        
        # 解析配置
        config = config or {}
        lib_path = config.get('lib_path', '/path/to/mcp.so')
        self.config_path = config.get('config_path', '/path/to/config.json')
        
        # 初始化MCPSoAdapter
        try:
            self.mcp_so_adapter = MCPSoAdapter(lib_path)
            self.is_available = MCP_SO_AVAILABLE and self.mcp_so_adapter.initialized
        except Exception as e:
            self.logger.error(f"MCPSoAdapter初始化失败: {e}")
            self.mcp_so_adapter = None
            self.is_available = False
        
        # 初始化指标
        self.metrics = {
            'execution_count': 0,
            'success_count': 0,
            'error_count': 0,
            'total_execution_time': 0,
            'tools_executed': 0,
            'tools_available': 0
        }
        
        # 尝试初始化MCP
        if self.is_available:
            try:
                if self.mcp_so_adapter.initialize(self.config_path):
                    self.tools = self.mcp_so_adapter.get_tools()
                    self.metrics['tools_available'] = len(self.tools)
                    self.logger.info(f"MCP.so初始化成功，可用工具: {len(self.tools)}")
                else:
                    self.logger.warning("MCP.so初始化失败")
                    self.is_available = False
            except Exception as e:
                self.logger.error(f"MCP.so初始化异常: {e}")
                self.is_available = False
        
        self.logger.info(f"MCP.so MCP适配器初始化完成，可用性: {self.is_available}")
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """MCP协议标准处理方法"""
        start_time = datetime.now()
        
        try:
            # 1. 输入验证
            if not self.validate_input(input_data):
                return self._create_error_response("输入验证失败", "INVALID_INPUT")
            
            # 2. 检查适配器可用性
            if not self.is_available:
                return self._create_error_response("MCP.so不可用", "ADAPTER_UNAVAILABLE")
            
            # 3. 解析操作类型
            action = input_data.get('action', 'execute_tool')
            parameters = input_data.get('parameters', {})
            
            # 4. 执行相应操作
            if action == 'execute_tool':
                result = self._execute_tool(parameters)
            elif action == 'get_tools':
                result = self._get_tools()
            elif action == 'get_tool_details':
                result = self._get_tool_details(parameters)
            elif action == 'initialize':
                result = self._initialize_mcp(parameters)
            elif action == 'finalize':
                result = self._finalize_mcp()
            elif action == 'get_capabilities':
                result = {'capabilities': self.get_capabilities()}
            elif action == 'get_status':
                result = self._get_status()
            else:
                return self._create_error_response(f"不支持的操作: {action}", "UNSUPPORTED_ACTION")
            
            # 5. 记录成功指标
            execution_time = (datetime.now() - start_time).total_seconds()
            self._record_execution(execution_time, True)
            
            # 6. 返回标准化结果
            return {
                'status': 'success',
                'data': {
                    'result': result,
                    'metrics': self._get_execution_metrics()
                },
                'metadata': {
                    'adapter_name': self.name,
                    'action': action,
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0.0'
                }
            }
            
        except Exception as e:
            # 记录错误指标
            execution_time = (datetime.now() - start_time).total_seconds()
            self._record_execution(execution_time, False)
            
            self.logger.error(f"MCP.so执行失败: {str(e)}")
            return self._create_error_response(str(e), "EXECUTION_ERROR")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """验证输入数据"""
        if not isinstance(input_data, dict):
            return False
        
        action = input_data.get('action', 'execute_tool')
        parameters = input_data.get('parameters', {})
        
        # 验证必需参数
        if action == 'execute_tool':
            return 'tool_name' in parameters
        elif action == 'get_tool_details':
            return 'tool_id' in parameters
        elif action == 'initialize':
            return 'config_path' in parameters
        elif action in ['get_tools', 'finalize', 'get_capabilities', 'get_status']:
            return True
        else:
            return False
    
    def get_capabilities(self) -> List[str]:
        """获取适配器能力列表"""
        return [
            "dynamic_library_loading",
            "tool_execution",
            "tool_discovery",
            "high_performance_computing",
            "native_code_integration",
            "ctypes_bridging",
            "resource_management",
            "configuration_management"
        ]
    
    def _execute_tool(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """执行MCP工具"""
        tool_name = parameters.get('tool_name')
        tool_params = parameters.get('tool_params', {})
        
        if self.mcp_so_adapter and hasattr(self.mcp_so_adapter, 'execute_tool'):
            # 将参数转换为JSON字符串
            params_json = json.dumps(tool_params)
            result_json = self.mcp_so_adapter.execute_tool(tool_name, params_json)
            
            try:
                result = json.loads(result_json) if isinstance(result_json, str) else result_json
            except json.JSONDecodeError:
                result = {'raw_result': result_json}
        else:
            # Mock实现
            result = {
                'tool': tool_name,
                'status': 'success',
                'result': f'Mock执行结果 for {tool_name}',
                'params': tool_params,
                'execution_time': 0.1
            }
        
        self.metrics['tools_executed'] += 1
        
        return {
            'action': 'execute_tool',
            'tool_name': tool_name,
            'tool_params': tool_params,
            'execution_result': result,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_tools(self) -> Dict[str, Any]:
        """获取可用工具列表"""
        if self.mcp_so_adapter and hasattr(self.mcp_so_adapter, 'get_tools'):
            tools = self.mcp_so_adapter.get_tools()
        else:
            # Mock实现
            tools = [
                {"id": "text_processor", "name": "文本处理器", "description": "处理文本数据"},
                {"id": "data_analyzer", "name": "数据分析器", "description": "分析数据模式"},
                {"id": "code_generator", "name": "代码生成器", "description": "生成代码片段"}
            ]
        
        return {
            'action': 'get_tools',
            'tools': tools,
            'tool_count': len(tools),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_tool_details(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """获取工具详细信息"""
        tool_id = parameters.get('tool_id')
        
        # 从工具列表中查找
        tools = self._get_tools()['tools']
        tool_details = next((tool for tool in tools if tool.get('id') == tool_id), None)
        
        if not tool_details:
            tool_details = {
                'id': tool_id,
                'name': f'工具 {tool_id}',
                'description': f'{tool_id} 的详细信息',
                'status': 'not_found'
            }
        
        return {
            'action': 'get_tool_details',
            'tool_id': tool_id,
            'tool_details': tool_details,
            'timestamp': datetime.now().isoformat()
        }
    
    def _initialize_mcp(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """初始化MCP"""
        config_path = parameters.get('config_path', self.config_path)
        
        if self.mcp_so_adapter and hasattr(self.mcp_so_adapter, 'initialize'):
            success = self.mcp_so_adapter.initialize(config_path)
            if success:
                self.tools = self.mcp_so_adapter.get_tools()
                self.metrics['tools_available'] = len(self.tools)
        else:
            # Mock实现
            success = True
            self.tools = [
                {"id": "text_processor", "name": "文本处理器", "description": "处理文本数据"},
                {"id": "data_analyzer", "name": "数据分析器", "description": "分析数据模式"},
                {"id": "code_generator", "name": "代码生成器", "description": "生成代码片段"}
            ]
            self.metrics['tools_available'] = len(self.tools)
        
        return {
            'action': 'initialize',
            'config_path': config_path,
            'success': success,
            'tools_available': self.metrics['tools_available'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _finalize_mcp(self) -> Dict[str, Any]:
        """释放MCP资源"""
        if self.mcp_so_adapter and hasattr(self.mcp_so_adapter, 'finalize'):
            success = self.mcp_so_adapter.finalize()
        else:
            # Mock实现
            success = True
        
        return {
            'action': 'finalize',
            'success': success,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_status(self) -> Dict[str, Any]:
        """获取适配器状态"""
        return {
            'action': 'get_status',
            'status': {
                'is_available': self.is_available,
                'tools_available': self.metrics['tools_available'],
                'tools_executed': self.metrics['tools_executed'],
                'success_rate': self._calculate_success_rate(),
                'uptime': 'active'
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_success_rate(self) -> float:
        """计算成功率"""
        if self.metrics['execution_count'] > 0:
            return self.metrics['success_count'] / self.metrics['execution_count']
        return 0.0
    
    def _create_error_response(self, message: str, error_code: str) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            'status': 'error',
            'error': {
                'code': error_code,
                'message': message,
                'timestamp': datetime.now().isoformat()
            },
            'metadata': {
                'adapter_name': self.name,
                'timestamp': datetime.now().isoformat()
            }
        }
    
    def _record_execution(self, execution_time: float, success: bool):
        """记录执行指标"""
        self.metrics['execution_count'] += 1
        self.metrics['total_execution_time'] += execution_time
        
        if success:
            self.metrics['success_count'] += 1
        else:
            self.metrics['error_count'] += 1
    
    def _get_execution_metrics(self) -> Dict[str, Any]:
        """获取执行指标"""
        if self.metrics['execution_count'] > 0:
            avg_time = self.metrics['total_execution_time'] / self.metrics['execution_count']
            success_rate = self.metrics['success_count'] / self.metrics['execution_count']
        else:
            avg_time = 0
            success_rate = 0
        
        return {
            'execution_count': self.metrics['execution_count'],
            'success_rate': success_rate,
            'average_execution_time': avg_time,
            'tools_available': self.metrics['tools_available'],
            'tools_executed': self.metrics['tools_executed'],
            'availability': self.is_available
        }

def test_mcp_so_adapter_mcp():
    """测试MCP.so MCP适配器"""
    print("=== 测试MCP.so MCP适配器 ===")
    
    # 创建适配器实例
    config = {
        'lib_path': '/path/to/mcp.so',
        'config_path': '/path/to/config.json'
    }
    adapter = MCPSoAdapterMCP(config)
    
    # 测试获取工具列表
    tools_input = {
        'action': 'get_tools',
        'parameters': {}
    }
    
    result = adapter.process(tools_input)
    print(f"获取工具列表结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 测试执行工具
    execute_input = {
        'action': 'execute_tool',
        'parameters': {
            'tool_name': 'text_processor',
            'tool_params': {
                'input_text': '这是一个测试文本',
                'operation': 'analyze'
            }
        }
    }
    
    result = adapter.process(execute_input)
    print(f"执行工具结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 测试状态查询
    status_input = {
        'action': 'get_status',
        'parameters': {}
    }
    
    result = adapter.process(status_input)
    print(f"状态查询结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    test_mcp_so_adapter_mcp()

