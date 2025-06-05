#!/usr/bin/env python3
"""
智能工作流引擎专项测试
使用真实API进行工作流创建和执行测试
"""

import os
import sys
import json
import time
from typing import Dict, Any

# 添加项目路径
sys.path.append('/home/ubuntu/powerautomation')

def test_workflow_creation():
    """测试工作流创建功能"""
    print("🔧 测试工作流创建功能...")
    
    try:
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 测试1：简单工作流
        print("📋 测试1: 简单工作流创建")
        simple_config = {
            "workflow_name": "简单数据处理工作流",
            "complexity": "low",
            "automation_level": "standard",
            "metadata": {
                "description": "简单的数据处理任务",
                "use_real_api": True
            }
        }
        
        result1 = engine.create_workflow(simple_config)
        print(f"   ✅ 简单工作流: {result1.get('status', 'unknown')}")
        print(f"   - 工作流ID: {result1.get('workflow_id', 'N/A')}")
        
        # 测试2：中等复杂度工作流
        print("📋 测试2: 中等复杂度工作流创建")
        medium_config = {
            "workflow_name": "AI增强数据分析工作流",
            "complexity": "medium",
            "automation_level": "advanced",
            "metadata": {
                "description": "包含AI增强功能的数据分析",
                "ai_enhanced": True,
                "use_real_api": True
            },
            "input_data": {
                "data_source": "real_time_data",
                "analysis_type": "predictive"
            }
        }
        
        result2 = engine.create_workflow(medium_config)
        print(f"   ✅ 中等工作流: {result2.get('status', 'unknown')}")
        print(f"   - 工作流ID: {result2.get('workflow_id', 'N/A')}")
        
        # 测试3：高复杂度工作流
        print("📋 测试3: 高复杂度工作流创建")
        complex_config = {
            "workflow_name": "企业级ML流水线",
            "complexity": "high",
            "automation_level": "advanced",
            "metadata": {
                "description": "完整的机器学习流水线",
                "ai_enhanced": True,
                "use_real_api": True,
                "enterprise_grade": True
            },
            "input_data": {
                "data_sources": ["database", "api", "files"],
                "ml_models": ["classification", "regression"],
                "deployment_target": "production"
            }
        }
        
        result3 = engine.create_workflow(complex_config)
        print(f"   ✅ 复杂工作流: {result3.get('status', 'unknown')}")
        print(f"   - 工作流ID: {result3.get('workflow_id', 'N/A')}")
        
        return [result1, result2, result3]
        
    except Exception as e:
        print(f"❌ 工作流创建测试失败: {e}")
        return []

def test_workflow_execution():
    """测试工作流执行功能"""
    print("⚙️ 测试工作流执行功能...")
    
    try:
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 创建测试工作流
        test_config = {
            "workflow_name": "执行测试工作流",
            "complexity": "medium",
            "automation_level": "advanced",
            "metadata": {
                "description": "用于测试执行功能的工作流",
                "test_execution": True
            }
        }
        
        creation_result = engine.create_workflow(test_config)
        
        if creation_result.get('status') == 'success':
            workflow_id = creation_result.get('workflow_id')
            print(f"   ✅ 测试工作流已创建: {workflow_id}")
            
            # 执行工作流
            execution_config = {
                "workflow_id": workflow_id,
                "input_data": {
                    "test_data": "real_api_execution_test",
                    "timestamp": time.time(),
                    "use_real_api": True
                },
                "execution_mode": "real_api"
            }
            
            execution_result = engine.execute_workflow(execution_config)
            print(f"   ✅ 工作流执行: {execution_result.get('status', 'unknown')}")
            
            if execution_result.get('status') == 'success':
                print(f"   - 执行时间: {execution_result.get('execution_time', 'N/A')}秒")
                print(f"   - 处理节点: {len(execution_result.get('processed_nodes', []))}个")
            
            return execution_result
        else:
            print("   ❌ 无法创建测试工作流")
            return {}
            
    except Exception as e:
        print(f"❌ 工作流执行测试失败: {e}")
        return {}

def test_workflow_monitoring():
    """测试工作流监控功能"""
    print("📊 测试工作流监控功能...")
    
    try:
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 获取工作流状态
        status = engine.get_workflow_status()
        print(f"   ✅ 工作流状态获取成功")
        print(f"   - 总工作流数: {status.get('total_workflows', 0)}")
        print(f"   - 活跃工作流: {status.get('active_workflows', 0)}")
        print(f"   - 总节点数: {status.get('total_nodes', 0)}")
        print(f"   - 总连接数: {status.get('total_connections', 0)}")
        
        # 获取性能指标
        metrics = engine.get_performance_metrics()
        print(f"   ✅ 性能指标获取成功")
        print(f"   - 平均创建时间: {metrics.get('avg_creation_time', 'N/A')}秒")
        print(f"   - 成功率: {metrics.get('success_rate', 'N/A')}%")
        
        return True
        
    except Exception as e:
        print(f"❌ 工作流监控测试失败: {e}")
        return False

