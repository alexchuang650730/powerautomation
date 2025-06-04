# MCP.so MCP服务器设计方案

## 🎯 **架构理念**

参考ACI.dev的MCP服务器实现，我们可以为mcp.so创建一个标准的MCP服务器，让MCP客户端通过统一的MCP协议来使用mcp.so的工具服务。

## 🏗️ **架构对比**

### 📋 **ACI.dev MCP架构**
```
MCP Client → ACI.dev MCP Server → ACI.dev API → 600+ Tools
    ↓              ↓                  ↓           ↓
Claude/其他    aci-mcp-unified    REST API    云端工具生态
```

### 🔧 **MCP.so MCP架构**
```
MCP Client → MCP.so MCP Server → MCP.so Library → Local Tools
    ↓              ↓                  ↓              ↓
Claude/其他    mcp-so-server      动态库调用      本地工具注册表
```

## 🛠️ **MCP.so MCP服务器实现**

### 📁 **项目结构**
```
mcp-so-server/
├── src/
│   ├── mcp_so_server/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── unified_server.py      # 统一MCP服务器
│   │   ├── tools_server.py        # 工具特定服务器
│   │   └── common/
│   │       ├── __init__.py
│   │       ├── mcp_so_client.py   # MCP.so客户端封装
│   │       └── tool_registry.py   # 工具注册表管理
├── pyproject.toml
└── README.md
```

### 🔧 **核心实现**

#### 1. **统一MCP服务器** (`unified_server.py`)
```python
import json
import logging
import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from .common.mcp_so_client import MCPSoClient
from .common.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)

# 初始化MCP.so客户端
mcp_so_client = MCPSoClient()
tool_registry = ToolRegistry()

# 创建MCP服务器
server = Server("mcp-so-unified")

# 定义元工具
mcp_so_search_tools = {
    "name": "MCP_SO_SEARCH_TOOLS",
    "description": "搜索MCP.so中可用的工具",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索查询字符串"
            },
            "category": {
                "type": "string", 
                "description": "工具类别过滤"
            },
            "limit": {
                "type": "integer",
                "description": "返回结果数量限制",
                "default": 10
            }
        }
    }
}

mcp_so_execute_tool = {
    "name": "MCP_SO_EXECUTE_TOOL",
    "description": "执行MCP.so中的指定工具",
    "input_schema": {
        "type": "object",
        "properties": {
            "tool_name": {
                "type": "string",
                "description": "要执行的工具名称"
            },
            "arguments": {
                "type": "object",
                "description": "工具执行参数"
            },
            "execution_context": {
                "type": "object",
                "description": "执行上下文信息"
            }
        },
        "required": ["tool_name"]
    }
}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用的元工具"""
    return [
        types.Tool(
            name=mcp_so_search_tools["name"],
            description=mcp_so_search_tools["description"],
            inputSchema=mcp_so_search_tools["input_schema"]
        ),
        types.Tool(
            name=mcp_so_execute_tool["name"],
            description=mcp_so_execute_tool["description"],
            inputSchema=mcp_so_execute_tool["input_schema"]
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用请求"""
    
    if name == mcp_so_search_tools["name"]:
        return await _handle_search_tools(arguments)
    elif name == mcp_so_execute_tool["name"]:
        return await _handle_execute_tool(arguments)
    else:
        raise ValueError(f"未知工具: {name}")

async def _handle_search_tools(arguments: dict):
    """处理工具搜索请求"""
    query = arguments.get("query", "")
    category = arguments.get("category")
    limit = arguments.get("limit", 10)
    
    try:
        # 调用MCP.so搜索工具
        results = await mcp_so_client.search_tools(
            query=query,
            category=category,
            limit=limit
        )
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(results, indent=2, ensure_ascii=False)
            )
        ]
    except Exception as e:
        logger.error(f"工具搜索失败: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"工具搜索失败: {str(e)}"
            )
        ]

async def _handle_execute_tool(arguments: dict):
    """处理工具执行请求"""
    tool_name = arguments.get("tool_name")
    tool_arguments = arguments.get("arguments", {})
    execution_context = arguments.get("execution_context", {})
    
    if not tool_name:
        raise ValueError("缺少必需参数: tool_name")
    
    try:
        # 调用MCP.so执行工具
        result = await mcp_so_client.execute_tool(
            tool_name=tool_name,
            arguments=tool_arguments,
            context=execution_context
        )
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )
        ]
    except Exception as e:
        logger.error(f"工具执行失败: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"工具执行失败: {str(e)}"
            )
        ]

async def start_server(transport: str = "stdio"):
    """启动MCP服务器"""
    logger.info("启动MCP.so MCP服务器...")
    
    # 初始化工具注册表
    await tool_registry.initialize()
    
    if transport == "stdio":
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    else:
        raise ValueError(f"不支持的传输方式: {transport}")
```

