# RL-Factory: Manus思考能力迁移框架

RL-Factory是一个专为PowerAutomation设计的强化学习框架，旨在将Manus的思考和方案设计能力迁移到code agent、MCP planner和MCP brainstorm等组件中，显著提升它们的性能。

## 核心功能

- **思考过程结构化表示**：将Manus的思考链和推理步骤转化为可学习的结构化表示
- **混合学习架构**：结合监督学习、强化学习和对比学习的混合架构
- **多层次奖励机制**：包含局部奖励、全局奖励和延迟奖励的多维度评估体系
- **无限上下文支持**：通过无限上下文适配器处理大规模上下文数据
- **MCP.so集成**：通过MCP.so适配器与现有MCP工具无缝集成
- **GitHub Actions集成**：与Release Manager协同，实现自动化CI/CD流程

## 系统架构

RL-Factory采用模块化设计，主要包含以下组件：

### 核心模块

- **思考过程模块**：包含思考过程的结构化表示、序列化和分解等功能
- **学习模块**：包含监督学习、强化学习、对比学习和混合学习等算法
- **适配器模块**：包含无限上下文适配器、MCP.so适配器和GitHub Actions适配器等

### 集成点

- **与MCP Planner集成**：提升规划能力和工具使用效率
- **与MCP Brainstorm集成**：增强创意生成和方案设计能力
- **与Code Agent集成**：提高代码生成质量和问题解决能力

## 安装与使用

### 依赖项

```bash
pip install -r requirements.txt
```

### 基本用法

```python
from rl_factory.core.thought.decomposer import ThoughtDecomposer
from rl_factory.core.learning.hybrid import HybridLearner

# 分解思考过程
decomposer = ThoughtDecomposer()
thought_process = decomposer.decompose_raw_thought(raw_thought)

# 创建混合学习器
learner = HybridLearner()

# 预测质量
quality = learner.predict_quality(thought_process)

# 改进思考
improved_thought = learner.improve_thought(raw_thought)
```

## 端到端测试

RL-Factory提供了全面的端到端测试，包括后端功能测试和前端视觉自动化测试：

```bash
# 运行后端集成测试
python -m pytest rl_factory/tests/end_to_end/test_rl_factory_integration.py

# 运行前端视觉自动化测试
python -m pytest rl_factory/tests/frontend/test_code_agent_frontend.py
```

## 与PowerAutomation集成

RL-Factory已与PowerAutomation系统深度集成，通过以下方式提升系统能力：

1. **增强MCP规划器**：通过思考能力迁移，提升规划器的问题分析和方案设计能力
2. **增强MCP头脑风暴器**：通过学习Manus的创意生成模式，提升方案多样性和创新性
3. **增强Code Agent**：通过学习Manus的代码设计思路，提升代码质量和可维护性

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议。请遵循以下步骤：

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件
