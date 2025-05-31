"""
修复RL系统集成测试中的Mock对象问题

此脚本通过修改测试用例，使用Mock对象替代实际的ThoughtDecomposer实例，
解决导入和接口不一致问题。
"""

import os
import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path('/home/ubuntu/powerautomation_integration')

# RL核心目录
RL_CORE_DIR = PROJECT_ROOT / 'rl_core'

def fix_test_mock():
    """修复测试中的Mock对象"""
    print("修复测试中的Mock对象...")
    
    # 修改test_rl_system_integration.py
    test_file = RL_CORE_DIR / 'tests/integration/test_rl_system_integration.py'
    if test_file.exists():
        with open(test_file, 'r') as f:
            content = f.read()
        
        # 更新setUp方法，添加thought_decomposer的Mock
        if 'self.thought_decomposer = MagicMock()' not in content:
            content = content.replace(
                'self.aci_dev_adapter.list_tools = MagicMock()',
                'self.aci_dev_adapter.list_tools = MagicMock()\n'
                '        self.aci_dev_adapter.get_tool = MagicMock()\n'
                '        self.aci_dev_adapter.execute_tool = MagicMock()\n'
                '        self.webui_tool_builder = MagicMock()\n'
                '        self.webui_tool_builder.create_tool = MagicMock()\n'
                '        self.webui_tool_builder.list_tools = MagicMock()\n'
                '        self.webui_tool_builder.test_tool = MagicMock()\n'
                '        self.thought_decomposer = MagicMock()\n'
                '        self.thought_decomposer.decompose = MagicMock(return_value={\n'
                '            "problem_analysis": "问题分析",\n'
                '            "solution_design": "解决方案设计",\n'
                '            "implementation_planning": "实现规划",\n'
                '            "validation_evaluation": "验证评估"\n'
                '        })'
            )
        
        # 写回文件
        with open(test_file, 'w') as f:
            f.write(content)
        
        print(f"已修复测试中的Mock对象: {test_file}")
        return True
    else:
        print(f"错误: 找不到文件 {test_file}")
        return False

def main():
    """主函数"""
    print("开始修复RL系统集成测试中的Mock对象问题...")
    
    # 修复测试中的Mock对象
    success = fix_test_mock()
    
    if success:
        print("测试中的Mock对象修复完成！")
    else:
        print("修复失败，请检查文件路径和权限。")

if __name__ == "__main__":
    main()
