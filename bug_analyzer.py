#!/usr/bin/env python3
"""
PowerAutomation Bug分析和诊断脚本
"""

import os
import sys
import traceback
from typing import Dict, Any

# 添加项目路径
sys.path.append('/home/ubuntu/powerautomation')

class BugAnalyzer:
    """Bug分析器"""
    
    def __init__(self):
        self.issues = []
        self.setup_api_keys()
    
    def setup_api_keys(self):
        """设置API密钥"""
        os.environ['CLAUDE_API_KEY'] = ""CLAUDE_API_KEY_PLACEHOLDER""
        os.environ['GEMINI_API_KEY'] = ""GEMINI_API_KEY_PLACEHOLDER""
        os.environ['KILO_API_KEY'] = ""CLAUDE_API_KEY_PLACEHOLDER""
        os.environ['SUPERMEMORY_API_KEY'] = ""SUPERMEMORY_API_KEY_PLACEHOLDER""
    
    def test_api_config_manager(self):
        """测试API配置管理器"""
        print("🔧 测试API配置管理器...")
        
        try:
            from mcptool.adapters.api_config_manager import get_api_config_manager, get_api_call_manager
            
            # 测试配置管理器
            config_manager = get_api_config_manager()
            print(f"✅ 配置管理器创建成功")
            
            # 测试API调用管理器
            call_manager = get_api_call_manager()
            print(f"✅ API调用管理器创建成功")
            
            # 测试API调用
            claude_test = call_manager.make_api_call("claude", "test", message="测试消息")
            print(f"✅ Claude API测试: {claude_test.get('status', 'unknown')}")
            
            gemini_test = call_manager.make_api_call("gemini", "test", message="测试消息")
            print(f"✅ Gemini API测试: {gemini_test.get('status', 'unknown')}")
            
            return True
            
        except Exception as e:
            error_msg = f"API配置管理器测试失败: {e}"
            print(f"❌ {error_msg}")
            self.issues.append({
                "component": "API配置管理器",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_ai_intent_understanding(self):
        """测试AI增强意图理解"""
        print("\n🧠 测试AI增强意图理解...")
        
        try:
            from mcptool.adapters.ai_enhanced_intent_understanding_mcp import AIEnhancedIntentUnderstandingMCP
            
            # 创建实例
            intent_analyzer = AIEnhancedIntentUnderstandingMCP({
                "claude_api_key": os.environ.get('CLAUDE_API_KEY'),
                "gemini_api_key": os.environ.get('GEMINI_API_KEY')
            })
            print(f"✅ AI意图理解模块创建成功")
            
            # 测试意图分析
            test_text = "我想要购买一台笔记本电脑"
            result = intent_analyzer.analyze_intent(test_text)
            print(f"✅ 意图分析测试: {result.get('status', 'unknown')}")
            
            return True
            
        except Exception as e:
            error_msg = f"AI意图理解测试失败: {e}"
            print(f"❌ {error_msg}")
            self.issues.append({
                "component": "AI增强意图理解",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_workflow_engine(self):
        """测试智能工作流引擎"""
        print("\n⚙️ 测试智能工作流引擎...")
        
        try:
            from mcptool.adapters.intelligent_workflow_engine_mcp import IntelligentWorkflowEngineMCP
            
            # 创建实例
            workflow_engine = IntelligentWorkflowEngineMCP("/home/ubuntu/powerautomation")
            print(f"✅ 工作流引擎创建成功")
            
            # 测试工作流创建
            workflow_config = {
                "workflow_name": "测试工作流",
                "complexity": "simple",
                "automation_level": "basic"
            }
            
            result = workflow_engine.create_workflow(workflow_config)
            print(f"✅ 工作流创建测试: {result.get('status', 'unknown')}")
            
            # 测试引擎能力
            capabilities = workflow_engine.get_engine_capabilities()
            print(f"✅ 引擎能力测试: {len(capabilities.get('capabilities', []))}个能力可用")
            
            return True
            
        except Exception as e:
            error_msg = f"工作流引擎测试失败: {e}"
            print(f"❌ {error_msg}")
            self.issues.append({
                "component": "智能工作流引擎",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_ai_coordination_hub(self):
        """测试AI协调中心"""
        print("\n🔄 测试AI协调中心...")
        
        try:
            from mcptool.adapters.ai_coordination_hub import AICoordinationHub
            
            # 创建实例
            coordination_hub = AICoordinationHub()
            print(f"✅ AI协调中心创建成功")
            
            # 测试协调功能
            test_task = {
                "task_type": "simple_coordination",
                "description": "测试协调任务"
            }
            
            result = coordination_hub.coordinate_task(test_task)
            print(f"✅ 协调功能测试: {result.get('status', 'unknown')}")
            
            return True
            
        except Exception as e:
            error_msg = f"AI协调中心测试失败: {e}"
            print(f"❌ {error_msg}")
            self.issues.append({
                "component": "AI协调中心",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def analyze_api_models(self):
        """分析API模型配置"""
        print("\n🔍 分析API模型配置...")
        
        try:
            from mcptool.adapters.api_config_manager import get_api_call_manager
            
            call_manager = get_api_call_manager()
            
            # 测试不同的API模型
            claude_models = ["claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-3-opus-20240229"]
            gemini_models = ["gemini-pro", "gemini-1.5-pro", "gemini-2.0-flash"]
            
            print("🔍 测试Claude模型...")
            for model in claude_models:
                try:
                    result = call_manager.make_api_call("claude", "test", message="测试", model=model)
                    status = "✅" if result.get('status') == 'success' else "❌"
                    print(f"   {status} {model}: {result.get('status', 'unknown')}")
                except Exception as e:
                    print(f"   ❌ {model}: {e}")
                    self.issues.append({
                        "component": f"Claude模型-{model}",
                        "error": str(e),
                        "type": "model_compatibility"
                    })
            
            print("🔍 测试Gemini模型...")
            for model in gemini_models:
                try:
                    result = call_manager.make_api_call("gemini", "test", message="测试", model=model)
                    status = "✅" if result.get('status') == 'success' else "❌"
                    print(f"   {status} {model}: {result.get('status', 'unknown')}")
                except Exception as e:
                    print(f"   ❌ {model}: {e}")
                    self.issues.append({
                        "component": f"Gemini模型-{model}",
                        "error": str(e),
                        "type": "model_compatibility"
                    })
            
            return True
            
        except Exception as e:
            error_msg = f"API模型分析失败: {e}"
            print(f"❌ {error_msg}")
            self.issues.append({
                "component": "API模型配置",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def generate_bug_report(self):
        """生成Bug报告"""
        print("\n📊 生成Bug分析报告...")
        
        print(f"\n🔍 发现的问题总数: {len(self.issues)}")
        
        if not self.issues:
            print("✅ 未发现严重问题！")
            return
        
        # 按组件分类问题
        component_issues = {}
        for issue in self.issues:
            component = issue['component']
            if component not in component_issues:
                component_issues[component] = []
            component_issues[component].append(issue)
        
        print("\n📋 问题分类:")
        for component, issues in component_issues.items():
            print(f"\n🔧 {component} ({len(issues)}个问题):")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue['error']}")
                if issue.get('type'):
                    print(f"      类型: {issue['type']}")
        
        # 生成修复建议
        print("\n💡 修复建议:")
        
        model_issues = [i for i in self.issues if i.get('type') == 'model_compatibility']
        if model_issues:
            print("1. 🔄 更新API模型版本配置")
            print("   - 使用最新的Claude和Gemini模型版本")
            print("   - 检查模型名称的正确性")
        
        init_issues = [i for i in self.issues if 'init' in i['error'].lower() or 'constructor' in i['error'].lower()]
        if init_issues:
            print("2. ⚙️ 修复模块初始化问题")
            print("   - 检查构造函数参数")
            print("   - 确保依赖模块正确加载")
        
        api_issues = [i for i in self.issues if 'api' in i['error'].lower()]
        if api_issues:
            print("3. 🔑 修复API配置问题")
            print("   - 验证API密钥有效性")
            print("   - 检查API调用格式")
    
    def run_analysis(self):
        """运行完整的Bug分析"""
        print("🚀 PowerAutomation Bug分析开始")
        print("=" * 60)
        
        tests = [
            ("API配置管理器", self.test_api_config_manager),
            ("AI增强意图理解", self.test_ai_intent_understanding),
            ("智能工作流引擎", self.test_workflow_engine),
            ("AI协调中心", self.test_ai_coordination_hub),
            ("API模型配置", self.analyze_api_models)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ {test_name}测试异常: {e}")
                results[test_name] = False
                self.issues.append({
                    "component": test_name,
                    "error": f"测试异常: {e}",
                    "traceback": traceback.format_exc()
                })
        
        # 生成报告
        self.generate_bug_report()
        
        print("\n" + "=" * 60)
        print("🎯 Bug分析完成")
        
        successful_tests = sum(1 for result in results.values() if result)
        total_tests = len(results)
        
        print(f"📊 测试结果: {successful_tests}/{total_tests} 通过")
        for test_name, result in results.items():
            status = "✅" if result else "❌"
            print(f"   {status} {test_name}")
        
        return results, self.issues

def main():
    """主函数"""
    analyzer = BugAnalyzer()
    return analyzer.run_analysis()

if __name__ == "__main__":
    main()