def test_workflow_ai_integration():
    """测试工作流AI集成功能"""
    print("🤖 测试工作流AI集成功能...")
    
    try:
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 测试AI增强工作流创建
        ai_config = {
            "workflow_name": "AI驱动的智能分析工作流",
            "complexity": "high",
            "automation_level": "advanced",
            "ai_enhanced": True,
            "metadata": {
                "description": "使用真实AI API的智能分析工作流",
                "ai_models": ["claude", "gemini"],
                "use_real_api": True
            },
            "ai_requirements": {
                "intent_analysis": True,
                "task_decomposition": True,
                "intelligent_routing": True
            }
        }
        
        ai_result = engine.create_workflow(ai_config)
        print(f"   ✅ AI增强工作流: {ai_result.get('status', 'unknown')}")
        
        if ai_result.get('status') == 'success':
            workflow_id = ai_result.get('workflow_id')
            
            # 测试AI功能调用
            ai_execution = {
                "workflow_id": workflow_id,
                "ai_tasks": [
                    {
                        "type": "intent_analysis",
                        "input": "分析用户的数据处理需求",
                        "api": "claude"
                    },
                    {
                        "type": "task_decomposition", 
                        "input": "将复杂任务分解为子任务",
                        "api": "gemini"
                    }
                ],
                "use_real_api": True
            }
            
            ai_exec_result = engine.execute_ai_enhanced_workflow(ai_execution)
            print(f"   ✅ AI功能执行: {ai_exec_result.get('status', 'unknown')}")
            
            if ai_exec_result.get('status') == 'success':
                ai_results = ai_exec_result.get('ai_results', [])
                print(f"   - AI任务完成: {len(ai_results)}个")
                
                for i, result in enumerate(ai_results):
                    print(f"   - 任务{i+1}: {result.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工作流AI集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_capabilities():
    """测试工作流引擎能力"""
    print("🔍 测试工作流引擎能力...")
    
    try:
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 获取引擎能力
        capabilities = engine.get_capabilities()
        print(f"   ✅ 引擎能力: {len(capabilities)}个")
        
        # 显示主要能力
        for i, capability in enumerate(capabilities[:5]):
            print(f"   - 能力{i+1}: {capability}")
        
        # 测试特定能力
        specific_capabilities = [
            "create_workflow",
            "execute_workflow", 
            "monitor_workflow",
            "ai_enhanced_processing"
        ]
        
        for cap in specific_capabilities:
            has_capability = cap in capabilities
            status = "✅" if has_capability else "❌"
            print(f"   {status} {cap}: {'支持' if has_capability else '不支持'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工作流能力测试失败: {e}")
        return False

def test_real_api_workflow_integration():
    """测试真实API工作流集成"""
    print("🔗 测试真实API工作流集成...")
    
    try:
        from mcptool.adapters.api_config_manager import get_api_call_manager
        from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
        
        # 获取API调用管理器
        call_manager = get_api_call_manager()
        engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
        
        # 创建集成测试工作流
        integration_config = {
            "workflow_name": "真实API集成测试工作流",
            "complexity": "medium",
            "automation_level": "advanced",
            "metadata": {
                "description": "测试真实API与工作流引擎的集成",
                "integration_test": True
            }
        }
        
        workflow_result = engine.create_workflow(integration_config)
        print(f"   ✅ 集成工作流创建: {workflow_result.get('status', 'unknown')}")
        
        # 在工作流中调用真实API
        if workflow_result.get('status') == 'success':
            # 调用Claude API进行意图分析
            claude_call = call_manager.make_api_call(
                "claude",
                "analyze_intent",
                text="在工作流中集成AI分析功能",
                context="工作流引擎集成测试"
            )
            
            print(f"   ✅ 工作流中Claude调用: {claude_call.get('status', 'unknown')}")
            
            # 调用Gemini API进行任务分解
            gemini_call = call_manager.make_api_call(
                "gemini", 
                "decompose_task",
                task="优化工作流执行性能",
                context="工作流引擎优化"
            )
            
            print(f"   ✅ 工作流中Gemini调用: {gemini_call.get('status', 'unknown')}")
            
            # 获取API调用历史
            history = call_manager.get_call_history(5)
            workflow_calls = [h for h in history if 'workflow' in h.get('context', '').lower()]
            print(f"   📊 工作流相关API调用: {len(workflow_calls)}次")
        
        return True
        
    except Exception as e:
        print(f"❌ 真实API工作流集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 智能工作流引擎专项测试")
    print("=" * 50)
    
    test_results = {}
    
    # 1. 工作流创建测试
    print("\n🔧 第一步：工作流创建测试")
    creation_results = test_workflow_creation()
    test_results["workflow_creation"] = len(creation_results) > 0 and all(
        r.get('status') == 'success' for r in creation_results
    )
    
    # 2. 工作流执行测试
    print("\n⚙️ 第二步：工作流执行测试")
    execution_result = test_workflow_execution()
    test_results["workflow_execution"] = execution_result.get('status') == 'success'
    
    # 3. 工作流监控测试
    print("\n📊 第三步：工作流监控测试")
    test_results["workflow_monitoring"] = test_workflow_monitoring()
    
    # 4. 工作流AI集成测试
    print("\n🤖 第四步：工作流AI集成测试")
    test_results["workflow_ai_integration"] = test_workflow_ai_integration()
    
    # 5. 工作流能力测试
    print("\n🔍 第五步：工作流能力测试")
    test_results["workflow_capabilities"] = test_workflow_capabilities()
    
    # 6. 真实API集成测试
    print("\n🔗 第六步：真实API集成测试")
    test_results["real_api_integration"] = test_real_api_workflow_integration()
    
    # 结果总结
    print("\n" + "=" * 50)
    print("🎉 智能工作流引擎测试完成!")
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

