# Supermemory.ai 无限记忆 API 集成指南

## 1. 概述

PowerAutomation 系统集成了 supermemory.ai 的无限记忆 API，为系统提供强大的无限上下文记忆能力。本指南详细说明如何配置和使用 supermemory.ai API，确保系统能够正确存储和检索上下文记忆。

## 2. API 集成架构

PowerAutomation 系统通过以下组件与 supermemory.ai 进行集成：

1. **无限上下文适配器**：`mcptool/adapters/infinite_context_adapter.py`
2. **记忆管理服务**：`backend/services/memory_service.py`
3. **前端记忆组件**：`frontend/src/utils/memory-manager.js`

这些组件协同工作，确保用户查询和系统思考过程能够被正确存储和检索，实现无限上下文记忆功能。

## 3. API Key 配置

### 3.1 获取 API Key

1. 访问 [supermemory.ai](https://supermemory.ai) 官方网站
2. 注册或登录您的账户
3. 导航至 API 管理页面
4. 创建新的 API Key，选择适当的权限级别
5. 复制生成的 API Key

### 3.2 配置 API Key

#### 3.2.1 环境变量配置（推荐）

在系统环境中设置以下环境变量：

```bash
# Linux/macOS
export SUPERMEMORY_API_KEY="your_api_key_here"
export SUPERMEMORY_API_URL="https://api.supermemory.ai/v1"

# Windows
set SUPERMEMORY_API_KEY=your_api_key_here
set SUPERMEMORY_API_URL=https://api.supermemory.ai/v1
```

对于生产环境，建议将这些环境变量添加到系统的启动脚本或服务配置中。

#### 3.2.2 配置文件配置

或者，您可以在 `config/api_keys.json` 文件中配置 API Key：

```json
{
  "supermemory": {
    "api_key": "your_api_key_here",
    "api_url": "https://api.supermemory.ai/v1"
  }
}
```

**注意**：确保 `api_keys.json` 文件不被提交到版本控制系统中，以保护 API Key 的安全。

### 3.3 API Key 轮换

为了安全起见，建议定期轮换 API Key：

1. 在 supermemory.ai 管理页面创建新的 API Key
2. 更新系统中的 API Key 配置
3. 验证系统功能正常
4. 在 supermemory.ai 管理页面删除旧的 API Key

## 4. 无限上下文适配器配置

无限上下文适配器 (`infinite_context_adapter.py`) 是系统与 supermemory.ai API 交互的核心组件。以下是其主要配置选项：

### 4.1 基本配置

```python
# mcptool/adapters/infinite_context_adapter.py

class InfiniteContextAdapter:
    def __init__(self, config=None):
        self.config = config or {}
        self.api_key = self.config.get('api_key') or os.environ.get('SUPERMEMORY_API_KEY')
        self.api_url = self.config.get('api_url') or os.environ.get('SUPERMEMORY_API_URL', 'https://api.supermemory.ai/v1')
        self.max_tokens = self.config.get('max_tokens', 100000)
        self.compression_ratio = self.config.get('compression_ratio', 0.5)
        
        if not self.api_key:
            raise ValueError("Supermemory API Key not found. Please set SUPERMEMORY_API_KEY environment variable or provide in config.")
```

### 4.2 高级配置

您可以通过修改 `config/memory_config.json` 文件来调整无限上下文适配器的高级配置：

```json
{
  "memory": {
    "max_tokens": 100000,
    "compression_ratio": 0.5,
    "cache_ttl": 3600,
    "priority_weights": {
      "recency": 0.7,
      "relevance": 0.3
    },
    "storage_strategy": "hybrid",
    "indexing_method": "semantic"
  }
}
```

## 5. API 使用示例

### 5.1 存储记忆

```python
from mcptool.adapters.infinite_context_adapter import InfiniteContextAdapter

# 创建适配器实例
adapter = InfiniteContextAdapter()

# 存储记忆
memory_id = adapter.store_memory({
    "query": "如何优化PowerAutomation的UI布局特性？",
    "response": "PowerAutomation的UI布局可以通过以下方式优化...",
    "features": {
        "platform_feature": "PowerAutomation自动化平台",
        "ui_layout": "两栏布局，左侧为导航栏，右侧为主内容区",
        "prompt": "用户输入优化UI布局的请求",
        "thinking": "分析用户需求，确定UI优化方向",
        "content": "生成UI优化建议",
        "memory": "记录用户查询和系统思考过程"
    }
})

print(f"Memory stored with ID: {memory_id}")
```

### 5.2 检索记忆

```python
# 检索记忆
memories = adapter.retrieve_memories("UI布局优化", limit=5)

for memory in memories:
    print(f"Query: {memory['query']}")
    print(f"Response: {memory['response']}")
    print(f"Features: {memory['features']}")
    print("---")
```

### 5.3 前端集成

```javascript
// frontend/src/utils/memory-manager.js

class MemoryManager {
  constructor() {
    this.apiUrl = process.env.REACT_APP_SUPERMEMORY_API_URL || 'https://api.supermemory.ai/v1';
    this.headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.REACT_APP_SUPERMEMORY_API_KEY}`
    };
  }

  async storeMemory(data) {
    try {
      const response = await fetch(`${this.apiUrl}/memories`, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(data)
      });
      
      return await response.json();
    } catch (error) {
      console.error('Error storing memory:', error);
      throw error;
    }
  }

  async retrieveMemories(query, limit = 5) {
    try {
      const response = await fetch(`${this.apiUrl}/memories/search?q=${encodeURIComponent(query)}&limit=${limit}`, {
        method: 'GET',
        headers: this.headers
      });
      
      return await response.json();
    } catch (error) {
      console.error('Error retrieving memories:', error);
      throw error;
    }
  }
}

