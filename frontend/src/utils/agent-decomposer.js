/**
 * 智能体需求拆解模块
 * 负责分析用户输入，决定最合适的智能体处理请求，并存储六大特性
 */

import { AGENT_TYPES } from './agent-router';

/**
 * 分解用户请求，确定目标智能体和特性
 * @param {string} query 用户查询
 * @param {string} sourceAgent 源智能体类型
 * @returns {Object} 分解结果
 */
export function decomposeRequest(query, sourceAgent) {
  console.log(`分解请求: ${query}，源智能体: ${sourceAgent}`);
  
  // 分析查询内容
  const analysis = analyzeQuery(query);
  
  // 确定是否为通用请求
  const isGeneralRequest = isQueryGeneral(query, analysis);
  
  // 确定目标智能体
  const targetAgent = determineTargetAgent(query, analysis, sourceAgent, isGeneralRequest);
  
  // 如果是通用请求，生成六大特性
  const generalFeatures = isGeneralRequest ? generateSixFeatures(query, analysis) : null;
  
  return {
    originalQuery: query,
    sourceAgent,
    targetAgent,
    isGeneralRequest,
    generalFeatures,
    analysis
  };
}

/**
 * 分析用户查询
 * @param {string} query 用户查询
 * @returns {Object} 分析结果
 */
function analyzeQuery(query) {
  const lowerQuery = query.toLowerCase();
  
  // 识别查询意图
  let intent = 'general';
  if (lowerQuery.includes('ppt') || lowerQuery.includes('演示') || lowerQuery.includes('幻灯片')) {
    intent = 'ppt_creation';
  } else if (lowerQuery.includes('网页') || lowerQuery.includes('网站') || lowerQuery.includes('html')) {
    intent = 'web_development';
  } else if (lowerQuery.includes('代码') || lowerQuery.includes('编程') || lowerQuery.includes('函数')) {
    intent = 'code_development';
  } else if (lowerQuery.includes('特性') || lowerQuery.includes('功能') || lowerQuery.includes('定义')) {
    intent = 'feature_definition';
  }
  
  // 识别是否涉及六大特性修改
  const featureKeywords = {
    platform_feature: ['特性1', '平台特性', '平台功能', 'powerautomation'],
    ui_layout: ['特性2', 'ui', '布局', '界面', '设计'],
    prompt: ['特性3', '提示词', '提示', '输入提示'],
    thinking: ['特性4', '思维', '思考', '逻辑', '推理'],
    content: ['特性5', '内容', '输出', '生成内容'],
    memory: ['特性6', '记忆', '上下文', '历史', '长度']
  };
  
  const involvedFeatures = {};
  Object.entries(featureKeywords).forEach(([feature, keywords]) => {
    involvedFeatures[feature] = keywords.some(keyword => lowerQuery.includes(keyword.toLowerCase()));
  });
  
  // 生成思考过程
  const thinkingProcess = `
分析用户输入: "${query}"
识别查询意图: ${intent}
涉及特性修改: ${Object.values(involvedFeatures).some(v => v) ? '是' : '否'}
涉及的特性: ${Object.entries(involvedFeatures).filter(([_, v]) => v).map(([k, _]) => k).join(', ')}
  `.trim();
  
  return {
    intent,
    involvedFeatures,
    thinkingProcess
  };
}

/**
 * 判断查询是否为通用请求
 * @param {string} query 用户查询
 * @param {Object} analysis 分析结果
 * @returns {boolean} 是否为通用请求
 */
function isQueryGeneral(query, analysis) {
  // 如果涉及特性修改，则视为通用请求
  if (Object.values(analysis.involvedFeatures).some(v => v)) {
    return true;
  }
  
  // 如果意图是feature_definition，则视为通用请求
  if (analysis.intent === 'feature_definition') {
    return true;
  }
  
  // 其他通用请求关键词
  const generalKeywords = ['通用', '帮助', '问题', '解释', '什么是', '如何'];
  if (generalKeywords.some(keyword => query.toLowerCase().includes(keyword))) {
    return true;
  }
  
  return false;
}

/**
 * 确定目标智能体
 * @param {string} query 用户查询
 * @param {Object} analysis 分析结果
 * @param {string} sourceAgent 源智能体类型
 * @param {boolean} isGeneralRequest 是否为通用请求
 * @returns {string} 目标智能体类型
 */
function determineTargetAgent(query, analysis, sourceAgent, isGeneralRequest) {
  // 如果是通用请求，路由到通用智能体
  if (isGeneralRequest) {
    return AGENT_TYPES.GENERAL;
  }
  
  // 根据意图确定目标智能体
  switch (analysis.intent) {
    case 'ppt_creation':
      return AGENT_TYPES.PPT;
    case 'web_development':
      return AGENT_TYPES.WEB;
    case 'code_development':
      return AGENT_TYPES.CODE;
    default:
      // 如果无法确定，保持在源智能体
      return sourceAgent;
  }
}

/**
 * 生成六大特性
 * @param {string} query 用户查询
 * @param {Object} analysis 分析结果
 * @returns {Object} 六大特性
 */
function generateSixFeatures(query, analysis) {
  return {
    platform_feature: `PowerAutomation自动化平台特性：智能体选择与后端通信，处理用户查询"${query}"`,
    ui_layout: "PowerAutomation自动化平台采用两栏布局，左侧为Sidebar导航栏，右侧为主内容区",
    prompt: `用户输入"${query}"，系统分析后确定由通用智能体处理`,
    thinking: analysis.thinkingProcess,
    content: `处理用户输入"${query}"，准备生成相应内容`,
    memory: `记录用户查询"${query}"及系统思考过程，确保后续交互的连贯性和上下文理解`
  };
}

/**
 * 存储上下文记忆
 * @param {string} query 用户查询
 * @param {Object} result 处理结果
 * @param {Object} features 六大特性
 * @returns {Promise<boolean>} 是否成功
 */
export async function storeContextMemory(query, result, features) {
  console.log('存储上下文记忆:', { query, features });
  
  try {
    // 这里是模拟代码，实际项目中应与后端API交互
    // 例如使用fetch或axios发送请求
    // const response = await fetch('/api/memory/store', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ query, result, features })
    // });
    // return response.ok;
    
    // 模拟存储成功
    return true;
  } catch (error) {
    console.error('存储上下文记忆失败:', error);
    return false;
  }
}

/**
 * 检索上下文记忆
 * @param {string} query 用户查询
 * @returns {Promise<Object|null>} 检索到的记忆
 */
export async function retrieveContextMemory(query) {
  console.log('检索上下文记忆:', query);
  
  try {
    // 这里是模拟代码，实际项目中应与后端API交互
    // 例如使用fetch或axios发送请求
    // const response = await fetch(`/api/memory/retrieve?query=${encodeURIComponent(query)}`);
    // if (response.ok) {
    //   return await response.json();
    // }
    // return null;
    
    // 模拟检索结果
    return {
      query: query,
      features: {
        platform_feature: `PowerAutomation自动化平台特性：智能体选择与后端通信，处理用户查询"${query}"`,
        ui_layout: "PowerAutomation自动化平台采用两栏布局，左侧为Sidebar导航栏，右侧为主内容区",
        prompt: `用户输入"${query}"，系统分析后确定由通用智能体处理`,
        thinking: `分析用户输入: "${query}"\n通用智能体处理中...\n确定最佳回应策略`,
        content: `处理用户输入"${query}"，准备生成相应内容`,
        memory: `记录用户查询"${query}"及系统思考过程，确保后续交互的连贯性和上下文理解`
      },
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('检索上下文记忆失败:', error);
    return null;
  }
}
