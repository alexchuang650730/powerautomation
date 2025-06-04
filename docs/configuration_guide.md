# PowerAutomation 工作流引擎配置指南

## 📋 概述

PowerAutomation工作流引擎提供了强大的自动化工作流创建和管理功能，支持智能节点配置、API切换和错误处理机制。本文档详细介绍了如何配置和使用这些功能。

## 🔧 工作流引擎配置

### 基本配置

工作流引擎支持多种复杂度级别的工作流创建：

#### 工作流复杂度级别

1. **低复杂度 (low)**
   - 适用场景：简单的线性任务
   - 默认节点：开始 → 执行 → 结束
   - 节点数量：3个
   - 连接数量：2个

2. **中等复杂度 (medium)**
   - 适用场景：需要准备阶段的任务
   - 默认节点：开始 → 准备 → 执行 → 结束
   - 节点数量：4个
   - 连接数量：3个

3. **高复杂度 (high)**
   - 适用场景：复杂的多阶段任务
   - 默认节点：开始 → 分析 → 处理 → 验证 → 结束
   - 节点数量：5个
   - 连接数量：4个

#### 自动化级别

1. **标准自动化 (standard)**
   - 基本的工作流执行
   - 不包含监控节点

2. **高级自动化 (advanced)**
   - 包含监控节点
   - 自动添加监控连接
   - 实时状态跟踪

### 工作流配置示例

```python
# 简单工作流配置
simple_config = {
    "workflow_name": "简单测试工作流",
    "complexity": "low",
    "automation_level": "standard",
    "metadata": {
        "description": "用于测试的简单工作流",
        "estimated_duration": 300,  # 秒
        "dependencies": []
    }
}

# 复杂工作流配置
complex_config = {
    "workflow_name": "企业级部署工作流",
    "complexity": "high",
    "automation_level": "advanced",
    "metadata": {
        "description": "企业级应用部署工作流",
        "estimated_duration": 1800,  # 30分钟
        "dependencies": ["docker", "kubernetes", "monitoring"]
    },
    "input_data": {
        "application_name": "my-app",
        "environment": "production",
        "replicas": 3
    }
}
```

## 🔄 API切换配置

### API配置文件

API配置存储在 `api_config.json` 文件中，支持以下配置：

```json
{
  "mode": "mock",
  "apis": {
    "claude": {
      "enabled": true,
      "mode": "mock",
      "api_key": null,
      "endpoint": "https://api.anthropic.com/v1/messages",
      "model": "claude-3-sonnet-20240229"
    },
    "gemini": {
      "enabled": true,
      "mode": "mock",
      "api_key": null,
      "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
      "model": "gemini-pro"
    },
    "openai": {
      "enabled": false,
      "mode": "mock",
      "api_key": null,
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "model": "gpt-4"
    }
  },
  "fallback": {
    "enabled": true,
    "fallback_to_mock": true
  },
  "monitoring": {
    "enabled": true,
    "log_api_calls": true,
    "track_usage": true
  }
}
```

### API模式

1. **模拟模式 (mock)**
   - 使用内置的模拟响应
   - 不需要真实API密钥
   - 适用于开发和测试

2. **真实模式 (real)**
   - 调用真实的API服务
   - 需要有效的API密钥
   - 适用于生产环境

3. **混合模式 (hybrid)**
   - 部分API使用真实模式
   - 部分API使用模拟模式
   - 灵活的配置选项

### 环境变量支持

系统支持通过环境变量设置API密钥：

```bash
# Claude API密钥
export CLAUDE_API_KEY="your_claude_api_key"

# Gemini API密钥
export GEMINI_API_KEY="your_gemini_api_key"

# OpenAI API密钥
export OPENAI_API_KEY="your_openai_api_key"
```

### API切换示例

```python
from mcptool.adapters.api_config_manager import (
    switch_to_mock_mode, 
    switch_to_real_mode,
    get_api_config_manager
)

# 切换到模拟模式
switch_to_mock_mode()

# 切换到真实模式
switch_to_real_mode()

# 设置特定API的密钥
config_manager = get_api_config_manager()
config_manager.set_api_key("claude", "your_api_key")
```



