# 网页智能体端到端测试方案 (基于视觉验证与自动化操作)

## 1. 测试目标

验证网页智能体在网页抓取、内容分析、数据提取、自动化操作以及与开发工具（如AgentProblemSolver、TestAndIssueCollector）交互等核心功能的端到端流程。

**重点验证：**

* **视觉一致性：** 网页抓取结果、数据提取展示、操作界面等视觉元素是否符合预期。
* **自动化操作：** 通过API调用或模拟用户交互触发网页智能体的各项功能，并自动完成结果校验。
* **功能完整性：** 覆盖网页抓取、内容分析、数据提取、表单填写、自动化点击等场景。
* **模块集成：** 验证网页智能体与六大MCP模块、开发工具模块的集成。

## 2. 测试环境

* **平台版本：** PowerAutomation 增强版 (当前开发版本)
* **运行环境：** 沙盒环境 (Ubuntu 22.04)
* **依赖服务：**
  * PowerAutomation后端服务 (包含网页智能体API)
  * 浏览器自动化环境 (如Playwright、Selenium)
  * PowerAutomation前端服务 (用于UI交互测试)
* **测试工具：**
  * `TestAndIssueCollector`: 用于执行测试流程、截图、视觉比对、生成报告、提交问题。
  * `ThoughtActionRecorder`: 用于记录智能体思考和操作日志。
  * `AgentProblemSolver`: 用于接收和处理测试中发现的问题。
  * Python `requests` 库: 用于API调用。
  * UI自动化工具 (如 Playwright): 用于模拟前端交互。
  * 图像处理库 (如 PIL): 用于截图比对。

## 3. 测试用例设计

**核心原则：** 每个测试用例都强调视觉验证和自动化操作，避免仅依赖脚本输出。

### 用例1：基本网页抓取与内容分析验证

