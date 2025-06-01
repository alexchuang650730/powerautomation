# AciDev 集成指南

## 概述

AciDev 是 PowerAutomation 系统中的外部工具适配器，提供高级代码开发和测试能力。它作为开发工具链的重要组成部分，与 TestAndIssueCollector 和 MCPBrainstorm 协同工作，为系统提供自动化测试、问题分析和解决方案生成等功能。本文档详细介绍了 AciDev 的功能、接口和集成方法，帮助开发者快速上手并有效利用这一组件。

## 功能特点

AciDev 适配器提供以下核心功能：

1. **自动化测试方案生成**：根据代码和需求自动生成测试方案
2. **问题分析与诊断**：分析测试失败原因并提供诊断信息
3. **解决方案生成**：为发现的问题自动生成解决方案
4. **代码质量评估**：评估代码质量并提供改进建议

## 安装与配置

AciDev 适配器已集成到 PowerAutomation 系统的开发工具链中，主要通过 TestAndIssueCollector 调用。确保系统依赖已正确安装：

```bash
cd /path/to/powerautomation_integration
pip install -r requirements.txt
```

## 使用方法

### 通过 TestAndIssueCollector 使用

AciDev 主要通过 TestAndIssueCollector 间接使用，作为其测试方案生成和问题分析的后端工具：

```python
from development_tools.test_and_issue_collector import TestAndIssueCollector

# 初始化测试收集器
collector = TestAndIssueCollector()

# 收集测试用例
test_cases = collector.collect_test_cases()

# 生成测试计划（内部会尝试使用 AciDev）
test_plan = collector.generate_test_plan(test_cases)

# 执行测试计划
test_results = collector.execute_test_plan(test_plan)

# 生成测试报告
test_report = collector.generate_test_report(test_results)
```

### 直接使用 AciDev 适配器

如果需要直接使用 AciDev 适配器，可以按照以下方式导入和使用：

```python
import sys
import os

# 添加适配器路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcptool', 'adapters'))
import acidev_adapter as acidev

# 初始化 AciDev 适配器
adapter = acidev.AciDevAdapter()

# 生成测试方案
test_plan = adapter.generate_test_plan(test_cases)

# 分析问题
issue_analysis = adapter.analyze_issue(issue_data)

# 生成解决方案
solution = adapter.generate_solution(issue_data, issue_analysis)
```

### 与六大特性集成

AciDev 可以与 PowerAutomation 系统的六大特性无缝集成，特别是在思维特性和特性定义方面提供支持：

```python
from agents.features import CodeAgentFeatures
import acidev_adapter as acidev

# 初始化代码智能体特性
agent_features = CodeAgentFeatures()

# 初始化 AciDev 适配器
adapter = acidev.AciDevAdapter()

# 使用 AciDev 分析代码并增强思维特性
code_analysis = adapter.analyze_code("path/to/code.py")
agent_features.update_thinking_feature({
    "code_analysis": code_analysis,
    "reasoning": "基于代码分析，我们可以发现...",
    "conclusions": code_analysis.get("conclusions", [])
})

# 使用 AciDev 评估特性定义
feature_evaluation = adapter.evaluate_features(agent_features.get_all_features())
for feature_name, evaluation in feature_evaluation.items():
    if evaluation["score"] < 0.7:  # 如果评分低于0.7
        # 生成改进建议
        improvement = adapter.generate_feature_improvement(feature_name, evaluation)
        # 更新特性
        agent_features.update_feature(feature_name, improvement["content"])
```

## 与 TestAndIssueCollector 集成流程

AciDev 在 TestAndIssueCollector 中的集成流程如下：

1. TestAndIssueCollector 初始化时尝试导入 AciDev 适配器
2. 如果导入成功，设置 `ACIDEV_AVAILABLE = True`
3. 在生成测试计划时，按照优先级依次尝试使用 mcp.so、AciDev 和 MCPBrainstorm
4. 如果 AciDev 可用且 mcp.so 不可用，则使用 AciDev 生成测试计划

```python
# TestAndIssueCollector 中的集成代码示例
def generate_test_plan(self, test_cases):
    # 优先使用 mcp.so
    if MCP_SO_AVAILABLE:
        return self._use_mcp_so_for_test_plan(test_cases)
    
    # 其次使用 AciDev
    elif ACIDEV_AVAILABLE:
        return self._use_acidev_for_test_plan(test_cases)
    
    # 最后使用 MCPBrainstorm
    elif MCP_BRAINSTORM_AVAILABLE:
        return self._use_mcpbrainstorm_for_test_plan(test_cases)
    
    # 如果都不可用，使用内置方法
    else:
        return self._generate_fallback_test_plan(test_cases)
```

## API 参考

### AciDevAdapter 类

#### 初始化

```python
AciDevAdapter()
```

初始化 AciDev 适配器。

#### 生成测试方案

```python
generate_test_plan(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]
```

生成测试方案。

**参数**：
- `test_cases`：测试用例列表

**返回值**：
- 测试方案

#### 分析问题

```python
analyze_issue(issue_data: Dict[str, Any]) -> Dict[str, Any]
```

分析问题。

**参数**：
- `issue_data`：问题数据

**返回值**：
- 问题分析结果

#### 生成解决方案

```python
generate_solution(issue_data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]
```

生成解决方案。

**参数**：
- `issue_data`：问题数据
- `analysis`：问题分析结果

**返回值**：
- 解决方案

#### 分析代码

```python
analyze_code(code_path: str) -> Dict[str, Any]
```

分析代码。

**参数**：
- `code_path`：代码文件路径

