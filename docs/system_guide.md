# PowerAutomation 系统集成与使用指南

## 1. 系统概述

PowerAutomation是一个多智能体协作平台，集成了代码、PPT、网页和通用四种智能体，通过六大特性定义和MCP组件实现高效的任务处理和智能体协作。系统采用分层架构，包括MCP核心组件层、MCP增强组件层、外部工具适配器层、开发工具层和RL Factory层。

### 1.1 系统架构

PowerAutomation系统采用以下分层架构：

1. **MCP核心组件层**
   - MCP中央协调器：负责智能体间的协调和通信
   - MCP规划器：负责任务规划和分解
   - MCP头脑风暴器：负责创意生成和问题解决

2. **MCP增强组件层**
   - Sequential Thinking适配器：提供结构化思考能力
   - Playwright适配器：提供环境交互和验证能力
   - WebAgent增强适配器：增强网页智能体能力
   - 增强版MCP规划器和头脑风暴器

3. **外部工具适配器层**
   - 无限上下文适配器：支持无限长度的上下文记忆
   - MCP.so适配器：连接外部MCP服务
   - GitHub Actions适配器：实现自动化部署和测试
   - ACI.dev适配器：提供云基础设施支持

4. **开发工具层**
   - 思考与操作记录器：记录系统思考和操作过程
   - Agent问题解决驱动器：提供自动回滚和问题解决能力
   - TestAndIssueCollector：自动化测试和问题收集

5. **RL Factory层**
   - 思考过程结构化：将思考过程转化为结构化数据
   - 混合学习架构：结合多种学习方法
   - 多层次奖励机制：优化学习效果
   - 能力迁移：在不同任务间迁移学习成果

### 1.2 智能体类型

PowerAutomation支持以下四种智能体：

1. **代码智能体**：专注于代码开发、调试和优化，能够理解和生成多种编程语言的代码。

2. **PPT智能体**：专注于演示文稿创建和设计，能够生成结构清晰、视觉吸引力强的PPT。

3. **网页智能体**：专注于网页设计和开发，能够创建响应式、美观的网页。

4. **通用智能体**：处理一般性查询和任务，是系统的基础智能体。

### 1.3 六大特性定义

每个智能体都具备以下六大特性：

1. **平台特性**：定义智能体的基本功能和能力范围
2. **UI布局**：定义智能体的界面展示方式
3. **提示词**：定义智能体如何理解和处理用户输入
4. **思维**：定义智能体的思考和决策过程
5. **内容**：定义智能体生成的内容类型和质量
6. **记忆长度**：定义智能体的上下文记忆能力

## 2. 系统安装与配置

### 2.1 环境要求

- **操作系统**：Ubuntu 22.04 或更高版本
- **Python**：3.11.0 或更高版本
- **Node.js**：20.18.0 或更高版本
- **数据库**：MySQL 8.0 或更高版本（可选）

### 2.2 安装步骤

1. **克隆代码仓库**

```bash
git clone https://github.com/alexchuang650730/powerautomation.git
cd powerautomation
```

2. **安装后端依赖**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # 在Windows上使用 venv\Scripts\activate
pip install -r requirements.txt
```

3. **安装前端依赖**

```bash
cd ../frontend
npm install
```

4. **配置环境变量**

创建`.env`文件，添加必要的环境变量：

```
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=powerautomation
```

5. **初始化数据库**（可选）

```bash
cd ../scripts
python init_db.py
```

### 2.3 启动系统

1. **启动后端服务**

```bash
cd ../backend
python app.py
```

2. **启动前端服务**

```bash
cd ../frontend
npm run dev
```

3. **访问系统**

打开浏览器，访问 http://localhost:5173

## 3. 使用指南

### 3.1 智能体选择与交互

1. **选择智能体**：在首页选择需要使用的智能体（代码、PPT、网页或通用）
2. **输入需求**：在输入框中输入您的需求或问题
3. **提交请求**：点击发送按钮或按Enter键提交请求
4. **查看响应**：系统会显示智能体的响应结果

### 3.2 代码智能体需求拆解

代码智能体具备需求拆解能力，可以：

1. 分析用户输入，确定最合适的处理智能体
2. 对于代码相关需求，直接由代码智能体处理
3. 对于通用需求，路由到通用智能体处理
4. 对于PPT或网页需求，路由到相应的专业智能体

使用示例：

```
输入：我需要一个能处理用户输入的程序
结果：代码智能体处理，生成相应代码

