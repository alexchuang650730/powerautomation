# 端到端视觉自动化测试指南

## 1. 概述

PowerAutomation系统的端到端视觉自动化测试框架位于`test/visual_test`目录下，由TestAndIssueCollector模块负责执行。本指南详细说明如何配置、运行和扩展这些测试，确保系统UI和功能的正确性。

## 2. 测试架构

### 2.1 目录结构

```
test/
├── visual_test/
│   ├── baseline/              # 基准图像
│   ├── fixtures/              # 测试固件
│   ├── pages/                 # 页面对象模型
│   ├── reports/               # 测试报告
│   ├── scenarios/             # 测试场景
│   ├── utils/                 # 测试工具
│   ├── config.json            # 测试配置
│   └── run_tests.py           # 测试入口
└── unit/                      # 单元测试
```

### 2.2 技术栈

- **Playwright**：用于浏览器自动化
- **pytest**：测试框架
- **pytest-playwright**：Playwright的pytest插件
- **pytest-html**：生成HTML测试报告
- **pixelmatch**：图像比较库
- **Qwen3-8B**：用于测试结果分析和问题解决

## 3. 测试类型

### 3.1 视觉回归测试

比较UI元素与基准图像的差异，确保UI没有意外变化。

```python
def test_homepage_visual(page, screenshot_comparison):
    # 导航到首页
    page.goto("http://localhost:5173")
    
    # 等待页面加载完成
    page.wait_for_selector(".agent-card")
    
    # 截取屏幕截图
    screenshot = page.screenshot()
    
    # 与基准图像比较
    diff = screenshot_comparison.compare(
        screenshot, 
        "homepage.png", 
        threshold=0.1
    )
    
    # 断言差异在可接受范围内
    assert diff < 0.05, f"Visual difference {diff} exceeds threshold"
```

### 3.2 功能流程测试

验证端到端用户流程的功能正确性。

```python
def test_code_agent_routing(page, assert_response):
    # 导航到首页
    page.goto("http://localhost:5173")
    
    # 选择代码智能体
    page.click("text=代码智能体")
    
    # 输入查询
    page.fill("textarea[placeholder='请输入您的需求...']", "帮我写一个Python函数计算斐波那契数列")
    page.press("textarea", "Enter")
    
    # 等待响应
    response_locator = page.locator(".response-content")
    response_locator.wait_for(state="visible")
    
    # 获取响应文本
    response_text = response_locator.inner_text()
    
    # 断言响应包含代码
    assert "def fibonacci" in response_text
    assert "return fibonacci" in response_text
    
    # 断言路由到了正确的智能体
    agent_indicator = page.locator(".current-agent")
    assert "代码智能体" in agent_indicator.inner_text()
```

### 3.3 六特性存储测试

验证六特性存储和检索功能。

```python
def test_feature_storage(page, assert_storage):
    # 导航到首页
    page.goto("http://localhost:5173")
    
    # 选择通用智能体
    page.click("text=通用智能体")
    
    # 输入特性修改请求
    page.fill("textarea[placeholder='请输入您的需求...']", "优化PowerAutomation的UI布局特性")
    page.press("textarea", "Enter")
    
    # 等待响应
    page.wait_for_selector(".response-content")
    
    # 验证特性已存储
    storage_result = assert_storage.verify_feature_stored(
        agent_type="general",
        feature_name="ui_layout",
        contains_text="布局"
    )
    
    assert storage_result.stored, f"Feature not stored: {storage_result.message}"
```

## 4. 测试配置

### 4.1 基本配置

在`test/visual_test/config.json`中配置测试参数：

```json
{
  "baseUrl": "http://localhost:5173",
  "apiUrl": "http://localhost:5000",
  "headless": true,
  "slowMo": 50,
  "viewport": {
    "width": 1280,
    "height": 720
  },
  "screenshotDir": "./screenshots",
  "baselineDir": "./baseline",
  "diffDir": "./diff",
  "threshold": 0.1,
  "timeout": 30000
}
```

### 4.2 环境配置

创建`.env.test`文件配置测试环境变量：

```
TEST_BASE_URL=http://localhost:5173
TEST_API_URL=http://localhost:5000
TEST_USERNAME=testuser
TEST_PASSWORD=testpassword
SUPERMEMORY_API_KEY=your_test_api_key
```

## 5. 运行测试

### 5.1 本地运行