**返回值**：
- 代码分析结果

#### 评估特性

```python
evaluate_features(features: Dict[str, Any]) -> Dict[str, Dict[str, Any]]
```

评估特性。

**参数**：
- `features`：特性字典

**返回值**：
- 特性评估结果

#### 生成特性改进

```python
generate_feature_improvement(feature_name: str, evaluation: Dict[str, Any]) -> Dict[str, Any]
```

生成特性改进建议。

**参数**：
- `feature_name`：特性名称
- `evaluation`：特性评估结果

**返回值**：
- 特性改进建议

## 与主工作流集成

AciDev 在 PowerAutomation 系统的主工作流中主要通过 TestAndIssueCollector 集成，为自动化测试和问题解决提供支持：

1. **测试方案生成阶段**：
   - TestAndIssueCollector 收集测试用例
   - 调用 AciDev 生成测试方案
   - 执行测试方案并收集结果

2. **问题分析阶段**：
   - 测试失败时收集问题信息
   - 调用 AciDev 分析问题原因
   - 生成问题分析报告

3. **解决方案生成阶段**：
   - 基于问题分析结果
   - 调用 AciDev 生成解决方案
   - 提供解决步骤和建议

### 集成示例

```python
# 主工作流中的集成示例
from development_tools.test_and_issue_collector import TestAndIssueCollector
from development_tools.agent_problem_solver import AgentProblemSolver

# 初始化组件
collector = TestAndIssueCollector()
problem_solver = AgentProblemSolver()

# 1. 测试方案生成阶段
test_cases = collector.collect_test_cases()
test_plan = collector.generate_test_plan(test_cases)  # 可能使用 AciDev
test_results = collector.execute_test_plan(test_plan)

# 2. 问题分析阶段
if test_results["overall_status"] == "failed":
    # 收集失败的测试
    failed_tests = [
        result for group in test_results["groups_results"] 
        for result in group["test_results"] 
        if result["status"] == "failed"
    ]
    
    # 3. 解决方案生成阶段
    for failed_test in failed_tests:
        # 使用问题解决器处理问题
        solution = problem_solver.solve_problem(failed_test)
        
        if solution["auto_fixable"]:
            # 自动修复问题
            problem_solver.apply_solution(solution)
        else:
            # 记录需要手动处理的问题
            problem_solver.record_manual_issue(solution)
```

## 与 AgentProblemSolver 协同工作

AciDev 可以与 AgentProblemSolver 协同工作，提供自动回滚和问题提交能力：

```python
from development_tools.agent_problem_solver import AgentProblemSolver
import acidev_adapter as acidev

# 初始化组件
problem_solver = AgentProblemSolver()
adapter = acidev.AciDevAdapter()

# 创建保存点
save_point = problem_solver.create_save_point("before_feature_update")

try:
    # 使用 AciDev 评估特性
    features = {...}  # 特性字典
    evaluation = adapter.evaluate_features(features)
    
    # 如果评估结果不理想，可能会引发异常
    if any(e["score"] < 0.5 for e in evaluation.values()):
        raise ValueError("Feature evaluation failed")
    
    # 应用特性更新
    # ...
    
except Exception as e:
    # 发生错误，回滚到保存点
    problem_solver.rollback_to_save_point(save_point)
    
    # 分析问题
    issue_data = {
        "error": str(e),
        "features": features,
        "evaluation": evaluation
    }
    analysis = adapter.analyze_issue(issue_data)
    
    # 生成解决方案
    solution = adapter.generate_solution(issue_data, analysis)
    
    # 提交问题
    problem_solver.submit_issue(issue_data, analysis, solution)
```

## 最佳实践

1. **错误处理**：始终检查 AciDev 是否可用，并处理可能的错误
2. **集成优先级**：在 TestAndIssueCollector 中遵循 mcp.so > AciDev > MCPBrainstorm 的优先级
3. **问题分析**：充分利用 AciDev 的问题分析能力，提高问题解决效率
4. **特性评估**：定期使用 AciDev 评估六大特性，确保特性定义的质量

## 常见问题

### AciDev 适配器导入失败

如果 AciDev 适配器导入失败，可能是因为：

1. 适配器文件不存在或路径错误
2. 依赖库缺失
3. 权限问题

检查适配器文件是否存在，并确保所有依赖已正确安装。

### 测试方案生成失败

如果测试方案生成失败，可能是因为：

1. 测试用例格式不正确
2. AciDev 内部错误
3. 资源限制

检查测试用例格式是否正确，并查看日志获取详细错误信息。

## 与 Qwen3-8B 模型集成

AciDev 与 Qwen3-8B 中文版大模型集成，提供强大的自然语言理解和生成能力：

```python
import acidev_adapter as acidev

# 初始化 AciDev 适配器
adapter = acidev.AciDevAdapter(model_path="Qwen3-8B")

# 使用 Qwen3-8B 模型分析问题
issue_data = {...}  # 问题数据
analysis = adapter.analyze_issue_with_model(issue_data)

# 使用 Qwen3-8B 模型生成解决方案
solution = adapter.generate_solution_with_model(issue_data, analysis)

print(f"问题分析: {analysis}")
print(f"解决方案: {solution}")
```

## 结论

AciDev 适配器为 PowerAutomation 系统提供了强大的自动化测试和问题解决能力，是开发工具链中的重要组成部分。通过与 TestAndIssueCollector 和 AgentProblemSolver 的协同工作，它能够有效提高系统的测试效率和问题解决能力，为开发者提供更智能、更高效的开发体验。
