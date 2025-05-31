# Sequential Thinking MCP 集成指南

## 概述

Sequential Thinking MCP 是 PowerAutomation 系统中的核心增强组件，提供任务拆解和反思能力。它能够将复杂任务分解为有序的子任务，并通过反思和优化不断改进执行计划。本文档详细介绍了 Sequential Thinking MCP 的功能、接口和集成方法，帮助开发者快速上手并有效利用这一组件。

## 功能特点

Sequential Thinking MCP 适配器提供以下核心功能：

1. **任务分解**：将复杂任务分解为有序的子任务，建立任务依赖关系
2. **计划反思**：分析执行计划的完整性和合理性，提供优化建议
3. **任务状态管理**：跟踪和更新任务完成状态
4. **与六大特性集成**：支持与 PowerAutomation 系统的六大特性无缝集成，特别是思维特性

## 安装与配置

Sequential Thinking MCP 适配器已集成到 PowerAutomation 系统的 MCP 增强组件层中，无需额外安装。只需确保项目依赖已正确安装：

```bash
cd /path/to/powerautomation_integration
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from mcptool.enhancers import SequentialThinkingAdapter

# 初始化 Sequential Thinking 适配器
sequential = SequentialThinkingAdapter()

# 分解任务
task_description = "开发一个用户认证模块"
context = {"platform": "web", "framework": "React"}
decomposed_task = sequential.decompose_task(task_description, context)

# 创建 todo.md 格式的任务清单
todo_md = sequential.create_todo_md(decomposed_task)

# 反思和优化计划
plan = {
    "task_structure": decomposed_task,
    "execution_plans": ["计划1", "计划2"],
    "dependencies": {"task1": ["task2"], "task2": ["task3"]}
}
refined_plan = sequential.reflect_and_refine(plan)

# 更新任务状态
updated_todo = sequential.update_todo_status(todo_md, "analyze", True)
```

### 与六大特性集成

Sequential Thinking MCP 可以与 PowerAutomation 系统的六大特性无缝集成，特别是在思维特性方面提供强大支持：

```python
from agents.features import GeneralAgentFeatures
from mcptool.enhancers import SequentialThinkingAdapter

# 初始化通用智能体特性
agent_features = GeneralAgentFeatures()

# 初始化 Sequential Thinking 适配器
sequential = SequentialThinkingAdapter()

# 分解任务
task_description = "优化网站性能"
decomposed_task = sequential.decompose_task(task_description)

# 使用 Sequential Thinking 增强思维特性
thinking_process = {
    "task": task_description,
    "decomposition": decomposed_task,
    "reasoning": "通过将任务分解为多个子任务，可以更有效地解决复杂问题...",
    "conclusions": ["结论1", "结论2", "结论3"]
}
agent_features.update_thinking_feature(thinking_process)
```

### 与多智能体路由集成

Sequential Thinking MCP 可以与多智能体路由系统集成，为代码智能体提供任务分解能力：

```python
from frontend.src.utils.agent_router import AgentRouter
from mcptool.enhancers import SequentialThinkingAdapter

# 初始化智能体路由器
router = AgentRouter()

# 初始化 Sequential Thinking 适配器
sequential = SequentialThinkingAdapter()

# 注册 Sequential Thinking 增强的代码智能体处理函数
def enhanced_code_agent_handler(request):
    # 使用 Sequential Thinking 处理请求
    if "task" in request:
        return sequential.decompose_task(request["task"])
    elif "plan" in request:
        return sequential.reflect_and_refine(request["plan"])
    else:
        return {"error": "Unsupported request type"}

# 注册处理函数
router.register_handler("code", enhanced_code_agent_handler)
```

## API 参考

### SequentialThinkingAdapter 类

#### 初始化

```python
SequentialThinkingAdapter()
```

初始化 Sequential Thinking 适配器。

#### 任务分解

```python
decompose_task(task_description: str, context: Optional[Dict] = None) -> Dict
```

将任务分解为子任务。

**参数**：
- `task_description`：任务描述
- `context`：上下文信息（可选）

**返回值**：
- 分解后的任务结构，包含任务描述、子任务列表和上下文信息

#### 创建任务清单

```python
create_todo_md(decomposed_task: Dict) -> str
```

创建 todo.md 格式的任务清单。

**参数**：
- `decomposed_task`：分解后的任务

**返回值**：
- todo.md 格式的任务清单字符串

#### 反思和优化

```python
reflect_and_refine(plan: Dict) -> Dict
```

