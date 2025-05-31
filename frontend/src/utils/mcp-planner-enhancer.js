/**
 * MCP Planner 增强模块
 * 负责代码开发、GitHub推送、增强组件集成和MCPBrainstorm自动补全
 */

// 导入必要的依赖
import { decomposeRequest, storeContextMemory } from './agent-decomposer';

/**
 * MCP Planner 状态枚举
 */
const MCPPlannerState = {
  IDLE: 'idle',
  ANALYZING: 'analyzing',
  DEVELOPING: 'developing',
  PUSHING: 'pushing',
  LEARNING: 'learning',
  BRAINSTORMING: 'brainstorming'
};

/**
 * 工具类型枚举
 */
const ToolType = {
  DEVELOPMENT: 'development',
  ENHANCER: 'enhancer',
  EXTERNAL: 'external',
  BRAINSTORM: 'brainstorm',
  RL_FACTORY: 'rl_factory'
};

/**
 * 检查工具是否足够处理当前任务
 * @param {string} task 任务描述
 * @param {Array} availableTools 可用工具列表
 * @returns {boolean} 工具是否足够
 */
function areToolsSufficient(task, availableTools) {
  // 根据任务复杂度和可用工具判断是否足够
  // 这里使用简单的关键词匹配逻辑，实际应用中可能需要更复杂的算法
  const complexityKeywords = [
    'complex', '复杂', 'advanced', '高级', 'innovative', '创新',
    'novel', '新颖', 'challenging', '挑战', 'unprecedented', '前所未有'
  ];
  
  const isComplexTask = complexityKeywords.some(keyword => 
    task.toLowerCase().includes(keyword.toLowerCase())
  );
  
  // 如果是复杂任务，需要检查是否有足够的工具
  if (isComplexTask) {
    const requiredToolTypes = [ToolType.DEVELOPMENT, ToolType.ENHANCER, ToolType.EXTERNAL];
    const availableToolTypes = availableTools.map(tool => tool.type);
    
    return requiredToolTypes.every(type => availableToolTypes.includes(type));
  }
  
  // 对于简单任务，只需要开发工具即可
  return availableTools.some(tool => tool.type === ToolType.DEVELOPMENT);
}

/**
 * 发送思考过程到MCP Planner
 * @param {string} thinkingProcess 思考过程
 * @param {Array} availableTools 可用工具列表
 * @returns {Promise<Object>} MCP Planner的响应
 */
