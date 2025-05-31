# PowerAutomation 部署与测试指南

本文档提供了PowerAutomation系统的完整部署指南和测试方法，包括环境配置、安装步骤、visual_test测试方案和GitHub Actions自动化测试配置。

## 目录

1. [环境要求](#环境要求)
2. [安装部署](#安装部署)
3. [Visual Test测试方案](#visual-test测试方案)
4. [GitHub Actions自动化测试](#github-actions自动化测试)
5. [常见问题排查](#常见问题排查)

## 环境要求

### 硬件要求

- CPU: 4核或更高
- 内存: 至少8GB RAM
- 存储: 至少20GB可用空间

### 软件要求

- 操作系统: Ubuntu 20.04 LTS或更高版本
- Python: 3.8或更高版本
- Node.js: 14.x或更高版本
- Docker: 20.10或更高版本(可选，用于容器化部署)

### 依赖库

- PyTorch: 1.10或更高版本
- Transformers: 4.15或更高版本
- Flask: 2.0或更高版本
- pytest: 6.2或更高版本
- Pillow: 8.3或更高版本

## 安装部署

### 方法一：直接安装

1. **克隆代码仓库**

```bash
git clone https://github.com/alexchuang650730/powerautomation.git
cd powerautomation
```

2. **创建并激活虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **安装PyTorch**

根据您的CUDA版本选择合适的PyTorch版本：

```bash
# CPU版本
pip install torch torchvision torchaudio

# CUDA版本(例如CUDA 11.6)
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
```

5. **初始化数据库**

```bash
# 创建数据目录（如果不存在）
mkdir -p data

# 初始化SQLite数据库
python scripts/init_db.py

# 初始化完成后，数据库文件将位于data/powerautomation.db
```

> **注意**：初始化脚本将创建必要的表结构并插入基础数据，包括默认的智能体配置和测试用户。

6. **启动服务**

```bash
# 启动后端服务
python backend/app.py

# 在另一个终端启动前端服务
cd frontend
npm install
npm run serve
```

7. **验证安装**

访问 http://localhost:8080 确认前端界面正常加载。

### 方法二：Docker部署

1. **构建Docker镜像**

```bash
docker build -t powerautomation:latest .
```

2. **运行容器**

```bash
docker run -d -p 8080:8080 -p 5000:5000 --name powerautomation powerautomation:latest
```

3. **验证安装**

访问 http://localhost:8080 确认前端界面正常加载。

## Visual Test测试方案

Visual Test是一种基于视觉比对的测试方法，用于验证PowerAutomation系统的UI和架构图是否符合预期。

### 运行Visual Test

1. **确保已安装测试依赖**

```bash
pip install pytest pytest-html pillow opencv-python
```

2. **运行测试**

```bash
cd powerautomation
python -m pytest tests/visual_test/test_visual_verification.py -v
```

3. **查看测试报告**

测试完成后，会在`test_reports`目录下生成HTML格式的测试报告：

```bash
firefox test_reports/visual_test_report.html  # 或使用其他浏览器
```

### 自定义Visual Test

您可以通过修改`tests/visual_test/test_visual_verification.py`文件来自定义测试用例：

```python
def test_custom_diagram():
    """测试自定义架构图"""
    # 指定参考图像和测试图像路径
    reference_image = "docs/images/reference_diagram.png"
    test_image = "docs/images/current_diagram.png"
    
    # 设置相似度阈值(0-1之间，1表示完全相同)
    threshold = 0.95
    
    # 执行测试
    assert compare_images(reference_image, test_image) >= threshold
```

### 更新参考图像

如果系统架构有意进行了更改，您需要更新参考图像：

```bash
cp docs/images/powerautomation_refactored_architecture.png tests/visual_test/reference_images/architecture_reference.png
```

## GitHub Actions自动化测试

PowerAutomation使用GitHub Actions进行持续集成和自动化测试，确保代码质量和功能稳定性。

### 配置GitHub Actions

项目已包含预配置的GitHub Actions工作流程文件，位于`.github/workflows/`目录下：

- `unit_tests.yml`: 单元测试
- `integration_tests.yml`: 集成测试
- `visual_tests.yml`: 视觉测试
- `deploy.yml`: 部署流程

### 查看测试结果

1. 在GitHub仓库页面，点击"Actions"标签
2. 选择要查看的工作流程
3. 点击具体的运行实例查看详细结果

### 自定义GitHub Actions工作流程

您可以根据需要自定义工作流程。以下是一个示例，用于添加性能测试：

1. 创建文件`.github/workflows/performance_tests.yml`：

```yaml
name: Performance Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-benchmark
    - name: Run performance tests
      run: |
        python -m pytest tests/performance/ --benchmark-json=benchmark.json
    - name: Upload benchmark results
      uses: actions/upload-artifact@v2
      with:
        name: benchmark-results
        path: benchmark.json
```

2. 创建性能测试文件`tests/performance/test_performance.py`：

```python
def test_agent_response_time(benchmark):
    """测试智能体响应时间"""
    from agents.general.general_agent import GeneralAgent
    
    agent = GeneralAgent()
    
    # 使用benchmark装饰器测量函数性能
    result = benchmark(agent.process_query, "计算1+1等于几")
    
    assert result is not None
```

### 触发GitHub Actions

GitHub Actions可以通过以下方式触发：

- 推送代码到指定分支
- 创建Pull Request
- 手动触发(在Actions页面点击"Run workflow")
- 定时触发(使用cron表达式)

## 常见问题排查

### 安装问题

**问题**: 安装PyTorch时出错
**解决方案**: 访问[PyTorch官网](https://pytorch.org/get-started/locally/)获取适合您系统的安装命令

**问题**: 找不到CUDA
**解决方案**: 确认CUDA已正确安装，并设置环境变量`CUDA_HOME`和`PATH`

### 运行问题

**问题**: 服务启动失败
**解决方案**: 检查日志文件`logs/app.log`，确认错误原因

**问题**: 前端无法连接后端
**解决方案**: 确认后端服务正在运行，并检查`frontend/.env`中的API地址配置

### 测试问题

**问题**: Visual Test失败
**解决方案**: 比较当前图像和参考图像的差异，确认是否需要更新参考图像

**问题**: GitHub Actions测试失败
**解决方案**: 查看失败日志，本地复现问题并修复

## 附录

### 有用的命令

```bash
# 检查服务状态
systemctl status powerautomation

# 查看日志
tail -f logs/app.log

# 重启服务
systemctl restart powerautomation

# 清理缓存
python scripts/clean_cache.py
```

### 配置文件

- `config/app_config.json`: 应用程序配置
- `config/logging_config.json`: 日志配置
- `config/model_config.json`: 模型配置

### 联系支持

如果您遇到无法解决的问题，请联系技术支持：

- 邮件: support@powerautomation.com
- 问题追踪: https://github.com/alexchuang650730/powerautomation/issues
