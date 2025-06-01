# PowerAutomation 项目说明

## 项目概述

PowerAutomation是一个多智能体协作平台，集成了代码、PPT、网页和通用四种智能体，通过六大特性定义和MCP组件实现高效的任务处理和智能体协作。本项目实现了多智能体路由、六特性存储、自动化测试、RL Factory能力对齐等核心功能。

## 目录结构

```
powerautomation_integration/
├── agents/                     # 智能体目录
│   ├── base/                   # 基础智能体
│   ├── code/                   # 代码智能体
│   ├── features/               # 六大特性定义
│   ├── general/                # 通用智能体
│   ├── ppt/                    # PPT智能体
│   └── web/                    # 网页智能体
├── backend/                    # 后端目录
│   ├── routes/                 # API路由
│   └── services/               # 服务层
├── development_tools/          # 开发工具
│   ├── agent_problem_solver.py # 问题解决驱动器
│   └── test_and_issue_collector.py # 测试收集器
├── docs/                       # 文档目录
│   ├── delivery_summary.md     # 交付总结
│   ├── supermemory_integration_guide.md # 无限记忆API集成指南
│   ├── system_guide.md         # 系统指南
│   ├── validation_report.md    # 验证报告
│   └── visual_test_guide.md    # 视觉测试指南
├── frontend/                   # 前端目录
│   └── src/                    # 源代码
│       ├── components/         # 组件
│       ├── pages/              # 页面
│       └── utils/              # 工具类
├── mcptool/                    # MCP工具
│   ├── adapters/               # 外部工具适配器
│   ├── core/                   # 核心组件
│   └── enhancers/              # 增强组件
├── rl_factory/                 # RL Factory
│   ├── adapters/               # 适配器
│   └── core/                   # 核心组件
├── test/                       # 端到端测试
│   └── visual_test/            # 视觉自动化测试
│       ├── baseline/           # 基准图像
│       ├── pages/              # 页面对象
│       ├── scenarios/          # 测试场景
│       └── utils/              # 测试工具
└── tests/                      # 单元和集成测试
    ├── integration/            # 集成测试
    └── unit/                   # 单元测试
```

## 系统分层架构图

![PowerAutomation 分层架构图](docs/images/layered_architecture.png)

## 核心功能

### 1. 多智能体路由

代码智能体能够分析用户输入，决定最合适的处理智能体，实现智能路由：
- 代码相关需求由代码智能体处理
- 通用需求路由到通用智能体
- PPT或网页需求路由到相应的专业智能体

### 2. 六特性存储与流转

系统实现了六大特性的定义、存储和流转：
- 平台特性：定义智能体的基本功能和能力范围
- UI布局：定义智能体的界面展示方式
- 提示词：定义智能体如何理解和处理用户输入
- 思维：定义智能体的思考和决策过程
- 内容：定义智能体生成的内容类型和质量
- 记忆长度：定义智能体的上下文记忆能力

### 3. 无限上下文记忆

系统集成了supermemory.ai的API，实现无限上下文记忆功能：
- 存储用户查询和系统思考过程
- 结构化存储六大特性
- 高效检索相关上下文

### 4. 自动化测试

系统实现了完整的自动化测试框架：
- 单元测试：测试各组件的独立功能
- 集成测试：测试组件间的交互
- 端到端视觉测试：测试用户界面和交互流程

### 5. RL Factory能力对齐

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
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd ../frontend
npm install
```

### 运行

1. 启动后端
```bash
cd backend
python app.py
```

2. 启动前端
```bash
cd frontend
npm run dev
```

3. 访问应用
打开浏览器，访问 http://localhost:5173

### 运行测试

1. 运行单元测试
```bash
cd tests
python -m pytest unit/
```

2. 运行集成测试
```bash
cd tests
python -m pytest integration/
```

3. 运行端到端视觉测试
```bash
cd test/visual_test
python run_tests.py
```

## 文档

详细文档请参阅docs目录：
- [交付总结](docs/delivery_summary.md)
- [无限记忆API集成指南](docs/supermemory_integration_guide.md)
- [系统指南](docs/system_guide.md)
- [验证报告](docs/validation_report.md)
- [视觉测试指南](docs/visual_test_guide.md)

## GitHub Actions集成

本项目已配置GitHub Actions工作流，用于自动化测试和部署：
- 单元测试和集成测试
- 端到端视觉自动化测试
- 代码质量检查
- 自动部署

详细配置请参阅`.github/workflows/`目录下的工作流文件。

## 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅[LICENSE](LICENSE)文件。
