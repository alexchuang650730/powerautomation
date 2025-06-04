# API Key配置文档

## 🔑 **环境变量配置标准**

PowerAutomation项目需要以下API密钥配置：

### 📋 **必需的API密钥**

#### 1️⃣ **Claude API Key**
```bash
export CLAUDE_API_KEY="your_claude_api_key_here"
```
- **用途**: Claude AI模型调用
- **获取方式**: https://console.anthropic.com/

#### 2️⃣ **Gemini API Key**
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```
- **用途**: Google Gemini模型调用
- **获取方式**: https://makersuite.google.com/

#### 3️⃣ **SuperMemory API Key**
```bash
export SUPERMEMORY_API_KEY="your_supermemory_api_key_here"
```
- **用途**: 外部记忆存储和检索
- **获取方式**: SuperMemory服务提供商

#### 4️⃣ **Kilo Code API Key**
```bash
export KILO_API_KEY="your_claude_api_key_here"
```
- **说明**: KILO_API_KEY使用与CLAUDE_API_KEY相同的值
- **自动回退**: 如果KILO_API_KEY未设置，自动使用CLAUDE_API_KEY

#### 5️⃣ **GitHub Token**
```bash
export GITHUB_TOKEN="your_github_token_here"
```
- **用途**: GitHub仓库访问和操作
- **获取方式**: GitHub Settings > Developer settings > Personal access tokens

### 🚀 **快速配置**

#### 方法1: 临时设置（当前会话）
```bash
export CLAUDE_API_KEY="your_claude_api_key"
export GEMINI_API_KEY="your_gemini_api_key"
export SUPERMEMORY_API_KEY="your_supermemory_api_key"
export KILO_API_KEY="$CLAUDE_API_KEY"  # 使用Claude API Key
export GITHUB_TOKEN="your_github_token"
```

#### 方法2: 永久设置（添加到~/.bashrc）
```bash
echo 'export CLAUDE_API_KEY="your_claude_api_key"' >> ~/.bashrc
echo 'export GEMINI_API_KEY="your_gemini_api_key"' >> ~/.bashrc
echo 'export SUPERMEMORY_API_KEY="your_supermemory_api_key"' >> ~/.bashrc
echo 'export KILO_API_KEY="$CLAUDE_API_KEY"' >> ~/.bashrc
echo 'export GITHUB_TOKEN="your_github_token"' >> ~/.bashrc
source ~/.bashrc
```

#### 方法3: 使用.env文件
```bash
# 创建.env文件
cat > .env << EOF
CLAUDE_API_KEY=your_claude_api_key
GEMINI_API_KEY=your_gemini_api_key
SUPERMEMORY_API_KEY=your_supermemory_api_key
KILO_API_KEY=your_claude_api_key
GITHUB_TOKEN=your_github_token
EOF

# 加载环境变量
source .env
```

### 🔍 **配置验证**

使用以下命令验证API密钥配置：

```bash
cd /home/ubuntu/powerautomation
python3 -c "
import os
print('🔑 API Key 配置检查:')
print(f'CLAUDE_API_KEY: {\"✅ 已设置\" if os.getenv(\"CLAUDE_API_KEY\") else \"❌ 未设置\"}')
print(f'GEMINI_API_KEY: {\"✅ 已设置\" if os.getenv(\"GEMINI_API_KEY\") else \"❌ 未设置\"}')
print(f'SUPERMEMORY_API_KEY: {\"✅ 已设置\" if os.getenv(\"SUPERMEMORY_API_KEY\") else \"❌ 未设置\"}')
print(f'KILO_API_KEY: {\"✅ 已设置\" if os.getenv(\"KILO_API_KEY\") else \"❌ 未设置\"}')
print(f'GITHUB_TOKEN: {\"✅ 已设置\" if os.getenv(\"GITHUB_TOKEN\") else \"❌ 未设置\"}')
"
```

### 📊 **API使用说明**

#### 🧠 **AI增强功能**
- **Claude**: 主要的AI分析和生成模型
- **Gemini**: 辅助AI模型，提供多样化的分析视角
- **Kilo**: 代码分析和优化工具（使用Claude API）

#### 💾 **数据存储**
- **SuperMemory**: 长期记忆存储和检索
- **GitHub**: 代码仓库管理和版本控制

#### 🔄 **自动回退机制**
```python
# KILO_API_KEY自动回退逻辑
self.kilo_api_key = os.getenv("KILO_API_KEY") or os.getenv("CLAUDE_API_KEY")
```

### ⚠️ **安全注意事项**

1. **不要在代码中硬编码API密钥**
2. **不要将API密钥提交到版本控制系统**
3. **定期轮换API密钥**
4. **使用最小权限原则配置GitHub Token**
5. **在生产环境中使用密钥管理服务**

### 🛠️ **故障排除**

#### 常见问题：
1. **API密钥未生效**: 重新加载环境变量 `source ~/.bashrc`
2. **权限不足**: 检查GitHub Token权限设置
3. **API配额超限**: 检查各服务的使用配额
4. **网络连接问题**: 确保网络可以访问相关API服务

### 📞 **支持**

如果遇到API配置问题，请：
1. 检查API密钥格式是否正确
2. 验证API服务是否可用
3. 查看日志文件获取详细错误信息
4. 联系相关API服务提供商获取支持

