/**
 * 端到端验证模块
 * 负责验证多智能体路由和六特性存储的完整流程
 */

import agentRouter, { AGENT_TYPES } from './agent-router';
import { decomposeRequest, storeContextMemory, retrieveContextMemory } from './agent-decomposer';
import codeGeneralIntegration from './code-general-integration';

/**
 * 端到端验证器
 * 负责验证多智能体路由和六特性存储的完整流程
 */
class EndToEndValidator {
  constructor() {
    this.testCases = [];
    this.results = [];
    this.initialized = false;
  }

  /**
   * 初始化验证器
   */
  initialize() {
    if (this.initialized) {
      console.log('端到端验证器已初始化');
      return;
    }

    // 初始化测试用例
    this._initializeTestCases();

    console.log('端到端验证器初始化完成');
    this.initialized = true;
  }

  /**
   * 初始化测试用例
   * @private
   */
  _initializeTestCases() {
    // 代码智能体路由测试
    this.testCases.push({
      id: 'code_routing_test',
      name: '代码智能体路由测试',
      query: '帮我写一个Python函数计算斐波那契数列',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.CODE,
      description: '验证代码相关查询是否正确路由到代码智能体'
    });

    // 通用智能体路由测试
    this.testCases.push({
      id: 'general_routing_test',
      name: '通用智能体路由测试',
      query: '什么是人工智能？',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.GENERAL,
      description: '验证通用查询是否正确路由到通用智能体'
    });

    // PPT智能体路由测试
    this.testCases.push({
      id: 'ppt_routing_test',
      name: 'PPT智能体路由测试',
      query: '帮我制作一个关于气候变化的PPT',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.PPT,
      description: '验证PPT相关查询是否正确路由到PPT智能体'
    });

    // 网页智能体路由测试
    this.testCases.push({
      id: 'web_routing_test',
      name: '网页智能体路由测试',
      query: '设计一个响应式网页布局',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.WEB,
      description: '验证网页相关查询是否正确路由到网页智能体'
    });

    // 六特性存储测试
    this.testCases.push({
      id: 'feature_storage_test',
      name: '六特性存储测试',
      query: '优化PowerAutomation的UI布局特性',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.GENERAL,
      description: '验证六特性相关查询是否正确存储特性定义'
    });

    // 上下文记忆测试
    this.testCases.push({
      id: 'context_memory_test',
      name: '上下文记忆测试',
      query: '继续优化刚才讨论的特性',
      sourceAgent: AGENT_TYPES.GENERAL,
      expectedTargetAgent: AGENT_TYPES.GENERAL,
      description: '验证上下文记忆是否正确工作'
    });

    // 代码智能体需求拆解测试
    this.testCases.push({
      id: 'code_decomposition_test',
      name: '代码智能体需求拆解测试',
      query: '我需要一个能处理用户输入的程序',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.CODE,
      description: '验证代码智能体是否能正确拆解需求'
    });

    // 通用智能体特性修改测试
    this.testCases.push({
      id: 'general_feature_modification_test',
      name: '通用智能体特性修改测试',
      query: '修改通用智能体的思维特性，使其更加注重逻辑推理',
      sourceAgent: AGENT_TYPES.CODE,
      expectedTargetAgent: AGENT_TYPES.GENERAL,
      description: '验证通用智能体是否能正确修改特性'
    });
  }

  /**
   * 运行所有测试
   * @returns {Promise<Object>} 测试结果
   */
  async runAllTests() {
    console.log('开始运行所有测试...');
    this.results = [];

    if (!this.initialized) {
      this.initialize();
    }

    // 初始化依赖组件
    agentRouter.initialize();
    codeGeneralIntegration.initialize();

    // 运行每个测试用例
    for (const testCase of this.testCases) {
      const result = await this.runTest(testCase);
      this.results.push(result);
    }

    // 计算总体结果
    const summary = this._generateSummary();

    console.log('所有测试完成');
    return {
      results: this.results,
      summary
    };
  }

