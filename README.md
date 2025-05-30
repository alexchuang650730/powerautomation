# PowerAutomation 多智能体平台

PowerAutomation是一个多智能体平台，集成了多种专业智能体，包括PPT智能体、文档智能体、表格智能体、网页智能体、播客智能体和通用智能体等。本项目采用模块化设计，每个智能体都集成了六大MCP（模块化认知处理器），提供高度定制化的AI服务。

## 项目结构

```
powerautomation/
├── agents/                  # 智能体目录
│   ├── ppt_agent/           # PPT智能体
│   │   ├── __init__.py
│   │   ├── ppt_agent.py     # PPT智能体主类
│   │   ├── core/            # 核心功能
│   │   │   ├── mcp/         # 模块化认知处理器
│   │   │   │   ├── base_mcp.py                      # MCP基类
│   │   │   │   ├── prompt_optimization_mcp.py       # 提示词优化MCP
│   │   │   │   ├── feature_optimization_mcp.py      # 特性优化MCP
│   │   │   │   ├── ui_journey_optimization_mcp.py   # 用户界面旅程优化MCP
│   │   │   │   ├── content_template_optimization_mcp.py  # 内容模板优化MCP
│   │   │   │   ├── context_matching_optimization_mcp.py  # 思维上下文匹配优化MCP
│   │   │   │   └── project_memory_optimization_mcp.py    # 项目级记忆优化MCP
│   │   │   └── utils/       # 工具函数
│   │   ├── templates/       # PPT模板
│   │   └── output/          # 输出目录
│   ├── web_agent/           # 网页智能体（集成WebAgentB和Claude）
│   │   ├── __init__.py
│   │   ├── web_agent.py
│   │   └── core/
│   │       ├── mcp/         # 模块化认知处理器
│   │       └── webagentb/   # WebAgentB集成
│   └── ...                  # 其他智能体
├── backend/                 # 后端服务
│   ├── __init__.py
│   ├── main.py              # 主应用入口
│   ├── routes/              # API路由
│   │   ├── __init__.py
│   │   ├── ppt_agent_routes.py
│   │   └── web_agent_routes.py
│   ├── services/            # 服务层
│   └── utils/               # 工具函数
├── frontend/                # 前端代码
│   ├── public/
│   └── src/
│       ├── components/      # 组件
│       ├── pages/           # 页面
│       ├── styles/          # 样式
│       └── utils/           # 工具函数
├── visual_test/             # 端到端视觉化测试
│   ├── README.md
│   ├── ppt_task_manager.py
│   ├── test_ppt_generation.py
│   ├── ppt_to_image.py
│   └── static/
│       └── templates/
└── requirements.txt         # 项目依赖
```

## 智能体架构

每个智能体都集成了六大MCP（模块化认知处理器）：

1. **提示词优化MCP**：负责生成和优化提示词
2. **特性优化MCP**：负责智能体的核心功能
3. **用户界面旅程优化MCP**：负责用户交互和体验
4. **内容模板优化MCP**：负责管理和应用内容模板
5. **思维上下文匹配优化MCP**：负责理解和匹配上下文
6. **项目级记忆优化MCP**：负责管理项目记忆（集成SuperMemory.ai）

## PPT智能体

PPT智能体是一个专业级PPT生成工具，能够根据用户需求自动生成高质量的PPT演示文稿。

### 主要功能

- 根据用户输入的主题和内容生成完整PPT
- 支持多种专业模板
- 自动优化内容结构和布局
- 智能匹配适合的样式和配色
- 保存项目记忆，支持后续修改和优化

### 使用方法

```python
from agents.ppt_agent.ppt_agent import PPTAgent

# 初始化PPT智能体
ppt_agent = PPTAgent()

# 生成PPT
result = ppt_agent.generate_ppt({
    "title": "公司业务介绍",
    "content": "这是一个关于我们公司业务的介绍...",
    "template_type": "business",
    "output_path": "output/business_presentation.pptx"
})

print(f"PPT已生成: {result['output_path']}")
```

## 网页智能体

网页智能体集成了WebAgentB和Claude，提供增强的网页搜索和内容分析能力。

### 主要功能

- 高级网页搜索和内容提取
- 多源信息整合和分析
- 网页内容理解和摘要
- 搜索历史记忆和个性化推荐

### 使用方法

```python
from agents.web_agent.web_agent import WebAgent

# 初始化网页智能体
web_agent = WebAgent()

# 执行网页搜索
result = web_agent.process({
    "mcp_type": "feature",
    "search_action": "web_search",
    "query": "人工智能最新发展",
    "result_count": 5
})

print(f"搜索结果: {result}")
```

## API接口

### PPT智能体API

- `GET /api/agents/ppt/info` - 获取PPT智能体信息
- `POST /api/agents/ppt/process` - 处理PPT智能体请求
- `POST /api/agents/ppt/generate` - 生成PPT
- `GET /api/agents/ppt/templates` - 列出可用的PPT模板
- `POST /api/agents/ppt/memory` - 管理项目记忆

### 网页智能体API

- `GET /api/agents/web/info` - 获取网页智能体信息
- `POST /api/agents/web/search` - 执行网页搜索
- `POST /api/agents/web/analyze` - 分析网页内容
- `GET /api/agents/web/templates` - 获取结果展示模板
- `POST /api/agents/web/memory` - 管理搜索历史

## 安装与部署

### 依赖安装

```bash
pip install -r requirements.txt
```

### 启动后端服务

```bash
cd backend
python main.py
```

### 启动前端开发服务器

```bash
cd frontend
npm install
npm start
```

## 端到端测试

详见 [visual_test/README.md](visual_test/README.md)

## 技术栈

- **后端**：Flask, Python 3.11
- **前端**：React, TypeScript
- **数据库**：SQLite (开发), MySQL (生产)
- **API**：RESTful API
- **外部服务**：SuperMemory.ai, WebAgentB, Claude

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT License