export default new MemoryManager();
```

## 6. 安全最佳实践

### 6.1 API Key 安全

1. **永不硬编码**：不要在代码中硬编码 API Key
2. **使用环境变量**：优先使用环境变量存储 API Key
3. **限制访问权限**：确保只有需要的服务和人员能够访问 API Key
4. **定期轮换**：定期更换 API Key，特别是在人员变动时
5. **监控使用情况**：定期检查 API 使用日志，发现异常及时处理

### 6.2 数据安全

1. **数据加密**：确保传输中和存储中的数据都经过加密
2. **最小权限原则**：只请求和存储必要的数据
3. **数据清理**：定期清理不再需要的历史数据
4. **合规性**：确保数据处理符合相关法规要求

## 7. 故障排除

### 7.1 常见问题

1. **API Key 无效**：
   - 检查 API Key 是否正确配置
   - 确认 API Key 未过期或被撤销
   - 验证 API Key 权限级别是否足够

2. **请求超时**：
   - 检查网络连接
   - 确认 API 服务状态
   - 考虑增加请求超时时间

3. **记忆检索不准确**：
   - 调整检索参数，如相关性阈值
   - 优化记忆存储结构
   - 考虑使用更精确的查询关键词

### 7.2 日志和监控

系统会自动记录与 supermemory.ai API 的交互日志，位于 `logs/api_interactions.log`。您可以通过以下命令查看最近的日志：

```bash
tail -f logs/api_interactions.log
```

## 8. API 限制和配额

supermemory.ai API 有以下使用限制：

- **每日请求限制**：10,000 次请求/天
- **每分钟请求限制**：60 次请求/分钟
- **单次请求大小限制**：10MB
- **存储容量限制**：根据您的订阅计划而定

超出限制可能导致请求被拒绝或额外费用。系统会自动处理限流情况，但建议监控使用情况，避免超出配额。

## 9. 升级和维护

### 9.1 API 版本更新

supermemory.ai 可能会更新其 API。当有新版本发布时：

1. 查阅官方更新文档
2. 测试新版本 API 的兼容性
3. 更新系统中的 API 集成代码
4. 全面测试系统功能

### 9.2 依赖管理

确保定期更新系统依赖，特别是与 API 交互相关的库：

```bash
pip install -U supermemory-client
```

## 10. 附录

### 10.1 API 参考文档

完整的 supermemory.ai API 文档可在以下位置找到：
- [Supermemory API 文档](https://docs.supermemory.ai)

### 10.2 相关文件

- `mcptool/adapters/infinite_context_adapter.py`：无限上下文适配器
- `backend/services/memory_service.py`：记忆管理服务
- `frontend/src/utils/memory-manager.js`：前端记忆组件
- `config/memory_config.json`：记忆配置文件
- `config/api_keys.json`：API Key 配置文件（不包含在版本控制中）
