# PowerAutomation 系统架构文档

## 1. 系统概述

PowerAutomation是一个基于智能体的自动化平台，通过多种专业智能体和MCP（Multi-agent Collaborative Protocol）模块提供高效的自动化解决方案。系统采用前后端分离架构，通过统一的API接口实现智能体与前端UI的解耦，确保特性需求和UI需求不被硬编码在代码中。

### 1.1 核心理念

- **智能体解耦**：所有智能体实现独立于前后端代码，通过统一接口调用
- **MCP驱动**：所有智能体通过MCP规划器和MCP头脑风暴器调用开发工具模块和已有工具
- **动态能力适配**：智能体通过能力声明机制动态适配UI和功能需求
- **前后端分离**：前端只负责UI渲染和用户交互，后端只负责API路由和请求处理

## 2. 系统架构

### 2.1 目录结构

```
powerautomation_new/
├── agents/                     # 所有智能体实现
│   ├── base/                   # 基础智能体模块
│   │   └── base_agent.py       # 智能体基类
│   ├── general/                # 通用智能体
│   │   └── general_agent.py    # 通用智能体实现
│   ├── ppt/                    # PPT智能体
│   │   └── ppt_agent.py        # PPT智能体实现
│   ├── web/                    # 网页智能体
│   │   └── web_agent.py        # 网页智能体实现
│   ├── code/                   # 代码智能体
│   │   └── code_agent.py       # 代码智能体实现
│   └── ppt_agent/              # PPT智能体MCP模块
│       └── core/
│           └── mcp/
│               ├── mcp_planner.py             # MCP规划器
│               ├── mcp_brainstorm.py          # MCP头脑风暴器
│               └── mcp_central_coordinator.py  # MCP中央协调器
├── backend/                    # 后端服务
│   ├── routes/                 # API路由
│   │   ├── general_agent_routes.py  # 通用智能体API路由
│   │   ├── ppt_agent_routes.py      # PPT智能体API路由
│   │   ├── web_agent_routes.py      # 网页智能体API路由
│   │   └── code_agent_routes.py     # 代码智能体API路由
│   ├── services/               # 服务层
│   └── main.py                 # 后端主入口
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/         # 通用组件
│   │   ├── pages/              # 页面组件
│   │   │   ├── Home.jsx        # 首页
│   │   │   ├── GeneralAgent.jsx  # 通用智能体页面
│   │   │   ├── WebAgent.jsx      # 网页智能体页面
│   │   │   └── ...
│   │   └── styles/             # 样式文件
│   └── ...
├── development_tools/          # 开发工具模块
│   ├── agent_problem_solver.py  # 智能体问题解决器
│   ├── thought_action_recorder.py  # 思考与操作记录器
│   ├── release_manager.py      # 发布管理器
│   └── test_issue_collector.py  # 测试与问题收集器
├── tests/                      # 测试目录
│   └── e2e/                    # 端到端测试
│       ├── general_agent_test_plan.md  # 通用智能体测试方案
│       ├── ppt_agent_test_plan.md      # PPT智能体测试方案
│       ├── code_agent_test_plan.md     # 代码智能体测试方案
│       └── ...
└── visual_test/                # 视觉测试
    ├── general_agent_test_plan.md  # 通用智能体视觉测试方案
    ├── web_agent_test_plan.md      # 网页智能体视觉测试方案
    └── ...
```

### 2.2 核心组件

#### 2.2.1 智能体 (Agents)

所有智能体都继承自`BaseAgent`基类，实现统一的接口，包括：

- **process(input_data)**: 处理输入数据并返回结果
- **get_capabilities()**: 获取智能体能力列表
- **validate_input(input_data)**: 验证输入数据是否有效
- **execute(input_data)**: 执行完整的处理流程

主要智能体包括：

1. **通用智能体 (GeneralAgent)**
   - 负责对话、任务执行和项目管理
   - 协调其他智能体完成复杂任务

2. **PPT智能体 (PPTAgent)**
   - 负责生成和管理PPT演示文稿
   - 支持文本转PPT、思维导图转PPT等功能

3. **网页智能体 (WebAgent)**
   - 负责网页抓取、内容分析和自动化操作
   - 支持数据提取、网页分析等功能

4. **代码智能体 (CodeAgent)**
   - 负责代码生成、调试和优化
   - 支持多语言代码生成、错误修复等功能

#### 2.2.2 MCP模块

MCP (Multi-agent Collaborative Protocol) 模块是智能体协作的核心，包括：

1. **MCP规划器 (MCPPlanner)**
   - 负责任务解析和规划
   - 生成执行计划和策略

