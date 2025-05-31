# 端到端视觉自动化操作测试方案

本文档详细描述了PowerAutomation MCP集成后的端到端视觉自动化测试方案，确保Sequential Thinking MCP和Playwright MCP（含WebAgentB增强）能够在主仓库结构下正常工作。

## 1. 测试目标

- 验证Sequential Thinking MCP的任务拆解和反思能力
- 验证Playwright MCP的网页自动化和信息收集能力
- 验证WebAgentB的语义理解和交互能力
- 验证增强版MCP规划器的功能完整性
- 验证增强版MCP头脑风暴器的功能完整性
- 验证主动问题解决器的功能完整性

## 2. 测试环境

- **操作系统**：Ubuntu 22.04 LTS
- **Python版本**：3.8+
- **浏览器**：Chrome 最新版
- **依赖库**：见requirements.txt

## 3. 测试用例

### 3.1 Sequential Thinking MCP测试

#### TC-ST-001: 任务拆解能力测试

**步骤**：
1. 初始化Sequential Thinking适配器
2. 提供复杂任务描述："设计一个智能家居系统，包括设备控制、场景管理和用户界面"
3. 调用decompose_task方法
4. 验证返回的任务分解结构

**预期结果**：
- 任务被分解为多个子任务
- 子任务包含明确的步骤和依赖关系
- 生成的todo.md格式正确

#### TC-ST-002: 反思与调整能力测试

**步骤**：
1. 初始化Sequential Thinking适配器
2. 提供任务执行结果和反馈
3. 调用reflect_and_adjust方法
4. 验证调整后的任务计划

**预期结果**：
- 根据反馈调整任务计划
- 识别并修正问题点
- 更新todo.md反映新的计划

### 3.2 Playwright MCP测试

#### TC-PW-001: 网页访问与信息提取测试

**步骤**：
1. 初始化Playwright适配器
2. 访问测试网页（如https://example.com）
3. 提取页面内容
4. 验证提取的内容

**预期结果**：
- 成功访问网页
- 正确提取页面标题、正文和链接
- 返回结构化的页面内容

#### TC-PW-002: 交互操作测试

**步骤**：
1. 初始化Playwright适配器
2. 访问测试表单页面
3. 填写表单并提交
4. 验证操作结果

**预期结果**：
- 成功填写表单字段
- 成功点击提交按钮
- 验证提交后的响应页面

### 3.3 WebAgentB测试

#### TC-WA-001: 语义搜索测试

**步骤**：
1. 初始化WebAgentB适配器
2. 执行语义搜索："人工智能最新进展"
3. 验证搜索结果

**预期结果**：
- 返回相关搜索结果
- 结果包含语义分析
- 结果按相关性排序

#### TC-WA-002: 网页内容语义理解测试

**步骤**：
1. 初始化WebAgentB适配器
2. 访问技术文档页面
3. 执行semantic_extract方法
4. 验证提取的结构化内容

**预期结果**：
- 成功提取关键概念
- 识别主要观点和论据
- 生成内容摘要

### 3.4 增强版MCP规划器测试

#### TC-EP-001: 集成规划能力测试

**步骤**：
1. 初始化增强版MCP规划器
2. 提供规划任务："开发一个在线教育平台"
3. 执行plan方法
4. 验证规划结果

**预期结果**：
- 生成详细的项目规划
- 规划包含任务分解和时间线
- 规划考虑到资源和依赖关系

#### TC-EP-002: 动态调整能力测试

**步骤**：
1. 初始化增强版MCP规划器
2. 提供初始规划任务
3. 提供执行反馈和变更需求
4. 调用adjust_plan方法
5. 验证调整后的规划

**预期结果**：
- 根据反馈调整规划
- 保持规划的一致性和完整性
- 适应变更需求

### 3.5 增强版MCP头脑风暴器测试

#### TC-EB-001: 创意生成能力测试

**步骤**：
1. 初始化增强版MCP头脑风暴器
2. 提供创意主题："智能家居创新应用"
3. 执行generate方法
4. 验证生成的创意

**预期结果**：
- 生成多个相关创意
- 创意具有创新性和可行性
- 创意包含实现建议

#### TC-EB-002: 创意验证能力测试

**步骤**：
1. 初始化增强版MCP头脑风暴器
2. 提供创意列表
3. 执行validate_ideas方法
4. 验证验证结果

