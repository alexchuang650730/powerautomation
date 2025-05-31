# Playwright MCP 集成指南

## 概述

Playwright MCP 是 PowerAutomation 系统中的核心增强组件，提供浏览器自动化能力。它能够执行网页搜索、内容提取、创意验证和交互式探索等操作，为系统提供强大的网页交互能力。本文档详细介绍了 Playwright MCP 的功能、接口和集成方法，帮助开发者快速上手并有效利用这一组件。

## 功能特点

Playwright MCP 适配器提供以下核心功能：

1. **信息搜索**：执行网页搜索并返回结构化结果
2. **页面内容提取**：从指定URL提取页面内容
3. **创意验证**：验证创意的可行性并提供评分和理由
4. **交互式探索**：交互式探索网页内容，发现可交互元素
5. **截图功能**：截取网页或特定元素的截图

## 安装与配置

Playwright MCP 适配器已集成到 PowerAutomation 系统的 MCP 增强组件层中，无需额外安装。只需确保项目依赖已正确安装：

```bash
cd /path/to/powerautomation_integration
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from mcptool.enhancers import PlaywrightAdapter

# 初始化 Playwright 适配器
playwright = PlaywrightAdapter()

# 搜索信息
results = playwright.search_information("人工智能最新发展")

# 提取页面内容
content = playwright.extract_page_content("https://example.com/ai-article")

# 验证创意可行性
idea = {
    "id": "idea-001",
    "content": "开发一个基于AI的自动化测试工具"
}
validation = playwright.validate_idea(idea)

# 交互式探索内容
exploration = playwright.explore_interactively("GitHub仓库链接: https://github.com/example/repo")

# 截取截图
screenshot_path = playwright.take_screenshot("https://example.com", element_selector=".main-content")
```

### 与六大特性集成

Playwright MCP 可以与 PowerAutomation 系统的六大特性无缝集成，特别是在内容特性和提示词特性方面提供强大支持：

```python
from agents.features import GeneralAgentFeatures
from mcptool.enhancers import PlaywrightAdapter

# 初始化通用智能体特性
agent_features = GeneralAgentFeatures()

# 初始化 Playwright 适配器
playwright = PlaywrightAdapter()

# 搜索信息并增强内容特性
search_results = playwright.search_information("最新AI技术趋势")
agent_features.update_content_feature({
    "search_query": "最新AI技术趋势",
    "search_results": search_results
})

# 提取页面内容并增强提示词特性
page_content = playwright.extract_page_content("https://example.com/ai-trends")
agent_features.update_prompt_feature({
    "source": "https://example.com/ai-trends",
    "content": page_content,
    "extracted_keywords": ["AI", "趋势", "技术", "发展"]
})
```

### 与多智能体路由集成

Playwright MCP 可以与多智能体路由系统集成，为网页智能体提供自动化能力：

```python
from frontend.src.utils.agent_router import AgentRouter
from mcptool.enhancers import PlaywrightAdapter

# 初始化智能体路由器
router = AgentRouter()

# 初始化 Playwright 适配器
playwright = PlaywrightAdapter()

# 注册 Playwright 增强的网页智能体处理函数
def enhanced_web_agent_handler(request):
    # 使用 Playwright 处理请求
    if "search" in request:
        return playwright.search_information(request["search"])
    elif "extract" in request:
        return playwright.extract_page_content(request["extract"])
    elif "validate" in request:
        return playwright.validate_idea(request["validate"])
    elif "explore" in request:
        return playwright.explore_interactively(request["explore"])
    else:
        return {"error": "Unsupported request type"}

# 注册处理函数
router.register_handler("web", enhanced_web_agent_handler)
```

## API 参考

### PlaywrightAdapter 类

#### 初始化

```python
PlaywrightAdapter()
```

初始化 Playwright 适配器。

#### 搜索信息

```python
search_information(query: str) -> List[Dict]
```

搜索信息。

**参数**：
- `query`：搜索查询

**返回值**：
- 搜索结果列表，每个结果包含标题、URL和摘要

#### 提取页面内容

```python
extract_page_content(url: str) -> Optional[str]
```

提取页面内容。

**参数**：
- `url`：页面URL

**返回值**：
- 页面内容，如果提取失败则返回None

#### 验证创意可行性

```python
validate_idea(idea: Dict) -> Dict
```

验证创意可行性。

**参数**：
- `idea`：创意信息

**返回值**：
- 验证结果，包含有效性、分数和理由

#### 交互式探索内容

```python
explore_interactively(content: str) -> Dict
```

交互式探索内容。

**参数**：
- `content`：探索内容

**返回值**：
- 探索结果，包含发现的内容和时间戳

#### 截取截图

```python
take_screenshot(url: str, element_selector: Optional[str] = None) -> Optional[str]
```

截取网页或元素截图。

**参数**：
- `url`：网页URL
- `element_selector`：元素选择器，如果为None则截取整个页面

