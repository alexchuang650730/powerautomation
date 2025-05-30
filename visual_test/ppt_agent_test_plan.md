# PPT智能体端到端测试方案 (基于视觉验证与自动化操作)

## 1. 测试目标

验证PPT智能体在接收用户请求、利用MCP模块进行优化、生成PPT演示文稿以及与开发工具（如AgentProblemSolver、TestAndIssueCollector）交互等核心功能的端到端流程。

**重点验证：**

*   **视觉一致性：** 生成的PPT内容、布局、样式（颜色、字体、字号）是否符合预期，与模板或指令是否一致。
*   **自动化操作：** 通过API调用或模拟用户交互触发PPT生成流程，并自动完成结果校验。
*   **功能完整性：** 覆盖PPT生成的基本流程、样式定制、错误处理等场景。
*   **模块集成：** 验证PPT智能体与MCP模块、开发工具模块（日志记录、问题提交）的集成。

## 2. 测试环境

*   **平台版本：** PowerAutomation 增强版 (当前开发版本)
*   **运行环境：** 沙盒环境 (Ubuntu 22.04)
*   **依赖服务：**
    *   PowerAutomation后端服务 (包含PPT智能体API)
    *   PowerAutomation前端服务 (用于UI交互测试)
*   **测试工具：**
    *   `TestAndIssueCollector`: 用于执行测试流程、截图、视觉比对、生成报告、提交问题。
    *   `ThoughtActionRecorder`: 用于记录智能体思考和操作日志。
    *   `AgentProblemSolver`: 用于接收和处理测试中发现的问题。
    *   Python `requests` 库: 用于API调用。
    *   UI自动化工具 (如 Playwright): 用于模拟前端交互。
    *   图像处理库 (如 PIL): 用于截图比对。

## 3. 测试用例设计

**核心原则：** 每个测试用例都强调视觉验证和自动化操作，避免仅依赖脚本输出。

### 用例1：基本PPT生成与视觉验证

*   **ID:** E2E-PPT-001
*   **描述:** 测试PPT智能体生成一个简单主题PPT的基本功能。
*   **输入:** 通过API向PPT智能体发送请求，主题为"人工智能简介"。
*   **自动化步骤:**
    1.  启动PowerAutomation后端服务。
    2.  使用`requests`调用PPT智能体API，发送生成请求。
    3.  轮询检查PPT文件是否在指定目录生成。
    4.  使用`TestAndIssueCollector`：
        *   记录测试开始。
        *   (如果可行) 尝试使用工具打开生成的PPTX文件（或提示需要手动操作）。
        *   针对PPT的**第一页（标题页）**，调用`take_screenshot`，保存为`e2e_ppt_001_title_actual.png`。
        *   针对PPT的**第二页（内容页）**，调用`take_screenshot`，保存为`e2e_ppt_001_content_actual.png`。
        *   (假设有基准图片) 调用`compare_screenshots`将实际截图与预定义的基准截图 (`e2e_ppt_001_title_baseline.png`, `e2e_ppt_001_content_baseline.png`) 进行比较。
        *   记录比较结果。
*   **视觉验证点:**
    *   标题页截图：检查标题是否为"人工智能简介"，布局是否合理，背景、字体是否为默认样式。
    *   内容页截图：检查是否有与AI相关的基本内容（如定义、应用等），排版是否清晰，样式是否一致。
    *   截图比对结果：`diff_percentage`是否在可接受范围内（例如 < 5%）。
*   **预期结果:**
    *   成功生成PPTX文件。
    *   截图比对成功（或视觉检查通过）。
    *   `TestAndIssueCollector`报告测试通过。
    *   `ThoughtActionRecorder`记录了完整的思考和操作流程。
*   **失败处理:**
    *   如果PPT未生成或截图比对失败，`TestAndIssueCollector`记录问题，生成失败报告，并将问题信息（包括截图、日志）提交给`AgentProblemSolver`。

### 用例2：带样式指令的PPT生成与视觉验证

*   **ID:** E2E-PPT-002
*   **描述:** 测试PPT智能体根据特定样式指令生成PPT的功能。
*   **输入:** 通过API请求生成PPT，主题为"云计算优势"，样式指令为"使用蓝色调，商务风格"。
*   **自动化步骤:**
    1.  同用例1，但API请求包含样式指令。
    2.  使用`TestAndIssueCollector`进行截图和比对（基准图片为`e2e_ppt_002_title_baseline.png`, `e2e_ppt_002_content_baseline.png`）。
*   **视觉验证点:**
    *   截图内容：标题为"云计算优势"，内容包含相关优点。
    *   截图样式：整体色调为蓝色，字体、布局体现商务风格。
    *   截图比对结果。
