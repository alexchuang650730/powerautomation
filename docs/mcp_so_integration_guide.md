# MCP.so 集成指南

## 概述

MCP.so 是 PowerAutomation 系统中的核心外部工具适配器，提供与底层 MCP 动态库的交互能力。它通过 ctypes 桥接 Python 和 C/C++ 接口，使系统能够调用高性能的 MCP 工具集，为智能体提供强大的扩展能力。本文档详细介绍了 MCP.so 的功能、接口和集成方法，帮助开发者快速上手并有效利用这一组件。

## 功能特点

MCP.so 适配器提供以下核心功能：

1. **动态库加载**：加载 MCP.so 动态库并设置函数签名
2. **工具执行**：执行 MCP 工具并处理结果
3. **工具列表获取**：获取可用的 MCP 工具列表
4. **友好接口封装**：通过 MCPToolWrapper 提供更友好的接口

## 安装与配置

MCP.so 适配器已集成到 PowerAutomation 系统的 RL Factory 适配器层中，无需额外安装。只需确保 MCP.so 动态库已正确部署：

```bash
# 检查 MCP.so 是否存在
ls -la /path/to/mcp.so

# 确保有执行权限
chmod +x /path/to/mcp.so
```

## 使用方法

### 基本使用

```python
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper

# 初始化 MCP.so 适配器
adapter = MCPSoAdapter("/path/to/mcp.so")

# 初始化 MCP
if adapter.initialized:
    success = adapter.initialize("/path/to/config.json")
    if success:
        print("MCP initialized successfully")
        
        # 获取工具列表
        tools = adapter.get_tools()
        print(f"Available tools: {len(tools)}")
        
        # 执行工具
        result = adapter.execute_tool("example_tool", {"param1": "value1"})
        print(f"Tool execution result: {result}")
        
        # 释放资源
        adapter.finalize()
```

### 使用工具包装器

```python
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper

# 初始化 MCP.so 适配器
adapter = MCPSoAdapter("/path/to/mcp.so")

# 初始化 MCP
if adapter.initialized and adapter.initialize("/path/to/config.json"):
    # 创建工具包装器
    wrapper = MCPToolWrapper(adapter)
    
    # 列出工具
    tool_names = wrapper.list_tools()
    print(f"Tool names: {tool_names}")
    
    # 执行工具
    result = wrapper.execute("example_tool", param1="value1", param2="value2")
    print(f"Tool execution result: {result}")
    
    # 获取工具信息
    tool_info = wrapper.get_tool_info("example_tool")
    print(f"Tool info: {tool_info}")
```

### 与六大特性集成

MCP.so 可以与 PowerAutomation 系统的六大特性无缝集成，特别是在思维特性和内容特性方面提供强大支持：

```python
from agents.features import GeneralAgentFeatures
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper

# 初始化通用智能体特性
agent_features = GeneralAgentFeatures()

# 初始化 MCP.so 适配器和包装器
adapter = MCPSoAdapter("/path/to/mcp.so")
if adapter.initialized and adapter.initialize("/path/to/config.json"):
    wrapper = MCPToolWrapper(adapter)
    
    # 使用 MCP 工具增强思维特性
    thinking_result = wrapper.execute("thinking_enhancer", 
                                     task="分析用户需求",
                                     context="用户希望开发一个自动化测试系统")
    
    agent_features.update_thinking_feature({
        "task": "分析用户需求",
        "mcp_analysis": thinking_result,
        "conclusions": thinking_result.get("conclusions", [])
    })
    
    # 使用 MCP 工具增强内容特性
    content_result = wrapper.execute("content_generator", 
                                    topic="自动化测试系统",
                                    style="技术文档")
    
    agent_features.update_content_feature({
        "topic": "自动化测试系统",
        "generated_content": content_result.get("content", ""),
        "structure": content_result.get("structure", {})
    })
```

### 与多智能体路由集成

MCP.so 可以与多智能体路由系统集成，为各种智能体提供高性能工具支持：

