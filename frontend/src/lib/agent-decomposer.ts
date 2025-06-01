/**
 * 智能体需求拆解模块
 * 负责分析用户输入，决定最适合处理的智能体
 */

import { AgentType } from './api';

// 六大特性定义接口
export interface GeneralAgentFeatures {
  feature1: string; // PowerAutomation自动化平台特性
  feature2: string; // UI两栏布局特性
  feature3: string; // 提示词特性
  feature4: string; // 思维输入特性
  feature5: string; // 内容输入特性
  feature6: string; // 无限上下文记忆特性
}

// 需求拆解结果接口
export interface DecompositionResult {
  targetAgent: AgentType;
  isGeneralRequest: boolean;
  originalQuery: string;
  processedQuery: string;
  thinkingProcess: string;
  generalFeatures?: GeneralAgentFeatures;
}

/**
 * 判断是否为代码相关需求
 * @param query 用户查询
 * @returns boolean
 */
function isCodeRelatedRequest(query: string): boolean {
  const codeKeywords = [
    'code', '代码', 'function', '函数', 'class', '类', 
    'programming', '编程', 'algorithm', '算法', 'debug', '调试',
    'javascript', 'python', 'java', 'c++', 'typescript', 'html', 'css',
    'compile', '编译', 'runtime', '运行时', 'error', '错误',
    'git', 'github', 'repository', '仓库', 'commit', 'pull request'
  ];
  
  return codeKeywords.some(keyword => 
    query.toLowerCase().includes(keyword.toLowerCase())
  );
}

/**
 * 判断是否为PPT相关需求
 * @param query 用户查询
 * @returns boolean
 */
function isPPTRelatedRequest(query: string): boolean {
  const pptKeywords = [
    'ppt', '演示', 'presentation', '幻灯片', 'slide', 
    'powerpoint', '演讲', 'speech', '报告', 'report'
  ];
  
  return pptKeywords.some(keyword => 
    query.toLowerCase().includes(keyword.toLowerCase())
  );
}

/**
 * 判断是否为网页相关需求
 * @param query 用户查询
 * @returns boolean
 */
function isWebRelatedRequest(query: string): boolean {
  const webKeywords = [
    'web', '网页', 'website', '网站', 'html', 'css', 
    'frontend', '前端', 'responsive', '响应式', 'layout', '布局',
    'ui', 'ux', '界面', '用户体验', 'design', '设计'
  ];
  
  return webKeywords.some(keyword => 
    query.toLowerCase().includes(keyword.toLowerCase())
  );
}

/**
 * 生成通用智能体六大特性
 * @param query 用户查询
 * @param thinkingProcess 思考过程
 * @returns GeneralAgentFeatures
 */
function generateGeneralFeatures(query: string, thinkingProcess: string): GeneralAgentFeatures {
  return {
    feature1: `PowerAutomation自动化平台特性：智能体选择与后端通信，实现了智能体选择逻辑，创建了API接口封装，处理用户查询"${query}"`,
    feature2: `UI两栏布局特性：PowerAutomation自动化平台采用两栏布局，左侧为Sidebar导航栏，右侧为主内容区，包含Header、四个智能体卡片（PPT、网页、代码、通用）、输入区和案例展示`,
    feature3: `提示词特性：用户输入"${query}"，系统分析后确定最适合处理的智能体`,
    feature4: `思维特性：${thinkingProcess}`,
    feature5: `内容特性：处理用户输入"${query}"，准备生成相应内容`,
    feature6: `无限上下文记忆特性：记录用户查询"${query}"及系统思考过程，确保后续交互的连贯性和上下文理解`
  };
}

/**
 * 拆解用户需求，决定最适合处理的智能体
 * @param query 用户查询
 * @param selectedAgent 用户选择的智能体
 * @returns DecompositionResult
 */
export function decomposeRequest(query: string, selectedAgent: AgentType): DecompositionResult {
  // 初始化思考过程
  let thinkingProcess = `分析用户输入: "${query}"\n`;
  
  // 如果用户选择的是代码智能体，进行需求拆解
  if (selectedAgent === 'code_agent') {
    thinkingProcess += "用户选择了代码智能体，进行需求拆解...\n";
    
    // 判断是否为代码相关需求
    if (isCodeRelatedRequest(query)) {
      thinkingProcess += "检测到代码相关关键词，确认为代码需求，由代码智能体处理\n";
      return {
        targetAgent: 'code_agent',
        isGeneralRequest: false,
        originalQuery: query,
        processedQuery: query,
        thinkingProcess
      };
    } 
    // 判断是否为PPT相关需求
    else if (isPPTRelatedRequest(query)) {
      thinkingProcess += "检测到PPT相关关键词，判断为PPT需求，转发给PPT智能体处理\n";
      return {
        targetAgent: 'ppt_agent',
        isGeneralRequest: false,
        originalQuery: query,
        processedQuery: query,
        thinkingProcess
      };
    }
    // 判断是否为网页相关需求
    else if (isWebRelatedRequest(query)) {
      thinkingProcess += "检测到网页相关关键词，判断为网页需求，转发给网页智能体处理\n";
      return {
        targetAgent: 'web_agent',
        isGeneralRequest: false,
        originalQuery: query,
        processedQuery: query,
        thinkingProcess
      };
    }
    // 其他情况视为通用需求
    else {
      thinkingProcess += "未检测到特定领域关键词，判断为通用需求，转发给通用智能体处理\n";
      
      // 生成通用智能体六大特性
      const generalFeatures = generateGeneralFeatures(query, thinkingProcess);
      
      return {
        targetAgent: 'general_agent',
        isGeneralRequest: true,
        originalQuery: query,
        processedQuery: query,
        thinkingProcess,
        generalFeatures
      };
    }
  } 
  // 如果用户选择的不是代码智能体，直接使用所选智能体
  else {
    thinkingProcess += `用户选择了${selectedAgent}，直接使用该智能体处理\n`;
    return {
      targetAgent: selectedAgent,
      isGeneralRequest: false,
      originalQuery: query,
      processedQuery: query,
      thinkingProcess
    };
  }
}

/**
 * 存储上下文记忆
 * @param query 用户查询
 * @param result 处理结果
 * @param features 通用智能体特性
 */
export function storeContextMemory(
  query: string, 
  result: any, 
  features?: GeneralAgentFeatures
): void {
  // 在实际应用中，这里会将上下文存储到数据库或会话存储中
  // 当前实现仅在控制台记录，实际项目中需替换为持久化存储
  console.log('存储上下文记忆:', {
    timestamp: new Date().toISOString(),
    query,
    result,
    features
  });
  
  // 如果浏览器支持，可以使用localStorage临时存储
  try {
    const contextHistory = JSON.parse(localStorage.getItem('contextHistory') || '[]');
    contextHistory.push({
      timestamp: new Date().toISOString(),
      query,
      result: typeof result === 'object' ? JSON.stringify(result) : result,
      features
    });
    
    // 只保留最近的50条记录，防止存储过大
    if (contextHistory.length > 50) {
      contextHistory.shift();
    }
    
    localStorage.setItem('contextHistory', JSON.stringify(contextHistory));
  } catch (error) {
    console.error('存储上下文记忆失败:', error);
  }
}