*   **预期结果:**
    *   成功生成PPTX文件。
    *   生成的PPT符合"蓝色调、商务风格"的视觉要求。
    *   截图比对成功（或视觉检查通过）。
    *   测试报告通过。
*   **失败处理:** 同用例1。

### 用例3：错误处理流程验证

*   **ID:** E2E-PPT-003
*   **描述:** 测试PPT智能体在接收到无效输入时的错误处理能力。
*   **输入:** 通过API发送一个无效请求（例如，缺少主题）。
*   **自动化步骤:**
    1.  启动后端服务。
    2.  发送无效API请求。
    3.  检查API的响应状态码和返回内容。
    4.  使用`TestAndIssueCollector`记录测试过程。
    5.  检查`ThoughtActionRecorder`的日志，确认是否记录了错误处理的思考过程。
*   **视觉验证点:** (主要为日志和API响应验证，非界面视觉)
    *   API响应是否包含明确的错误信息或要求补充信息的提示。
    *   日志中是否记录了识别到无效输入的思考步骤。
*   **预期结果:**
    *   API返回表示请求失败或需要更多信息的响应 (e.g., 4xx status code)。
    *   API响应体包含错误说明。
    *   日志记录了错误处理过程。
    *   未生成PPT文件。
    *   `TestAndIssueCollector`报告测试符合预期（验证了错误处理）。
*   **失败处理:**
    *   如果API未返回错误或日志未记录，`TestAndIssueCollector`记录问题，生成失败报告，提交给`AgentProblemSolver`。

### 用例4：思维导图生成与PPT转换端到端验证

*   **ID:** E2E-PPT-004
*   **描述:** 测试思维导图生成功能及其转换为PPT的完整流程，包括前端界面交互和后端处理。
*   **输入:** 通过前端界面创建思维导图，主题为"数字化转型策略"。
*   **自动化步骤:**
    1.  启动PowerAutomation前端和后端服务。
    2.  使用Playwright自动化工具打开浏览器并访问平台首页。
    3.  导航到思维导图创建界面（例如，点击"创建思维导图"按钮）。
    4.  使用`TestAndIssueCollector`：
        *   记录测试开始。
        *   调用`take_screenshot`，保存为`e2e_ppt_004_mindmap_ui_actual.png`。
        *   通过Playwright在思维导图编辑器中：
            *   输入中心主题"数字化转型策略"。
            *   添加主要分支"技术升级"、"流程优化"、"人才培养"、"文化变革"。
            *   为每个主要分支添加2-3个子节点。
        *   调用`take_screenshot`，保存为`e2e_ppt_004_mindmap_created_actual.png`。
        *   点击"生成PPT"按钮。
        *   等待PPT生成完成。
        *   调用`take_screenshot`，保存为`e2e_ppt_004_generation_progress_actual.png`。
        *   下载生成的PPT文件。
        *   打开PPT文件并截取关键页面：
            *   调用`take_screenshot`，保存为`e2e_ppt_004_ppt_title_actual.png`。
            *   调用`take_screenshot`，保存为`e2e_ppt_004_ppt_mindmap_actual.png`。
            *   调用`take_screenshot`，保存为`e2e_ppt_004_ppt_content_actual.png`。
        *   调用`compare_screenshots`将实际截图与预定义的基准截图进行比较。
        *   记录比较结果。
*   **视觉验证点:**
    *   思维导图UI截图：检查思维导图编辑器界面是否正确加载，工具栏和功能按钮是否可见。
    *   创建的思维导图截图：检查思维导图是否正确显示所有节点和连接，布局是否合理。
    *   生成进度截图：检查进度指示器是否正确显示PPT生成过程。
    *   PPT标题页截图：检查标题是否为"数字化转型策略"，布局是否合理。
    *   PPT思维导图页截图：检查是否包含完整的思维导图可视化，与原始思维导图是否一致。
    *   PPT内容页截图：检查是否根据思维导图节点生成了相应的内容页，内容是否完整，排版是否清晰。
    *   截图比对结果：各截图的`diff_percentage`是否在可接受范围内（例如 < 5%）。
*   **预期结果:**
    *   思维导图编辑器正确加载和显示。
    *   成功创建思维导图并保存。
    *   成功将思维导图转换为PPT。
    *   生成的PPT包含思维导图的完整内容，并按照思维导图结构组织。
    *   PPT中包含思维导图的可视化表示。
    *   截图比对成功（或视觉检查通过）。
    *   `TestAndIssueCollector`报告测试通过。
    *   `ThoughtActionRecorder`记录了完整的思考和操作流程。
*   **失败处理:**
    *   如果思维导图编辑器未正确加载、思维导图创建失败、PPT生成失败或截图比对失败，`TestAndIssueCollector`记录问题，生成失败报告，并将问题信息（包括截图、日志）提交给`AgentProblemSolver`。

