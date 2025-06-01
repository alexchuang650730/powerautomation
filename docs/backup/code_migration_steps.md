# PowerAutomation 代码重构与迁移步骤

本文档详细说明了PowerAutomation项目的代码重构与迁移步骤，旨在解决当前代码结构中存在的重叠问题，实现智能体能力的集中化管理和前后端职责的清晰分离。

## 重构目标

1. **智能体能力集中化**：将所有智能体能力定义集中到`agents`目录
2. **前后端职责分离**：`frontend`和`backend`目录只保留各自的职责，不包含智能体能力定义
3. **RL能力统一**：合并`rl_factory`和`enhancers/rl_enhancer`中的重复实现

## 迁移步骤

### 1. 智能体能力集中化

#### 1.1 基础智能体类

```bash
# 确认agents/base/base_agent.py已包含完整的基础智能体定义
# 移除backend/agents/base_agent.py中的重复实现
rm backend/agents/base_agent.py

# 在backend/agents/__init__.py中添加导入
echo "from agents.base.base_agent import BaseAgent" > backend/agents/__init__.py
```

#### 1.2 具体智能体实现

```bash
# 对于每个智能体类型，确保agents目录包含完整实现，移除backend中的重复实现

# PPT智能体
rm backend/agents/ppt_agent.py
echo "from agents.ppt.ppt_agent import PPTAgent" >> backend/agents/__init__.py

# Web智能体
rm backend/agents/web_agent.py
echo "from agents.web.web_agent import WebAgent" >> backend/agents/__init__.py

# 代码智能体
rm backend/agents/code_agent.py
echo "from agents.code_agent.code_agent import CodeAgent" >> backend/agents/__init__.py

# 通用智能体
rm backend/agents/general_agent.py
echo "from agents.general.general_agent import GeneralAgent" >> backend/agents/__init__.py
```

#### 1.3 更新后端服务引用

```bash
# 更新backend/services中的智能体引用
sed -i 's/from backend.agents/from agents/g' backend/services/*.py

# 更新backend/routes中的智能体引用
sed -i 's/from backend.agents/from agents/g' backend/routes/*.py
```

### 2. RL能力统一

#### 2.1 合并适配器

```bash
# 创建统一的适配器目录
mkdir -p rl_core/adapters

# 从rl_factory和enhancers/rl_enhancer中复制并合并适配器
cp rl_factory/adapters/*.py rl_core/adapters/
cp enhancers/rl_enhancer/adapters/*.py rl_core/adapters/

# 去除重复实现
# 注意：需要手动检查并合并不同版本的实现差异
```

#### 2.2 合并学习模块

```bash
# 创建统一的学习模块目录
mkdir -p rl_core/learning

# 从rl_factory和enhancers/rl_enhancer中复制并合并学习模块
cp rl_factory/core/learning/*.py rl_core/learning/
cp enhancers/rl_enhancer/core/learning/*.py rl_core/learning/

# 去除重复实现
# 注意：需要手动检查并合并不同版本的实现差异
```

#### 2.3 合并思考模块

```bash
# 创建统一的思考模块目录
mkdir -p rl_core/thought

# 从rl_factory和enhancers/rl_enhancer中复制并合并思考模块
cp rl_factory/core/thought/*.py rl_core/thought/
cp enhancers/rl_enhancer/core/thought/*.py rl_core/thought/

# 去除重复实现
# 注意：需要手动检查并合并不同版本的实现差异
```

#### 2.4 更新导入路径

```bash
# 更新所有文件中的导入路径
find rl_core -type f -name "*.py" -exec sed -i 's/from \.\.core/from rl_core/g' {} \;
find rl_core -type f -name "*.py" -exec sed -i 's/from \.\.\.core/from rl_core/g' {} \;
```

### 3. 前后端职责分离

#### 3.1 清理前端代码

```bash
# 确保前端代码不直接引用智能体实现
find frontend -type f -name "*.js" -o -name "*.ts" -o -name "*.vue" -exec grep -l "import.*from.*agents" {} \; | xargs sed -i 's/import.*from.*agents.*/\/\/ 通过API调用智能体功能，不直接导入/g'
```

#### 3.2 更新后端API

```bash
# 确保后端API正确引用集中化后的智能体
find backend/routes -type f -name "*.py" -exec sed -i 's/from backend.agents/from agents/g' {} \;
```

#### 3.3 添加明确的API接口文档

```bash
# 创建API接口文档目录
mkdir -p docs/api

# 为每个智能体创建API接口文档
touch docs/api/ppt_agent_api.md
touch docs/api/web_agent_api.md
touch docs/api/code_agent_api.md
touch docs/api/general_agent_api.md
```

### 4. 测试与验证

#### 4.1 单元测试更新

```bash
# 更新测试用例中的导入路径
find tests -type f -name "*.py" -exec sed -i 's/from backend.agents/from agents/g' {} \;
find tests -type f -name "*.py" -exec sed -i 's/from rl_factory/from rl_core/g' {} \;
find tests -type f -name "*.py" -exec sed -i 's/from enhancers.rl_enhancer/from rl_core/g' {} \;
```

#### 4.2 运行测试

```bash
# 运行单元测试
python -m pytest tests/unit

# 运行集成测试
python -m pytest tests/integration

# 运行端到端测试
python -m pytest tests/end_to_end

# 运行视觉测试
python -m pytest tests/visual_test
```

### 5. 清理旧目录

```bash
# 在确认所有测试通过后，可以清理旧目录
# 注意：请先备份重要数据

# 备份
mkdir -p backup
cp -r rl_factory backup/
cp -r enhancers backup/

# 清理
rm -rf rl_factory
rm -rf enhancers/rl_enhancer
```

## 目录结构对照表

| 重构前 | 重构后 | 说明 |
|-------|-------|------|
| agents/base/base_agent.py | agents/base/base_agent.py | 保持不变，作为唯一实现 |
| backend/agents/base_agent.py | (移除) | 重复实现，改为导入agents中的类 |
| rl_factory/adapters/* | rl_core/adapters/* | 合并为统一实现 |
| enhancers/rl_enhancer/adapters/* | rl_core/adapters/* | 合并为统一实现 |
| rl_factory/core/learning/* | rl_core/learning/* | 合并为统一实现 |
| enhancers/rl_enhancer/core/learning/* | rl_core/learning/* | 合并为统一实现 |
| rl_factory/core/thought/* | rl_core/thought/* | 合并为统一实现 |
| enhancers/rl_enhancer/core/thought/* | rl_core/thought/* | 合并为统一实现 |

## 注意事项

1. **备份**：在进行任何删除或移动操作前，确保已备份所有代码
2. **增量迁移**：建议按模块逐步迁移，每完成一个模块就进行测试
3. **导入路径**：特别注意更新所有文件中的导入路径
4. **冲突解决**：合并重复实现时，需手动检查并解决可能的冲突
5. **测试覆盖**：确保所有重构的代码都有对应的测试用例

## 后续工作

完成代码重构后，建议进行以下工作：

1. 更新项目文档，反映新的代码结构
2. 创建详细的API文档，说明各模块的接口和用法
3. 更新CI/CD流程，确保自动化测试覆盖所有重构的代码
4. 进行性能测试，确保重构不会带来性能下降
