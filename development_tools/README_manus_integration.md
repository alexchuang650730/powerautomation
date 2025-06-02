# Manus集成与多工作流自动化

## 概述

本文档详细介绍了PowerAutomation系统与Manus平台的集成，以及基于六大特性驱动的多工作流自动化功能。通过这些功能，通用智能体能够输入信息及传送文件给Manus，驱动自动化测试工作流、UI工作流和智能体工作流，逐步完善网站功能。

## 核心功能

### 1. Manus平台集成

PowerAutomation系统通过Playwright自动化技术与Manus平台深度集成，实现以下功能：

- **自动化任务获取**：视觉识别并获取powerautomation相关的最新工作任务
- **指令发送**：在Manus平台右侧输入框中发送文本信息和上传文件
- **任务监控**：实时监控任务执行状态，收集输出信息
- **数据同步**：将任务数据分类存储到SuperMemory.ai，按六大特性进行归档

### 2. 多工作流自动化

基于六大特性驱动的多工作流自动化，包括：

- **自动化测试工作流**：单元测试、集成测试、UI测试、性能测试的自动化执行
- **UI工作流**：组件渲染、布局管理、样式应用、交互处理的自动化流程
- **智能体工作流**：任务分发、智能体协调、结果聚合、错误处理的自动化流程

### 3. 数据分类存储

按照六大特性对任务数据进行分类存储，支持四类数据的追踪：

- **任务进度**：当前状态、完成百分比、里程碑等
- **用户历史**：交互记录、意图分析等
- **动作记录**：创建、更新、替换、删除等操作日志
- **工作更新**：成果物、验证结果等

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

## 组件说明

### 1. Manus自动化模块 (manus_automation.py)

负责与Manus平台的自动化交互，包括：

- 初始化Playwright浏览器
- 访问Manus平台
- 获取最新任务
- 执行命令和上传文件
- 监控任务输出

```python
# 示例用法
async def main():
    # 创建Manus自动化实例
    manus = ManusAutomation()
    
    try:
        # 初始化
        await manus.initialize()
        
        # 获取最新任务
        latest_task = await manus.get_latest_powerautomation_task()
        
        # 执行命令
        await manus.execute_task_command(
            latest_task["id"],
            "分析代码质量",
            "/path/to/file.py"
        )
        
        # 监控输出
        # ...
    finally:
        # 关闭
        await manus.close()
```

### 2. SuperMemory集成模块 (supermemory_integration.py)

负责任务数据的分类存储，包括：

- 与SuperMemory.ai API交互
- 对文本进行分类
- 按六大特性和四类数据存储
- 提供数据检索功能

```python
# 示例用法
def main():
    # 创建SuperMemory集成实例
    api_key = "sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL"
    supermemory = SuperMemoryIntegration(api_key)
    
    # 处理Manus输出
    task_id = "task_123456"
    text = "任务已完成50%，正在进行第三阶段的开发工作"
    result = supermemory.process_manus_output(task_id, text)
    
    # 获取任务进度数据
    progress_data = supermemory.get_task_progress(task_id)
```

### 3. 任务追踪系统 (task_tracking_system.py)

整合Manus自动化和SuperMemory集成，实现端到端的任务追踪，包括：

- 初始化系统组件
- 获取最新任务
- 执行命令和监控输出
- 处理mcpplanner/mcpbrainstorm输入
- 分类存储任务数据

```python
# 示例用法
async def main():
    # 创建任务追踪系统
    system = TaskTrackingSystem()
    
    try:
        # 初始化系统
        await system.initialize()
        
        # 处理输入
        result = await system.process_input_with_mcpcoordinator(
            "分析PowerAutomation项目的代码质量",
            "/path/to/file.txt"
        )
    finally:
        # 关闭系统
        await system.close()
```

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
            "/path/to/file.txt"
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

## 测试与验证

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

## 部署

### 本地部署

1. 克隆仓库
```bash
git clone https://github.com/alexchuang650730/powerautomation.git
```

2. 安装依赖
```bash
cd powerautomation
pip install -r requirements.txt
playwright install
```

3. 设置环境变量
```bash
export SUPERMEMORY_API_KEY="sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL"
```

4. 运行测试
```bash
python development_tools/test_task_tracking.py
```

### 服务器部署

1. 克隆仓库
```bash
git clone https://github.com/alexchuang650730/powerautomation.git
```

2. 安装依赖
```bash
cd powerautomation
pip install -r requirements.txt
playwright install chromium
```

3. 设置环境变量
```bash
export SUPERMEMORY_API_KEY="sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL"
```

4. 创建服务
```bash
# 创建systemd服务文件
cat > /etc/systemd/system/task-tracking.service << EOL
[Unit]
Description=Task Tracking System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/powerautomation
ExecStart=/usr/bin/python3 development_tools/task_tracking_server.py
Restart=always
Environment=SUPERMEMORY_API_KEY=sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL

[Install]
WantedBy=multi-user.target
EOL

# 启动服务
systemctl enable task-tracking
systemctl start task-tracking
```

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

## 贡献指南

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证。