**预期结果**：
- 对每个创意进行可行性评估
- 识别潜在问题和限制
- 提供改进建议

### 3.6 主动问题解决器测试

#### TC-PS-001: 问题发现能力测试

**步骤**：
1. 初始化主动问题解决器
2. 提供测试仓库路径
3. 执行solve_on_event方法，事件类型为"manual_check"
4. 验证发现的问题

**预期结果**：
- 成功分析系统信息
- 识别潜在问题
- 问题描述清晰且有严重程度分类

#### TC-PS-002: 解决方案生成与实现测试

**步骤**：
1. 初始化主动问题解决器
2. 提供预定义的问题列表
3. 执行_generate_solutions和_implement_solutions方法
4. 验证生成和实现的解决方案

**预期结果**：
- 为每个问题生成解决方案
- 解决方案包含具体实现步骤
- 成功实现解决方案（修改相关文件）

## 4. 视觉验证

### 4.1 视觉比较方法

使用以下方法进行视觉验证：

```python
def compare_images(expected_image_path, actual_image_path, threshold=0.95):
    """
    比较两个图像的相似度
    
    Args:
        expected_image_path: 预期图像路径
        actual_image_path: 实际图像路径
        threshold: 相似度阈值，默认0.95
        
    Returns:
        bool: 是否通过视觉验证
    """
    import cv2
    import numpy as np
    
    # 读取图像
    expected_img = cv2.imread(expected_image_path)
    actual_img = cv2.imread(actual_image_path)
    
    # 调整大小
    if expected_img.shape != actual_img.shape:
        actual_img = cv2.resize(actual_img, (expected_img.shape[1], expected_img.shape[0]))
    
    # 计算相似度
    similarity = cv2.matchTemplate(actual_img, expected_img, cv2.TM_CCOEFF_NORMED)[0][0]
    
    return similarity >= threshold
```

### 4.2 视觉验证用例

#### VC-001: Playwright页面操作视觉验证

**步骤**：
1. 使用Playwright适配器访问测试页面
2. 执行一系列操作（点击、填写表单等）
3. 在关键步骤截图
4. 与预期截图进行比较

**预期结果**：
- 所有截图与预期截图相似度高于阈值
- 操作流程视觉上符合预期

#### VC-002: WebAgentB结果展示视觉验证

**步骤**：
1. 使用WebAgentB适配器执行语义搜索
2. 将结果可视化展示
3. 截取结果展示页面
4. 与预期展示效果比较

**预期结果**：
- 结果展示格式符合预期
- 视觉元素排布正确
- 关键信息清晰可见

## 5. 测试数据

测试数据位于`tests/fixtures`目录：

- `sample_tasks.json`: 任务示例
- `sample_problems.json`: 问题示例
- `sample_solutions.json`: 解决方案示例

## 6. 测试执行

### 6.1 自动化测试执行

```bash
# 运行所有测试
pytest tests/e2e/

# 运行特定模块测试
pytest tests/e2e/test_sequential_thinking.py
pytest tests/e2e/test_playwright_adapter.py
pytest tests/e2e/test_webagent_adapter.py
pytest tests/e2e/test_enhanced_planner.py
pytest tests/e2e/test_enhanced_brainstorm.py
pytest tests/e2e/test_problem_solver.py
```

### 6.2 视觉验证执行

```bash
# 运行视觉验证测试
pytest tests/e2e/test_visual_verification.py
```

### 6.3 生成测试报告

```bash
# 生成HTML测试报告
pytest tests/e2e/ --html=report.html
```

## 7. 测试结果分析

测试结果将包含以下内容：

- 测试通过率
- 失败测试详情
- 视觉验证结果
- 性能指标（执行时间等）

## 8. 持续集成

测试方案已集成到GitHub Actions工作流中，每次提交都会自动执行测试并生成报告。

## 9. 故障排除

常见问题及解决方案：

- **Playwright浏览器启动失败**：检查Chrome安装和驱动版本
- **WebAgentB API调用失败**：检查网络连接和API密钥
- **视觉验证失败**：检查屏幕分辨率和浏览器窗口大小

## 10. 附录

### 10.1 测试环境设置

```bash
# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chrome

# 设置环境变量
export PYTHONPATH=$PYTHONPATH:/path/to/powerautomation
```

### 10.2 测试辅助函数

详见`tests/e2e/test_utils.py`文件。