```python
from frontend.src.utils.agent_router import AgentRouter
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper

# 初始化智能体路由器
router = AgentRouter()

# 初始化 MCP.so 适配器和包装器
adapter = MCPSoAdapter("/path/to/mcp.so")
if adapter.initialized and adapter.initialize("/path/to/config.json"):
    wrapper = MCPToolWrapper(adapter)
    
    # 注册 MCP.so 增强的通用智能体处理函数
    def enhanced_general_agent_handler(request):
        # 根据请求类型使用不同的 MCP 工具
        if "thinking" in request:
            return wrapper.execute("thinking_enhancer", task=request["thinking"])
        elif "content" in request:
            return wrapper.execute("content_generator", topic=request["content"])
        elif "tool" in request and request["tool"] in wrapper.list_tools():
            return wrapper.execute(request["tool"], **request.get("params", {}))
        else:
            return {"error": "Unsupported request type or tool not found"}
    
    # 注册处理函数
    router.register_handler("general", enhanced_general_agent_handler)
```

## API 参考

### MCPSoAdapter 类

#### 初始化

```python
MCPSoAdapter(lib_path: str = "/path/to/mcp.so")
```

初始化 MCP.so 适配器。

**参数**：
- `lib_path`：MCP.so 库路径

#### 初始化 MCP

```python
initialize(config_path: str) -> bool
```

初始化 MCP。

**参数**：
- `config_path`：配置文件路径

**返回值**：
- 是否成功初始化

#### 执行工具

```python
execute_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]
```

执行 MCP 工具。

**参数**：
- `tool_name`：工具名称
- `params`：工具参数

**返回值**：
- 执行结果

#### 获取工具列表

```python
get_tools() -> List[Dict[str, Any]]
```

获取 MCP 工具列表。

**返回值**：
- 工具列表

#### 释放资源

```python
finalize() -> bool
```

释放 MCP 资源。

**返回值**：
- 是否成功释放

### MCPToolWrapper 类

#### 初始化

```python
MCPToolWrapper(adapter: MCPSoAdapter)
```

初始化 MCP 工具包装器。

**参数**：
- `adapter`：MCP 适配器

#### 执行工具

```python
execute(tool_name: str, **kwargs) -> Dict[str, Any]
```

执行工具。

**参数**：
- `tool_name`：工具名称
- `**kwargs`：工具参数

**返回值**：
- 执行结果

#### 获取工具信息

```python
get_tool_info(tool_name: str) -> Optional[Dict[str, Any]]
```

获取工具信息。

**参数**：
- `tool_name`：工具名称

**返回值**：
- 工具信息

#### 列出工具

```python
list_tools() -> List[str]
```

列出所有工具。

**返回值**：
- 工具名称列表

## 与主工作流集成

MCP.so 在 PowerAutomation 系统的主工作流中扮演着重要角色，特别是在高性能工具调用和复杂任务处理方面：

1. **工具发现阶段**：
   - 系统初始化时加载 MCP.so
   - 获取可用工具列表
   - 注册工具到系统工具库

2. **工具执行阶段**：
   - 智能体确定需要使用的工具
   - 调用 MCP.so 执行工具
   - 处理工具执行结果

3. **资源管理阶段**：
   - 监控工具执行状态
   - 管理资源使用
   - 释放不再需要的资源

### 集成示例