输入：什么是人工智能？
结果：路由到通用智能体，提供解释

输入：帮我制作一个关于气候变化的PPT
结果：路由到PPT智能体，生成PPT
```

### 3.3 六特性修改与存储

用户可以通过特定输入修改智能体的六大特性：

1. **修改特定智能体的特性**：

```
输入：优化PPT智能体的UI布局特性
结果：系统会更新PPT智能体的UI布局特性
```

2. **修改所有智能体的特性**：

```
输入：增强所有智能体的记忆特性
结果：系统会更新所有智能体的记忆特性
```

3. **查看当前特性定义**：

```
输入：显示通用智能体的特性定义
结果：系统会显示通用智能体的六大特性定义
```

### 3.4 上下文记忆使用

系统支持无限上下文记忆，用户可以：

1. **引用之前的对话**：

```
输入：继续优化刚才讨论的特性
结果：系统会检索之前的对话，继续相关讨论
```

2. **多轮对话**：系统会自动保持对话连贯性，记住之前的交互内容

## 4. 开发者指南

### 4.1 目录结构

```
powerautomation/
├── agents/                 # 智能体定义和实现
│   ├── base/               # 基础智能体
│   ├── code/               # 代码智能体
│   ├── ppt/                # PPT智能体
│   ├── web/                # 网页智能体
│   └── features/           # 六大特性定义
├── backend/                # 后端服务
│   ├── routes/             # API路由
│   └── services/           # 业务逻辑服务
├── frontend/               # 前端应用
│   ├── public/             # 静态资源
│   └── src/                # 源代码
│       ├── components/     # 组件
│       ├── pages/          # 页面
│       └── utils/          # 工具函数
├── mcptool/                # MCP工具
│   ├── core/               # MCP核心组件
│   ├── enhancers/          # MCP增强组件
│   └── adapters/           # 外部工具适配器
├── development_tools/      # 开发工具
│   └── test_and_issue_collector.py  # 自动化测试工具
├── rl_factory/             # RL Factory
│   └── adapters/           # RL适配器
└── docs/                   # 文档
```

### 4.2 扩展智能体

要添加新的智能体，需要：

1. 在`agents/`目录下创建新的智能体目录
2. 实现基本的智能体类，继承自`BaseAgent`
3. 在`agents/features/`中定义新智能体的六大特性
4. 在`backend/routes/`中添加新的API路由
5. 在`frontend/src/components/`中添加新的智能体卡片和交互组件

示例：

```python
# agents/new_agent/new_agent.py
from agents.base.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__("new_agent")
        
    def process_request(self, request):
        # 处理请求的逻辑
        return {"status": "success", "result": "处理结果"}
```

### 4.3 使用MCP组件

MCP组件提供了强大的规划、思考和问题解决能力，可以通过以下方式使用：

1. **使用MCP规划器**：

```python
from mcptool.core.mcp_planner import MCPPlanner

planner = MCPPlanner()
plan = planner.plan("需要解决的问题")
print(plan)
```

2. **使用MCP头脑风暴器**：

```python
from mcptool.core.mcp_brainstorm import MCPBrainstorm

brainstorm = MCPBrainstorm()
ideas = brainstorm.generate_ideas("创意主题")
print(ideas)
```

3. **使用Sequential Thinking适配器**：

```python
from mcptool.enhancers.sequential_thinking_adapter import SequentialThinkingAdapter

adapter = SequentialThinkingAdapter()
result = adapter.process("需要分步思考的问题")
print(result)
```

### 4.4 使用AgentProblemSolver

AgentProblemSolver提供了自动回滚和问题解决能力：

```python
from development_tools.agent_problem_solver import AgentProblemSolver

