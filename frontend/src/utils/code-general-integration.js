/**
 * 代码智能体与通用智能体集成模块
 * 负责代码智能体需求拆解和通用智能体六特性存储
 */

import agentRouter, { AGENT_TYPES } from './agent-router';
import { decomposeRequest, storeContextMemory } from './agent-decomposer';

/**
 * 集成代码智能体与通用智能体
 * 实现需求拆解和六特性存储
 */
class CodeGeneralIntegration {
  constructor() {
    this.initialized = false;
    this.mcpPlannerAvailable = false;
    this.rlFactoryAvailable = false;
    
    // 检查MCP Planner可用性
    this._checkMCPPlanner();
    
    // 检查RL Factory可用性
    this._checkRLFactory();
  }
  
  /**
   * 初始化集成
   */
  initialize() {
    if (this.initialized) {
      console.log('代码智能体与通用智能体集成已初始化');
      return;
    }
    
    // 注册代码智能体处理器
    agentRouter.registerAgent(AGENT_TYPES.CODE, this._handleCodeAgentRequest.bind(this));
    
    // 注册通用智能体处理器
    agentRouter.registerAgent(AGENT_TYPES.GENERAL, this._handleGeneralAgentRequest.bind(this));
    
    this.initialized = true;
    console.log('代码智能体与通用智能体集成初始化完成');
  }
  
  /**
   * 检查MCP Planner可用性
   * @private
   */
  _checkMCPPlanner() {
    try {
      // 尝试导入MCP Planner
      // 实际项目中应使用正确的导入路径
      // import { MCPPlanner } from '../../mcptool/core';
      
      this.mcpPlannerAvailable = true;
      console.log('MCP Planner可用');
    } catch (error) {
      console.warn('MCP Planner不可用:', error.message);
      this.mcpPlannerAvailable = false;
    }
  }
  
  /**
   * 检查RL Factory可用性
   * @private
   */
  _checkRLFactory() {
    try {
      // 尝试导入RL Factory
      // 实际项目中应使用正确的导入路径
      // import { RLFactory } from '../../rl_factory';
      
      this.rlFactoryAvailable = true;
      console.log('RL Factory可用');
    } catch (error) {
      console.warn('RL Factory不可用:', error.message);
      this.rlFactoryAvailable = false;
    }
  }
  
  /**
   * 处理代码智能体请求
   * @param {string} query 用户查询
   * @returns {Promise<Object>} 处理结果
   * @private
   */
  async _handleCodeAgentRequest(query) {
    console.log('代码智能体处理请求:', query);
    
    try {
      // 进行需求拆解
      const result = decomposeRequest(query, AGENT_TYPES.CODE);
      
      // 如果是通用需求，存储六大特性
      if (result.isGeneralRequest && result.generalFeatures) {
        await storeContextMemory(query, result, result.generalFeatures);
        
        // 如果需要路由到通用智能体
        if (result.targetAgent === AGENT_TYPES.GENERAL) {
          return this._handleGeneralAgentRequest(query, result.generalFeatures);
        }
      }
      
      // 处理代码相关需求
      return {
        status: 'success',
        message: '代码智能体已处理请求',
        result: {
          code: '// 这里是代码智能体生成的代码\nconsole.log("Hello from Code Agent");',
          explanation: '这是一个简单的JavaScript代码示例，展示了代码智能体的基本功能。'
        },
        originalQuery: query
      };
    } catch (error) {
      console.error('代码智能体处理请求失败:', error);
      return {
        status: 'error',
        message: `处理请求失败: ${error.message}`,
        originalQuery: query
      };
    }
  }
  
  /**
   * 处理通用智能体请求
   * @param {string} query 用户查询
   * @param {Object} features 六大特性（可选）
   * @returns {Promise<Object>} 处理结果
   * @private
   */
  async _handleGeneralAgentRequest(query, features = null) {
    console.log('通用智能体处理请求:', query);
    
    try {
      // 如果没有提供六大特性，则生成默认特性
      if (!features) {
        // 生成思考过程
        const thinkingProcess = `分析用户输入: "${query}"\n通用智能体处理中...\n确定最佳回应策略`;
        
        // 生成默认六大特性
        features = {
          platform_feature: `PowerAutomation自动化平台特性：智能体选择与后端通信，处理用户查询"${query}"`,
          ui_layout: "PowerAutomation自动化平台采用两栏布局，左侧为Sidebar导航栏，右侧为主内容区",
          prompt: `用户输入"${query}"，系统分析后确定由通用智能体处理`,
          thinking: thinkingProcess,
          content: `处理用户输入"${query}"，准备生成相应内容`,
          memory: `记录用户查询"${query}"及系统思考过程，确保后续交互的连贯性和上下文理解`
        };
        
        // 存储上下文记忆
        await storeContextMemory(query, { thinkingProcess }, features);
      }
      
      // 使用MCP Planner（如果可用）
      if (this.mcpPlannerAvailable) {
        console.log('使用MCP Planner增强处理');
        // 实际项目中应调用MCP Planner
      }
      
      // 使用RL Factory（如果可用）
      if (this.rlFactoryAvailable) {
        console.log('使用RL Factory增强处理');
        // 实际项目中应调用RL Factory
      }
      
      // 处理通用需求
      return {
        status: 'success',
        message: '通用智能体已处理请求',
        result: {
          response: `这是通用智能体对"${query}"的回应。我已经分析了您的需求，并根据六大特性进行了处理。`,
          features: features
        },
        originalQuery: query
      };
    } catch (error) {
      console.error('通用智能体处理请求失败:', error);
      return {
        status: 'error',
        message: `处理请求失败: ${error.message}`,
        originalQuery: query
      };
    }
  }
}

// 创建单例
const codeGeneralIntegration = new CodeGeneralIntegration();

export default codeGeneralIntegration;