export async function sendToMCPPlanner(thinkingProcess, availableTools = []) {
  try {
    // 默认工具列表
    const defaultTools = [
      { id: 'dev-tool-1', type: ToolType.DEVELOPMENT, name: '代码生成器' },
      { id: 'enhancer-1', type: ToolType.ENHANCER, name: 'MCP增强器' }
    ];
    
    // 合并可用工具列表
    const tools = [...defaultTools, ...availableTools];
    
    const response = await fetch('/api/mcp/planner', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        thinkingProcess,
        tools
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('发送思考过程到MCP Planner失败:', error);
    return { error: error.message };
  }
}

/**
 * 使用MCPBrainstorm进行创意生成
 * @param {string} task 任务描述
 * @param {string} context 上下文信息
 * @returns {Promise<Object>} MCPBrainstorm的响应
 */
export async function useMCPBrainstorm(task, context) {
  try {
    const response = await fetch('/api/mcp/brainstorm', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        task,
        context
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('使用MCPBrainstorm失败:', error);
    return { error: error.message };
  }
}

/**
 * 使用开发模块生成代码
 * @param {string} requirement 需求描述
 * @param {string} language 编程语言
 * @returns {Promise<Object>} 开发模块的响应
 */
export async function generateCode(requirement, language = 'javascript') {
  try {
    const response = await fetch('/api/development/generate-code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        requirement,
        language
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('代码生成失败:', error);
    return { error: error.message };
  }
}

/**
 * 推送代码到GitHub
 * @param {string} repository 仓库名称
 * @param {string} branch 分支名称
 * @param {string} filePath 文件路径
 * @param {string} content 文件内容
 * @param {string} commitMessage 提交信息
 * @returns {Promise<Object>} GitHub API的响应
 */
export async function pushToGitHub(repository, branch, filePath, content, commitMessage) {
  try {
    const response = await fetch('/api/github/push', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        repository,
        branch,
        filePath,
        content,
        commitMessage
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('推送到GitHub失败:', error);
    return { error: error.message };
  }
}

/**
 * 使用RL Factory进行强化学习
 * @param {string} codeContent 代码内容
 * @param {string} feedbackType 反馈类型
 * @returns {Promise<Object>} RL Factory的响应
 */
export async function learnWithRLFactory(codeContent, feedbackType = 'quality') {
  try {
    const response = await fetch('/api/rl-factory/learn', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        codeContent,
        feedbackType
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('RL Factory学习失败:', error);
    return { error: error.message };
  }
}

/**
 * MCP Planner 完整处理流程
 * @param {string} task 任务描述
 * @param {string} thinkingProcess 思考过程
 * @param {Object} options 选项
 * @returns {Promise<Object>} 处理结果
 */
export async function mcpPlannerProcess(task, thinkingProcess, options = {}) {
  // 默认选项
  const defaultOptions = {
    language: 'javascript',
    repository: 'powerautomation',
    branch: 'main',
    autoCommit: true,
    enableLearning: true,
    enableBrainstorm: true
  };
  
  // 合并选项
  const config = { ...defaultOptions, ...options };
  
  // 状态跟踪
  let state = MCPPlannerState.IDLE;
  let result = {
    task,
    steps: [],
    outputs: {},
    errors: []
  };
  
  try {
    // 步骤1: 分析任务
    state = MCPPlannerState.ANALYZING;
    result.steps.push({ id: 1, name: '分析任务', state });
    
    // 获取可用工具
    const availableTools = [
      { id: 'dev-tool-1', type: ToolType.DEVELOPMENT, name: '代码生成器' },
      { id: 'enhancer-1', type: ToolType.ENHANCER, name: 'MCP增强器' },
      { id: 'external-1', type: ToolType.EXTERNAL, name: '外部工具' },
      { id: 'rl-factory-1', type: ToolType.RL_FACTORY, name: 'RL Factory' }
    ];
    
    // 检查工具是否足够
    const toolsSufficient = areToolsSufficient(task, availableTools);
    
    // 如果工具不足且启用了Brainstorm，则使用MCPBrainstorm
    if (!toolsSufficient && config.enableBrainstorm) {
      state = MCPPlannerState.BRAINSTORMING;
      result.steps.push({ id: 2, name: '使用MCPBrainstorm', state });
      
      const brainstormResult = await useMCPBrainstorm(task, thinkingProcess);
      result.outputs.brainstorm = brainstormResult;
      
      // 更新思考过程
      thinkingProcess += `\n\nMCPBrainstorm输出:\n${JSON.stringify(brainstormResult, null, 2)}`;
    }
    
    // 步骤2: 发送到MCP Planner
    const plannerResponse = await sendToMCPPlanner(thinkingProcess, availableTools);
    result.outputs.planner = plannerResponse;
    
    // 步骤3: 生成代码
    state = MCPPlannerState.DEVELOPING;
    result.steps.push({ id: 3, name: '生成代码', state });
    
    const codeResult = await generateCode(task, config.language);
    result.outputs.code = codeResult;
    
    // 步骤4: 推送到GitHub
    if (config.autoCommit) {
      state = MCPPlannerState.PUSHING;
      result.steps.push({ id: 4, name: '推送到GitHub', state });
      
      const filePath = `generated/${Date.now()}.${config.language === 'javascript' ? 'js' : config.language}`;
      const commitMessage = `自动生成: ${task.substring(0, 50)}${task.length > 50 ? '...' : ''}`;
      
      const pushResult = await pushToGitHub(
        config.repository,
        config.branch,
        filePath,
        codeResult.code || '',
        commitMessage
      );
      
      result.outputs.github = pushResult;
    }
    
    // 步骤5: 强化学习
    if (config.enableLearning && codeResult.code) {
      state = MCPPlannerState.LEARNING;
      result.steps.push({ id: 5, name: '强化学习', state });
      
      const learningResult = await learnWithRLFactory(codeResult.code, 'quality');
      result.outputs.learning = learningResult;
    }
    
    // 完成
    state = MCPPlannerState.IDLE;
    result.steps.push({ id: 6, name: '完成', state });
    result.success = true;
    
  } catch (error) {
    console.error('MCP Planner处理失败:', error);
    result.errors.push({
      step: state,
      message: error.message,
      timestamp: new Date().toISOString()
    });
    result.success = false;
  }
  
  return result;
}

export default {
  MCPPlannerState,
  ToolType,
  sendToMCPPlanner,
  useMCPBrainstorm,
  generateCode,
  pushToGitHub,
  learnWithRLFactory,
  mcpPlannerProcess
};
