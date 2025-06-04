# 代码重构迁移计划

## 🎯 **重构目标**
将development_tools和rl_factory的功能完全迁移到MCP适配器，确保功能完整性后安全移除旧目录。

## 📊 **依赖关系分析**

### 🔍 **development_tools依赖分析**

#### 被引用的核心模块：
1. **agent_problem_solver.py** - 被多处引用
   - `agents/code_agent/__init__.py`
   - `agents/general_agent/automated_testing.py`
   - `agents/workflow_driver/workflow_driver.py`
   - `mcptool/adapters/development_tools/agent_problem_solver_mcp.py`

2. **release_manager.py** - 工作流管理
   - `agents/workflow_driver/workflow_driver.py`

3. **thought_action_recorder.py** - 思考记录
   - `backend/agents_backup/general_agent.py`
   - `backend/agents_backup/web_agent.py`
   - `mcptool/adapters/development_tools/thought_action_recorder_mcp.py`

### 🔍 **rl_factory依赖分析**

#### 被引用的核心模块：
1. **github_actions_adapter.py** - GitHub Actions集成
   - `mcptool/adapters/ai_enhanced_intent_understanding_mcp.py`

2. **infinite_context_adapter.py** - 无限上下文处理
   - 内部模块引用

3. **test_and_issue_collector.py** - 测试集成
   - `development_tools/test_and_issue_collector.py`

## 🚀 **迁移策略**

### 📋 **Phase 1: 创建缺失的MCP适配器**

#### 1️⃣ **需要创建的MCP适配器**
- `mcptool/adapters/manus_automation_mcp.py`
- `mcptool/adapters/supermemory_integration_mcp.py`
- `mcptool/adapters/task_tracking_system_mcp.py`
- `mcptool/adapters/test_issue_collector_mcp.py`
- `mcptool/adapters/proactive_problem_solver_mcp.py`

#### 2️⃣ **需要迁移的rl_factory功能**
- GitHub Actions适配器 → 已在`ai_enhanced_intent_understanding_mcp.py`中集成
- 无限上下文适配器 → 已有`infinite_context_adapter_mcp.py`
- 其他核心功能 → 创建对应MCP适配器

### 📋 **Phase 2: 更新import引用**

#### 1️⃣ **agents目录更新**
```python
# 旧引用
from development_tools.agent_problem_solver import AgentProblemSolver

# 新引用
from mcptool.adapters.development_tools.agent_problem_solver_mcp import AgentProblemSolverMCP
```

#### 2️⃣ **backend目录更新**
```python
# 旧引用
from ..development_tools.thought_action_recorder import ThoughtActionRecorder

# 新引用
from mcptool.adapters.development_tools.thought_action_recorder_mcp import ThoughtActionRecorderMCP
```

### 📋 **Phase 3: 功能验证和测试**

#### 1️⃣ **单元测试**
- 验证每个MCP适配器功能
- 确保API兼容性

#### 2️⃣ **集成测试**
- 验证整体工作流
- 确保性能无回退

### 📋 **Phase 4: 安全移除**

#### 1️⃣ **备份策略**
- 创建备份分支
- 保留重要配置文件

#### 2️⃣ **移除顺序**
1. 移除development_tools目录
2. 移除rl_factory目录
3. 清理相关配置

## 🔧 **实施步骤**

### Step 1: 创建缺失的MCP适配器
### Step 2: 更新所有import语句
### Step 3: 运行完整测试套件
### Step 4: 验证功能完整性
### Step 5: 安全移除旧目录
### Step 6: 推送到GitHub

## 📈 **预期收益**

- ✅ **架构统一** - 所有功能都通过MCP协议
- ✅ **代码简化** - 移除重复和冗余代码
- ✅ **维护性提升** - 统一的适配器模式
- ✅ **性能优化** - 减少不必要的依赖

---

**开始执行重构计划...**

