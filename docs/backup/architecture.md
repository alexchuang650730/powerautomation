# PowerAutomation 架构文档

## 1. 系统概述

PowerAutomation是一个多智能体自动化平台，支持PPT智能体、代码智能体、网页智能体和通用智能体。通过集成Sequential Thinking MCP和Playwright MCP（含WebAgentB增强），系统获得了更强大的任务规划、创意生成和问题解决能力。

## 2. 架构设计

### 2.1 整体架构

PowerAutomation采用模块化、分层架构设计，主要包括以下层次：

1. **智能体层**：包含各类专用智能体，如PPT智能体、代码智能体等
2. **MCP核心层**：提供MCP（Multi-agent Collaborative Protocol）核心功能
3. **工具适配层**：提供与外部工具和服务的集成接口
4. **开发工具层**：提供开发支持和辅助功能
5. **前后端层**：提供用户界面和API服务

### 2.2 目录结构

```
powerautomation/
├── agents/                     # 智能体模块
│   ├── ppt_agent/             # PPT智能体
│   │   ├── core/              # 核心功能
│   │   │   └── mcp/           # MCP优化模块（新增）
│   │   │       ├── sequential_thinking_adapter.py  # Sequential Thinking适配器
│   │   │       ├── playwright_adapter.py           # Playwright适配器
│   │   │       ├── webagent_adapter.py             # WebAgentB增强适配器
│   │   │       ├── enhanced_mcp_planner.py         # 增强版MCP规划器
│   │   │       ├── enhanced_mcp_brainstorm.py      # 增强版MCP头脑风暴器
│   │   │       └── proactive_problem_solver.py     # 主动问题解决器
│   ├── code_agent/            # 代码智能体
│   ├── web_agent/             # 网页智能体
│   └── general_agent/         # 通用智能体
├── backend/                    # 后端服务
│   ├── routes/                # API路由
│   └── services/              # 业务服务
├── frontend/                   # 前端界面
├── development_tools/          # 开发工具模块
├── tests/                      # 测试目录
│   └── e2e/                   # 端到端测试
└── docs/                       # 文档
```

### 2.3 核心组件

#### 2.3.1 智能体组件

- **PPT智能体**：负责PPT生成和编辑
- **代码智能体**：负责代码生成和优化
- **网页智能体**：负责网页抓取和分析
- **通用智能体**：负责通用任务处理

#### 2.3.2 MCP核心组件

- **MCP规划器**：负责任务规划和分解
- **MCP头脑风暴器**：负责创意生成和验证
- **MCP中央协调器**：负责多智能体协调

#### 2.3.3 新增MCP增强组件

- **Sequential Thinking适配器**：提供任务拆解和反思能力
- **Playwright适配器**：提供浏览器自动化能力
- **WebAgentB适配器**：提供高级网页理解与交互能力
- **增强版MCP规划器**：集成Sequential Thinking的规划器
- **增强版MCP头脑风暴器**：集成Playwright和WebAgentB的头脑风暴器
- **主动问题解决器**：集成Sequential Thinking和WebAgentB的问题解决器

## 3. 模块关系

### 3.1 模块依赖关系

```
                                  +-------------------+
                                  |  智能体 (Agents)   |
                                  +--------+----------+
                                           |
                                           v
+----------------+            +------------------------+
|  开发工具       |<---------->|  MCP核心组件           |
| (Dev Tools)    |            | (MCP Core Components) |
+----------------+            +------------+-----------+
                                           |
                                           v
                              +------------------------+
                              |  MCP增强组件           |
                              | (MCP Enhancements)    |
                              +------------+-----------+
                                           |
                                           v
                              +------------------------+
                              |  外部工具适配器        |
                              | (External Adapters)   |
                              +------------------------+
```

### 3.2 关键接口

#### 3.2.1 MCP规划器接口

```python
class MCPPlanner:
    def plan(self, task_description: str) -> Dict:
        """规划任务"""
        pass
    
    def adjust_plan(self, plan: Dict, feedback: Dict) -> Dict:
        """根据反馈调整规划"""
        pass
```

#### 3.2.2 MCP头脑风暴器接口

```python
class MCPBrainstorm:
    def generate(self, topic: str, context: Optional[Dict] = None) -> Dict:
        """生成创意"""
        pass
    
    def validate(self, ideas: List[Dict]) -> List[Dict]:
        """验证创意可行性"""
        pass
```

#### 3.2.3 问题解决器接口

```python
class ProblemSolver:
    def solve_problem(self, problem: Dict) -> Dict:
        """解决问题"""
        pass
    
    def solve_on_event(self, event_type: str) -> Dict:
        """基于事件触发问题解决"""
        pass
```

## 4. 集成方案

### 4.1 集成策略

本集成方案采用渐进式策略，分为以下阶段：

1. **基础集成**：将Sequential Thinking和Playwright适配器集成到MCP核心组件
2. **功能增强**：基于适配器增强MCP规划器和头脑风暴器
3. **高级功能**：实现主动问题解决器等高级功能

### 4.2 集成点

主要集成点包括：

1. **agents/ppt_agent/core/mcp/**：MCP增强组件的主要集成位置
2. **development_tools/**：与开发工具的集成点
3. **tests/e2e/**：端到端测试集成点

### 4.3 接口适配

为确保兼容性，所有新增组件都遵循以下原则：

1. **向后兼容**：保持与原有接口的兼容性
2. **适配器模式**：使用适配器隔离外部依赖
3. **统一接口**：提供统一的接口定义

## 5. 数据流

### 5.1 任务规划数据流

```
用户请求 -> 智能体 -> MCP规划器 -> Sequential Thinking适配器 -> 任务分解
                                                          -> 任务执行
                                                          -> 反思与调整
```

### 5.2 创意生成数据流

```
用户请求 -> 智能体 -> MCP头脑风暴器 -> WebAgentB适配器 -> 信息收集
                                                    -> 创意生成
                                  -> Playwright适配器 -> 创意验证
```

### 5.3 问题解决数据流

```
事件触发 -> 主动问题解决器 -> Sequential Thinking适配器 -> 任务规划
                         -> WebAgentB适配器 -> 信息收集
                                           -> 问题分析
                                           -> 解决方案生成
                         -> GitHub推送管理器 -> 解决方案实现
                                            -> 代码提交
```

## 6. 部署架构

### 6.1 开发环境

- **操作系统**：Ubuntu 22.04 LTS
- **Python版本**：3.8+
- **浏览器**：Chrome 最新版
- **依赖库**：见requirements.txt

### 6.2 生产环境

- **容器化**：使用Docker容器化部署
- **编排**：使用Kubernetes进行容器编排
- **CI/CD**：使用GitHub Actions进行持续集成和部署

## 7. 安全考虑

- **API认证**：所有API接口使用OAuth2认证
- **数据加密**：敏感数据使用AES-256加密
- **权限控制**：基于角色的访问控制（RBAC）

## 8. 性能考虑

- **异步处理**：使用异步任务处理长时间运行的任务
- **缓存策略**：使用Redis缓存频繁访问的数据
- **资源限制**：对资源密集型操作设置限制

## 9. 扩展性考虑

- **插件系统**：支持通过插件扩展功能
- **微服务架构**：关键组件可独立部署为微服务
- **API版本控制**：支持API版本控制以便平滑升级

## 10. 未来规划

### 10.1 近期规划

- 集成RL-Factory的环境解耦和异步工具调用机制
- 增强多智能体协作能力
- 开发WebUI用于可视化配置和监控

### 10.2 长期规划

- 支持更多类型的智能体
- 实现自适应学习机制
- 构建知识图谱增强决策能力
