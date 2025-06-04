# MCPPlanner驱动时机与工作流设计

## 🤔 **当前工作流分析**

### 📋 **现有工作流**
```
用户需求 → MCPBrainstorm → InfiniteContext → 工具注册表查询
    ↓           ↓              ↓              ↓
  需求输入   意图理解      上下文分析      工具匹配检索
```

### ❓ **MCPPlanner的缺失**
当前工作流中确实缺少了MCPPlanner的明确驱动时机，这是一个重要的架构问题！

## 🎯 **MCPPlanner的核心作用**

### 🧠 **MCPPlanner职责**
1. **任务分解** - 将复杂需求分解为可执行的子任务
2. **执行规划** - 制定最优的执行计划和顺序
3. **资源调度** - 协调各种工具和适配器的使用
4. **依赖管理** - 处理任务间的依赖关系
5. **风险评估** - 评估执行风险和备选方案
6. **进度监控** - 跟踪执行进度和调整计划

## 🔄 **完整工作流设计**

### 🎯 **方案一：MCPPlanner作为中央协调器**
```
用户需求 → MCPBrainstorm → MCPPlanner → InfiniteContext → 工具发现执行
    ↓           ↓             ↓            ↓              ↓
  需求输入   意图理解      任务规划    上下文增强      工具执行
                           ↓
                    [任务分解、执行计划、资源调度]
```

#### 📋 **详细流程**
1. **用户需求** → 原始需求输入
2. **MCPBrainstorm** → 意图理解和需求澄清
3. **MCPPlanner** → 任务分解和执行规划 ⭐
4. **InfiniteContext** → 基于计划进行上下文增强
5. **工具发现执行** → 按计划执行具体工具

### 🎯 **方案二：MCPPlanner作为执行引擎**
```
用户需求 → MCPBrainstorm → InfiniteContext → MCPPlanner → 工具执行监控
    ↓           ↓              ↓             ↓              ↓
  需求输入   意图理解      上下文分析    执行规划      监控调度
                                        ↓
                              [工具选择、执行顺序、监控反馈]
```

#### 📋 **详细流程**
1. **用户需求** → 原始需求输入
2. **MCPBrainstorm** → 意图理解
3. **InfiniteContext** → 上下文分析和记忆增强
4. **MCPPlanner** → 基于理解和上下文制定执行计划 ⭐
5. **工具执行监控** → 按计划执行并实时调整

### 🎯 **方案三：MCPPlanner作为智能决策层**
```
用户需求 → MCPBrainstorm → InfiniteContext → 工具注册表查询
    ↓           ↓              ↓              ↓
  需求输入   意图理解      上下文分析      候选工具
                                            ↓
                                      MCPPlanner ⭐
                                            ↓
                              [智能选择、执行策略、优化决策]
                                            ↓
                                      工具执行引擎
```

#### 📋 **详细流程**
1. **用户需求** → 原始需求输入
2. **MCPBrainstorm** → 意图理解
3. **InfiniteContext** → 上下文分析
4. **工具注册表查询** → 获取候选工具列表
5. **MCPPlanner** → 智能决策和优化选择 ⭐
6. **工具执行引擎** → 执行最优方案

## 🚀 **推荐方案：混合智能工作流**

### 🏗️ **最优架构设计**
```
用户需求 → MCPBrainstorm → MCPPlanner → InfiniteContext → 智能工具引擎
    ↓           ↓             ↓            ↓              ↓
  需求输入   意图理解      任务规划    上下文增强      执行监控
                           ↓                            ↑
                    [分解、规划、调度]                   ↓
                           ↓                      [反馈、调整]
                      工具注册表查询 ←→ 候选工具评估
```

### 📋 **MCPPlanner驱动时机**

#### 🎯 **主要驱动时机**
1. **意图理解完成后** - MCPBrainstorm完成意图分析
2. **复杂任务检测** - 检测到需要多步骤执行的复杂任务
3. **资源冲突时** - 多个工具竞争相同资源
4. **执行失败时** - 需要重新规划备选方案
5. **用户交互时** - 需要用户确认或选择方案

#### ⚡ **具体触发条件**
```python
def should_trigger_mcpplanner(brainstorm_result):
    """判断是否需要触发MCPPlanner"""
    
    # 1. 复杂度检测
    if brainstorm_result.get("complexity_score", 0) > 0.7:
        return True
    
    # 2. 多步骤任务
    if len(brainstorm_result.get("sub_tasks", [])) > 3:
        return True
    
    # 3. 资源密集型任务
    if brainstorm_result.get("resource_intensive", False):
        return True
    
    # 4. 需要协调多个工具
    if len(brainstorm_result.get("required_tools", [])) > 5:
        return True
    
    # 5. 用户明确要求规划
    if brainstorm_result.get("requires_planning", False):
        return True
    
    return False
```