### 用例5：思维导图导入与编辑功能验证

*   **ID:** E2E-PPT-005
*   **描述:** 测试思维导图导入、编辑功能及其与PPT生成的集成。
*   **输入:** 一个预先准备的思维导图文件（JSON或其他支持的格式），主题为"项目管理最佳实践"。
*   **自动化步骤:**
    1.  启动PowerAutomation前端和后端服务。
    2.  使用Playwright自动化工具打开浏览器并访问平台首页。
    3.  导航到思维导图导入界面。
    4.  使用`TestAndIssueCollector`：
        *   记录测试开始。
        *   调用`take_screenshot`，保存为`e2e_ppt_005_import_ui_actual.png`。
        *   通过Playwright上传预先准备的思维导图文件。
        *   等待思维导图加载完成。
        *   调用`take_screenshot`，保存为`e2e_ppt_005_imported_mindmap_actual.png`。
        *   在思维导图编辑器中：
            *   修改一个现有节点的文本。
            *   添加一个新的分支"风险管理"。
            *   为新分支添加2-3个子节点。
        *   调用`take_screenshot`，保存为`e2e_ppt_005_edited_mindmap_actual.png`。
        *   点击"生成PPT"按钮。
        *   等待PPT生成完成。
        *   下载生成的PPT文件。
        *   打开PPT文件并截取关键页面：
            *   调用`take_screenshot`，保存为`e2e_ppt_005_ppt_title_actual.png`。
            *   调用`take_screenshot`，保存为`e2e_ppt_005_ppt_mindmap_actual.png`。
            *   调用`take_screenshot`，保存为`e2e_ppt_005_ppt_new_content_actual.png`。
        *   调用`compare_screenshots`将实际截图与预定义的基准截图进行比较。
        *   记录比较结果。
*   **视觉验证点:**
    *   导入界面截图：检查导入界面是否正确显示，上传控件是否可用。
    *   导入的思维导图截图：检查导入的思维导图是否正确显示所有节点和连接。
    *   编辑后的思维导图截图：检查修改和新增的节点是否正确显示，布局是否合理。
    *   PPT标题页截图：检查标题是否为"项目管理最佳实践"，布局是否合理。
    *   PPT思维导图页截图：检查是否包含完整的思维导图可视化，与编辑后的思维导图是否一致。
    *   PPT新内容页截图：检查是否包含新增的"风险管理"分支内容，内容是否完整，排版是否清晰。
    *   截图比对结果：各截图的`diff_percentage`是否在可接受范围内（例如 < 5%）。
*   **预期结果:**
    *   思维导图成功导入并正确显示。
    *   成功编辑思维导图并保存更改。
    *   成功将编辑后的思维导图转换为PPT。
    *   生成的PPT包含编辑后思维导图的完整内容，包括修改和新增的节点。
    *   PPT中包含思维导图的可视化表示，与编辑后的思维导图一致。
    *   截图比对成功（或视觉检查通过）。
    *   `TestAndIssueCollector`报告测试通过。
*   **失败处理:**
    *   如果思维导图导入失败、编辑功能不可用、PPT生成失败或截图比对失败，`TestAndIssueCollector`记录问题，生成失败报告，并将问题信息（包括截图、日志）提交给`AgentProblemSolver`。

## 4. 测试执行与报告

1.  **执行:**
    *   创建一个主测试脚本（例如 `run_ppt_e2e_tests.py`）。
    *   该脚本依次执行上述测试用例。
    *   脚本负责启动/停止依赖服务，调用API，并驱动`TestAndIssueCollector`完成测试步骤（截图、比对、记录）。
2.  **报告:**
    *   每个用例执行后，`TestAndIssueCollector`记录结果。
    *   所有用例执行完毕后，`TestAndIssueCollector`调用`generate_test_report`生成最终的Markdown格式测试报告。
    *   报告应包含每个用例的执行状态、关键截图（或差异图）、比对结果、日志摘要。
3.  **问题处理:**
    *   测试脚本检查每个用例的`TestAndIssueCollector`返回结果。
    *   如果检测到失败（如截图比对失败、API错误未按预期处理），则调用`TestAndIssueCollector.collect_issues`收集详细信息，并通过`TestAndIssueCollector.submit_issues_to_problem_solver`将问题提交给`AgentProblemSolver`。

## 5. 基准图片管理

*   为需要进行视觉比对的测试用例准备基准截图（Baseline Screenshots）。
*   首次运行测试或UI/模板更新后，需要生成或更新基准图片。
*   基准图片应存储在版本控制中，与测试代码一起管理。

## 6. 文档维护

*   本测试方案文档 (`ppt_agent_test_plan.md`) 应随代码一同维护。
*   当PPT智能体功能、API或依赖发生变化时，及时更新测试方案和测试用例。
