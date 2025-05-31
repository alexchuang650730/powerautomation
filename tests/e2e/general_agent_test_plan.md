# 通用智能体端到端测试方案 (基于视觉验证与自动化操作)

## 1. 测试目标

验证通用智能体作为平台总控的核心功能，包括多智能体调度、UI交互、MCP模块协调以及与开发工具集成等端到端流程。

**重点验证：**

* **视觉一致性：** UI界面、交互流程、结果展示等视觉元素是否符合预期。
* **自动化操作：** 通过API调用或模拟用户交互触发通用智能体的各项功能，并自动完成结果校验。
* **功能完整性：** 覆盖智能体调度、任务分配、结果整合、错误处理等场景。
* **模块集成：** 验证通用智能体与PPT智能体、代码智能体、六大MCP模块以及开发工具模块的集成。
* **多场景协同：** 验证在复杂任务下多智能体和多模块的协同工作能力。
* **动态能力适配：** 验证通用智能体能否根据get_capabilities()方法动态适应UI和功能需求。

## 2. 测试环境

* **平台版本：** PowerAutomation 增强版 (当前开发版本)
* **运行环境：** 沙盒环境 (Ubuntu 22.04)
* **依赖服务：**
  * PowerAutomation后端服务 (包含通用智能体API)
  * PowerAutomation前端服务 (用于UI交互测试)
  * 其他智能体服务 (用于测试调度功能)
* **测试工具：**
  * `TestAndIssueCollector`: 用于执行测试流程、截图、视觉比对、生成报告、提交问题。
  * `ThoughtActionRecorder`: 用于记录智能体思考和操作日志。
  * `AgentProblemSolver`: 用于接收和处理测试中发现的问题。
  * Python `requests` 库: 用于API调用。
  * UI自动化工具 (如 Playwright): 用于模拟前端交互。
  * 图像处理库 (如 PIL): 用于截图比对。

## 3. 测试用例设计

**核心原则：** 每个测试用例都强调视觉验证和自动化操作，避免仅依赖脚本输出。

### 用例1：UI界面加载与交互验证

* **ID:** E2E-GENERAL-001
* **描述:** 测试通用智能体的UI界面加载和基本交互功能。
* **输入:** 通过浏览器访问PowerAutomation前端界面。
* **自动化步骤:**
  1. 启动PowerAutomation前端和后端服务。
  2. 使用Playwright自动化工具打开浏览器并访问平台首页。
  3. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_general_001_homepage_actual.png`。
     * 通过Playwright点击"创建新任务"按钮。
     * 调用`take_screenshot`，保存为`e2e_general_001_newtask_actual.png`。
     * 通过Playwright在任务输入框中输入"创建一个简单的网站"。
     * 点击提交按钮。
     * 等待响应，调用`take_screenshot`，保存为`e2e_general_001_response_actual.png`。
     * 调用`compare_screenshots`将实际截图与预定义的基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 首页截图：检查UI元素是否正确加载，布局是否符合设计。
  * 新任务页截图：检查任务创建界面是否正确显示。
  * 响应截图：检查系统是否正确响应并显示适当的反馈。
  * 截图比对结果：`diff_percentage`是否在可接受范围内（例如 < 5%）。
* **预期结果:**
  * UI界面正确加载和显示。
  * 交互功能（点击按钮、输入文本、提交表单）正常工作。
  * 系统正确响应用户输入。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:**
  * 如果UI未正确加载、交互失败或截图比对失败，`TestAndIssueCollector`记录问题，生成失败报告，并将问题信息（包括截图、日志）提交给`AgentProblemSolver`。

### 用例2：智能体调度功能验证

* **ID:** E2E-GENERAL-002
* **描述:** 测试通用智能体调度其他智能体的能力。
* **输入:** 通过API或UI提交一个需要多智能体协作的任务（例如，"创建一个关于人工智能的演示文稿，并附带一个演示用的Python脚本"）。
* **自动化步骤:**
  1. 启动所有必要的服务（通用智能体、PPT智能体、代码智能体）。
  2. 使用Playwright访问平台并提交任务，或使用`requests`调用API提交任务。
  3. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_general_002_task_submission_actual.png`。
     * 等待任务处理（可能需要轮询状态）。
     * 调用`take_screenshot`，保存为`e2e_general_002_processing_actual.png`。
     * 等待任务完成。
     * 调用`take_screenshot`，保存为`e2e_general_002_results_actual.png`。
     * 检查是否生成了PPT文件和Python脚本。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 任务提交截图：检查任务是否正确提交。
  * 处理中截图：检查是否显示适当的处理状态和进度。
  * 结果截图：检查是否显示完整的任务结果，包括PPT和Python脚本的链接或预览。
  * 截图比对结果。
* **预期结果:**
  * 任务成功提交并被通用智能体接收。
  * 通用智能体正确调度PPT智能体和代码智能体。
  * 成功生成PPT文件和Python脚本。
  * UI正确显示任务状态和结果。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

### 用例3：MCP模块集成验证 - 项目记忆优化