## ⚠️ 错误处理和故障排除

### 常见错误类型

#### 1. 工作流创建错误

**错误**: `'IntelligentWorkflowEngineMCP' object has no attribute '_add_default_nodes'`

**原因**: _add_default_nodes方法未正确定义在IntelligentWorkflowEngineMCP类中

**解决方案**: 
- 确保_add_default_nodes方法在正确的类中定义
- 检查方法的缩进和类归属
- 重新启动应用程序

**预防措施**:
```python
# 验证方法是否存在
engine = IntelligentWorkflowEngineMCP("/path/to/project")
if hasattr(engine, '_add_default_nodes'):
    print("✅ _add_default_nodes方法可用")
else:
    print("❌ _add_default_nodes方法不可用")
```

#### 2. API调用错误

**错误**: `API配置不存在: api_name`

**原因**: 尝试调用未配置的API

**解决方案**:
- 检查API名称是否正确
- 确认API在配置文件中已定义
- 验证API是否已启用

**错误**: `API不可用: api_name`

**原因**: API被禁用或缺少必要配置

**解决方案**:
```python
# 检查API可用性
config_manager = get_api_config_manager()
if config_manager.is_api_available("claude"):
    print("✅ Claude API可用")
else:
    print("❌ Claude API不可用")
    # 启用API
    config_manager.config["apis"]["claude"]["enabled"] = True
```

#### 3. 配置文件错误

**错误**: JSON配置文件格式错误

**原因**: 配置文件语法不正确

**解决方案**:
- 验证JSON格式
- 检查括号和引号匹配
- 使用JSON验证工具

**错误**: 配置文件权限错误

**原因**: 无法读取或写入配置文件

**解决方案**:
```bash
# 检查文件权限
ls -la api_config.json

# 修改权限
chmod 644 api_config.json
```

### 错误处理机制

#### 1. 自动回退机制

当真实API调用失败时，系统会自动回退到模拟模式：

```python
# 启用回退机制
config_manager = get_api_config_manager()
config_manager.enable_fallback_mode()

# 禁用回退机制
config_manager.disable_fallback_mode()
```

#### 2. 错误日志记录

系统会自动记录所有错误和API调用：

```python
import logging

# 配置日志级别
logging.basicConfig(level=logging.INFO)

# 查看API调用历史
call_manager = get_api_call_manager()
history = call_manager.get_call_history(10)
for record in history:
    if record['status'] == 'error':
        print(f"错误: {record['error']}")
```

#### 3. 健康检查

定期检查系统状态：

```python
def health_check():
    """系统健康检查"""
    config_manager = get_api_config_manager()
    status = config_manager.get_status()
    
    issues = []
    
    # 检查API可用性
    for api_name, api_status in status['apis'].items():
        if api_status['enabled'] and not api_status['available']:
            issues.append(f"API不可用: {api_name}")
    
    # 检查配置文件
    if not os.path.exists(status['config_file']):
        issues.append(f"配置文件不存在: {status['config_file']}")
    
    return {
        "healthy": len(issues) == 0,
        "issues": issues,
        "status": status
    }
```

### 性能优化建议

#### 1. API调用优化

- 使用连接池减少连接开销
- 实现请求缓存机制
- 设置合理的超时时间

```python
# 配置API调用超时
api_config = {
    "timeout": 30,  # 30秒超时
    "retry_count": 3,  # 重试3次
    "retry_delay": 1  # 重试间隔1秒
}
```

#### 2. 工作流优化

- 合理设置工作流复杂度
- 避免创建过多的监控连接
- 定期清理历史数据

```python
# 清理API调用历史
call_manager = get_api_call_manager()
call_manager.clear_call_history()
```

#### 3. 内存管理

- 定期清理工作流节点
- 限制并发工作流数量
- 监控内存使用情况

### 监控和调试

#### 1. 启用详细日志

```python
import logging

# 设置详细日志
logging.getLogger('mcptool.adapters').setLevel(logging.DEBUG)
```

#### 2. API调用监控

