# PowerAutomation 多智能体六特性增强与MCP集成文档

## 功能概述

PowerAutomation系统现已增强代码智能体(code_agent)的能力，使其能够智能分析用户输入，并根据需求类型将请求路由到最合适的智能体处理。同时，系统支持通过用户输入来完善四个智能体（PPT、网页、代码、通用）的六大特性功能，并与MCP Planner、MCPBrainstorm、开发模块和RL Factory深度集成，实现自动代码开发、GitHub推送和持续强化学习。

## 核心功能

1. **智能需求拆解**：代码智能体能够分析用户输入，判断是代码、PPT、网页还是通用需求
2. **多智能体协作**：根据需求类型自动路由到最合适的智能体处理
3. **六特性完善**：通过用户输入完善四个智能体的六大特性功能
4. **MCP Planner集成**：将思考过程传递给MCP Planner进行规划和代码开发
5. **GitHub自动推送**：自动将生成的代码推送到GitHub仓库
6. **MCPBrainstorm补充**：在工具不足时自动调用MCPBrainstorm进行创意生成
7. **RL Factory学习**：通过RL Factory对生成的代码进行持续强化学习
8. **无限上下文记忆**：保存用户查询历史和系统思考过程，确保交互连贯性

## 六大特性定义

1. **PowerAutomation自动化平台特性**：智能体选择与后端通信，实现智能体选择逻辑和API接口封装
2. **UI两栏布局特性**：PowerAutomation自动化平台采用两栏布局，左侧为Sidebar导航栏，右侧为主内容区
3. **提示词特性**：用户输入的提示词及系统分析结果
4. **思维特性**：系统的思考过程和决策逻辑
5. **内容特性**：处理用户输入，准备生成相应内容
6. **无限上下文记忆特性**：记录用户查询及系统思考过程，确保后续交互的连贯性和上下文理解

## 技术实现

### 前端实现

1. **agent-decomposer.js**：
   - 实现需求拆解逻辑
   - 生成六大特性
   - 与MCP Planner和ThoughtActionRecorder通信
   - 存储上下文记忆

2. **mcp-planner-enhancer.js**：
   - 集成MCP Planner的代码开发功能
   - 实现GitHub自动推送
   - 集成MCPBrainstorm自动补全
   - 与RL Factory交互进行强化学习

3. **multi-agent-enhancer.js**：
   - 分析用户输入，确定目标智能体和特性
   - 获取和更新智能体六大特性
   - 使用MCP Planner增强智能体特性
   - 处理多智能体特性增强

4. **CodeAgentInputEnhanced组件**：
   - 处理用户输入
   - 调用需求拆解逻辑
   - 进行六特性增强
   - 集成MCP Planner处理
   - 展示处理结果

### 后端集成

1. **MCP Planner API**：
   - 接收思考过程
   - 生成执行计划
   - 开发代码
   - 推送到GitHub

2. **MCPBrainstorm API**：
   - 在工具不足时提供创意生成
   - 补充MCP Planner的能力

3. **RL Factory API**：
   - 对生成的代码进行强化学习
   - 持续优化代码质量

4. **ThoughtActionRecorder API**：
   - 接收六大特性
   - 记录和分析特性
   - 返回分析结果

## 使用流程

1. 用户选择代码智能体
2. 输入需求并提交
3. 系统分析需求类型：
   - 如果是代码需求，由代码智能体处理
   - 如果是PPT需求，路由到PPT智能体
   - 如果是网页需求，路由到网页智能体
   - 如果是通用需求，路由到通用智能体，并存储六大特性
4. 系统分析用户输入，确定需要增强的智能体和特性
5. 系统使用MCP Planner增强目标智能体的特性
6. 如果工具不足，系统自动调用MCPBrainstorm进行补充
7. 系统使用开发模块生成代码，并推送到GitHub
8. 系统使用RL Factory对生成的代码进行强化学习
9. 系统存储上下文记忆，确保后续交互的连贯性

## 代码示例

### 需求拆解示例

