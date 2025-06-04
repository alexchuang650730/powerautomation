#!/usr/bin/env python3
"""
测试API切换功能
验证模拟API和真实API的无缝切换
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from mcptool.adapters.api_config_manager import (
    APIConfigManager, APICallManager, APIMode,
    get_api_config_manager, get_api_call_manager,
    switch_to_mock_mode, switch_to_real_mode, switch_to_hybrid_mode
)

def test_api_config_manager():
    """测试API配置管理器"""
    print("🔧 测试API配置管理器")
    print("=" * 50)
    
    # 获取配置管理器
    config_manager = get_api_config_manager()
    
    # 测试1: 获取初始状态
    print("\n📋 测试1: 获取初始状态")
    status = config_manager.get_status()
    print(f"✅ 当前模式: {status['current_mode']}")
    print(f"   - 配置文件: {status['config_file']}")
    print(f"   - 回退模式: {status['fallback_enabled']}")
    print(f"   - 监控模式: {status['monitoring_enabled']}")
    
    for api_name, api_status in status['apis'].items():
        print(f"   - {api_name}: 启用={api_status['enabled']}, 模式={api_status['mode']}, 可用={api_status['available']}")
    
    # 测试2: 切换API模式
    print("\n📋 测试2: 切换API模式")
    
    # 切换到真实模式
    print("   切换到真实模式...")
    switch_to_real_mode()
    status = config_manager.get_status()
    print(f"   ✅ 当前模式: {status['current_mode']}")
    
    # 切换到混合模式
    print("   切换到混合模式...")
    switch_to_hybrid_mode()
    status = config_manager.get_status()
    print(f"   ✅ 当前模式: {status['current_mode']}")
    
    # 切换回模拟模式
    print("   切换回模拟模式...")
    switch_to_mock_mode()
    status = config_manager.get_status()
    print(f"   ✅ 当前模式: {status['current_mode']}")
    
    # 测试3: 设置API密钥
    print("\n📋 测试3: 设置API密钥")
    config_manager.set_api_key("claude", "test_claude_key_123")
    config_manager.set_api_key("gemini", "test_gemini_key_456")
    
    claude_config = config_manager.get_api_config("claude")
    gemini_config = config_manager.get_api_config("gemini")
    
    print(f"   ✅ Claude配置: 模式={claude_config['mode']}, 有密钥={bool(claude_config.get('api_key'))}")
    print(f"   ✅ Gemini配置: 模式={gemini_config['mode']}, 有密钥={bool(gemini_config.get('api_key'))}")
    
    # 测试4: 检查可用API
    print("\n📋 测试4: 检查可用API")
    available_apis = config_manager.get_available_apis()
    print(f"   ✅ 可用API: {available_apis}")
    
    for api_name in ["claude", "gemini", "openai"]:
        is_available = config_manager.is_api_available(api_name)
        print(f"   - {api_name}: {'可用' if is_available else '不可用'}")

def test_api_call_manager():
    """测试API调用管理器"""
    print("\n🔧 测试API调用管理器")
    print("=" * 50)
    
    # 获取调用管理器
    call_manager = get_api_call_manager()
    
    # 测试1: 模拟API调用
    print("\n📋 测试1: 模拟API调用")
    
    # Claude意图分析
    claude_result = call_manager.make_api_call(
        "claude", 
        "analyze_intent", 
        text="创建一个测试工作流"
    )
    print(f"   ✅ Claude调用结果: {claude_result['status']}")
    if claude_result['status'] == 'success':
        print(f"      - 意图类型: {claude_result.get('intent_type', 'N/A')}")
        print(f"      - 置信度: {claude_result.get('confidence', 'N/A')}")
        print(f"      - 模拟模式: {claude_result.get('mock', False)}")
    
    # Gemini任务分解
    gemini_result = call_manager.make_api_call(
        "gemini",
        "decompose_task",
        text="部署应用到生产环境"
    )
    print(f"   ✅ Gemini调用结果: {gemini_result['status']}")
    if gemini_result['status'] == 'success':
        print(f"      - 子任务数: {len(gemini_result.get('subtasks', []))}")
        print(f"      - 复杂度: {gemini_result.get('complexity', 'N/A')}")
        print(f"      - 模拟模式: {gemini_result.get('mock', False)}")
    
    # 测试2: 切换到真实模式并测试回退
    print("\n📋 测试2: 测试真实模式和回退机制")
    
    # 切换到真实模式
    switch_to_real_mode()
    
    # 尝试调用（应该回退到模拟模式，因为没有真实的API密钥）
    openai_result = call_manager.make_api_call(
        "openai",
        "chat_completion",
        text="Hello, how are you?"
    )
    print(f"   ✅ OpenAI调用结果: {openai_result['status']}")
    
    # 测试3: 获取调用历史
    print("\n📋 测试3: 获取调用历史")
    call_history = call_manager.get_call_history(5)
    print(f"   ✅ 调用历史记录数: {len(call_history)}")
    
    for i, record in enumerate(call_history):
        print(f"   - 记录{i+1}: {record['api_name']}.{record['method']} ({record['status']})")

def test_integration_with_ai_modules():
    """测试与AI模块的集成"""
    print("\n🔧 测试与AI模块的集成")
    print("=" * 50)
    
    try:
        from mcptool.adapters.ai_enhanced_intent_understanding_mcp import AIEnhancedIntentUnderstandingMCP
        
        # 初始化AI模块
        ai_module = AIEnhancedIntentUnderstandingMCP()
        
        # 测试意图理解
        print("\n📋 测试AI增强意图理解模块")
        test_input = {
            "action": "analyze_intent",
            "text": "我想创建一个自动化测试工作流",
            "context": {"user_id": "test_user", "session_id": "test_session"}
        }
        
        result = ai_module.process(test_input)
        print(f"   ✅ 意图理解结果: {result['status']}")
        if result['status'] == 'success':
            analysis = result.get('analysis', {})
            print(f"      - 主要意图: {analysis.get('primary_intent', 'N/A')}")
            print(f"      - 置信度: {analysis.get('confidence', 'N/A')}")
            print(f"      - 关键词: {analysis.get('keywords', [])}")
        
    except ImportError as e:
        print(f"   ⚠️ AI模块导入失败: {e}")
    except Exception as e:
        print(f"   ❌ AI模块测试失败: {e}")

def test_environment_variables():
    """测试环境变量支持"""
    print("\n🔧 测试环境变量支持")
    print("=" * 50)
    
    config_manager = get_api_config_manager()
    
    # 模拟设置环境变量
    original_claude_key = os.environ.get("CLAUDE_API_KEY")
    original_gemini_key = os.environ.get("GEMINI_API_KEY")
    
    try:
        # 设置测试环境变量
        os.environ["CLAUDE_API_KEY"] = "env_claude_key_789"
        os.environ["GEMINI_API_KEY"] = "env_gemini_key_012"
        
        # 重新加载配置
        claude_config = config_manager.get_api_config("claude")
        gemini_config = config_manager.get_api_config("gemini")
        
        print(f"   ✅ Claude从环境变量获取密钥: {claude_config.get('api_key') == 'env_claude_key_789'}")
        print(f"   ✅ Gemini从环境变量获取密钥: {gemini_config.get('api_key') == 'env_gemini_key_012'}")
        
        # 检查模式是否自动切换到真实模式
        print(f"   ✅ Claude模式: {claude_config.get('mode')}")
        print(f"   ✅ Gemini模式: {gemini_config.get('mode')}")
        
    finally:
        # 恢复原始环境变量
        if original_claude_key:
            os.environ["CLAUDE_API_KEY"] = original_claude_key
        else:
            os.environ.pop("CLAUDE_API_KEY", None)
            
        if original_gemini_key:
            os.environ["GEMINI_API_KEY"] = original_gemini_key
        else:
            os.environ.pop("GEMINI_API_KEY", None)

def test_error_handling():
    """测试错误处理"""
    print("\n🔧 测试错误处理")
    print("=" * 50)
    
    call_manager = get_api_call_manager()
    
    # 测试1: 不存在的API
    print("\n📋 测试1: 调用不存在的API")
    result = call_manager.make_api_call("nonexistent_api", "test_method")
    print(f"   ✅ 结果: {result['status']} - {result.get('message', 'N/A')}")
    
    # 测试2: 禁用的API
    print("\n📋 测试2: 调用禁用的API")
    config_manager = get_api_config_manager()
    config_manager.config["apis"]["openai"]["enabled"] = False
    
    result = call_manager.make_api_call("openai", "test_method")
    print(f"   ✅ 结果: {result['status']} - {result.get('message', 'N/A')}")
    
    # 恢复设置
    config_manager.config["apis"]["openai"]["enabled"] = True

if __name__ == "__main__":
    print("🚀 PowerAutomation API切换功能测试")
    print("=" * 60)
    
    test_api_config_manager()
    test_api_call_manager()
    test_integration_with_ai_modules()
    test_environment_variables()
    test_error_handling()
    
    print("\n🎉 API切换功能测试完成!")
    print("=" * 60)

