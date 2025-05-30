# PowerAutomation 平台

PowerAutomation 是一个多智能体协作平台，集成了PPT智能体、代码智能体、网页智能体和通用智能体，通过MCP（多智能体通信协议）实现智能体间的协作与优化。

## 项目结构

```
powerautomation/
├── agents/                      # 智能体模块
│   ├── ppt_agent/               # PPT智能体
│   │   ├── core/                # 核心功能
│   │   │   └── mcp/             # MCP优化模块
│   │   └── ppt_agent.py         # PPT智能体主类
│   ├── code_agent/              # 代码智能体
│   ├── web_agent/               # 网页智能体
│   └── general_agent/           # 通用智能体
├── backend/                     # 后端服务
│   ├── agents/                  # 智能体实现
│   ├── routes/                  # API路由
│   ├── services/                # 服务层
│   └── main.py                  # 主入口
├── frontend/                    # 前端界面
│   ├── src/                     # 源代码
│   │   ├── components/          # 组件
│   │   ├── pages/               # 页面
│   │   └── styles/              # 样式
│   └── public/                  # 静态资源
├── development_tools/           # 开发工具模块
│   ├── agent_problem_solver.py  # 智能体问题解决器
│   ├── thought_action_recorder.py # 思考与操作记录器
│   ├── release_manager.py       # Release管理器
│   └── test_issue_collector.py  # 测试与问题收集器
├── visual_test/                 # 视觉化测试
│   ├── ppt_agent_test_plan.md   # PPT智能体测试方案
│   ├── code_agent_test_plan.md  # 代码智能体测试方案
│   ├── web_agent_test_plan.md   # 网页智能体测试方案
│   ├── general_agent_test_plan.md # 通用智能体测试方案
│   └── TEST_REPORT.md           # 测试报告
└── README.md                    # 项目说明文档
```

## 核心功能

- **PPT智能体**：根据用户需求自动生成专业PPT，支持思维导图生成与编辑
- **代码智能体**：接收问题报告，通过manus.im定位、分析、解决问题，并更新代码
- **网页智能体**：提供网页抓取、内容分析、数据提取和自动化操作功能
- **通用智能体**：支持对话、任务执行和项目管理功能

## 开发工具模块

### 1. 智能体问题解决器 (AgentProblemSolver)

该模块负责分析测试日志和问题报告，调用智能体能力进行问题定位，生成修复策略建议，提出测试方案。主要特点：

- 从问题报告中提取问题信息
- 分析问题，确定问题类别、严重性和可能原因
- 生成修复策略，包括优先级、预估工作量和推荐操作
- 生成测试方案，验证修复效果
- 更新文档，添加解决方案

### 2. 思考与操作记录器 (ThoughtActionRecorder)

该模块负责记录智能体的思考过程和执行的操作，提供结构化的日志存储和查询功能。主要特点：

- 记录思考过程，包括推理、决策和计划
- 记录执行的操作，包括输入参数和执行结果
- 支持按时间、类型、内容等条件查询日志
- 提供日志导出和可视化功能

### 3. Release管理器 (ReleaseManager)

该模块负责监控GitHub release事件，自动下载代码到指定路径，处理GitHub上传流程。主要特点：

- 检查GitHub上是否有新的release
- 下载release代码到指定的本地路径
- 支持SSH密钥认证
- 提供代码上传功能，自动处理提交和推送

### 4. 测试与问题收集器 (TestAndIssueCollector)

该模块负责执行自动化测试，收集问题并更新文档。主要特点：

- 执行指定的测试脚本
- 分析测试日志，提取问题信息
- 将问题信息结构化存储
- 更新文档，添加测试发现的问题

## MCP优化模块

每个智能体都集成了以下MCP优化模块：

1. **上下文匹配优化MCP (ContextMatchingOptimizationMCP)**：优化智能体对用户需求的理解和匹配
2. **内容模板优化MCP (ContentTemplateOptimizationMCP)**：优化内容生成的模板和结构
3. **特性优化MCP (FeatureOptimizationMCP)**：优化智能体功能特性的使用和组合
4. **UI旅程优化MCP (UIJourneyOptimizationMCP)**：优化用户界面交互流程
5. **项目记忆优化MCP (ProjectMemoryOptimizationMCP)**：优化项目相关的记忆和知识管理
6. **提示词优化MCP (PromptOptimizationMCP)**：优化智能体的提示词生成和使用

## 端到端测试

平台提供了基于视觉验证和自动化操作的端到端测试方案，覆盖所有智能体和MCP模块。测试方案位于`visual_test`目录，包括：

- PPT智能体测试方案（包含思维导图生成与编辑测试）
- 代码智能体测试方案
- 网页智能体测试方案
- 通用智能体测试方案

## 安装与使用

1. 克隆仓库：`git clone https://github.com/alexchuang650730/powerautomation.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 启动后端服务：`python backend/main.py`
4. 启动前端开发服务器：`cd frontend && npm install && npm start`

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议。请遵循以下步骤：

1. Fork 仓库
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature-name`
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。
