import React from 'react';
import './CodeView.css';

interface CodeViewProps {
  agentType: string;
  testType?: string; // 可选参数，指定测试类型：'integration', 'e2e', 'visual'
}

const CodeView: React.FC<CodeViewProps> = ({ agentType, testType = 'integration' }) => {
  // 根据测试类型渲染不同的代码内容
  const renderTestCode = () => {
    switch (testType) {
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
      
      <div className="code-tabs">
        <button className={`code-tab ${testType === 'integration' ? 'active' : ''}`}>集成测试</button>
        <button className={`code-tab ${testType === 'e2e' ? 'active' : ''}`}>端到端测试</button>
        <button className={`code-tab ${testType === 'visual' ? 'active' : ''}`}>视觉自动化测试</button>
      </div>
      
      <div className="code-content">
        {renderTestCode()}
      </div>
    </div>
  );
};

export default CodeView;
