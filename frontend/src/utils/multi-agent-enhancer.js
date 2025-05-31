/**
 * 多智能体特性增强模块
 * 负责完善四个智能体的六大特性功能
 */

import { mcpPlannerProcess } from './mcp-planner-enhancer';

// 智能体类型
const AGENT_TYPES = {
  PPT: 'ppt_agent',
  WEB: 'web_agent',
  CODE: 'code_agent',
  GENERAL: 'general_agent'
};

/**
 * 六大特性类型
 */
const FeatureTypes = {
  PLATFORM: 'platform_feature',    // 特性1: PowerAutomation自动化平台功能
  UI_LAYOUT: 'ui_layout',          // 特性2: UI布局
  PROMPT: 'prompt',                // 特性3: 提示词
  THINKING: 'thinking',            // 特性4: 思维
  CONTENT: 'content',              // 特性5: 内容
  MEMORY: 'memory'                 // 特性6: 记忆长度
};

/**
 * 获取智能体当前的六大特性
 * @param {string} agentType 智能体类型
 * @returns {Promise<Object>} 六大特性对象
 */
export async function getAgentFeatures(agentType) {
  try {
    // 从本地存储或API获取智能体特性
    const storedFeatures = localStorage.getItem(`${agentType}_features`);
    if (storedFeatures) {
      return JSON.parse(storedFeatures);
    }
    
    // 如果本地没有，则从API获取
    const response = await fetch(`/api/${agentType}/features`);
    if (!response.ok) {
      throw new Error(`获取${agentType}特性失败: ${response.status}`);
    }
    
    const features = await response.json();
    
    // 存储到本地
    localStorage.setItem(`${agentType}_features`, JSON.stringify(features));
    
    return features;
  } catch (error) {
    console.error(`获取${agentType}特性失败:`, error);
    
    // 返回默认特性
    return {
      [FeatureTypes.PLATFORM]: `${agentType}的PowerAutomation自动化平台功能`,
      [FeatureTypes.UI_LAYOUT]: `${agentType}的两栏布局设计`,
      [FeatureTypes.PROMPT]: `${agentType}的提示词处理`,
      [FeatureTypes.THINKING]: `${agentType}的思考过程`,
      [FeatureTypes.CONTENT]: `${agentType}的内容生成`,
      [FeatureTypes.MEMORY]: `${agentType}的无限上下文记忆`
    };
  }
}

/**
 * 更新智能体的六大特性
 * @param {string} agentType 智能体类型
 * @param {Object} features 六大特性对象
 * @returns {Promise<Object>} 更新结果
 */