**返回值**：
- 截图文件路径，如果截图失败则返回None

## 与主工作流集成

Playwright MCP 在 PowerAutomation 系统的主工作流中扮演着重要角色，特别是在网页智能体的信息收集和内容验证阶段：

1. **信息收集阶段**：
   - 用户请求网页相关信息
   - 网页智能体调用 Playwright MCP 进行搜索和内容提取
   - 生成结构化的搜索结果和页面内容

2. **内容验证阶段**：
   - 系统生成创意或方案
   - 调用创意验证功能评估可行性
   - 根据验证结果调整方案

3. **交互探索阶段**：
   - 分析用户提供的内容
   - 发现可交互元素和链接
   - 提供进一步探索的建议

### 集成示例

```python
# 主工作流中的集成示例
from mcptool.enhancers import PlaywrightAdapter
from agents.features import WebAgentFeatures

def process_web_request(request, features):
    # 初始化组件
    playwright = PlaywrightAdapter()
    
    # 1. 信息收集阶段
    query = request.get("query", "")
    search_results = playwright.search_information(query)
    
    # 提取第一个结果的页面内容
    if search_results:
        url = search_results[0]["url"]
        page_content = playwright.extract_page_content(url)
    else:
        page_content = None
    
    # 2. 内容验证阶段
    if "idea" in request:
        validation = playwright.validate_idea(request["idea"])
    else:
        validation = None
    
    # 3. 更新内容特性
    content_update = {
        "query": query,
        "search_results": search_results,
        "page_content": page_content,
        "validation": validation
    }
    features.update_content_feature(content_update)
    
    return {
        "search_results": search_results,
        "page_content": page_content,
        "validation": validation
    }
```

## 与 WebAgentB 协同工作

Playwright MCP 可以与 WebAgentB 协同工作，提供更强大的网页交互能力：

```python
from mcptool.enhancers import PlaywrightAdapter, WebAgentBAdapter

# 初始化适配器
playwright = PlaywrightAdapter()
webagent = WebAgentBAdapter()

# 使用 Playwright 进行基础搜索
basic_results = playwright.search_information("人工智能最新发展")

# 使用 WebAgentB 进行增强搜索
enhanced_results = webagent.enhanced_search("人工智能最新发展", depth=2)

# 比较结果
comparison = {
    "basic_results_count": len(basic_results),
    "enhanced_results_count": len(enhanced_results),
    "enhanced_features": ["semantic_analysis", "related_pages"]
}

print(f"基础搜索结果数量: {comparison['basic_results_count']}")
print(f"增强搜索结果数量: {comparison['enhanced_results_count']}")
print(f"增强特性: {', '.join(comparison['enhanced_features'])}")
```

## 最佳实践

1. **错误处理**：Playwright 适配器内部已实现错误处理，但在生产环境中，建议额外添加错误处理逻辑
2. **性能优化**：对于频繁访问的页面，考虑实现缓存机制，避免重复提取内容
3. **并发控制**：在高并发场景下，控制同时打开的浏览器实例数量，避免资源耗尽
4. **超时设置**：为长时间运行的操作设置合理的超时时间，避免阻塞

## 常见问题

### Playwright 适配器初始化失败

如果 Playwright 适配器初始化失败，可能是因为：

1. Playwright 依赖未正确安装
2. 系统缺少必要的浏览器驱动
3. 权限问题导致无法启动浏览器

尝试运行 `playwright install` 安装必要的浏览器和驱动。

### 页面内容提取失败

如果页面内容提取失败，可能是因为：

1. URL 格式不正确
2. 网络连接问题
3. 页面需要认证或包含反爬虫机制

尝试使用有效的 URL，并确保网络连接正常。

## 与 Supermemory.ai 集成

Playwright MCP 可以与 Supermemory.ai 无限上下文记忆功能集成，提供更强大的网页内容记忆能力：

```python
from mcptool.adapters import InfiniteContextAdapter
from mcptool.enhancers import PlaywrightAdapter

# 初始化适配器
context_adapter = InfiniteContextAdapter()
playwright = PlaywrightAdapter()

# 搜索信息
search_results = playwright.search_information("人工智能最新发展")

# 提取页面内容
url = search_results[0]["url"]
page_content = playwright.extract_page_content(url)

# 将内容存储到无限上下文记忆
context_id = context_adapter.store_context({
    "type": "web_search",
    "query": "人工智能最新发展",
    "results": search_results,
    "page_content": page_content
})

# 后续可以通过 context_id 检索内容
retrieved_content = context_adapter.retrieve_context(context_id)
```

## 结论

Playwright MCP 适配器为 PowerAutomation 系统提供了强大的浏览器自动化能力，是构建高效网页智能体的重要组件。通过本文档的指导，开发者可以快速上手并有效利用这一组件，为用户提供更智能、更高效的网页交互体验。