#### 2. **MCP.so客户端封装** (`common/mcp_so_client.py`)
```python
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
import ctypes
from pathlib import Path

logger = logging.getLogger(__name__)

class MCPSoClient:
    """MCP.so动态库客户端封装"""
    
    def __init__(self, library_path: Optional[str] = None):
        self.library_path = library_path or self._find_mcp_so_library()
        self.library = None
        self._initialize_library()
    
    def _find_mcp_so_library(self) -> str:
        """查找MCP.so动态库"""
        possible_paths = [
            "/usr/local/lib/libmcp.so",
            "/usr/lib/libmcp.so",
            "./libmcp.so",
            "../mcp.so/build/libmcp.so"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        raise FileNotFoundError("未找到MCP.so动态库")
    
    def _initialize_library(self):
        """初始化动态库"""
        try:
            self.library = ctypes.CDLL(self.library_path)
            
            # 定义函数签名
            self.library.mcp_search_tools.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
            self.library.mcp_search_tools.restype = ctypes.c_char_p
            
            self.library.mcp_execute_tool.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
            self.library.mcp_execute_tool.restype = ctypes.c_char_p
            
            self.library.mcp_list_tools.argtypes = []
            self.library.mcp_list_tools.restype = ctypes.c_char_p
            
            logger.info(f"成功加载MCP.so库: {self.library_path}")
            
        except Exception as e:
            logger.error(f"加载MCP.so库失败: {e}")
            raise
    
    async def search_tools(self, query: str = "", category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """搜索工具"""
        try:
            # 构建搜索参数
            search_params = {
                "query": query,
                "category": category,
                "limit": limit
            }
            
            # 调用动态库函数
            result_ptr = self.library.mcp_search_tools(
                query.encode('utf-8') if query else b"",
                category.encode('utf-8') if category else b"",
                limit
            )
            
            if result_ptr:
                result_str = ctypes.string_at(result_ptr).decode('utf-8')
                return json.loads(result_str)
            else:
                return []
                
        except Exception as e:
            logger.error(f"搜索工具失败: {e}")
            raise
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict:
        """执行工具"""
        try:
            # 序列化参数
            args_json = json.dumps(arguments, ensure_ascii=False)
            context_json = json.dumps(context or {}, ensure_ascii=False)
            
            # 调用动态库函数
            result_ptr = self.library.mcp_execute_tool(
                tool_name.encode('utf-8'),
                args_json.encode('utf-8'),
                context_json.encode('utf-8')
            )
            
            if result_ptr:
                result_str = ctypes.string_at(result_ptr).decode('utf-8')
                return json.loads(result_str)
            else:
                raise RuntimeError("工具执行返回空结果")
                
        except Exception as e:
            logger.error(f"执行工具失败: {e}")
            raise
    
    async def list_tools(self) -> List[Dict]:
        """列出所有可用工具"""
        try:
            result_ptr = self.library.mcp_list_tools()
            
            if result_ptr:
                result_str = ctypes.string_at(result_ptr).decode('utf-8')
                return json.loads(result_str)
            else:
                return []
                
        except Exception as e:
            logger.error(f"列出工具失败: {e}")
            raise
```