* **ID:** E2E-WEB-001
* **描述:** 测试网页智能体抓取指定网页并分析内容的基本功能。
* **输入:** 通过前端界面或API向网页智能体发送请求，要求抓取并分析特定网页（例如，"https://example.com"）。
* **自动化步骤:**
  1. 启动PowerAutomation前端和后端服务。
  2. 使用Playwright打开浏览器并访问平台首页。
  3. 导航到网页智能体界面。
  4. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_web_001_ui_actual.png`。
     * 通过Playwright在输入框中输入目标URL "https://example.com"。
     * 点击"抓取分析"按钮。
     * 等待抓取和分析完成。
     * 调用`take_screenshot`，保存为`e2e_web_001_processing_actual.png`。
     * 等待结果显示。
     * 调用`take_screenshot`，保存为`e2e_web_001_results_actual.png`。
     * 调用`compare_screenshots`将实际截图与预定义的基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * UI截图：检查网页智能体界面是否正确加载，输入框和按钮是否可见。
  * 处理中截图：检查是否显示适当的处理状态和进度。
  * 结果截图：检查抓取结果是否正确显示，包括网页标题、主要内容、链接等。
  * 截图比对结果：`diff_percentage`是否在可接受范围内（例如 < 5%）。
* **预期结果:**
  * 网页智能体界面正确加载和显示。
  * 成功抓取目标网页并分析内容。
  * 结果页面正确显示抓取的内容和分析结果。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
  * `ThoughtActionRecorder`记录了完整的思考和操作流程。
* **失败处理:**
  * 如果界面未正确加载、抓取失败或截图比对失败，`TestAndIssueCollector`记录问题，生成失败报告，并将问题信息（包括截图、日志）提交给`AgentProblemSolver`。

### 用例2：数据提取与结构化输出验证

* **ID:** E2E-WEB-002
* **描述:** 测试网页智能体从网页中提取特定数据并生成结构化输出的能力。
* **输入:** 通过前端界面或API向网页智能体发送请求，要求从特定网页（例如，一个产品列表页面）提取产品信息。
* **自动化步骤:**
  1. 启动PowerAutomation前端和后端服务。
  2. 使用Playwright打开浏览器并访问平台首页。
  3. 导航到网页智能体界面。
  4. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 通过Playwright在输入框中输入目标URL（例如，"https://example.com/products"）。
     * 在提取指令框中输入"提取所有产品的名称、价格和评分"。
     * 点击"数据提取"按钮。
     * 等待提取完成。
     * 调用`take_screenshot`，保存为`e2e_web_002_extraction_actual.png`。
     * 检查生成的结构化数据（如JSON或表格）。
     * 调用`take_screenshot`，保存为`e2e_web_002_structured_data_actual.png`。
     * 点击"导出数据"按钮（如果有）。
     * 检查导出的文件。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 提取过程截图：检查提取过程是否正确显示，包括进度指示。
  * 结构化数据截图：检查提取的数据是否正确显示为结构化格式（如表格或JSON视图）。
  * 截图比对结果。
* **预期结果:**
  * 成功从目标网页提取指定的产品信息。
  * 提取的数据正确显示为结构化格式。
  * 数据导出功能正常工作。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

### 用例3：网页自动化操作验证

* **ID:** E2E-WEB-003
* **描述:** 测试网页智能体执行自动化网页操作（如表单填写、点击按钮）的能力。
* **输入:** 通过前端界面或API向网页智能体发送请求，要求在特定网页上执行一系列操作。
* **自动化步骤:**
  1. 启动PowerAutomation前端和后端服务。
  2. 使用Playwright打开浏览器并访问平台首页。
  3. 导航到网页智能体界面。
  4. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 通过Playwright在输入框中输入目标URL（例如，"https://example.com/contact"）。
     * 在操作指令框中输入"填写联系表单并提交"。
     * 点击"执行操作"按钮。
     * 等待网页智能体加载目标网页。
     * 调用`take_screenshot`，保存为`e2e_web_003_page_loaded_actual.png`。
     * 观察网页智能体自动填写表单的过程。
     * 调用`take_screenshot`，保存为`e2e_web_003_form_filling_actual.png`。
     * 观察网页智能体点击提交按钮的操作。
     * 等待操作完成和结果显示。
     * 调用`take_screenshot`，保存为`e2e_web_003_submission_result_actual.png`。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 页面加载截图：检查目标网页是否正确加载。
  * 表单填写截图：检查网页智能体是否正确识别并填写表单字段。
  * 提交结果截图：检查表单提交后的结果页面或确认消息。
  * 截图比对结果。
* **预期结果:**
  * 成功加载目标网页。
  * 正确识别并填写表单字段。
  * 成功提交表单并显示确认页面或消息。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

### 用例4：多页面导航与数据聚合验证

* **ID:** E2E-WEB-004
* **描述:** 测试网页智能体在多个页面间导航并聚合数据的能力。
* **输入:** 通过前端界面或API向网页智能体发送请求，要求从多个相关页面收集并聚合信息。
* **自动化步骤:**
  1. 启动PowerAutomation前端和后端服务。
  2. 使用Playwright打开浏览器并访问平台首页。
  3. 导航到网页智能体界面。
  4. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 通过Playwright在输入框中输入起始URL（例如，"https://example.com/blog"）。
     * 在指令框中输入"收集最新5篇博客文章的标题、发布日期和摘要"。
     * 点击"执行任务"按钮。
     * 观察网页智能体浏览博客列表页面。
     * 调用`take_screenshot`，保存为`e2e_web_004_blog_list_actual.png`。
     * 观察网页智能体点击文章链接并导航到详情页面的过程。
     * 调用`take_screenshot`，保存为`e2e_web_004_article_page_actual.png`。
     * 等待所有文章数据收集完成。
     * 调用`take_screenshot`，保存为`e2e_web_004_aggregated_data_actual.png`。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 博客列表截图：检查网页智能体是否正确加载博客列表页面。
  * 文章页面截图：检查网页智能体是否正确导航到文章详情页面。
  * 聚合数据截图：检查收集的数据是否正确聚合和显示。
  * 截图比对结果。
* **预期结果:**
  * 成功加载博客列表页面。
  * 正确导航到多个文章详情页面。
  * 成功收集并聚合所有文章的相关信息。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

### 用例5：MCP模块集成验证 - 上下文匹配优化

* **ID:** E2E-WEB-005
* **描述:** 测试网页智能体与上下文匹配优化MCP模块的集成。
* **输入:** 通过前端界面或API向网页智能体发送一个需要上下文理解的任务（例如，"在这个网站上找到与我上次搜索相关的产品"）。
* **自动化步骤:**
  1. 启动PowerAutomation前端和后端服务。
  2. 使用Playwright打开浏览器并访问平台首页。
  3. 导航到网页智能体界面。
  4. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 通过Playwright模拟一个先前的搜索会话（例如，搜索"智能手机"）。
     * 调用`take_screenshot`，保存为`e2e_web_005_previous_search_actual.png`。
     * 在新的任务输入框中输入"找到与我上次搜索相关的配件"。
     * 点击"执行任务"按钮。
     * 观察网页智能体如何理解上下文并执行任务。
     * 调用`take_screenshot`，保存为`e2e_web_005_context_understanding_actual.png`。
     * 等待任务完成和结果显示。
     * 调用`take_screenshot`，保存为`e2e_web_005_related_results_actual.png`。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 先前搜索截图：记录先前的搜索上下文。
  * 上下文理解截图：检查网页智能体是否正确理解并处理上下文相关的任务。
  * 相关结果截图：检查是否找到与先前搜索（智能手机）相关的配件。
  * 截图比对结果。
* **预期结果:**
  * 成功记录并理解先前的搜索上下文。
  * 正确执行上下文相关的任务。
  * 找到与先前搜索相关的产品或信息。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

## 4. 测试执行与报告

1. **执行:**
   * 创建一个主测试脚本（例如 `run_web_e2e_tests.py`）。
   * 该脚本依次执行上述测试用例。
   * 脚本负责启动/停止依赖服务，调用API或驱动UI自动化工具，并驱动`TestAndIssueCollector`完成测试步骤（截图、比对、记录）。
2. **报告:**
   * 每个用例执行后，`TestAndIssueCollector`记录结果。
   * 所有用例执行完毕后，`TestAndIssueCollector`调用`generate_test_report`生成最终的Markdown格式测试报告。
   * 报告应包含每个用例的执行状态、关键截图（或差异图）、比对结果、日志摘要。
3. **问题处理:**
   * 测试脚本检查每个用例的`TestAndIssueCollector`返回结果。
   * 如果检测到失败（如截图比对失败、API错误未按预期处理），则调用`TestAndIssueCollector.collect_issues`收集详细信息，并通过`TestAndIssueCollector.submit_issues_to_problem_solver`将问题提交给`AgentProblemSolver`。

## 5. 基准图片管理

* 为需要进行视觉比对的测试用例准备基准截图（Baseline Screenshots）。
* 首次运行测试或UI更新后，需要生成或更新基准图片。
* 基准图片应存储在版本控制中，与测试代码一起管理。

## 6. 文档维护

* 本测试方案文档 (`web_agent_test_plan.md`) 应随代码一同维护。
* 当网页智能体功能、API、UI或依赖发生变化时，及时更新测试方案和测试用例。
