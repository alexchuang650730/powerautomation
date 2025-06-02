# PowerAutomation 项目说明

## 项目概述

PowerAutomation是一个多智能体协作平台，集成了代码、PPT、网页和通用四种智能体，通过六大特性定义和MCP组件实现高效的任务处理和智能体协作。本项目实现了多智能体路由、六特性存储、自动化测试、RL Factory能力对齐等核心功能，并增强了版本回滚能力、工作节点可视化功能、输入框与工作流集成等特性。

## 目录结构

```
powerautomation/
├── agents/                     # 智能体目录
│   ├── code_agent/             # 代码智能体
│   ├── general_agent/          # 通用智能体
│   │   └── general_agent_features.py  # 通用智能体六大特性定义
│   ├── ppt_agent/              # PPT智能体
│   ├── web_agent/              # 网页智能体
│   └── workflow_driver/        # 工作流驱动智能体
├── backend/                    # 后端目录
│   ├── routes/                 # API路由
│   ├── services/               # 服务层
│   └── main.py                 # 后端入口文件
├── config/                     # 配置文件目录
│   ├── agent_problem_solver.json  # 问题解决器配置
│   ├── release_manager.json       # 发布管理器配置
│   ├── rollback_history.json      # 回滚历史记录
│   ├── savepoints.json            # 保存点配置
│   └── work_nodes.json            # 工作节点配置
├── development_tools/          # 开发工具
│   ├── agent_problem_solver.py    # 问题解决驱动器
│   ├── proactive_problem_solver.py # 主动问题解决器
│   └── release_manager.py         # 发布管理器
├── docs/                       # 文档目录
│   └── images/                 # 文档图片
├── frontend/                   # 前端目录
│   └── src/                    # 源代码
│       ├── App.tsx             # 应用入口组件
│       ├── App.css             # 应用主样式
│       ├── main.tsx            # 应用入口文件
│       ├── index.css           # 全局样式
│       ├── components/         # 组件
│       │   ├── input-area/     # 输入框组件
│       │   │   ├── InputBox.tsx  # 输入框组件
│       │   │   └── InputBox.css  # 输入框样式
│       │   ├── agent-cards/    # 智能体卡片组件
│       │   │   ├── AgentCard.tsx # 智能体卡片组件
│       │   │   └── AgentCard.css # 智能体卡片样式
│       │   ├── work-node-timeline/ # 工作节点时间线组件
│       │   │   ├── WorkNodeTimeline.tsx # 工作节点时间线组件
│       │   │   └── WorkNodeTimeline.css # 工作节点时间线样式
│       │   ├── workflow-nodes/ # 工作流节点组件
│       │   ├── N8nWorkflowVisualizer.tsx # 工作流可视化组件
│       │   └── WorkflowIntegrationPanel.tsx # 工作流集成面板
│       └── styles/             # 样式文件
│           ├── N8nWorkflowVisualizer.css # 工作流可视化样式
│           └── WorkflowIntegrationPanel.css # 工作流集成面板样式
├── mcptool/                    # MCP工具
│   ├── adapters/               # 外部工具适配器
│   ├── core/                   # 核心组件
│   ├── enhancers/              # 增强组件
│   └── mcp/                    # MCP实现
├── releases/                   # 发布目录
│   └── test_release/           # 测试发布
├── rl_factory/                 # RL Factory
│   ├── adapters/               # 适配器
│   ├── core/                   # 核心组件
│   │   ├── learning/           # 学习模块
│   │   └── thought/            # 思考模块
│   └── tests/                  # RL Factory测试
├── test/                       # 测试目录
│   ├── end_to_end/             # 端到端测试
│   ├── integration/            # 集成测试
│   └── visual_test/            # 视觉自动化测试
└── workflow_driver/            # 工作流驱动器
    └── workflow_driver.py      # 工作流驱动实现
```

## 核心功能

### 1. 多智能体路由

代码智能体能够分析用户输入，决定最合适的处理智能体，实现智能路由：
- 代码相关需求由代码智能体处理
- 通用需求路由到通用智能体
- PPT或网页需求路由到相应的专业智能体

### 2. 六特性存储与流转

系统实现了六大特性的定义、存储和流转：
- 平台特性：定义智能体的基本功能和能力范围，包括集成工作流管理和统一界面体验
- UI布局：定义智能体的界面展示方式，包括集成输入区域和统一工作节点与工作流视图
- 提示词：定义智能体如何理解和处理用户输入，包括智能体模式自适应提示
- 思维：定义智能体的思考和决策过程，包括工作流优化
- 内容：定义智能体生成的内容类型和质量，包括消息历史管理和文件附件处理
- 记忆：定义智能体的上下文记忆能力，包括工作流状态持久化和消息历史持久化

### 3. 版本回滚能力

系统增强了AgentProblemSolver的版本回滚能力：
- 回滚历史记录和统计功能
- 回滚前后对比验证
- 工作节点记录和管理
- 检查点管理