2. **MCP头脑风暴器 (MCPBrainstorm)**
   - 负责创意生成和方案设计
   - 在规划器无法处理时提供备选方案

3. **MCP中央协调器 (MCPCentralCoordinator)**
   - 负责多智能体协调和资源分配
   - 管理任务优先级和执行顺序

#### 2.2.3 开发工具模块

开发工具模块提供支持智能体开发和测试的工具：

1. **智能体问题解决器 (AgentProblemSolver)**
   - 分析和解决智能体运行中遇到的问题
   - 提供问题诊断和修复建议

2. **思考与操作记录器 (ThoughtActionRecorder)**
   - 记录智能体的思考过程和操作
   - 支持调试和性能分析

3. **发布管理器 (ReleaseManager)**
   - 管理代码版本和发布流程
   - 确保代码质量和兼容性

4. **测试与问题收集器 (TestAndIssueCollector)**
   - 执行测试用例并收集结果
   - 生成测试报告和问题清单

### 2.3 前后端交互

#### 2.3.1 后端API路由

后端通过API路由层将请求转发给相应的智能体：

```python
@router.post("/chat")
async def chat(request: ChatRequest):
    # 获取通用智能体实例
    agent = get_general_agent()
    
    # 准备输入数据
    input_data = {
        "task_type": "chat",
        "query": request.query,
        "session_id": request.session_id,
        "context": request.context
    }
    
    # 调用智能体处理请求
    result = agent.process(input_data)
    
    return result
```

#### 2.3.2 前端动态适配

前端根据智能体声明的能力动态生成UI组件：

```jsx
// 获取智能体能力
useEffect(() => {
  const fetchCapabilities = async () => {
    const response = await api.getAgentCapabilities('general');
    setCapabilities(response.data.capabilities);
  };
  
  fetchCapabilities();
}, []);

// 根据能力动态渲染UI
return (
  <div className="agent-container">
    <h1>通用智能体</h1>
    
    {capabilities.map((capability, index) => (
      <CapabilityCard 
        key={index}
        title={capability}
        onClick={() => activateCapability(capability)}
      />
    ))}
  </div>
);
```

## 3. 数据流

### 3.1 请求处理流程

1. 用户通过前端界面提交请求
2. 前端将请求发送到后端API
3. 后端API路由将请求转发给相应的智能体
4. 智能体通过MCP模块处理请求
5. 智能体返回处理结果
6. 后端API将结果返回给前端
7. 前端根据结果更新UI

### 3.2 智能体协作流程

1. 通用智能体接收复杂任务
2. 通用智能体通过MCP规划器分析任务
3. MCP规划器生成任务执行计划
4. 通用智能体根据计划调度其他智能体
5. 其他智能体执行子任务并返回结果
6. 通用智能体整合所有结果
7. 通用智能体返回最终结果

## 4. 扩展性设计

### 4.1 添加新智能体

添加新智能体的步骤：

1. 在`agents/`目录下创建新的子目录
2. 创建新智能体类，继承自`BaseAgent`
3. 实现必要的方法（process, get_capabilities等）
4. 在后端创建相应的API路由
5. 在前端添加相应的UI组件

### 4.2 添加新MCP模块

添加新MCP模块的步骤：

1. 在`agents/ppt_agent/core/mcp/`目录下创建新的MCP模块
2. 实现必要的方法（plan, optimize等）
3. 在智能体中集成新的MCP模块

## 5. 部署架构

### 5.1 开发环境

- **前端**: Node.js, React
- **后端**: Python, FastAPI
- **数据库**: SQLite (开发), PostgreSQL (生产)

### 5.2 生产环境

- **容器化**: Docker
- **编排**: Kubernetes
- **CI/CD**: GitHub Actions
- **监控**: Prometheus, Grafana

## 6. 安全考虑

- **API认证**: JWT令牌
- **数据加密**: HTTPS, AES
- **输入验证**: 所有输入经过验证
- **权限控制**: 基于角色的访问控制

## 7. 未来规划

- **更多智能体**: 添加更多专业智能体
- **增强MCP**: 改进MCP模块的协作能力
- **移动端支持**: 开发移动应用
- **多语言支持**: 添加多语言界面

## 8. 附录

### 8.1 技术栈

- **前端**: React, Redux, Ant Design
- **后端**: Python, FastAPI, SQLAlchemy
- **测试**: Pytest, Playwright
- **文档**: Markdown, Swagger

### 8.2 相关资源

- **代码仓库**: GitHub
- **API文档**: Swagger UI
- **测试报告**: TestAndIssueCollector生成