  /**
   * 运行单个测试
   * @param {Object} testCase 测试用例
   * @returns {Promise<Object>} 测试结果
   */
  async runTest(testCase) {
    console.log(`运行测试: ${testCase.name}`);

    try {
      // 步骤1: 分解请求
      const decompositionResult = decomposeRequest(testCase.query, testCase.sourceAgent);
      
      // 步骤2: 处理请求
      const processingResult = await agentRouter.processRequest(testCase.query, decompositionResult.targetAgent);
      
      // 步骤3: 如果是通用智能体，存储六特性
      let storageResult = null;
      if (decompositionResult.targetAgent === AGENT_TYPES.GENERAL && processingResult.result && processingResult.result.features) {
        storageResult = await storeContextMemory(testCase.query, processingResult, processingResult.result.features);
      }
      
      // 步骤4: 如果是上下文记忆测试，检索上下文
      let memoryResult = null;
      if (testCase.id === 'context_memory_test') {
        memoryResult = await retrieveContextMemory(testCase.query);
      }
      
      // 验证结果
      const targetAgentCorrect = decompositionResult.targetAgent === testCase.expectedTargetAgent;
      const processingSuccessful = processingResult.status === 'success';
      const featuresStored = testCase.id === 'feature_storage_test' ? 
        (processingResult.result && processingResult.result.features && Object.keys(processingResult.result.features).length === 6) : 
        true;
      const memoryRetrieved = testCase.id === 'context_memory_test' ? 
        (memoryResult && memoryResult.features) : 
        true;
      
      // 确定测试是否通过
      const passed = targetAgentCorrect && processingSuccessful && featuresStored && memoryRetrieved;
      
      return {
        testCase,
        passed,
        details: {
          decompositionResult,
          processingResult,
          storageResult,
          memoryResult,
          targetAgentCorrect,
          processingSuccessful,
          featuresStored,
          memoryRetrieved
        },
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error(`测试失败: ${testCase.name}`, error);
      return {
        testCase,
        passed: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * 生成测试摘要
   * @returns {Object} 测试摘要
   * @private
   */
  _generateSummary() {
    const total = this.results.length;
    const passed = this.results.filter(r => r.passed).length;
    const failed = total - passed;
    const passRate = total > 0 ? (passed / total) * 100 : 0;

    // 按类别统计
    const categoryCounts = {
      routing: 0,
      routing_passed: 0,
      feature_storage: 0,
      feature_storage_passed: 0,
      context_memory: 0,
      context_memory_passed: 0
    };

    for (const result of this.results) {
      const { id, name } = result.testCase;
      
      if (id.includes('routing') || id.includes('decomposition')) {
        categoryCounts.routing++;
        if (result.passed) categoryCounts.routing_passed++;
      }
      
      if (id.includes('feature')) {
        categoryCounts.feature_storage++;
        if (result.passed) categoryCounts.feature_storage_passed++;
      }
      
      if (id.includes('context') || id.includes('memory')) {
        categoryCounts.context_memory++;
        if (result.passed) categoryCounts.context_memory_passed++;
      }
    }

    return {
      total,
      passed,
      failed,
      passRate: passRate.toFixed(2) + '%',
      categories: {
        routing: {
          total: categoryCounts.routing,
          passed: categoryCounts.routing_passed,
          passRate: categoryCounts.routing > 0 ? 
            ((categoryCounts.routing_passed / categoryCounts.routing) * 100).toFixed(2) + '%' : 
            'N/A'
        },
        feature_storage: {
          total: categoryCounts.feature_storage,
          passed: categoryCounts.feature_storage_passed,
          passRate: categoryCounts.feature_storage > 0 ? 
            ((categoryCounts.feature_storage_passed / categoryCounts.feature_storage) * 100).toFixed(2) + '%' : 
            'N/A'
        },
        context_memory: {
          total: categoryCounts.context_memory,
          passed: categoryCounts.context_memory_passed,
          passRate: categoryCounts.context_memory > 0 ? 
            ((categoryCounts.context_memory_passed / categoryCounts.context_memory) * 100).toFixed(2) + '%' : 
            'N/A'
        }
      },
      timestamp: new Date().toISOString()
    };
  }
}

// 创建单例
const endToEndValidator = new EndToEndValidator();

export default endToEndValidator;