反思和优化计划。

**参数**：
- `plan`：执行计划

**返回值**：
- 优化后的计划，包含反思和优化建议

#### 更新任务状态

```python
update_todo_status(todo_md: str, task_id: str, completed: bool) -> str
```

更新 todo.md 中任务的完成状态。

**参数**：
- `todo_md`：todo.md 内容
- `task_id`：任务 ID
- `completed`：是否完成

**返回值**：
- 更新后的 todo.md 内容

## 与主工作流集成

Sequential Thinking MCP 在 PowerAutomation 系统的主工作流中扮演着重要角色，特别是在代码智能体的需求拆解和任务规划阶段：

1. **需求拆解阶段**：
   - 用户输入复杂需求
   - 代码智能体调用 Sequential Thinking MCP 进行任务分解
   - 生成结构化的子任务和依赖关系

2. **任务规划阶段**：
   - 基于分解结果创建执行计划
   - 调用反思和优化功能完善计划
   - 生成 todo.md 任务清单

3. **执行跟踪阶段**：
   - 随着任务执行更新任务状态
   - 根据执行情况调整计划
   - 记录执行过程中的思考和决策

### 集成示例

```python
# 主工作流中的集成示例
from mcptool.enhancers import SequentialThinkingAdapter
from agents.features import CodeAgentFeatures

def process_code_request(request, features):
    # 初始化组件
    sequential = SequentialThinkingAdapter()
    
    # 1. 需求拆解阶段
    task = request.get("task", "")
    decomposed_task = sequential.decompose_task(task)
    
    # 2. 任务规划阶段
    todo_md = sequential.create_todo_md(decomposed_task)
    
    # 创建执行计划
    plan = {
        "task_structure": decomposed_task,
        "execution_plans": ["步骤1", "步骤2", "步骤3"],
        "dependencies": {"step1": [], "step2": ["step1"], "step3": ["step2"]}
    }
    
    # 反思和优化计划
    refined_plan = sequential.reflect_and_refine(plan)
    
    # 3. 更新思维特性
    thinking_process = {
        "task": task,
        "decomposition": decomposed_task,
        "plan": refined_plan,
        "reasoning": "通过系统性分解任务，我们可以更有效地解决复杂问题..."
    }
    features.update_thinking_feature(thinking_process)
    
    return {
        "decomposed_task": decomposed_task,
        "todo_md": todo_md,
        "refined_plan": refined_plan
    }
```

## 最佳实践

1. **任务粒度控制**：确保任务分解的粒度适中，既不过于细碎也不过于粗略
2. **依赖关系管理**：明确定义任务间的依赖关系，避免循环依赖
3. **反思与优化**：定期使用反思和优化功能，不断改进执行计划
4. **与其他MCP组件协同**：结合Playwright MCP和WebAgentB等组件，实现更强大的功能

## 常见问题

### 任务分解不够合理

如果任务分解结果不够合理，可能是因为：

1. 任务描述不够清晰或过于复杂
2. 缺少必要的上下文信息
3. 需要调整分解逻辑

尝试提供更清晰的任务描述和更完整的上下文信息。

### 执行计划优化不足

如果执行计划优化不足，可能是因为：

1. 计划结构不完整
2. 依赖关系定义不清晰
3. 缺少必要的执行顺序

确保提供完整的计划结构，包括任务结构、执行计划和依赖关系。

## 与 Supermemory.ai 集成

Sequential Thinking MCP 可以与 Supermemory.ai 无限上下文记忆功能集成，提供更强大的任务分解和规划能力：

```python
from mcptool.adapters import InfiniteContextAdapter
from mcptool.enhancers import SequentialThinkingAdapter

# 初始化适配器
context_adapter = InfiniteContextAdapter()
sequential = SequentialThinkingAdapter()

# 分解任务
task_description = "开发一个复杂的数据分析系统"
decomposed_task = sequential.decompose_task(task_description)

# 将分解结果存储到无限上下文记忆
context_id = context_adapter.store_context({
    "type": "task_decomposition",
    "task": task_description,
    "decomposition": decomposed_task
})

# 后续可以通过 context_id 检索分解结果
retrieved_decomposition = context_adapter.retrieve_context(context_id)
```

## 结论

Sequential Thinking MCP 适配器为 PowerAutomation 系统提供了强大的任务分解和反思能力，是构建高效智能体的重要组件。通过本文档的指导，开发者可以快速上手并有效利用这一组件，为用户提供更智能、更高效的任务处理体验。
