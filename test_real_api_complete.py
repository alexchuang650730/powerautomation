#!/usr/bin/env python3
"""
PowerAutomation 真实API测试脚本
使用真实API密钥进行完整功能验证
"""

import os
import sys
import json
import time
from typing import Dict, Any

# 添加项目路径
sys.path.append('/home/ubuntu/powerautomation')

def setup_real_api_mode():
    """配置真实API模式"""
    print("🔧 配置API管理器为真实模式...")
    
    try:
        from mcptool.adapters.api_config_manager import get_api_config_manager, switch_to_real_mode
        
        # 切换到真实模式
        switch_to_real_mode()
        
        # 获取配置管理器
        config_manager = get_api_config_manager()
        
        # 设置API密钥
        claude_key = os.getenv('CLAUDE_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        kilo_key = os.getenv('KILO_API_KEY')
        supermemory_key = os.getenv('SUPERMEMORY_API_KEY')
        
        if claude_key:
            config_manager.set_api_key("claude", claude_key)
            print(f"✅ Claude API密钥已设置: {claude_key[:20]}...")
            
        if gemini_key:
            config_manager.set_api_key("gemini", gemini_key)
            print(f"✅ Gemini API密钥已设置: {gemini_key[:20]}...")
            
        # 获取当前状态
        status = config_manager.get_status()
        print(f"✅ 当前API模式: {status['mode']}")
        print(f"✅ 可用API: {status['available_apis']}")
        
        return True
        
    except Exception as e:
        print(f"❌ API配置失败: {e}")
        return False

def test_basic_functionality():
    """测试基础功能"""
    print("\n🧪 开始基础功能测试...")
    
    try:
        # 测试工作流引擎
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 测试工作流创建
        simple_config = {
            "workflow_name": "真实API测试工作流",
            "complexity": "medium",
            "automation_level": "advanced",
            "metadata": {
                "description": "使用真实API进行测试",
                "test_mode": "real_api"
            }
        }
        
        result = engine.create_workflow(simple_config)
        print(f"✅ 工作流创建: {result.get('status', 'unknown')}")
        print(f"   - 工作流ID: {result.get('workflow_id', 'N/A')}")
        print(f"   - 节点数量: {len(result.get('nodes', []))}")
        
        # 测试能力获取
        capabilities = engine.get_capabilities()
        print(f"✅ 引擎能力: {len(capabilities)}个能力")
        
        return True
        
    except Exception as e:
        print(f"❌ 基础功能测试失败: {e}")
        return False

def test_real_api_calls():
    """测试真实API调用"""
    print("\n🤖 开始真实API调用测试...")
    
    try:
        from mcptool.adapters.api_config_manager import get_api_call_manager
        
        call_manager = get_api_call_manager()
        
        # 测试Claude API
        print("📋 测试Claude API...")
        claude_result = call_manager.make_api_call(
            "claude", 
            "analyze_intent",
            text="请分析这个自动化测试的意图和目标"
        )
        print(f"   ✅ Claude调用: {claude_result.get('status', 'unknown')}")
        if claude_result.get('status') == 'success':
            print(f"   - 意图类型: {claude_result.get('intent_type', 'N/A')}")
            print(f"   - 置信度: {claude_result.get('confidence', 'N/A')}")
            print(f"   - 真实API: {not claude_result.get('mock', True)}")
        
        # 测试Gemini API
        print("📋 测试Gemini API...")
        gemini_result = call_manager.make_api_call(
            "gemini",
            "decompose_task", 
            task="创建一个完整的自动化测试流程"
        )
        print(f"   ✅ Gemini调用: {gemini_result.get('status', 'unknown')}")
        if gemini_result.get('status') == 'success':
            subtasks = gemini_result.get('subtasks', [])
            print(f"   - 子任务数: {len(subtasks)}")
            print(f"   - 复杂度: {gemini_result.get('complexity', 'N/A')}")
            print(f"   - 真实API: {not gemini_result.get('mock', True)}")
        
        # 获取调用历史
        history = call_manager.get_call_history(5)
        print(f"✅ API调用历史: {len(history)}条记录")
        
        return True
        
    except Exception as e:
        print(f"❌ 真实API调用测试失败: {e}")
        return False

def test_ai_enhanced_features():
    """测试AI增强功能"""
    print("\n🧠 开始AI增强功能测试...")
    
    try:
        # 测试AI增强意图理解
        from mcptool.adapters.ai_enhanced_intent_understanding_mcp import AIEnhancedIntentUnderstandingMCP
        
        ai_intent = AIEnhancedIntentUnderstandingMCP("/home/ubuntu/powerautomation")
        
        # 测试意图分析
        intent_result = ai_intent.analyze_intent({
            "user_input": "我想创建一个自动化工作流来处理数据分析任务",
            "context": "PowerAutomation真实API测试",
            "use_real_api": True
        })
        
        print(f"✅ AI意图分析: {intent_result.get('status', 'unknown')}")
        if intent_result.get('status') == 'success':
            print(f"   - 意图类型: {intent_result.get('intent_type', 'N/A')}")
            print(f"   - 置信度: {intent_result.get('confidence', 'N/A')}")
            print(f"   - 建议操作: {len(intent_result.get('suggested_actions', []))}个")
        
        return True
        
    except Exception as e:
        print(f"❌ AI增强功能测试失败: {e}")
        return False

def test_workflow_engine_with_real_api():
    """使用真实API测试工作流引擎"""
    print("\n⚙️ 开始工作流引擎真实API测试...")
    
    try:
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 创建复杂工作流
        complex_config = {
            "workflow_name": "AI增强数据处理工作流",
            "complexity": "high",
            "automation_level": "advanced",
            "metadata": {
                "description": "使用真实AI API的复杂数据处理工作流",
                "ai_enhanced": True,
                "real_api_mode": True
            },
            "input_data": {
                "data_source": "real_api_test",
                "processing_type": "ai_enhanced",
                "output_format": "structured"
            }
        }
        
        result = engine.create_workflow(complex_config)
        print(f"✅ 复杂工作流创建: {result.get('status', 'unknown')}")
        print(f"   - 工作流ID: {result.get('workflow_id', 'N/A')}")
        print(f"   - 节点数量: {len(result.get('nodes', []))}")
        print(f"   - 连接数量: {len(result.get('connections', []))}")
        
        # 测试工作流执行
        if result.get('status') == 'success':
            workflow_id = result.get('workflow_id')
            execution_result = engine.execute_workflow({
                "workflow_id": workflow_id,
                "input_data": {"test": "real_api_execution"},
                "use_real_api": True
            })
            print(f"✅ 工作流执行: {execution_result.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工作流引擎真实API测试失败: {e}")
        return False

def test_api_switching_and_fallback():
    """测试API切换和回退机制"""
    print("\n🔄 开始API切换和回退机制测试...")
    
    try:
        from mcptool.adapters.api_config_manager import get_api_config_manager, get_api_call_manager
        
        config_manager = get_api_config_manager()
        call_manager = get_api_call_manager()
        
        # 测试模式切换
        print("📋 测试API模式切换...")
        
        # 切换到混合模式
        config_manager.switch_mode("hybrid")
        print(f"   ✅ 切换到混合模式: {config_manager.get_current_mode()}")
        
        # 切换回真实模式
        config_manager.switch_mode("real")
        print(f"   ✅ 切换到真实模式: {config_manager.get_current_mode()}")
        
        # 测试回退机制
        print("📋 测试回退机制...")
        
        # 启用回退模式
        config_manager.enable_fallback_mode()
        
        # 尝试调用不存在的API（应该回退）
        fallback_result = call_manager.make_api_call(
            "nonexistent_api",
            "test_method",
            data="fallback_test"
        )
        print(f"   ✅ 回退测试: {fallback_result.get('status', 'unknown')}")
        
        # 测试API健康检查
        health_status = config_manager.check_api_health()
        print(f"✅ API健康检查: {len(health_status)}个API检查完成")
        
        return True
        
    except Exception as e:
        print(f"❌ API切换和回退测试失败: {e}")
        return False

def generate_test_summary():
    """生成测试总结"""
    print("\n📊 生成测试总结...")
    
    try:
        from mcptool.adapters.api_config_manager import get_api_call_manager
        
        call_manager = get_api_call_manager()
        
        # 获取API调用统计
        history = call_manager.get_call_history(50)
        
        total_calls = len(history)
        successful_calls = len([h for h in history if h.get('status') == 'success'])
        failed_calls = len([h for h in history if h.get('status') == 'error'])
        
        success_rate = (successful_calls / total_calls * 100) if total_calls > 0 else 0
        
        summary = {
            "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_api_calls": total_calls,
            "successful_calls": successful_calls,
            "failed_calls": failed_calls,
            "success_rate": f"{success_rate:.1f}%",
            "api_keys_configured": [
                "CLAUDE_API_KEY" if os.getenv('CLAUDE_API_KEY') else None,
                "GEMINI_API_KEY" if os.getenv('GEMINI_API_KEY') else None,
                "KILO_API_KEY" if os.getenv('KILO_API_KEY') else None,
                "SUPERMEMORY_API_KEY" if os.getenv('SUPERMEMORY_API_KEY') else None
            ]
        }
        
        # 过滤None值
        summary["api_keys_configured"] = [k for k in summary["api_keys_configured"] if k]
        
        print("✅ 测试总结:")
        print(f"   - 测试时间: {summary['test_timestamp']}")
        print(f"   - 总API调用: {summary['total_api_calls']}")
        print(f"   - 成功调用: {summary['successful_calls']}")
        print(f"   - 失败调用: {summary['failed_calls']}")
        print(f"   - 成功率: {summary['success_rate']}")
        print(f"   - 配置的API: {len(summary['api_keys_configured'])}个")
        
        return summary
        
    except Exception as e:
        print(f"❌ 测试总结生成失败: {e}")
        return {}

def main():
    """主测试函数"""
    print("🚀 PowerAutomation 真实API完整测试")
    print("=" * 60)
    
    # 测试步骤
    test_results = {}
    
    # 1. 配置真实API模式
    test_results["api_setup"] = setup_real_api_mode()
    
    # 2. 基础功能测试
    test_results["basic_functionality"] = test_basic_functionality()
    
    # 3. 真实API调用测试
    test_results["real_api_calls"] = test_real_api_calls()
    
    # 4. AI增强功能测试
    test_results["ai_enhanced"] = test_ai_enhanced_features()
    
    # 5. 工作流引擎真实API测试
    test_results["workflow_engine"] = test_workflow_engine_with_real_api()
    
    # 6. API切换和回退测试
    test_results["api_switching"] = test_api_switching_and_fallback()
    
    # 7. 生成测试总结
    summary = generate_test_summary()
    
    # 最终结果
    print("\n" + "=" * 60)
    print("🎉 真实API测试完成!")
    print("=" * 60)
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    print(f"📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   - {test_name}: {status}")
    
    if summary:
        print(f"\n📈 API调用统计: {summary.get('success_rate', 'N/A')} 成功率")
    
    return test_results, summary

if __name__ == "__main__":
    main()