```python
# 主工作流中的集成示例
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper

class MCPToolManager:
    def __init__(self, lib_path="/path/to/mcp.so", config_path="/path/to/config.json"):
        # 初始化 MCP.so 适配器
        self.adapter = MCPSoAdapter(lib_path)
        self.initialized = False
        
        if self.adapter.initialized:
            # 初始化 MCP
            if self.adapter.initialize(config_path):
                self.wrapper = MCPToolWrapper(self.adapter)
                self.initialized = True
                print(f"MCP Tool Manager initialized with {len(self.wrapper.list_tools())} tools")
            else:
                print("Failed to initialize MCP")
        else:
            print("Failed to load MCP.so library")
    
    def execute_tool(self, tool_name, **params):
        """执行 MCP 工具"""
        if not self.initialized:
            return {"error": "MCP Tool Manager not initialized"}
        
        return self.wrapper.execute(tool_name, **params)
    
    def get_available_tools(self):
        """获取可用工具列表"""
        if not self.initialized:
            return []
        
        return self.wrapper.list_tools()
    
    def __del__(self):
        """析构函数，确保资源被释放"""
        if hasattr(self, 'adapter') and hasattr(self, 'initialized') and self.initialized:
            self.adapter.finalize()
```

## 与 TestAndIssueCollector 集成

MCP.so 可以与 TestAndIssueCollector 集成，提供高性能的测试方案生成和问题分析能力：

```python
from development_tools.test_and_issue_collector import TestAndIssueCollector
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter, MCPToolWrapper

# 初始化 MCP.so 适配器和包装器
adapter = MCPSoAdapter("/path/to/mcp.so")
if adapter.initialized and adapter.initialize("/path/to/config.json"):
    wrapper = MCPToolWrapper(adapter)
    
    # 初始化测试收集器
    collector = TestAndIssueCollector()
    
    # 收集测试用例
    test_cases = collector.collect_test_cases()
    
    # 使用 MCP.so 生成测试计划
    if "generate_test_plan" in wrapper.list_tools():
        test_plan = wrapper.execute("generate_test_plan", test_cases=test_cases)
        
        # 执行测试计划
        test_results = collector.execute_test_plan(test_plan)
        
        # 生成测试报告
        test_report = collector.generate_test_report(test_results)
        
        print(f"Test report generated: {test_report['name']}")
```

## 最佳实践

1. **错误处理**：始终检查 MCP.so 是否成功加载和初始化，并处理可能的错误
2. **资源管理**：使用完 MCP.so 后调用 finalize 方法释放资源
3. **参数验证**：在调用工具前验证参数，确保符合工具要求
4. **异常捕获**：捕获并处理可能的异常，避免程序崩溃

## 常见问题

### MCP.so 库加载失败

如果 MCP.so 库加载失败，可能是因为：

1. 库文件不存在或路径错误
2. 库文件没有执行权限
3. 库依赖的其他库缺失

检查库文件是否存在，并确保有正确的权限。使用 `ldd` 命令检查库依赖。

### 工具执行失败

如果工具执行失败，可能是因为：

1. 工具名称错误
2. 参数不符合要求
3. MCP 内部错误

检查工具名称是否正确，参数是否符合要求，并查看日志获取详细错误信息。

## 与 RL Factory 集成

MCP.so 与 RL Factory 紧密集成，为强化学习提供高性能工具支持：

```python
from rl_factory.adapters.mcp_so_adapter import MCPSoAdapter
from rl_factory.recipe import load_recipe

# 初始化 MCP.so 适配器
adapter = MCPSoAdapter("/path/to/mcp.so")
if adapter.initialized and adapter.initialize("/path/to/config.json"):
    # 加载 RL 配方
    recipe = load_recipe("configs/tool_generator_recipe.yaml")
    
    # 创建工具环境
    tools = adapter.get_tools()
    tool_env = {
        "tools": tools,
        "reward_function": lambda tool, results: results.get("score", 0)
    }
    
    # 训练模型
    model = recipe.train(
        None,  # 初始模型为空
        [],    # 空训练数据，将从工具执行中学习
        tool_env,
        {"epochs": 50, "batch_size": 8}
    )
    
    print("Model training completed")
```

## 结论

MCP.so 适配器为 PowerAutomation 系统提供了强大的外部工具调用能力，是连接 Python 代码和高性能 C/C++ 库的重要桥梁。通过本文档的指导，开发者可以快速上手并有效利用这一组件，为系统提供更强大、更高效的工具支持。
