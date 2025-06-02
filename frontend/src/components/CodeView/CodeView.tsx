import React, { useState, useEffect } from 'react';
import './CodeView.css';

interface CodeViewProps {
  agentType: string;
  testType?: string; // 可选参数，指定测试类型：'integration', 'e2e', 'visual'
  selectedNodeId?: string; // 选中的节点ID
}

const CodeView: React.FC<CodeViewProps> = ({ agentType, testType = 'integration', selectedNodeId }) => {
  const [activeTab, setActiveTab] = useState(testType);
  
  // 当外部传入testType变化时，更新activeTab
  useEffect(() => {
    if (testType) {
      setActiveTab(testType);
    }
  }, [testType]);
  
  // 根据选中的节点ID过滤显示相关代码
  const getNodeRelatedCode = (nodeId?: string) => {
    if (!nodeId) return null;
    
    // 根据节点ID返回相关代码片段
    // 这里可以实现一个映射关系，将节点ID映射到对应的代码片段
    const codeMapping: Record<string, { filename: string, content: string }> = {
      'integration-test': {
        filename: 'integration_test_node.js',
        content: `// 集成测试节点代码
const { test, expect } = require('@playwright/test');

/**
 * 集成测试节点实现
 * @param {Object} input - 输入数据
 * @param {Object} context - 执行上下文
 * @returns {Object} - 测试结果
 */
async function integrationTestNode(input, context) {
  console.log('开始执行集成测试节点');
  
  try {
    // 初始化测试环境
    const testEnv = await context.getTestEnvironment();
    
    // 执行测试
    const results = await test.step('组件交互测试', async () => {
      const componentA = await testEnv.getComponent('ComponentA');
      const componentB = await testEnv.getComponent('ComponentB');
      
      // 测试组件交互
      await componentA.sendData('测试数据');
      const receivedData = await componentB.getReceivedData();
      
      expect(receivedData).toContain('测试数据');
      return { success: true, message: '组件交互测试通过' };
    });
    
    console.log('集成测试节点执行成功');
    return {
      status: 'success',
      results: results,
      executionTime: 1250, // ms
      memoryUsage: 85, // MB
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('集成测试节点执行失败', error);
    return {
      status: 'error',
      error: error.message,
      executionTime: 850, // ms
      timestamp: new Date().toISOString()
    };
  }
}`
      },
      'e2e-test': {
        filename: 'e2e_test_node.js',
        content: `// 端到端测试节点代码
const { test, expect } = require('@playwright/test');

/**
 * 端到端测试节点实现
 * @param {Object} input - 输入数据
 * @param {Object} context - 执行上下文
 * @returns {Object} - 测试结果
 */
async function e2eTestNode(input, context) {
  console.log('开始执行端到端测试节点');
  
  try {
    // 获取浏览器实例
    const browser = await context.getBrowser();
    const page = await browser.newPage();
    
    // 执行登录流程测试
    const loginResults = await test.step('用户登录流程测试', async () => {
      await page.goto('http://localhost:3000/login');
      await page.fill('#username', 'testuser');
      await page.fill('#password', 'password123');
      await page.click('#login-button');
      
      // 验证登录成功
      await expect(page).toHaveURL('http://localhost:3000/dashboard');
      return { success: true, message: '登录流程测试通过' };
    });
    
    // 执行工作流创建测试
    const workflowResults = await test.step('工作流创建测试', async () => {
      await page.click('nav >> text=工作流节点及工作流');
      await page.click('#create-workflow');
      await page.fill('#workflow-name', '测试工作流');
      
      // 验证工作流创建成功
      await expect(page.locator('.success-message')).toBeVisible();
      return { success: true, message: '工作流创建测试通过' };
    });
    
    console.log('端到端测试节点执行成功');
    return {
      status: 'success',
      results: {
        login: loginResults,
        workflow: workflowResults
      },
      executionTime: 3250, // ms
      memoryUsage: 120, // MB
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('端到端测试节点执行失败', error);
    return {
      status: 'error',
      error: error.message,
      executionTime: 1850, // ms
      timestamp: new Date().toISOString()
    };
  }
}`
      },
      'visual-test': {
        filename: 'visual_test_node.js',
        content: `// 视觉自动化测试节点代码
const { test, expect } = require('@playwright/test');
const { compareScreenshots } = require('../utils/visual-comparison');

/**
 * 视觉自动化测试节点实现
 * @param {Object} input - 输入数据
 * @param {Object} context - 执行上下文
 * @returns {Object} - 测试结果
 */
async function visualTestNode(input, context) {
  console.log('开始执行视觉自动化测试节点');
  
  try {
    // 获取浏览器实例
    const browser = await context.getBrowser();
    const page = await browser.newPage();
    
    // 访问组件测试页面
    await page.goto('http://localhost:3000/component-test');
    await page.waitForSelector('.component-ready', { state: 'visible' });
    
    // 执行组件视觉测试
    const componentResults = await test.step('组件视觉测试', async () => {
      // 对不同组件进行截图
      await page.screenshot({ path: './screenshots/button-component.png', selector: '.button-component' });
      await page.screenshot({ path: './screenshots/input-component.png', selector: '.input-component' });
      
      // 与基准图像进行比较
      const buttonDiff = await compareScreenshots('./screenshots/button-component.png', './baseline/button-component.png');
      const inputDiff = await compareScreenshots('./screenshots/input-component.png', './baseline/input-component.png');
      
      // 验证视觉差异在可接受范围内
      expect(buttonDiff.diffPercentage).toBeLessThan(0.1);
      expect(inputDiff.diffPercentage).toBeLessThan(0.1);
      
      return { 
        success: true, 
        message: '组件视觉测试通过',
        diffResults: {
          button: buttonDiff,
          input: inputDiff
        }
      };
    });
    
    // 执行响应式布局测试
    const responsiveResults = await test.step('响应式布局测试', async () => {
      await page.goto('http://localhost:3000/responsive-test');
      
      // 测试不同设备布局
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.screenshot({ path: './screenshots/desktop-layout.png' });
      
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.screenshot({ path: './screenshots/tablet-layout.png' });
      
      await page.setViewportSize({ width: 375, height: 667 });
      await page.screenshot({ path: './screenshots/mobile-layout.png' });
      
      return { success: true, message: '响应式布局测试通过' };
    });
    
    console.log('视觉自动化测试节点执行成功');
    return {
      status: 'success',
      results: {
        component: componentResults,
        responsive: responsiveResults
      },
      executionTime: 4750, // ms
      memoryUsage: 180, // MB
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('视觉自动化测试节点执行失败', error);
    return {
      status: 'error',
      error: error.message,
      executionTime: 2250, // ms
      timestamp: new Date().toISOString()
    };
  }
}`
      },
      'general-agent': {
        filename: 'general_agent.js',
        content: `// 通用智能体节点代码
/**
 * 通用智能体实现
 * @param {Object} input - 用户输入
 * @param {Object} context - 执行上下文
 * @returns {Object} - 处理结果
 */
async function generalAgent(input, context) {
  console.log('通用智能体开始处理用户输入');
  
  try {
    // 解析用户输入
    const userInput = input.message || '';
    if (!userInput) {
      throw new Error('用户输入为空');
    }
    
    // 记录用户输入
    await context.recordUserInput(userInput);
    
    // 触发SuperMemory记忆检查
    const memoryCheck = await context.triggerMemoryCheck();
    console.log('SuperMemory记忆检查结果:', memoryCheck);
    
    // 将输入传递给MCP协调器
    const result = await context.sendToMCP(userInput);
    
    return {
      status: 'success',
      result: result,
      memoryStatus: memoryCheck,
      executionTime: 850, // ms
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('通用智能体处理失败', error);
    return {
      status: 'error',
      error: error.message,
      executionTime: 450, // ms
      timestamp: new Date().toISOString()
    };
  }
}`
      },
      'mcp-coordinator': {
        filename: 'mcp_coordinator.js',
        content: `// MCP协调器节点代码
/**
 * MCP协调器实现
 * @param {Object} input - 输入数据
 * @param {Object} context - 执行上下文
 * @returns {Object} - 协调结果
 */
async function mcpCoordinator(input, context) {
  console.log('MCP协调器开始工作');
  
  try {
    // 分析输入
    const inputData = input.data || input;
    
    // 创建任务计划
    const plan = await context.createTaskPlan(inputData);
    console.log('任务计划创建成功:', plan);
    
    // 分配任务给各子系统
    const plannerTask = context.assignTask('mcp-planner', plan);
    const recorderTask = context.assignTask('thought-recorder', { action: 'record', data: inputData });
    const releaseTask = context.assignTask('release-manager', { action: 'check' });
    
    // 等待所有任务完成
    const [plannerResult, recorderResult, releaseResult] = await Promise.all([
      plannerTask,
      recorderTask,
      releaseTask
    ]);
    
    // 整合结果
    const result = {
      planner: plannerResult,
      recorder: recorderResult,
      release: releaseResult
    };
    
    return {
      status: 'success',
      result: result,
      executionTime: 1250, // ms
      memoryUsage: 95, // MB
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    console.error('MCP协调器执行失败', error);
    return {
      status: 'error',
      error: error.message,
      executionTime: 750, // ms
      timestamp: new Date().toISOString()
    };
  }
}`
      },
      'supermemory': {
        filename: 'supermemory.js',
        content: `// SuperMemory.ai 集成代码
const axios = require('axios');

/**
 * SuperMemory API客户端
 */
class SuperMemoryClient {
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey;
    this.baseUrl = options.baseUrl || 'https://api.supermemory.ai/v1';
    this.timeout = options.timeout || 30000;
  }
  
  /**
   * 创建HTTP客户端
   * @returns {Object} - Axios实例
   */
  createHttpClient() {
    return axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers: {
        'Authorization': \`Bearer \${this.apiKey}\`,
        'Content-Type': 'application/json'
      }
    });
  }
  
  /**
   * 记录记忆
   * @param {Object} memory - 记忆数据
   * @returns {Promise<Object>} - API响应
   */
  async recordMemory(memory) {
    const client = this.createHttpClient();
    try {
      const response = await client.post('/memories', memory);
      return response.data;
    } catch (error) {
      console.error('记录记忆失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 检索记忆
   * @param {Object} query - 查询条件
   * @returns {Promise<Object>} - 检索结果
   */
  async retrieveMemories(query) {
    const client = this.createHttpClient();
    try {
      const response = await client.get('/memories', { params: query });
      return response.data;
    } catch (error) {
      console.error('检索记忆失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 检查记忆状态
   * @returns {Promise<Object>} - 记忆状态
   */
  async checkMemoryStatus() {
    const client = this.createHttpClient();
    try {
      const response = await client.get('/status');
      return response.data;
    } catch (error) {
      console.error('检查记忆状态失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 触发记忆检查
   * @param {string} trigger - 触发器名称
   * @returns {Promise<Object>} - 检查结果
   */
  async triggerMemoryCheck(trigger) {
    const client = this.createHttpClient();
    try {
      const response = await client.post('/triggers', { name: trigger });
      return response.data;
    } catch (error) {
      console.error('触发记忆检查失败:', error.message);
      throw error;
    }
  }
}

module.exports = SuperMemoryClient;`
      }
    };
    
    return codeMapping[nodeId] || null;
  };
  
  // 获取当前选中节点的相关代码
  const selectedNodeCode = getNodeRelatedCode(selectedNodeId);
  
  // 根据测试类型渲染不同的代码内容
  const renderTestCode = () => {
    // 如果有选中节点且有对应代码，优先显示节点相关代码
    if (selectedNodeId && selectedNodeCode) {
      return (
        <div className="code-section">
          <h3 className="code-section-title">节点代码: {selectedNodeId}</h3>
          
          <div className="code-block">
            <div className="code-header">
              <span className="code-filename">{selectedNodeCode.filename}</span>
              <div className="code-actions">
                <button className="code-action-button">
                  <span className="code-action-icon">📋</span>
                  复制
                </button>
                <button className="code-action-button">
                  <span className="code-action-icon">▶️</span>
                  运行
                </button>
              </div>
            </div>
            
            <pre className="code-content-block">
              <code>
                {selectedNodeCode.content}
              </code>
            </pre>
          </div>
        </div>
      );
    }
    
    // 如果没有选中节点或没有对应代码，显示测试类型相关代码
    switch (activeTab) {
      case 'integration':
        return (
          <>
            <div className="code-section">
              <h3 className="code-section-title">集成测试代码</h3>
              
              <div className="code-block">
                <div className="code-header">
                  <span className="code-filename">integration_test.js</span>
                  <div className="code-actions">
                    <button className="code-action-button">
                      <span className="code-action-icon">📋</span>
                      复制
                    </button>
                    <button className="code-action-button">
                      <span className="code-action-icon">▶️</span>
                      运行
                    </button>
                  </div>
                </div>
                
                <pre className="code-content-block">
                  <code>
{`// 集成测试示例
const { test, expect } = require('@playwright/test');
const { ComponentA } = require('../src/components/ComponentA');
const { ComponentB } = require('../src/components/ComponentB');
const { DataService } = require('../src/services/DataService');

/**
 * 测试组件A和组件B的交互
 */
test('ComponentA 和 ComponentB 交互测试', async ({ page }) => {
  // 初始化测试环境
  await page.goto('http://localhost:3000/test-environment');
  
  // 模拟组件A的操作
  await page.locator('#componentA-input').fill('测试数据');
  await page.locator('#componentA-submit').click();
  
  // 验证组件B是否正确接收数据
  const componentBOutput = await page.locator('#componentB-output').textContent();
  expect(componentBOutput).toContain('测试数据');
  
  // 验证数据服务是否正确处理
  const dataServiceStatus = await page.locator('#data-service-status').textContent();
  expect(dataServiceStatus).toBe('已处理');
});

/**
 * 测试数据流转
 */
test('数据服务与组件交互测试', async ({ page }) => {
  // 初始化测试环境
  await page.goto('http://localhost:3000/test-environment');
  
  // 模拟数据服务操作
  await page.evaluate(() => {
    window.dataService = new DataService();
    window.dataService.setData({ key: 'value' });
  });
  
  // 触发组件更新
  await page.locator('#refresh-components').click();
  
  // 验证组件是否正确更新
  const componentAStatus = await page.locator('#componentA-status').textContent();
  expect(componentAStatus).toBe('已更新');
  
  const componentBStatus = await page.locator('#componentB-status').textContent();
  expect(componentBStatus).toBe('已更新');
});`}
                  </code>
                </pre>
              </div>
            </div>
            
            <div className="code-section">
              <h3 className="code-section-title">集成测试配置</h3>
              
              <div className="code-block">
                <div className="code-header">
                  <span className="code-filename">integration.config.js</span>
                  <div className="code-actions">
                    <button className="code-action-button">
                      <span className="code-action-icon">📋</span>
                      复制
                    </button>
                  </div>
                </div>
                
                <pre className="code-content-block">
                  <code>
{`// 集成测试配置
module.exports = {
  // 测试环境配置
  testEnvironment: 'jsdom',
  
  // 测试文件匹配模式
  testMatch: [
    '**/integration/**/*.test.js',
    '**/integration/**/*.spec.js'
  ],
  
  // 测试超时设置
  testTimeout: 30000,
  
  // 测试覆盖率收集
  collectCoverage: true,
  coverageDirectory: 'coverage/integration',
  
  // 模块模拟设置
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  
  // 测试报告设置
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: './reports/integration',
      outputName: 'results.xml'
    }]
  ],
  
  // 测试钩子
  setupFilesAfterEnv: [
    '<rootDir>/test/integration/setup.js'
  ]
};`}
                  </code>
                </pre>
              </div>
            </div>
          </>
        );
        
      case 'e2e':
        return (
          <>
            <div className="code-section">
              <h3 className="code-section-title">端到端测试代码</h3>
              
              <div className="code-block">
                <div className="code-header">
                  <span className="code-filename">e2e_test.js</span>
                  <div className="code-actions">
                    <button className="code-action-button">
                      <span className="code-action-icon">📋</span>
                      复制
                    </button>
                    <button className="code-action-button">
                      <span className="code-action-icon">▶️</span>
                      运行
                    </button>
                  </div>
                </div>
                
                <pre className="code-content-block">
                  <code>
{`// 端到端测试示例
const { test, expect } = require('@playwright/test');

/**
 * 测试用户登录流程
 */
test('用户登录流程测试', async ({ page }) => {
  // 访问登录页面
  await page.goto('http://localhost:3000/login');
  
  // 填写登录表单
  await page.locator('#username').fill('testuser');
  await page.locator('#password').fill('password123');
  
  // 提交表单
  await page.locator('#login-button').click();
  
  // 验证登录成功
  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  await expect(page.locator('.user-welcome')).toContainText('欢迎, testuser');
});

/**
 * 测试工作流创建流程
 */
test('工作流创建流程测试', async ({ page }) => {
  // 登录系统
  await page.goto('http://localhost:3000/login');
  await page.locator('#username').fill('testuser');
  await page.locator('#password').fill('password123');
  await page.locator('#login-button').click();
  
  // 导航到工作流页面
  await page.locator('nav >> text=工作流节点及工作流').click();
  
  // 创建新工作流
  await page.locator('#create-workflow').click();
  await page.locator('#workflow-name').fill('测试工作流');
  await page.locator('#workflow-description').fill('这是一个测试工作流');
  
  // 添加工作流节点
  await page.locator('#add-node').click();
  await page.locator('#node-type-selector').selectOption('integration-test');
  await page.locator('#add-node-confirm').click();
  
  // 添加第二个节点
  await page.locator('#add-node').click();
  await page.locator('#node-type-selector').selectOption('e2e-test');
  await page.locator('#add-node-confirm').click();
  
  // 连接节点
  await page.locator('#connect-nodes').click();
  await page.locator('#node-0').click();
  await page.locator('#node-1').click();
  
  // 保存工作流
  await page.locator('#save-workflow').click();
  
  // 验证工作流创建成功
  await expect(page.locator('.success-message')).toBeVisible();
  await expect(page.locator('.workflow-list')).toContainText('测试工作流');
});`}
                  </code>
                </pre>
              </div>
            </div>
            
            <div className="code-section">
              <h3 className="code-section-title">端到端测试配置</h3>
              
              <div className="code-block">
                <div className="code-header">
                  <span className="code-filename">playwright.config.js</span>
                  <div className="code-actions">
                    <button className="code-action-button">
                      <span className="code-action-icon">📋</span>
                      复制
                    </button>
                  </div>
                </div>
                
                <pre className="code-content-block">
                  <code>
{`// Playwright 端到端测试配置
const { devices } = require('@playwright/test');

module.exports = {
  // 测试目录
  testDir: './test/end_to_end',
  
  // 测试文件匹配模式
  testMatch: '**/*.e2e.js',
  
  // 超时设置
  timeout: 60000,
  
  // 并发运行设置
  workers: process.env.CI ? 2 : undefined,
  
  // 测试报告
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/e2e-results.json' }]
  ],
  
  // 测试使用的浏览器
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'mobile chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'mobile safari',
      use: { ...devices['iPhone 12'] }
    }
  ],
  
  // 测试环境设置
  webServer: {
    command: 'npm run start',
    port: 3000,
    timeout: 120000,
    reuseExistingServer: !process.env.CI
  }
};`}
                  </code>
                </pre>
              </div>
            </div>
          </>
        );
        
      case 'visual':
        return (
          <>
            <div className="code-section">
              <h3 className="code-section-title">视觉自动化测试代码</h3>
              
              <div className="code-block">
                <div className="code-header">
                  <span className="code-filename">visual_test.js</span>
                  <div className="code-actions">
                    <button className="code-action-button">
                      <span className="code-action-icon">📋</span>
                      复制
                    </button>
                    <button className="code-action-button">
                      <span className="code-action-icon">▶️</span>
                      运行
                    </button>
                  </div>
                </div>
                
                <pre className="code-content-block">
                  <code>
{`// 视觉自动化测试示例
const { test, expect } = require('@playwright/test');
const { compareScreenshots } = require('../utils/visual-comparison');

/**
 * 测试组件视觉一致性
 */
test('组件视觉一致性测试', async ({ page }) => {
  // 访问组件测试页面
  await page.goto('http://localhost:3000/component-test');
  
  // 等待组件完全加载
  await page.waitForSelector('.component-ready', { state: 'visible' });
  
  // 对不同组件进行截图
  await page.screenshot({ path: './screenshots/button-component.png', selector: '.button-component' });
  await page.screenshot({ path: './screenshots/input-component.png', selector: '.input-component' });
  await page.screenshot({ path: './screenshots/card-component.png', selector: '.card-component' });
  
  // 与基准图像进行比较
  const buttonDiff = await compareScreenshots('./screenshots/button-component.png', './baseline/button-component.png');
  const inputDiff = await compareScreenshots('./screenshots/input-component.png', './baseline/input-component.png');
  const cardDiff = await compareScreenshots('./screenshots/card-component.png', './baseline/card-component.png');
  
  // 验证视觉差异在可接受范围内
  expect(buttonDiff.diffPercentage).toBeLessThan(0.1);
  expect(inputDiff.diffPercentage).toBeLessThan(0.1);
  expect(cardDiff.diffPercentage).toBeLessThan(0.1);
});

/**
 * 测试响应式布局
 */
test('响应式布局测试', async ({ page }) => {
  // 访问测试页面
  await page.goto('http://localhost:3000/responsive-test');
  
  // 测试桌面布局
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.waitForTimeout(500); // 等待布局调整
  await page.screenshot({ path: './screenshots/desktop-layout.png' });
  
  // 测试平板布局
  await page.setViewportSize({ width: 768, height: 1024 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: './screenshots/tablet-layout.png' });
  
  // 测试手机布局
  await page.setViewportSize({ width: 375, height: 667 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: './screenshots/mobile-layout.png' });
  
  // 与基准图像进行比较
  const desktopDiff = await compareScreenshots('./screenshots/desktop-layout.png', './baseline/desktop-layout.png');
  const tabletDiff = await compareScreenshots('./screenshots/tablet-layout.png', './baseline/tablet-layout.png');
  const mobileDiff = await compareScreenshots('./screenshots/mobile-layout.png', './baseline/mobile-layout.png');
  
  // 验证视觉差异在可接受范围内
  expect(desktopDiff.diffPercentage).toBeLessThan(0.1);
  expect(tabletDiff.diffPercentage).toBeLessThan(0.1);
  expect(mobileDiff.diffPercentage).toBeLessThan(0.1);
});`}
                  </code>
                </pre>
              </div>
            </div>
            
            <div className="code-section">
              <h3 className="code-section-title">视觉比较工具</h3>
              
              <div className="code-block">
                <div className="code-header">
                  <span className="code-filename">visual-comparison.js</span>
                  <div className="code-actions">
                    <button className="code-action-button">
                      <span className="code-action-icon">📋</span>
                      复制
                    </button>
                  </div>
                </div>
                
                <pre className="code-content-block">
                  <code>
{`// 视觉比较工具
const fs = require('fs');
const { PNG } = require('pngjs');
const pixelmatch = require('pixelmatch');
const path = require('path');

/**
 * 比较两张截图的差异
 * @param {string} actualPath - 实际截图路径
 * @param {string} baselinePath - 基准截图路径
 * @param {Object} options - 比较选项
 * @returns {Object} - 比较结果
 */
async function compareScreenshots(actualPath, baselinePath, options = {}) {
  // 默认选项
  const defaultOptions = {
    threshold: 0.1,
    outputDiffPath: null
  };
  
  const config = { ...defaultOptions, ...options };
  
  // 检查基准图像是否存在
  if (!fs.existsSync(baselinePath)) {
    console.log(\`基准图像不存在: \${baselinePath}, 将当前截图设为基准\`);
    fs.copyFileSync(actualPath, baselinePath);
    return { diffPercentage: 0, diffPixels: 0, match: true };
  }
  
  // 读取图像
  const actualImg = PNG.sync.read(fs.readFileSync(actualPath));
  const baselineImg = PNG.sync.read(fs.readFileSync(baselinePath));
  
  // 确保图像尺寸相同
  if (actualImg.width !== baselineImg.width || actualImg.height !== baselineImg.height) {
    throw new Error(\`图像尺寸不匹配: 
      实际图像: \${actualImg.width}x\${actualImg.height}, 
      基准图像: \${baselineImg.width}x\${baselineImg.height}\`);
  }
  
  // 创建差异图像
  const { width, height } = actualImg;
  const diffImg = new PNG({ width, height });
  
  // 比较图像
  const diffPixels = pixelmatch(
    actualImg.data,
    baselineImg.data,
    diffImg.data,
    width,
    height,
    { threshold: config.threshold }
  );
  
  // 计算差异百分比
  const diffPercentage = diffPixels / (width * height);
  
  // 如果需要，保存差异图像
  if (config.outputDiffPath) {
    const diffPngBuffer = PNG.sync.write(diffImg);
    fs.writeFileSync(config.outputDiffPath, diffPngBuffer);
  }
  
  return {
    diffPercentage,
    diffPixels,
    match: diffPercentage < config.threshold,
    width,
    height
  };
}

module.exports = {
  compareScreenshots
};`}
                  </code>
                </pre>
              </div>
            </div>
          </>
        );
        
      default:
        return (
          <div className="code-section">
            <h3 className="code-section-title">测试代码</h3>
            <p className="placeholder-text">请选择测试类型查看对应代码</p>
          </div>
        );
    }
  };

  return (
    <div className="code-view">
      <h2 className="section-title">代码视图</h2>
      
      {selectedNodeId && (
        <div className="selected-node-info">
          <span className="selected-node-label">当前选中节点:</span>
          <span className="selected-node-id">{selectedNodeId}</span>
        </div>
      )}
      
      <div className="code-tabs">
        <button 
          className={`code-tab ${activeTab === 'integration' ? 'active' : ''}`}
          onClick={() => setActiveTab('integration')}
        >
          集成测试
        </button>
        <button 
          className={`code-tab ${activeTab === 'e2e' ? 'active' : ''}`}
          onClick={() => setActiveTab('e2e')}
        >
          端到端测试
        </button>
        <button 
          className={`code-tab ${activeTab === 'visual' ? 'active' : ''}`}
          onClick={() => setActiveTab('visual')}
        >
          视觉自动化测试
        </button>
      </div>
      
      <div className="code-content">
        {/* SuperMemory程序部分 */}
        {!selectedNodeId && (
          <div className="code-section">
            <h3 className="code-section-title">SuperMemory程序</h3>
            
            <div className="code-block">
              <div className="code-header">
                <span className="code-filename">supermemory.js</span>
                <div className="code-actions">
                  <button className="code-action-button">
                    <span className="code-action-icon">📋</span>
                    复制
                  </button>
                  <button className="code-action-button">
                    <span className="code-action-icon">▶️</span>
                    运行
                  </button>
                </div>
              </div>
              
              <pre className="code-content-block">
                <code>
{`// SuperMemory.ai 集成代码
const axios = require('axios');

/**
 * SuperMemory API客户端
 */
class SuperMemoryClient {
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey;
    this.baseUrl = options.baseUrl || 'https://api.supermemory.ai/v1';
    this.timeout = options.timeout || 30000;
  }
  
  /**
   * 创建HTTP客户端
   * @returns {Object} - Axios实例
   */
  createHttpClient() {
    return axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers: {
        'Authorization': \`Bearer \${this.apiKey}\`,
        'Content-Type': 'application/json'
      }
    });
  }
  
  /**
   * 记录记忆
   * @param {Object} memory - 记忆数据
   * @returns {Promise<Object>} - API响应
   */
  async recordMemory(memory) {
    const client = this.createHttpClient();
    try {
      const response = await client.post('/memories', memory);
      return response.data;
    } catch (error) {
      console.error('记录记忆失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 检索记忆
   * @param {Object} query - 查询条件
   * @returns {Promise<Object>} - 检索结果
   */
  async retrieveMemories(query) {
    const client = this.createHttpClient();
    try {
      const response = await client.get('/memories', { params: query });
      return response.data;
    } catch (error) {
      console.error('检索记忆失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 检查记忆状态
   * @returns {Promise<Object>} - 记忆状态
   */
  async checkMemoryStatus() {
    const client = this.createHttpClient();
    try {
      const response = await client.get('/status');
      return response.data;
    } catch (error) {
      console.error('检查记忆状态失败:', error.message);
      throw error;
    }
  }
  
  /**
   * 触发记忆检查
   * @param {string} trigger - 触发器名称
   * @returns {Promise<Object>} - 检查结果
   */
  async triggerMemoryCheck(trigger) {
    const client = this.createHttpClient();
    try {
      const response = await client.post('/triggers', { name: trigger });
      return response.data;
    } catch (error) {
      console.error('触发记忆检查失败:', error.message);
      throw error;
    }
  }
}

module.exports = SuperMemoryClient;`}
                </code>
              </pre>
            </div>
          </div>
        )}
        
        {renderTestCode()}
      </div>
    </div>
  );
};

export default CodeView;
