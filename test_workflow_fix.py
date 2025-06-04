#!/usr/bin/env python3
"""
测试工作流引擎修复效果
验证_add_default_nodes方法和create_workflow功能
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP

def test_workflow_creation():
    """测试工作流创建功能"""
    print("🔧 测试工作流引擎修复效果")
    print("=" * 50)
    
    # 初始化工作流引擎
    engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
    
    # 测试1: 创建简单工作流（无节点配置）
    print("\n📋 测试1: 创建简单工作流（无节点配置）")
    simple_config = {
        "workflow_name": "简单测试工作流",
        "complexity": "low",
        "automation_level": "standard"
    }
    
    try:
        result = engine.create_workflow(simple_config)
        print(f"✅ 简单工作流创建结果: {result['status']}")
        if result['status'] == 'success':
            print(f"   - 工作流ID: {result['workflow_id']}")
            print(f"   - 节点数量: {result['nodes_created']}")
            print(f"   - 连接数量: {result['connections_created']}")
        else:
            print(f"   - 错误信息: {result['message']}")
    except Exception as e:
        print(f"❌ 简单工作流创建失败: {e}")
    
    # 测试2: 创建中等复杂度工作流
    print("\n📋 测试2: 创建中等复杂度工作流")
    medium_config = {
        "workflow_name": "中等复杂度测试工作流",
        "complexity": "medium",
        "automation_level": "standard"
    }
    
    try:
        result = engine.create_workflow(medium_config)
        print(f"✅ 中等工作流创建结果: {result['status']}")
        if result['status'] == 'success':
            print(f"   - 工作流ID: {result['workflow_id']}")
            print(f"   - 节点数量: {result['nodes_created']}")
            print(f"   - 连接数量: {result['connections_created']}")
        else:
            print(f"   - 错误信息: {result['message']}")
    except Exception as e:
        print(f"❌ 中等工作流创建失败: {e}")
    
    # 测试3: 创建高复杂度工作流
    print("\n📋 测试3: 创建高复杂度工作流")
    high_config = {
        "workflow_name": "高复杂度测试工作流",
        "complexity": "high",
        "automation_level": "advanced"
    }
    
    try:
        result = engine.create_workflow(high_config)
        print(f"✅ 高复杂度工作流创建结果: {result['status']}")
        if result['status'] == 'success':
            print(f"   - 工作流ID: {result['workflow_id']}")
            print(f"   - 节点数量: {result['nodes_created']}")
            print(f"   - 连接数量: {result['connections_created']}")
        else:
            print(f"   - 错误信息: {result['message']}")
    except Exception as e:
        print(f"❌ 高复杂度工作流创建失败: {e}")
    
    # 测试4: 测试_add_default_nodes方法直接调用
    print("\n📋 测试4: 直接测试_add_default_nodes方法")
    test_config = {
        "workflow_name": "直接测试工作流",
        "complexity": "medium"
    }
    
    try:
        enhanced_config = engine._add_default_nodes(test_config)
        print(f"✅ _add_default_nodes方法调用成功")
        print(f"   - 原始节点数: {len(test_config.get('nodes', []))}")
        print(f"   - 增强后节点数: {len(enhanced_config.get('nodes', []))}")
        print(f"   - 连接数: {len(enhanced_config.get('connections', []))}")
        print(f"   - 复杂度: {enhanced_config.get('complexity', 'unknown')}")
    except Exception as e:
        print(f"❌ _add_default_nodes方法调用失败: {e}")
    
    # 测试5: 获取工作流状态
    print("\n📋 测试5: 获取工作流状态")
    try:
        workflow_data = engine.get_workflow_data()
        print(f"✅ 工作流状态获取成功")
        print(f"   - 总节点数: {len(workflow_data['nodes'])}")
        print(f"   - 总连接数: {len(workflow_data['connections'])}")
        print(f"   - 运行状态: {workflow_data['status']['is_running']}")
    except Exception as e:
        print(f"❌ 工作流状态获取失败: {e}")
    
    print("\n🎉 工作流引擎测试完成!")

def test_api_compatibility():
    """测试API兼容性"""
    print("\n🔧 测试API兼容性")
    print("=" * 50)
    
    engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
    
    # 测试MCP接口
    print("\n📋 测试MCP接口兼容性")
    test_data = {
        "action": "create_workflow_node",
        "node_type": "action",
        "name": "测试节点",
        "description": "API兼容性测试节点",
        "data": {"test": True}
    }
    
    try:
        result = engine.process(test_data)
        print(f"✅ MCP接口调用成功: {result['status']}")
        if result['status'] == 'success':
            print(f"   - 节点ID: {result['node_id']}")
    except Exception as e:
        print(f"❌ MCP接口调用失败: {e}")
    
    # 测试能力获取
    print("\n📋 测试能力获取")
    try:
        capabilities = engine.get_capabilities()
        print(f"✅ 能力获取成功: {len(capabilities)}个能力")
        for cap in capabilities:
            print(f"   - {cap}")
    except Exception as e:
        print(f"❌ 能力获取失败: {e}")

if __name__ == "__main__":
    test_workflow_creation()
    test_api_compatibility()