```bash
# 安装依赖
pip install -r test/visual_test/requirements.txt

# 安装Playwright浏览器
playwright install

# 运行所有视觉测试
python test/visual_test/run_tests.py

# 运行特定测试
python test/visual_test/run_tests.py --test test_homepage_visual
```

### 5.2 GitHub Actions集成

测试会在GitHub Actions工作流中自动运行：

```yaml
name: Visual Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  visual-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r test/visual_test/requirements.txt
          playwright install
      - name: Start application
        run: |
          cd backend
          pip install -r requirements.txt
          python app.py &
          cd ../frontend
          npm install
          npm run dev &
          sleep 10
      - name: Run visual tests
        run: python test/visual_test/run_tests.py
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: test/visual_test/reports/
```

## 6. 测试报告

测试完成后，报告将生成在`test/visual_test/reports/`目录下：

- `report.html`：HTML格式的测试报告
- `screenshots/`：测试过程中的屏幕截图
- `diff/`：视觉差异图像

## 7. 添加新测试

### 7.1 添加视觉回归测试

1. 在`test/visual_test/scenarios/`目录下创建新的测试文件
2. 实现测试函数
3. 生成基准图像：`python test/visual_test/utils/generate_baseline.py --test your_test_name`

### 7.2 添加功能流程测试

1. 在`test/visual_test/scenarios/`目录下创建新的测试文件
2. 实现测试函数，使用页面对象模型
3. 在`test/visual_test/pages/`目录下添加新的页面对象（如果需要）

### 7.3 页面对象模型示例

```python
# test/visual_test/pages/home_page.py
class HomePage:
    def __init__(self, page):
        self.page = page
        self.url = "/"
        self.agent_cards = page.locator(".agent-card")
        self.input_field = page.locator("textarea[placeholder='请输入您的需求...']")
        self.send_button = page.locator("button.send-button")
        self.response_content = page.locator(".response-content")
    
    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state("networkidle")
    
    def select_agent(self, agent_name):
        self.page.click(f"text={agent_name}")
    
    def send_query(self, query):
        self.input_field.fill(query)
        self.send_button.click()
    
    def wait_for_response(self):
        self.response_content.wait_for(state="visible")
        return self.response_content.inner_text()
```

## 8. TestAndIssueCollector集成

TestAndIssueCollector模块负责执行端到端视觉自动化测试，并收集和分析测试结果：

```python
# 使用TestAndIssueCollector执行测试
from development_tools.test_and_issue_collector import TestAndIssueCollector

collector = TestAndIssueCollector()

# 收集视觉测试用例
test_cases = collector.collect_visual_test_cases()

# 执行测试
results = collector.run_visual_tests(test_cases)

# 分析问题
issues = collector.analyze_issues(results)

# 生成报告
report = collector.generate_report(results, issues)

# 提交问题（如果有）
if issues:
    collector.submit_issues(issues)
```

## 9. 故障排除

### 9.1 常见问题

1. **测试失败但UI看起来正常**：
   - 检查基准图像是否过时
   - 调整比较阈值
   - 考虑动态内容的影响

2. **测试在本地通过但在CI中失败**：
   - 检查环境差异
   - 确保所有依赖都已安装
   - 增加等待时间或稳定性检查

3. **截图不一致**：
   - 确保视口大小一致
   - 检查字体和渲染差异
   - 考虑使用区域截图而非全页面截图

### 9.2 更新基准图像

当UI有意更改时，需要更新基准图像：

```bash
python test/visual_test/utils/update_baseline.py --test test_homepage_visual
```

## 10. 最佳实践

1. **保持测试独立**：每个测试应该独立运行，不依赖其他测试的状态
2. **使用页面对象模型**：将页面交互逻辑封装在页面对象中
3. **稳定的选择器**：使用稳定的选择器，如data-testid，而非CSS类或XPath
4. **适当的等待**：使用显式等待而非固定延迟
5. **合理的断言**：确保断言能够准确反映测试意图
6. **定期更新基准**：随着UI的有意更改，定期更新基准图像
7. **CI集成**：确保测试在CI环境中自动运行

## 11. 附录

### 11.1 依赖列表

```
playwright==1.35.0
pytest==7.3.1
pytest-playwright==0.3.3
pytest-html==3.2.0
pixelmatch==0.3.0
pillow==9.5.0
```

### 11.2 相关文件

- `development_tools/test_and_issue_collector.py`：测试收集和执行
- `test/visual_test/run_tests.py`：测试入口
- `test/visual_test/config.json`：测试配置
- `.github/workflows/visual-tests.yml`：GitHub Actions配置