### 4. 工作节点与工作流整合

系统实现了工作节点与工作流的统一可视化：
- 工作节点时间线组件，展示不同类型和状态的工作节点
- n8n风格工作流可视化组件，直观展示工作流程和数据流转
- 统一界面，提供连贯的任务执行视图
- 响应式布局，适配不同设备
- 状态指示和自动刷新功能

### 5. 集成输入区域

系统在智能体卡片上方添加了集成输入区域：
- 支持多行文本输入
- 支持文件上传功能，包括拖放上传
- 根据选择的智能体模式自动调整输入框提示文本
- 消息历史显示，记录用户与智能体的交互

### 6. 自动化测试

系统实现了完整的自动化测试框架：
- 单元测试：测试各组件的独立功能
- 集成测试：测试组件间的交互
- 端到端测试：测试完整工作流程

### 7. RL Factory能力对齐

RL Factory实现了与MCPPlanner和MCPBrainstorm的能力对齐：
- 以MCPPlanner和MCPBrainstorm的输入作为学习者
- 持续强化学习对齐ThoughtActionRecorder的输入
- 通过迭代训练达到与ThoughtActionRecorder相同的输入处理水平

## 安装与使用

### 安装

1. 克隆代码仓库
```bash
git clone https://github.com/alexchuang650730/powerautomation.git
cd powerautomation
```

2. 安装后端依赖
```bash
cd backend
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
pip install -r ../requirements.txt
```

3. 安装前端依赖
```bash
cd ../frontend
npm install --legacy-peer-deps  # 使用legacy-peer-deps解决依赖冲突
# 或者降级date-fns到兼容版本
# npm install date-fns@3.0.0
```

4. 安装TypeScript（如果需要构建前端）
```bash
npm install -g typescript
```

### 运行

1. 启动后端
```bash
cd backend
python main.py  # 注意：入口文件是main.py，不是app.py
```

2. 启动前端
```bash
cd frontend
npm run dev
```

3. 访问应用
打开浏览器，访问 http://localhost:5173
如果无法访问localhost，可以尝试使用127.0.0.1:5173

### 运行测试

1. 运行单元测试
```bash
python -m pytest test/unit/
```

2. 运行集成测试
```bash
python -m pytest test/integration/
```

3. 运行端到端测试
```bash
python -m pytest test/end_to_end/
```

## 核心治理原则

所有功能扩展严格遵循以下五大核心治理原则：

1. **结构保护原则**：所有功能扩展严格基于原本的文件结构进行，不会更改现有结构
2. **兼容性原则**：新增功能必须与现有功能保持向后兼容，确保系统稳定性
3. **空间利用原则**：UI扩展只在空白区域进行，不影响原有控件和布局
4. **模块化原则**：新功能作为独立模块添加，不修改现有代码逻辑
5. **一致性原则**：保持与现有代码风格和架构的一致性

## 前端界面功能

### 主界面布局

- **两栏式布局**：左侧为导航栏，右侧为主内容区
- **输入区域**：位于智能体卡片上方，支持文本输入和文件上传
- **智能体卡片**：横向排列的四种智能体模式卡片，支持选择切换
- **工作节点时间线**：展示工作节点状态和历史
- **工作流可视化**：n8n风格的节点连接图，直观展示工作流程
- **消息历史**：记录用户与智能体的交互历史

### 交互功能

- **智能体选择**：点击智能体卡片切换当前工作的智能体模式
- **输入框提示**：根据选择的智能体模式自动调整输入框提示文本
- **文件上传**：支持点击上传和拖放上传文件
- **工作节点查看**：点击工作节点可查看详细信息
- **工作流节点交互**：点击工作流节点可查看节点详情

## 常见问题

### 后端依赖问题

如果遇到缺少依赖的错误（如 `ModuleNotFoundError: No module named 'flask_cors'`），请确保已安装所有必要的依赖：

```bash
pip install -r requirements.txt
```

如果仍有缺失的依赖，可以单独安装：

```bash
pip install flask-cors
```

### 前端依赖冲突

如果在安装前端依赖时遇到冲突（如date-fns与react-day-picker的版本冲突），可以：

1. 使用`--legacy-peer-deps`参数：
```bash
npm install --legacy-peer-deps
```

2. 或降级date-fns到兼容版本：
```bash
npm install date-fns@3.0.0
```

### 前端构建问题

如果遇到`tsc: not found`错误，需要安装TypeScript：

```bash
npm install -g typescript
```

### 前端访问问题

如果无法通过localhost访问前端，可以尝试：

1. 使用IP地址：http://127.0.0.1:5173
2. 使用--host参数启动：`npm run dev -- --host`
3. 更改端口：`npm run dev -- --port 3000`

## 文档

详细文档请参阅docs目录。

## 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅[LICENSE](LICENSE)文件。
