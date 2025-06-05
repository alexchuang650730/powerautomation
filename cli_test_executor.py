#!/usr/bin/env python3
"""
PowerAutomation CLI测试执行器
使用现有的CLI工具运行完整测试套件和AI增强功能测试
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

# 设置环境变量
os.environ['PYTHONPATH'] = '/home/ubuntu/powerautomation'
os.environ['CLAUDE_API_KEY'] = '"CLAUDE_API_KEY_PLACEHOLDER"
os.environ['GEMINI_API_KEY'] = '"GEMINI_API_KEY_PLACEHOLDER"
os.environ['SUPERMEMORY_API_KEY'] = '"SUPERMEMORY_API_KEY_PLACEHOLDER"

class PowerAutomationCLITester:
    """PowerAutomation CLI测试执行器"""
    
    def __init__(self):
        self.base_dir = Path('/home/ubuntu/powerautomation')
        self.cli_dir = self.base_dir / 'mcptool' / 'cli_testing'
        self.test_results = []
        
    def run_command(self, command, description):
        """运行命令并记录结果"""
        print(f"\n🔧 {description}")
        print(f"执行命令: {command}")
        print("=" * 60)
        
        start_time = time.time()
        try:
            # 切换到正确的目录
            os.chdir(self.base_dir)
            
            # 运行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            success = result.returncode == 0
            
            # 记录结果
            test_result = {
                "description": description,
                "command": command,
                "success": success,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
            self.test_results.append(test_result)
            
            # 显示结果
            if success:
                print(f"✅ 成功 (耗时: {duration:.2f}秒)")
                if result.stdout:
                    print("输出:")
                    print(result.stdout)
            else:
                print(f"❌ 失败 (耗时: {duration:.2f}秒)")
                if result.stderr:
                    print("错误:")
                    print(result.stderr)
                if result.stdout:
                    print("输出:")
                    print(result.stdout)
                    
            return success, result
            
        except subprocess.TimeoutExpired:
            print(f"❌ 超时 (>300秒)")
            return False, None
        except Exception as e:
            print(f"❌ 异常: {e}")
            return False, None
    
    def test_basic_functionality(self):
        """测试基础功能"""
        print("\n🎯 第一阶段: 基础功能测试")
        
        # 测试Python环境
        self.run_command(
            "python3 --version",
            "检查Python版本"
        )
        
        # 测试项目结构
        self.run_command(
            "ls -la mcptool/",
            "检查mcptool目录结构"
        )
        
        # 测试CLI工具存在性
        self.run_command(
            "ls -la mcptool/cli_testing/",
            "检查CLI测试工具"
        )
    
    def test_ai_enhanced_features(self):
        """测试AI增强功能"""
        print("\n🤖 第二阶段: AI增强功能测试")
        
        # 运行之前创建的AI增强测试
        self.run_command(
            "python3 ai_enhanced_full_demo.py",
            "运行AI增强功能完整演示"
        )
        
        # 运行综合AI演示
        self.run_command(
            "python3 comprehensive_ai_demo.py",
            "运行综合AI演示"
        )
        
        # 运行AI协调演示
        self.run_command(
            "python3 ai_coordination_demo.py",
            "运行AI协调演示"
        )
    
    def test_real_api_integration(self):
        """测试真实API集成"""
        print("\n🌐 第三阶段: 真实API集成测试")
        
        # 运行真实API验证
        self.run_command(
            "python3 real_api_validator.py",
            "运行真实API验证器"
        )
        
        # 运行增强版API验证
        self.run_command(
            "python3 enhanced_api_validator.py",
            "运行增强版API验证器"
        )
        
        # 运行supermemory API测试
        self.run_command(
            "python3 supermemory_api_tester.py",
            "运行Supermemory API测试"
        )
    
    def test_workflow_engine(self):
        """测试工作流引擎"""
        print("\n⚙️ 第四阶段: 工作流引擎测试")
        
        # 运行工作流引擎测试
        self.run_command(
            "python3 test_workflow_engine_enhanced.py",
            "运行增强版工作流引擎测试"
        )
        
        # 运行高级工作流演示
        self.run_command(
            "python3 advanced_workflow_demo.py",
            "运行高级工作流演示"
        )
    
    def test_complete_suite(self):
        """运行完整测试套件"""
        print("\n🚀 第五阶段: 完整测试套件")
        
        # 运行完整测试套件
        self.run_command(
            "python3 complete_test_suite_real_api.py",
            "运行完整测试套件(真实API版本)"
        )
        
        # 运行AI增强测试套件
        self.run_command(
            "python3 ai_enhanced_test_suite.py",
            "运行AI增强测试套件"
        )
    
    def test_cli_tools(self):
        """测试CLI工具"""
        print("\n💻 第六阶段: CLI工具测试")
        
        # 尝试运行CLI工具(如果导入问题已解决)
        commands = [
            "cd mcptool && python3 -c \"import cli_testing.unified_cli_tester; print('CLI工具导入成功')\"",
            "cd mcptool && python3 -c \"import cli_testing.mcpcoordinator_cli; print('MCP协调器CLI导入成功')\"",
            "cd mcptool && python3 -c \"import cli_testing.unified_cli_tester_v2; print('CLI工具V2导入成功')\""
        ]
        
        for cmd in commands:
            self.run_command(cmd, f"测试CLI工具导入: {cmd.split('import')[1].split(';')[0].strip()}")
    
    def generate_report(self):
        """生成测试报告"""
        print("\n📊 生成测试报告")
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": total_tests - successful_tests,
                "success_rate": f"{success_rate:.1f}%",
                "total_duration": sum(result['duration'] for result in self.test_results)
            },
            "test_results": self.test_results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 保存报告
        report_file = self.base_dir / "cli_test_comprehensive_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 显示摘要
        print(f"\n🎯 测试摘要:")
        print(f"   总测试数: {total_tests}")
        print(f"   成功测试: {successful_tests}")
        print(f"   失败测试: {total_tests - successful_tests}")
        print(f"   成功率: {success_rate:.1f}%")
        print(f"   总耗时: {report['test_summary']['total_duration']:.2f}秒")
        print(f"\n📄 详细报告已保存到: {report_file}")
        
        return report

def main():
    """主函数"""
    print("🚀 PowerAutomation CLI测试执行器启动")
    print("=" * 60)
    
    tester = PowerAutomationCLITester()
    
    try:
        # 执行各阶段测试
        tester.test_basic_functionality()
        tester.test_ai_enhanced_features()
        tester.test_real_api_integration()
        tester.test_workflow_engine()
        tester.test_complete_suite()
        tester.test_cli_tools()
        
        # 生成报告
        report = tester.generate_report()
        
        print("\n🎉 PowerAutomation CLI测试执行完成!")
        
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试执行异常: {e}")
    finally:
        # 确保生成报告
        if hasattr(tester, 'test_results') and tester.test_results:
            tester.generate_report()

if __name__ == "__main__":
    main()