#### 3. **工具注册表管理** (`common/tool_registry.py`)
```python
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import aiofiles

logger = logging.getLogger(__name__)

class ToolRegistry:
    """工具注册表管理器"""
    
    def __init__(self, registry_path: str = "./mcp_so_tools_registry.json"):
        self.registry_path = Path(registry_path)
        self.tools_cache = {}
        self.categories_cache = {}
    
    async def initialize(self):
        """初始化工具注册表"""
        try:
            if self.registry_path.exists():
                await self._load_registry()
            else:
                await self._create_default_registry()
            
            logger.info(f"工具注册表初始化完成，共{len(self.tools_cache)}个工具")
            
        except Exception as e:
            logger.error(f"初始化工具注册表失败: {e}")
            raise
    
    async def _load_registry(self):
        """加载工具注册表"""
        async with aiofiles.open(self.registry_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            registry_data = json.loads(content)
            
            self.tools_cache = registry_data.get("tools", {})
            self.categories_cache = registry_data.get("categories", {})
    
    async def _create_default_registry(self):
        """创建默认工具注册表"""
        default_registry = {
            "tools": {
                "file_processor": {
                    "name": "file_processor",
                    "description": "文件处理工具",
                    "category": "file_operations",
                    "capabilities": ["read", "write", "transform"],
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string"},
                            "file_path": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    }
                },
                "data_analyzer": {
                    "name": "data_analyzer", 
                    "description": "数据分析工具",
                    "category": "data_processing",
                    "capabilities": ["analyze", "visualize", "export"],
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "data_source": {"type": "string"},
                            "analysis_type": {"type": "string"},
                            "parameters": {"type": "object"}
                        }
                    }
                }
            },
            "categories": {
                "file_operations": {
                    "name": "文件操作",
                    "description": "文件读写和处理相关工具"
                },
                "data_processing": {
                    "name": "数据处理",
                    "description": "数据分析和处理相关工具"
                }
            }
        }
        
        await self._save_registry(default_registry)
        self.tools_cache = default_registry["tools"]
        self.categories_cache = default_registry["categories"]
    
    async def _save_registry(self, registry_data: Dict):
        """保存工具注册表"""
        async with aiofiles.open(self.registry_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(registry_data, indent=2, ensure_ascii=False))
    
    async def search_tools(self, query: str = "", category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """搜索工具"""
        results = []
        
        for tool_id, tool_info in self.tools_cache.items():
            # 类别过滤
            if category and tool_info.get("category") != category:
                continue
            
            # 查询过滤
            if query:
                if (query.lower() not in tool_info.get("name", "").lower() and
                    query.lower() not in tool_info.get("description", "").lower()):
                    continue
            
            results.append({
                "id": tool_id,
                "name": tool_info.get("name"),
                "description": tool_info.get("description"),
                "category": tool_info.get("category"),
                "capabilities": tool_info.get("capabilities", [])
            })
            
            if len(results) >= limit:
                break
        
        return results
    
    async def get_tool_info(self, tool_name: str) -> Optional[Dict]:
        """获取工具信息"""
        return self.tools_cache.get(tool_name)
    
    async def register_tool(self, tool_info: Dict):
        """注册新工具"""
        tool_name = tool_info.get("name")
        if not tool_name:
            raise ValueError("工具名称不能为空")
        
        self.tools_cache[tool_name] = tool_info
        
        # 保存到文件
        registry_data = {
            "tools": self.tools_cache,
            "categories": self.categories_cache
        }
        await self._save_registry(registry_data)
        
        logger.info(f"成功注册工具: {tool_name}")
```

#### 4. **主入口** (`__main__.py`)
```python
import asyncio
import argparse
import logging
from .unified_server import start_server

def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(description="MCP.so MCP服务器")
    parser.add_argument(
        "--transport",
        choices=["stdio"],
        default="stdio",
        help="传输方式"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="日志级别"
    )
    
    args = parser.parse_args()
    
    # 配置日志
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 启动服务器
    asyncio.run(start_server(args.transport))

if __name__ == "__main__":
    main()
```

## 🚀 **使用方式**

### 📦 **安装和运行**
```bash
# 安装依赖
pip install mcp anyio

# 运行MCP.so MCP服务器
python -m mcp_so_server --transport stdio

# 或者使用uvx运行
uvx mcp-so-server --transport stdio
```

### 🔧 **MCP客户端配置**
```json
{
  "mcpServers": {
    "mcp-so": {
      "command": "python",
      "args": ["-m", "mcp_so_server"],
      "env": {
        "MCP_SO_LIBRARY_PATH": "/path/to/libmcp.so"
      }
    }
  }
}
```

### 🧪 **调试和测试**
```bash
# 使用MCP检查器调试
npx @modelcontextprotocol/inspector python -m mcp_so_server

# 查看日志
tail -f ~/.local/share/mcp-so-server/logs/server.log
```

## 🎯 **统一架构优势**

### ✅ **协议统一**
- **标准MCP接口** - 所有工具都通过MCP协议访问
- **客户端兼容** - 支持Claude、其他MCP客户端
- **API一致性** - 统一的搜索和执行接口

### ✅ **功能整合**
- **本地+云端** - MCP.so本地工具 + ACI.dev云端工具
- **智能路由** - 根据需求自动选择最佳工具
- **负载均衡** - 分散工具调用负载

### ✅ **开发效率**
- **标准化开发** - 统一的工具开发规范
- **插件化架构** - 支持动态加载新工具
- **测试友好** - 统一的测试框架

## 🔄 **完整工作流**

### 🎯 **智能工具发现和执行流程**
```
MCP Client → 意图分析 → 工具发现 → 智能选择 → 并行执行 → 结果聚合
    ↓           ↓         ↓         ↓         ↓         ↓
Claude等   MCPBrainstorm  多源搜索   智能决策   混合执行   统一返回
                          ↓
                    MCP.so Server + ACI.dev Server
                          ↓
                    本地工具 + 云端600+工具
```

### 📋 **具体实现步骤**
1. **工具发现阶段**
   - 并行查询MCP.so和ACI.dev
   - 合并去重工具列表
   - 智能排序和推荐

2. **工具选择阶段**
   - 性能评估（本地 vs 云端）
   - 成本评估（免费 vs 付费）
   - 可用性检查（在线状态）

3. **执行阶段**
   - 本地工具优先（速度快）
   - 云端工具补充（功能强）
   - 并行执行提升效率

4. **结果处理阶段**
   - 结果验证和格式化
   - 错误处理和重试
   - 性能指标收集

这种设计完美实现了本地工具和云端工具的统一访问，为用户提供了最佳的工具使用体验！