# 创建问题解决器
solver = AgentProblemSolver("/path/to/project")

# 创建保存点
savepoint = solver.create_savepoint("初始版本")

# 报告错误
result = solver.report_error("发现的错误")

# 提交问题
problem_result = solver.submit_problem("如何优化代码性能？")

# 监控项目状态
status = solver.monitor_project()
```

### 4.5 使用RL Factory

RL Factory提供了强化学习能力，可以通过以下方式使用：

```python
from rl_factory.adapters.rl_factory_aligner import RLFactoryAligner

# 创建RL Factory对齐器
aligner = RLFactoryAligner()

# 训练模型
aligner.train(training_data, epochs=50)

# 生成解决方案
solution = aligner.generate("需要解决的问题")

# 比较解决方案
comparison = aligner.compare(solution1, solution2)
```

## 5. 自动化测试与部署

### 5.1 使用TestAndIssueCollector

TestAndIssueCollector提供了自动化测试和问题收集能力：

```python
from development_tools.test_and_issue_collector import TestAndIssueCollector

# 创建测试收集器
collector = TestAndIssueCollector()

# 收集测试用例
test_cases = collector.collect_test_cases()

# 执行测试
results = collector.run_tests(test_cases)

# 分析问题
issues = collector.analyze_issues(results)

# 生成报告
report = collector.generate_report(results, issues)
```

### 5.2 使用GitHub Actions

系统集成了GitHub Actions，支持自动化测试和部署：

1. **自动化测试**：每次提交代码时，GitHub Actions会自动运行测试
2. **自动化部署**：合并到main分支时，GitHub Actions会自动部署应用
3. **问题报告**：测试失败时，GitHub Actions会自动创建问题报告

配置文件位于`.github/workflows/tests.yml`。

## 6. 常见问题与解决方案

### 6.1 智能体路由问题

**问题**：智能体路由不准确，请求被发送到错误的智能体

**解决方案**：
1. 检查`frontend/src/utils/agent-router.js`中的路由逻辑
2. 优化关键词匹配算法，增加领域特定词汇
3. 使用更明确的需求描述

### 6.2 六特性存储问题

**问题**：六特性存储偶尔出现并发冲突

**解决方案**：
1. 实现乐观锁机制，确保数据一致性
2. 在更新特性前先获取最新版本
3. 使用事务处理特性更新

### 6.3 上下文记忆问题

**问题**：极端情况下上下文记忆检索可能超时

**解决方案**：
1. 实现分层缓存机制，提高检索效率
2. 优化记忆存储结构，使用索引加速检索
3. 限制单次检索的上下文长度

### 6.4 自动回滚问题

**问题**：自动回滚可能导致未保存的更改丢失

**解决方案**：
1. 增加自动保存功能，定期创建临时保存点
2. 在触发自动回滚前提示用户
3. 提供恢复未保存更改的选项

## 7. 未来规划

### 7.1 功能增强

1. **增加更多智能体类型**：如数据分析智能体、图像处理智能体等
2. **增强六特性定义**：支持更细粒度的特性定义和自定义特性
3. **优化上下文记忆**：实现更高效的记忆存储和检索机制
4. **增强RL Factory**：支持更多模型和学习方法

### 7.2 性能优化

1. **优化响应时间**：减少智能体路由和处理的延迟
2. **优化资源使用**：减少内存和CPU占用
3. **优化并发处理**：支持更高的并发请求数

### 7.3 用户体验改进

1. **增加可视化配置界面**：让用户更直观地配置智能体特性
2. **增加交互式教程**：帮助用户快速上手
3. **增加个性化设置**：让用户根据自己的需求定制系统

## 8. 附录

### 8.1 API文档

详细的API文档请参考`docs/api_documentation.md`。

### 8.2 配置选项

详细的配置选项请参考`docs/configuration_guide.md`。

### 8.3 版本历史

详细的版本历史请参考`docs/version_history.md`。
