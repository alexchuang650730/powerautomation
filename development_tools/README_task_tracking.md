"""
任务追踪系统使用文档
版本: 1.0.0
更新日期: 2025-06-02
"""

# PowerAutomation 任务追踪系统

## 概述

PowerAutomation任务追踪系统是一个端到端的自动化解决方案，用于提升agentProblemSolver的能力。系统通过整合mcpplanner、mcpbrainstorm和agentProblemSolver，实现了自动化任务获取、指令发送和数据分类存储功能。

本系统主要包含以下核心组件：
1. Manus.im自动化访问模块 - 使用Playwright实现自动访问、任务获取和指令发送
2. SuperMemory.ai集成模块 - 实现任务进度和历史数据的分类存储
3. 端到端任务数据分类与追踪模块 - 整合上述两个模块，实现完整的工作流程

## 系统架构

```
用户输入 → mcpcoordinator → 分流判断 → mcpplanner/mcpbrainstorm → agentProblemSolver → Playwright自动化 → supermemory.ai记录
```

### 数据流程

1. 用户向mcpcoordinator提供输入问题和文件
2. mcpcoordinator分析输入，判断是否包含工具：
   - 有工具的命令交给mcpplanner处理
   - 没有工具的命令交给mcpbrainstorm处理
3. mcpplanner/mcpbrainstorm生成处理方案
4. agentProblemSolver接收方案并执行
5. Playwright自动访问manus.im，获取任务并发送指令
6. 系统监控任务执行过程，收集输出信息
7. SuperMemory.ai对收集的信息进行分类存储，按照六大特性和四类数据进行归档

### 数据分类

系统将数据分为四类：
1. 任务进度 (task_progress) - 记录任务的当前状态、完成百分比、里程碑等
2. 用户历史回复及分析 (user_history) - 记录用户交互记录、意图分析等
3. 创建及更新/取代/消除动作 (action_record) - 记录操作日志、变更记录等
4. 更新及完成的工作 (work_completion) - 记录成果物、验证结果等

### 六大特性映射

系统将数据与智能体六大特性进行映射：
1. 平台特性 (platform) - 系统功能、能力、接口、服务、集成相关
2. UI布局特性 (ui_layout) - 界面、布局、设计、视觉、交互相关
3. 提示词特性 (prompt) - 指令、命令、输入、请求、查询相关
4. 思维特性 (thinking) - 分析、推理、判断、决策、规划相关
5. 内容特性 (content) - 文本、图像、视频、数据、信息相关
6. 记忆特性 (memory) - 历史、上下文、存储、检索相关

## 安装与配置

### 前提条件

- Python 3.8+
- Playwright
- SuperMemory.ai API密钥

### 安装步骤

1. 安装Python依赖
```bash
pip install playwright requests
```

2. 安装Playwright浏览器
```bash
playwright install
```

3. 设置SuperMemory.ai API密钥
```bash
export SUPERMEMORY_API_KEY="sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL"
```

## 使用方法

### 基本用法

```python
import asyncio
from task_tracking_system import TaskTrackingSystem

async def main():
    # 创建任务追踪系统
    system = TaskTrackingSystem()
    
    try:
        # 初始化系统
        await system.initialize()
        
        # 处理输入
        result = await system.process_input_with_mcpcoordinator(
            "分析PowerAutomation项目的代码质量",
            "/path/to/file.txt",  # 可选
            has_tools=True  # 可选，如果为None则自动判断
        )
        
        print(f"处理结果: {result}")
    finally:
        # 关闭系统
        await system.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 高级用法

#### 直接使用MCPPlanner处理任务

```python
# 获取最新任务
latest_task = await system.get_latest_task()
task_id = latest_task["id"]

# 使用MCPPlanner处理任务
result = await system.process_task_with_mcpplanner(
    task_id,
    "分析PowerAutomation项目的代码质量"
)
```

#### 直接使用MCPBrainstorm处理任务

```python
# 获取最新任务
latest_task = await system.get_latest_task()
task_id = latest_task["id"]

# 使用MCPBrainstorm处理任务
result = await system.process_task_with_mcpbrainstorm(
    task_id,
    "为PowerAutomation项目提供创意改进方案"
)
```

#### 执行特定命令

```python
# 获取最新任务
latest_task = await system.get_latest_task()
task_id = latest_task["id"]

# 执行命令
result = await system.execute_command(
    task_id,
    "执行特定命令",
    "/path/to/file.txt"  # 可选
)
```

#### 监控任务输出

```python
# 获取最新任务
latest_task = await system.get_latest_task()
task_id = latest_task["id"]

# 监控任务输出
results = await system.monitor_task_output(task_id, 60)  # 监控60秒
```

## 数据查询

系统支持从SuperMemory.ai查询存储的数据：

```python
# 获取任务进度
progress_data = system.supermemory.get_task_progress(task_id)

# 获取用户历史
history_data = system.supermemory.get_user_history(task_id)

# 获取动作记录
action_data = system.supermemory.get_action_records(task_id)

# 获取工作完成记录
completion_data = system.supermemory.get_work_completions(task_id)

# 按特性查询数据
platform_data = system.supermemory.get_task_data(task_id, feature="platform")
```

## 测试

系统提供了完整的测试模块，用于验证端到端自动化流程和数据同步：

```bash
python test_task_tracking.py
```

测试模块会自动执行以下测试：
1. 获取最新任务
2. 执行命令
3. 监控任务输出
4. 使用MCPPlanner处理任务
5. 使用MCPBrainstorm处理任务
6. 使用MCPCoordinator处理输入

## 故障排除

### 常见问题

1. **无法连接到Manus.im**
   - 检查网络连接
   - 确认URL是否正确
   - 尝试增加超时时间

2. **SuperMemory.ai API调用失败**
   - 检查API密钥是否正确
   - 确认API端点是否可访问
   - 检查请求格式是否正确

3. **任务分类不准确**
   - 调整关键词映射
   - 增加更多特征词
   - 考虑使用更复杂的分类算法

### 日志文件

系统会生成以下日志文件，可用于故障排除：
- manus_automation.log - Manus.im自动化访问日志
- supermemory_integration.log - SuperMemory.ai集成日志
- task_tracking.log - 任务追踪系统日志
- test_task_tracking.log - 测试日志

## 扩展与定制

### 添加新的数据类型

1. 在SuperMemoryIntegration类中的data_types列表中添加新类型
2. 在classify_text方法中添加相应的关键词映射
3. 添加相应的getter方法

### 添加新的特性映射

1. 在SuperMemoryIntegration类中的six_features列表中添加新特性
2. 在_determine_feature方法中添加相应的关键词映射

### 集成其他外部系统

可以参考Manus.im自动化和SuperMemory.ai集成的模式，添加新的外部系统集成。

## 贡献指南

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证。