```javascript
// 导入需求拆解模块
import { decomposeRequest } from '../utils/agent-decomposer';

// 进行需求拆解
const result = decomposeRequest('帮我生成一个React组件', 'code_agent');

// 输出拆解结果
console.log('目标智能体:', result.targetAgent);
console.log('是否通用请求:', result.isGeneralRequest);
console.log('思考过程:', result.thinkingProcess);
```

### 六特性增强示例

```javascript
// 导入多智能体增强模块
import { processMultiAgentEnhancement } from '../utils/multi-agent-enhancer';

// 处理多智能体增强
const result = await processMultiAgentEnhancement('优化PPT智能体的UI布局特性');

// 输出增强结果
console.log('分析结果:', result.analysisResult);
console.log('增强结果:', result.enhancementResults);
```

### MCP Planner处理示例

```javascript
// 导入MCP Planner增强模块
import { mcpPlannerProcess } from '../utils/mcp-planner-enhancer';

// 使用MCP Planner处理
const result = await mcpPlannerProcess(
  '生成一个React表单组件',
  '分析如何创建一个包含验证功能的React表单组件'
);

// 输出处理结果
console.log('处理状态:', result.success ? '成功' : '失败');
console.log('处理步骤:', result.steps);
console.log('代码输出:', result.outputs.code?.code);
```

## 配置选项

### MCP Planner配置

```javascript
const mcpPlannerOptions = {
  language: 'javascript', // 编程语言
  repository: 'powerautomation', // GitHub仓库
  branch: 'main', // 分支名称
  autoCommit: true, // 是否自动提交到GitHub
  enableLearning: true, // 是否启用RL Factory学习
  enableBrainstorm: true // 是否在工具不足时启用MCPBrainstorm
};

const result = await mcpPlannerProcess(task, thinkingProcess, mcpPlannerOptions);
```

### 多智能体增强配置

```javascript
// 获取智能体特性
const features = await getAgentFeatures('ppt_agent');

// 更新智能体特性
const updateResult = await updateAgentFeatures('ppt_agent', {
  platform_feature: '更新后的平台特性',
  ui_layout: '更新后的UI布局特性',
  prompt: '更新后的提示词特性',
  thinking: '更新后的思维特性',
  content: '更新后的内容特性',
  memory: '更新后的记忆特性'
});
```

## 最佳实践

1. **需求明确化**：
   - 在输入需求时，尽量明确指出目标智能体和特性
   - 例如："优化PPT智能体的UI布局特性"或"增强所有智能体的记忆特性"

2. **特性增强建议**：
   - 提供具体的增强方向和目标
   - 例如："让PPT智能体的UI布局更适合移动设备"或"增强代码智能体的思维特性，提高逻辑分析能力"

3. **代码开发指导**：
   - 提供清晰的代码需求和预期功能
   - 例如："生成一个带有表单验证的React登录组件"或"创建一个处理文件上传的Node.js模块"

4. **工具不足时**：
   - 系统会自动调用MCPBrainstorm，但也可以明确指出需要创意生成
   - 例如："使用MCPBrainstorm生成创新的UI设计方案"

## 扩展与优化

1. **关键词库扩展**：
   - 扩充智能体和特性的关键词库
   - 添加更多领域的专业术语

2. **需求拆解算法优化**：
   - 使用机器学习提高分类准确性
   - 添加上下文理解能力

3. **六特性生成优化**：
   - 增强特性内容的丰富度和准确性
   - 添加更多维度的特性分析

4. **MCP Planner能力扩展**：
   - 支持更多编程语言和框架
   - 增强代码质量和可维护性

5. **RL Factory学习优化**：
   - 添加更多学习维度和反馈机制
   - 提高学习效率和效果

## 注意事项

1. 确保MCP Planner、MCPBrainstorm和RL Factory API可用
2. 处理网络错误和异常情况
3. 定期清理上下文记忆，避免存储过大
4. 保护用户隐私，不存储敏感信息
5. GitHub推送需要适当的权限配置