### 🔧 **实际工作流实现**

#### 📝 **完整流程代码示例**
```python
class IntelligentWorkflowEngine:
    """智能工作流引擎"""
    
    def __init__(self):
        self.mcpbrainstorm = MCPBrainstorm()
        self.mcpplanner = MCPPlanner()
        self.infinite_context = InfiniteContext()
        self.tool_engine = UnifiedSmartToolEngine()
    
    async def process_user_request(self, user_request):
        """处理用户请求的完整工作流"""
        
        # 1. 意图理解
        brainstorm_result = await self.mcpbrainstorm.process({
            "action": "analyze_intent",
            "parameters": {"request": user_request}
        })
        
        # 2. 判断是否需要MCPPlanner
        if self._should_trigger_planner(brainstorm_result):
            
            # 2a. 任务规划
            planning_result = await self.mcpplanner.process({
                "action": "create_execution_plan",
                "parameters": {
                    "intent": brainstorm_result,
                    "constraints": {"time": "1h", "resources": "standard"}
                }
            })
            
            # 2b. 上下文增强（基于计划）
            context_result = await self.infinite_context.process({
                "action": "enhance_context",
                "parameters": {
                    "plan": planning_result,
                    "historical_data": True
                }
            })
            
            # 2c. 按计划执行
            execution_result = await self._execute_planned_workflow(
                planning_result, context_result
            )
            
        else:
            # 直接执行简单工作流
            context_result = await self.infinite_context.process({
                "action": "enhance_context",
                "parameters": {"intent": brainstorm_result}
            })
            
            execution_result = await self.tool_engine.process({
                "action": "smart_execute",
                "parameters": {
                    "intent": brainstorm_result,
                    "context": context_result
                }
            })
        
        return execution_result
    
    def _should_trigger_planner(self, brainstorm_result):
        """判断是否触发MCPPlanner"""
        # 实现触发逻辑
        return brainstorm_result.get("complexity_score", 0) > 0.7
    
    async def _execute_planned_workflow(self, plan, context):
        """执行规划的工作流"""
        results = []
        
        for step in plan.get("execution_steps", []):
            step_result = await self.tool_engine.process({
                "action": "execute_tool",
                "parameters": {
                    "tool_id": step["tool_id"],
                    "arguments": step["arguments"],
                    "context": context
                }
            })
            
            results.append(step_result)
            
            # 检查是否需要调整计划
            if not step_result.get("success"):
                # 触发重新规划
                revised_plan = await self.mcpplanner.process({
                    "action": "revise_plan",
                    "parameters": {
                        "original_plan": plan,
                        "failure_point": step,
                        "results_so_far": results
                    }
                })
                plan = revised_plan
        
        return {"success": True, "results": results}
```

## 📊 **不同场景的MCPPlanner使用**

### 🎯 **场景1：简单查询**
```
用户: "今天天气如何？"
→ MCPBrainstorm: 简单查询，复杂度低
→ 跳过MCPPlanner ❌
→ 直接工具执行: 天气API查询
```

### 🎯 **场景2：复杂分析**
```
用户: "分析我的项目数据，生成报告，并发送给团队"
→ MCPBrainstorm: 多步骤任务，复杂度高
→ 触发MCPPlanner ✅
→ 任务分解: [数据分析] → [报告生成] → [邮件发送]
→ 资源调度: 数据分析工具 + 报告工具 + 邮件工具
→ 执行监控: 逐步执行并监控进度
```

### 🎯 **场景3：创新任务**
```
用户: "设计一个新的AI工具来优化我们的工作流"
→ MCPBrainstorm: 创新任务，需要规划
→ 触发MCPPlanner ✅
→ 需求分析: 工作流痛点识别
→ 设计规划: 工具架构设计
→ 开发计划: 分阶段开发策略
→ 测试部署: 验证和部署计划
```

## 💡 **关键洞察**

### ✅ **MCPPlanner的价值**
1. **复杂任务管理** - 处理多步骤、多工具的复杂任务
2. **资源优化** - 最优化工具选择和执行顺序
3. **风险控制** - 预测和处理执行风险
4. **用户体验** - 提供清晰的执行计划和进度反馈

### 🎯 **最佳实践**
1. **智能触发** - 根据任务复杂度智能决定是否使用MCPPlanner
2. **动态调整** - 执行过程中根据反馈动态调整计划
3. **用户参与** - 重要决策点让用户参与确认
4. **性能平衡** - 在规划精度和执行效率间找到平衡

**结论：MCPPlanner应该在MCPBrainstorm完成意图理解后，根据任务复杂度智能触发，作为复杂任务的规划和协调中心！**