```python
# 启用API调用监控
config_manager = get_api_config_manager()
config_manager.config["monitoring"]["enabled"] = True
config_manager.config["monitoring"]["log_api_calls"] = True
config_manager.config["monitoring"]["track_usage"] = True
```

#### 3. 性能指标

```python
def get_performance_metrics():
    """获取性能指标"""
    call_manager = get_api_call_manager()
    history = call_manager.get_call_history(100)
    
    total_calls = len(history)
    successful_calls = len([r for r in history if r['status'] == 'success'])
    failed_calls = len([r for r in history if r['status'] == 'error'])
    fallback_calls = len([r for r in history if r['status'] == 'fallback_success'])
    
    return {
        "total_calls": total_calls,
        "success_rate": successful_calls / total_calls if total_calls > 0 else 0,
        "failure_rate": failed_calls / total_calls if total_calls > 0 else 0,
        "fallback_rate": fallback_calls / total_calls if total_calls > 0 else 0
    }
```

## 🔧 高级配置

### 自定义节点类型

可以扩展工作流引擎支持自定义节点类型：

```python
# 自定义节点配置
custom_node = {
    "id": "custom_analysis",
    "type": "custom_analysis",
    "name": "自定义分析",
    "description": "执行自定义分析逻辑",
    "data": {
        "analysis_type": "sentiment",
        "parameters": {
            "language": "zh-CN",
            "confidence_threshold": 0.8
        }
    }
}
```

### 工作流模板

创建可重用的工作流模板：

```python
# 数据处理工作流模板
data_processing_template = {
    "workflow_name": "数据处理模板",
    "complexity": "medium",
    "automation_level": "advanced",
    "template": True,
    "nodes": [
        {"id": "data_ingestion", "type": "ingestion", "name": "数据摄取"},
        {"id": "data_validation", "type": "validation", "name": "数据验证"},
        {"id": "data_transformation", "type": "transformation", "name": "数据转换"},
        {"id": "data_output", "type": "output", "name": "数据输出"}
    ],
    "connections": [
        {"from": "data_ingestion", "to": "data_validation", "type": "success"},
        {"from": "data_validation", "to": "data_transformation", "type": "success"},
        {"from": "data_transformation", "to": "data_output", "type": "success"}
    ]
}
```

### 集成外部系统

配置与外部系统的集成：

```python
# 外部系统配置
external_systems = {
    "database": {
        "type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "database": "powerautomation",
        "username": "admin",
        "password": "password"
    },
    "message_queue": {
        "type": "rabbitmq",
        "host": "localhost",
        "port": 5672,
        "virtual_host": "/",
        "username": "guest",
        "password": "guest"
    },
    "monitoring": {
        "type": "prometheus",
        "endpoint": "http://localhost:9090",
        "metrics_path": "/metrics"
    }
}
```

## 📚 最佳实践

### 1. 配置管理

- 使用版本控制管理配置文件
- 为不同环境创建不同的配置
- 定期备份配置文件

### 2. 安全考虑

- 不要在代码中硬编码API密钥
- 使用环境变量或密钥管理服务
- 定期轮换API密钥

### 3. 测试策略

- 在开发环境使用模拟模式
- 在测试环境使用混合模式
- 在生产环境使用真实模式

### 4. 监控和维护

- 设置API调用限制和监控
- 定期检查系统健康状态
- 建立错误告警机制

## 🆘 技术支持

如果遇到问题，请按以下步骤进行故障排除：

1. **检查日志文件** - 查看详细的错误信息
2. **验证配置** - 确认所有配置项正确
3. **测试连接** - 验证API和外部系统连接
4. **查看文档** - 参考本配置指南
5. **联系支持** - 如果问题仍然存在，请联系技术支持

### 常用命令

```bash
# 检查系统状态
python -c "from mcptool.adapters.api_config_manager import get_api_config_manager; print(get_api_config_manager().get_status())"

# 测试工作流创建
python test_workflow_fix.py

# 测试API切换
python test_api_switching.py

# 查看日志
tail -f powerautomation.log
```

---

*本文档最后更新时间: 2025年6月4日*

