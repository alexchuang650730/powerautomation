# WebAgentB 集成指南

## 概述

WebAgentB 是 PowerAutomation 系统中的高级网页理解与交互增强组件，它在基础 Playwright 适配器的基础上，提供了更强大的网页内容理解、语义分析和交互能力。本文档详细介绍了 WebAgentB 的功能、接口和集成方法，帮助开发者快速上手并有效利用这一组件。

## 功能特点

WebAgentB 增强适配器提供以下核心功能：

1. **增强搜索**：支持多层次信息收集，可以跟踪链接并进行深度分析
2. **语义化提取**：从网页中提取结构化内容，包括主要观点、实体和代码片段
3. **交互式任务**：执行复杂的网页交互任务，支持任务描述和结果验证
4. **与六大特性集成**：支持与 PowerAutomation 系统的六大特性无缝集成

## 安装与配置

WebAgentB 增强适配器已集成到 PowerAutomation 系统的 MCP 增强组件层中，无需额外安装。只需确保项目依赖已正确安装：

```bash
cd /path/to/powerautomation_integration
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from mcptool.enhancers import WebAgentBAdapter

# 初始化 WebAgentB 适配器
webagent = WebAgentBAdapter()

# 执行增强搜索
results = webagent.enhanced_search("人工智能最新发展", depth=2)

# 语义化提取页面内容
semantic_content = webagent.semantic_extract("https://example.com/ai-article")

# 执行交互式任务
task_result = webagent.interactive_task(
    "https://example.com/form", 
    "填写表单并提交，然后验证提交成功"
)
```

### 与六大特性集成

WebAgentB 可以与 PowerAutomation 系统的六大特性无缝集成，特别是在内容特性和思维特性方面提供强大支持：

```python
from agents.features import GeneralAgentFeatures
from mcptool.enhancers import WebAgentBAdapter

# 初始化通用智能体特性
agent_features = GeneralAgentFeatures()

# 初始化 WebAgentB 适配器
webagent = WebAgentBAdapter()

# 使用 WebAgentB 增强内容特性
semantic_content = webagent.semantic_extract("https://example.com/article")
agent_features.update_content_feature(semantic_content["structured_content"])

# 使用 WebAgentB 增强思维特性
search_results = webagent.enhanced_search("最新AI技术趋势", depth=2)
thinking_process = {
    "search_query": "最新AI技术趋势",
    "search_results": search_results,
    "analysis": "基于搜索结果的分析...",
    "conclusions": ["结论1", "结论2", "结论3"]
}
agent_features.update_thinking_feature(thinking_process)
```

### 与多智能体路由集成

WebAgentB 可以与多智能体路由系统集成，为网页智能体提供增强能力：

```python
from frontend.src.utils.agent_router import AgentRouter
from mcptool.enhancers import WebAgentBAdapter

# 初始化智能体路由器
router = AgentRouter()

# 初始化 WebAgentB 适配器
webagent = WebAgentBAdapter()

# 注册 WebAgentB 增强的网页智能体处理函数
def enhanced_web_agent_handler(request):
    # 使用 WebAgentB 处理请求
    if "search" in request:
        return webagent.enhanced_search(request["search"])
    elif "extract" in request:
        return webagent.semantic_extract(request["extract"])
    elif "task" in request:
        return webagent.interactive_task(request["url"], request["task"])
    else:
        return {"error": "Unsupported request type"}

# 注册处理函数
router.register_handler("web", enhanced_web_agent_handler)
```

## API 参考

### WebAgentBAdapter 类

#### 初始化

```python
WebAgentBAdapter()
```

初始化 WebAgentB 增强适配器。

#### 增强搜索

```python
enhanced_search(query: str, depth: int = 2) -> List[Dict]
```

执行增强搜索，支持多层次信息收集。

**参数**：
- `query`：搜索查询
- `depth`：搜索深度，表示跟踪链接的层数

**返回值**：
- 增强搜索结果列表，每个结果包含标题、URL、摘要、语义分析等信息

#### 语义化提取

```python
semantic_extract(url: str) -> Dict
```

语义化提取页面内容。

**参数**：
- `url`：页面 URL

**返回值**：
- 语义化内容字典，包含原始内容和结构化内容

#### 交互式任务

```python
interactive_task(url: str, task_description: str) -> Dict
```

执行交互式任务。

**参数**：
- `url`：页面 URL
- `task_description`：任务描述

**返回值**：
- 任务执行结果字典，包含状态、消息、执行步骤和截图等信息

## 最佳实践

1. **错误处理**：WebAgentB 适配器内部已实现错误处理，但在生产环境中，建议额外添加错误处理逻辑
2. **性能优化**：对于大量请求，考虑实现缓存机制，避免重复处理相同的页面
3. **集成测试**：在集成到生产环境前，确保通过端到端测试验证功能正常

## 常见问题

### WebAgentB 适配器初始化失败

如果 WebAgentB 适配器初始化失败，可能是因为依赖组件不可用。请检查：

1. 确保所有依赖已正确安装
2. 检查网络连接是否正常
3. 查看日志获取详细错误信息

### 增强搜索返回基础结果

如果增强搜索只返回基础结果，没有增强内容，可能是因为：

1. WebAgentB 组件不可用
2. 搜索查询过于复杂或模糊
3. 网络连接问题

尝试使用更具体的查询，或检查 WebAgentB 组件状态。

## 与 Supermemory.ai 集成

WebAgentB 可以与 Supermemory.ai 无限上下文记忆功能集成，提供更强大的网页理解能力：

```python
from mcptool.adapters import InfiniteContextAdapter
from mcptool.enhancers import WebAgentBAdapter

# 初始化适配器
context_adapter = InfiniteContextAdapter()
webagent = WebAgentBAdapter()

# 使用 WebAgentB 提取页面内容
semantic_content = webagent.semantic_extract("https://example.com/article")

# 将内容存储到无限上下文记忆
context_id = context_adapter.store_context({
    "type": "web_content",
    "url": "https://example.com/article",
    "content": semantic_content
})

# 后续可以通过 context_id 检索内容
retrieved_content = context_adapter.retrieve_context(context_id)
```

## 结论

WebAgentB 增强适配器为 PowerAutomation 系统提供了强大的网页理解与交互能力，是构建高级网页智能体的重要组件。通过本文档的指导，开发者可以快速上手并有效利用这一组件，为用户提供更智能、更高效的网页交互体验。