* **ID:** E2E-GENERAL-003
* **描述:** 测试通用智能体与项目记忆优化MCP模块的集成。
* **输入:** 通过API或UI提交一个后续任务，该任务依赖于之前任务的上下文（例如，"基于之前的AI演示文稿，添加一个关于机器学习的新章节"）。
* **自动化步骤:**
  1. 确保用例2已成功执行，并且系统中存在之前的任务记录。
  2. 使用Playwright或`requests`提交后续任务。
  3. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_general_003_context_task_actual.png`。
     * 等待任务处理和完成。
     * 调用`take_screenshot`，保存为`e2e_general_003_context_results_actual.png`。
     * 检查更新后的PPT文件是否包含新章节，且与原有内容风格一致。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 任务提交截图：检查任务是否正确提交，系统是否识别出上下文关联。
  * 结果截图：检查是否显示更新后的任务结果，新内容是否与原有内容保持一致性。
  * 截图比对结果。
* **预期结果:**
  * 系统正确识别任务与之前任务的关联。
  * 通用智能体成功调用项目记忆优化MCP模块。
  * 更新后的PPT包含新章节，且与原有内容风格一致。
  * UI正确显示任务状态和结果。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

### 用例4：错误处理与恢复流程验证

* **ID:** E2E-GENERAL-004
* **描述:** 测试通用智能体在遇到子任务失败时的错误处理和恢复能力。
* **输入:** 通过API或UI提交一个会导致子任务失败的任务（例如，要求生成一个包含无效参数的代码）。
* **自动化步骤:**
  1. 启动所有必要的服务。
  2. 使用Playwright或`requests`提交包含无效参数的任务。
  3. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_general_004_error_task_actual.png`。
     * 等待系统处理并检测到错误。
     * 调用`take_screenshot`，保存为`e2e_general_004_error_detected_actual.png`。
     * 观察系统是否自动调用`AgentProblemSolver`处理错误。
     * 调用`take_screenshot`，保存为`e2e_general_004_error_handling_actual.png`。
     * 检查系统是否提供了有关错误的反馈和可能的解决方案。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 任务提交截图：检查任务是否正确提交。
  * 错误检测截图：检查系统是否正确识别并显示错误。
  * 错误处理截图：检查系统是否显示错误处理过程和结果。
  * 截图比对结果。
* **预期结果:**
  * 系统正确识别子任务失败。
  * 通用智能体自动调用`AgentProblemSolver`处理错误。
  * UI显示适当的错误信息和处理状态。
  * 系统提供有关错误的反馈和可能的解决方案。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过（验证了错误处理功能）。
* **失败处理:** 同用例1。

### 用例5：多MCP模块协同工作验证

* **ID:** E2E-GENERAL-005
* **描述:** 测试通用智能体协调多个MCP模块共同工作的能力。
* **输入:** 通过API或UI提交一个复杂任务，需要多个MCP模块协同工作（例如，"创建一个企业级数据分析应用，包括前端界面设计和后端代码"）。
* **自动化步骤:**
  1. 启动所有必要的服务。
  2. 使用Playwright或`requests`提交复杂任务。
  3. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_general_005_complex_task_actual.png`。
     * 等待任务处理（可能需要较长时间）。
     * 定期调用`take_screenshot`，记录处理过程中的状态更新。
     * 等待任务完成。
     * 调用`take_screenshot`，保存为`e2e_general_005_complex_results_actual.png`。
     * 检查生成的前端界面设计和后端代码。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * 任务提交截图：检查复杂任务是否正确提交。
  * 处理过程截图：检查系统是否显示多个MCP模块的协同工作状态。
  * 结果截图：检查是否显示完整的任务结果，包括前端设计和后端代码。
  * 截图比对结果。
* **预期结果:**
  * 通用智能体成功协调多个MCP模块共同工作。
  * 系统生成符合要求的前端界面设计和后端代码。
  * UI正确显示任务状态和结果。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

### 用例6：动态能力适配验证

* **ID:** E2E-GENERAL-006
* **描述:** 测试通用智能体的动态能力适配机制，验证前端是否能根据智能体声明的能力动态调整UI。
* **输入:** 通过API获取通用智能体的能力列表，然后通过UI访问相应功能。
* **自动化步骤:**
  1. 启动所有必要的服务。
  2. 使用`requests`调用API获取通用智能体的能力列表。
  3. 使用Playwright访问平台首页。
  4. 使用`TestAndIssueCollector`：
     * 记录测试开始。
     * 调用`take_screenshot`，保存为`e2e_general_006_capabilities_api_actual.png`。
     * 使用Playwright导航到通用智能体功能页面。
     * 调用`take_screenshot`，保存为`e2e_general_006_ui_capabilities_actual.png`。
     * 检查UI是否显示了与API返回的能力列表相匹配的功能选项。
     * 尝试使用其中一个功能（例如，"创建项目"）。
     * 调用`take_screenshot`，保存为`e2e_general_006_capability_usage_actual.png`。
     * 调用`compare_screenshots`将实际截图与基准截图进行比较。
     * 记录比较结果。
* **视觉验证点:**
  * API能力列表截图：记录API返回的能力列表。
  * UI能力显示截图：检查UI是否正确显示了与API返回的能力列表相匹配的功能选项。
  * 能力使用截图：检查选定的功能是否正确执行。
  * 截图比对结果。
* **预期结果:**
  * API成功返回通用智能体的能力列表。
  * UI正确显示与API返回的能力列表相匹配的功能选项。
  * 选定的功能正确执行。
  * 截图比对成功（或视觉检查通过）。
  * `TestAndIssueCollector`报告测试通过。
* **失败处理:** 同用例1。

## 4. 测试执行与报告

1. **执行:**
   * 创建一个主测试脚本（例如 `run_general_e2e_tests.py`）。
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

* 本测试方案文档 (`general_agent_test_plan.md`) 应随代码一同维护。
* 当通用智能体功能、API、UI或依赖发生变化时，及时更新测试方案和测试用例。
