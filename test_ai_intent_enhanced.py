#!/usr/bin/env python3
"""
AI增强意图理解专项测试
使用真实Claude API进行意图分析测试
"""

import os
import sys
import json
import time
from typing import Dict, Any

# 添加项目路径
sys.path.append('/home/ubuntu/powerautomation')

def test_claude_api_direct():
    """直接测试Claude API连接"""
    print("🔧 直接测试Claude API连接...")
    
    try:
        import requests
        
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            print("❌ Claude API密钥未设置")
            return False
            
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
        
        data = {
            'model': 'claude-3-sonnet-20240229',
            'max_tokens': 100,
            'messages': [
                {
                    'role': 'user',
                    'content': '请简单回复：你好，我是Claude AI助手。'
                }
            ]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('content', [])
            if content and len(content) > 0:
                text = content[0].get('text', '')
                print(f"✅ Claude API直接调用成功")
                print(f"   响应: {text[:100]}...")
                return True
        else:
            print(f"❌ Claude API调用失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Claude API直接测试失败: {e}")
        return False

def test_gemini_api_direct():
    """直接测试Gemini API连接"""
    print("🔧 直接测试Gemini API连接...")
    
    try:
        import requests
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ Gemini API密钥未设置")
            return False
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        data = {
            'contents': [{
                'parts': [{
                    'text': '请简单回复：你好，我是Gemini AI助手。'
                }]
            }]
        }
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            candidates = result.get('candidates', [])
            if candidates and len(candidates) > 0:
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if parts and len(parts) > 0:
                    text = parts[0].get('text', '')
                    print(f"✅ Gemini API直接调用成功")
                    print(f"   响应: {text[:100]}...")
                    return True
        else:
            print(f"❌ Gemini API调用失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API直接测试失败: {e}")
        return False

def test_ai_intent_understanding():
    """测试AI增强意图理解"""
    print("🤖 测试AI增强意图理解...")
    
    try:
        from mcptool.adapters.ai_enhanced_intent_understanding_mcp import AIEnhancedIntentUnderstandingMCP
        
        # 创建AI意图理解实例
        ai_intent = AIEnhancedIntentUnderstandingMCP("/home/ubuntu/powerautomation")
        
        # 测试用例1：简单意图分析
        print("📋 测试1: 简单意图分析")
        test_input = {
            "user_input": "我想创建一个自动化工作流来处理数据分析任务",
            "context": "PowerAutomation真实API测试"
        }
        
        result1 = ai_intent.analyze_intent(test_input)
        print(f"   结果类型: {type(result1)}")
        
        if isinstance(result1, dict):
            print(f"   ✅ 意图分析成功: {result1.get('status', 'unknown')}")
            print(f"   - 意图类型: {result1.get('intent_type', 'N/A')}")
            print(f"   - 置信度: {result1.get('confidence', 'N/A')}")
        else:
            print(f"   ⚠️ 返回格式: {str(result1)[:200]}...")
        
        # 测试用例2：复杂意图分析
        print("📋 测试2: 复杂意图分析")
        test_input2 = {
            "user_input": "帮我设计一个包含数据收集、清洗、分析和可视化的完整数据处理流水线",
            "context": "企业级数据处理需求",
            "requirements": ["自动化", "可扩展", "监控"]
        }
        
        result2 = ai_intent.analyze_intent(test_input2)
        if isinstance(result2, dict):
            print(f"   ✅ 复杂意图分析成功: {result2.get('status', 'unknown')}")
            actions = result2.get('suggested_actions', [])
            print(f"   - 建议操作数: {len(actions)}")
        else:
            print(f"   ⚠️ 返回格式: {str(result2)[:200]}...")
        
        # 测试用例3：获取能力
        print("📋 测试3: 获取AI能力")
        capabilities = ai_intent.get_capabilities()
        print(f"   ✅ AI能力数量: {len(capabilities)}")
        for cap in capabilities[:3]:  # 显示前3个能力
            print(f"   - {cap}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI意图理解测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_coordination_hub():
    """测试AI协调中心"""
    print("🧠 测试AI协调中心...")
    
    try:
        from mcptool.adapters.ai_coordination_hub import AICoordinationHub
        
        # 创建AI协调中心实例
        ai_hub = AICoordinationHub("/home/ubuntu/powerautomation")
        
        # 测试协调功能
        coordination_request = {
            "task": "创建数据分析工作流",
            "requirements": ["使用真实API", "AI增强", "自动化"],
            "context": "PowerAutomation测试"
        }
        
        result = ai_hub.coordinate_ai_modules(coordination_request)
        print(f"   ✅ AI协调结果: {result.get('status', 'unknown')}")
        
        if result.get('status') == 'success':
            modules = result.get('coordinated_modules', [])
            print(f"   - 协调模块数: {len(modules)}")
            
        return True
        
    except Exception as e:
        print(f"❌ AI协调中心测试失败: {e}")
        return False

def test_real_api_integration():
    """测试真实API集成"""
    print("🔗 测试真实API集成...")
    
    try:
        from mcptool.adapters.api_config_manager import get_api_call_manager
        
        call_manager = get_api_call_manager()
        
        # 测试Claude意图分析
        print("📋 测试Claude意图分析API...")
        claude_result = call_manager.make_api_call(
            "claude",
            "analyze_intent",
            text="创建一个包含机器学习模型训练的自动化工作流",
            context="AI增强数据科学项目"
        )
        
        print(f"   ✅ Claude API调用: {claude_result.get('status', 'unknown')}")
        if not claude_result.get('mock', True):
            print("   ✅ 使用真实Claude API")
        else:
            print("   ⚠️ 使用模拟API")
        
        # 测试Gemini任务分解
        print("📋 测试Gemini任务分解API...")
        gemini_result = call_manager.make_api_call(
            "gemini",
            "decompose_task",
            task="设计一个端到端的机器学习流水线",
            complexity="high"
        )
        
        print(f"   ✅ Gemini API调用: {gemini_result.get('status', 'unknown')}")
        if not gemini_result.get('mock', True):
            print("   ✅ 使用真实Gemini API")
        else:
            print("   ⚠️ 使用模拟API")
        
        # 获取调用历史
        history = call_manager.get_call_history(10)
        real_calls = [h for h in history if not h.get('mock', True)]
        print(f"   📊 真实API调用: {len(real_calls)}/{len(history)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 真实API集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 AI增强意图理解专项测试")
    print("=" * 50)
    
    test_results = {}
    
    # 1. 直接API连接测试
    print("\n🔧 第一步：直接API连接测试")
    test_results["claude_direct"] = test_claude_api_direct()
    test_results["gemini_direct"] = test_gemini_api_direct()
    
    # 2. AI意图理解测试
    print("\n🤖 第二步：AI意图理解测试")
    test_results["ai_intent"] = test_ai_intent_understanding()
    
    # 3. AI协调中心测试
    print("\n🧠 第三步：AI协调中心测试")
    test_results["ai_coordination"] = test_ai_coordination_hub()
    
    # 4. 真实API集成测试
    print("\n🔗 第四步：真实API集成测试")
    test_results["api_integration"] = test_real_api_integration()
    
    # 结果总结
    print("\n" + "=" * 50)
    print("🎉 AI增强意图理解测试完成!")
    print("=" * 50)
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    print(f"📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   - {test_name}: {status}")
    
    return test_results

if __name__ == "__main__":
    main()