export async function updateAgentFeatures(agentType, features) {
  try {
    // 存储到本地
    localStorage.setItem(`${agentType}_features`, JSON.stringify(features));
    
    // 同步到API
    const response = await fetch(`/api/${agentType}/features`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });
    
    if (!response.ok) {
      throw new Error(`更新${agentType}特性失败: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`更新${agentType}特性失败:`, error);
    return { error: error.message };
  }
}

/**
 * 分析用户输入，确定需要增强的智能体和特性
 * @param {string} userInput 用户输入
 * @returns {Object} 分析结果
 */
export function analyzeEnhancementTarget(userInput) {
  // 智能体关键词映射
  const agentKeywords = {
    [AGENT_TYPES.PPT]: ['ppt', '演示', 'presentation', '幻灯片', 'slide', 'powerpoint'],
    [AGENT_TYPES.WEB]: ['web', '网页', 'website', '网站', 'html', 'css', 'frontend', '前端'],
    [AGENT_TYPES.CODE]: ['code', '代码', 'programming', '编程', 'algorithm', '算法', 'function', '函数'],
    [AGENT_TYPES.GENERAL]: ['general', '通用', 'assistant', '助手', 'chat', '聊天', 'help', '帮助']
  };
  
  // 特性关键词映射
  const featureKeywords = {
    [FeatureTypes.PLATFORM]: ['platform', '平台', 'automation', '自动化', 'function', '功能', 'feature', '特性'],
    [FeatureTypes.UI_LAYOUT]: ['ui', '界面', 'layout', '布局', 'design', '设计', 'column', '栏', 'interface', '接口'],
    [FeatureTypes.PROMPT]: ['prompt', '提示词', 'input', '输入', 'query', '查询', 'instruction', '指令'],
    [FeatureTypes.THINKING]: ['thinking', '思维', 'thought', '思考', 'logic', '逻辑', 'reasoning', '推理', 'process', '过程'],
    [FeatureTypes.CONTENT]: ['content', '内容', 'output', '输出', 'generate', '生成', 'result', '结果', 'response', '响应'],
    [FeatureTypes.MEMORY]: ['memory', '记忆', 'context', '上下文', 'history', '历史', 'length', '长度', 'store', '存储']
  };
  
  // 初始化结果
  const result = {
    targetAgents: [],
    targetFeatures: [],
    enhancementType: 'specific', // specific或all
    confidence: 0
  };
  
  // 检查是否包含"所有"或"全部"关键词
  if (userInput.match(/所有|全部|all|every|each|四个|4个|四种|4种/i)) {
    result.targetAgents = Object.values(AGENT_TYPES);
    result.enhancementType = 'all';
    result.confidence += 0.3;
  } else {
    // 分析目标智能体
    for (const [agentType, keywords] of Object.entries(agentKeywords)) {
      for (const keyword of keywords) {
        if (userInput.toLowerCase().includes(keyword.toLowerCase())) {
          if (!result.targetAgents.includes(agentType)) {
            result.targetAgents.push(agentType);
            result.confidence += 0.1;
          }
        }
      }
    }
  }
  
  // 检查是否包含"所有特性"或"全部特性"关键词
  if (userInput.match(/所有特性|全部特性|all features|every feature|六个特性|6个特性|六种特性|6种特性/i)) {
    result.targetFeatures = Object.values(FeatureTypes);
    result.enhancementType = 'all';
    result.confidence += 0.3;
  } else {
    // 分析目标特性
    for (const [featureType, keywords] of Object.entries(featureKeywords)) {
      for (const keyword of keywords) {
        if (userInput.toLowerCase().includes(keyword.toLowerCase())) {
          if (!result.targetFeatures.includes(featureType)) {
            result.targetFeatures.push(featureType);
            result.confidence += 0.1;
          }
        }
      }
    }
  }
  
  // 如果没有明确指定智能体，默认为代码智能体
  if (result.targetAgents.length === 0) {
    result.targetAgents = [AGENT_TYPES.CODE];
  }
  
  // 如果没有明确指定特性，默认为所有特性
  if (result.targetFeatures.length === 0) {
    result.targetFeatures = Object.values(FeatureTypes);
  }
  
  return result;
}

/**
 * 生成特性增强提示
 * @param {string} agentType 智能体类型
 * @param {string} featureType 特性类型
 * @param {string} userInput 用户输入
 * @returns {string} 增强提示
 */
function generateEnhancementPrompt(agentType, featureType, userInput) {
  const agentNames = {
    [AGENT_TYPES.PPT]: 'PPT智能体',
    [AGENT_TYPES.WEB]: '网页智能体',
    [AGENT_TYPES.CODE]: '代码智能体',
    [AGENT_TYPES.GENERAL]: '通用智能体'
  };
  
  const featureNames = {
    [FeatureTypes.PLATFORM]: 'PowerAutomation自动化平台功能',
    [FeatureTypes.UI_LAYOUT]: '两栏布局设计',
    [FeatureTypes.PROMPT]: '提示词处理',
    [FeatureTypes.THINKING]: '思考过程',
    [FeatureTypes.CONTENT]: '内容生成',
    [FeatureTypes.MEMORY]: '无限上下文记忆'
  };
  
  return `根据用户输入"${userInput}"，增强${agentNames[agentType]}的${featureNames[featureType]}特性。`;
}

/**
 * 使用MCP Planner增强智能体特性
 * @param {string} agentType 智能体类型
 * @param {Array} featureTypes 特性类型数组
 * @param {string} userInput 用户输入
 * @returns {Promise<Object>} 增强结果
 */
export async function enhanceAgentFeatures(agentType, featureTypes, userInput) {
  try {
    // 获取当前特性
    const currentFeatures = await getAgentFeatures(agentType);
    
    // 增强结果
    const enhancementResults = {};
    
    // 对每个特性进行增强
    for (const featureType of featureTypes) {
      // 生成增强提示
      const enhancementPrompt = generateEnhancementPrompt(agentType, featureType, userInput);
      
      // 使用MCP Planner处理
      const thinkingProcess = `分析如何增强${agentType}的${featureType}特性，基于用户输入: "${userInput}"`;
      const mcpResult = await mcpPlannerProcess(enhancementPrompt, thinkingProcess);
      
      // 提取增强后的特性内容
      let enhancedFeatureContent = currentFeatures[featureType];
      
      if (mcpResult.success && mcpResult.outputs.code && mcpResult.outputs.code.code) {
        // 从代码输出中提取特性内容
        const codeOutput = mcpResult.outputs.code.code;
        
        // 简单提取引号中的内容作为特性描述
        const matches = codeOutput.match(/"([^"]+)"|'([^']+)'/);
        if (matches && (matches[1] || matches[2])) {
          enhancedFeatureContent = matches[1] || matches[2];
        } else {
          // 如果没有找到引号内容，使用整个代码输出的前200个字符
          enhancedFeatureContent = codeOutput.substring(0, 200);
        }
      }
      
      // 更新特性
      currentFeatures[featureType] = enhancedFeatureContent;
      
      // 记录结果
      enhancementResults[featureType] = {
        original: currentFeatures[featureType],
        enhanced: enhancedFeatureContent,
        mcpResult
      };
    }
    
    // 更新智能体特性
    const updateResult = await updateAgentFeatures(agentType, currentFeatures);
    
    return {
      agentType,
      features: currentFeatures,
      enhancementResults,
      updateResult
    };
  } catch (error) {
    console.error(`增强${agentType}特性失败:`, error);
    return { error: error.message };
  }
}

/**
 * 处理用户输入，增强多个智能体的多个特性
 * @param {string} userInput 用户输入
 * @returns {Promise<Object>} 处理结果
 */
export async function processMultiAgentEnhancement(userInput) {
  try {
    // 分析用户输入，确定目标智能体和特性
    const analysisResult = analyzeEnhancementTarget(userInput);
    
    // 处理结果
    const results = {
      analysisResult,
      enhancementResults: {},
      timestamp: new Date().toISOString()
    };
    
    // 对每个目标智能体进行增强
    for (const agentType of analysisResult.targetAgents) {
      const agentResult = await enhanceAgentFeatures(
        agentType, 
        analysisResult.targetFeatures,
        userInput
      );
      
      results.enhancementResults[agentType] = agentResult;
    }
    
    return results;
  } catch (error) {
    console.error('处理多智能体增强失败:', error);
    return { error: error.message };
  }
}

export default {
  AGENT_TYPES,
  FeatureTypes,
  getAgentFeatures,
  updateAgentFeatures,
  analyzeEnhancementTarget,
  enhanceAgentFeatures,
  processMultiAgentEnhancement
};
