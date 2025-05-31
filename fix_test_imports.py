"""
修复RL系统集成测试的导入路径问题
"""

import os
import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path('/home/ubuntu/powerautomation_integration')

def fix_test_imports():
    """修复测试文件中的导入路径问题"""
    print("修复测试文件中的导入路径问题...")
    
    # 修复rl_core/tests/integration/test_rl_system_integration.py
    test_file = PROJECT_ROOT / 'rl_core/tests/integration/test_rl_system_integration.py'
    
    if test_file.exists():
        with open(test_file, 'r') as f:
            content = f.read()
        
        # 更新导入路径
        updated_content = content.replace(
            'from powerautomation_integration.enhancers.rl_enhancer.core.learning.hybrid import HybridLearningArchitecture',
            'from powerautomation_integration.rl_core.core.learning.hybrid import HybridLearningArchitecture'
        ).replace(
            'from enhancers.rl_enhancer.core.learning.hybrid import HybridLearningArchitecture',
            'from powerautomation_integration.rl_core.core.learning.hybrid import HybridLearningArchitecture'
        )
        
        with open(test_file, 'w') as f:
            f.write(updated_content)
        
        print(f"已修复: {test_file}")
    
    # 查找并修复所有测试文件
    for test_file in PROJECT_ROOT.glob('rl_core/tests/**/*.py'):
        with open(test_file, 'r') as f:
            content = f.read()
        
        # 检查是否包含对enhancers/rl_enhancer或rl_factory的导入
        if 'from powerautomation_integration.enhancers.rl_enhancer' in content or 'import powerautomation_integration.enhancers.rl_enhancer' in content:
            # 更新导入路径
            updated_content = content.replace(
                'from powerautomation_integration.enhancers.rl_enhancer', 
                'from powerautomation_integration.rl_core'
            ).replace(
                'import powerautomation_integration.enhancers.rl_enhancer', 
                'import powerautomation_integration.rl_core'
            )
            
            # 写回文件
            with open(test_file, 'w') as f:
                f.write(updated_content)
            
            print(f"已修复导入路径: {test_file}")
        
        if 'from powerautomation_integration.rl_factory' in content or 'import powerautomation_integration.rl_factory' in content:
            # 更新导入路径
            updated_content = content.replace(
                'from powerautomation_integration.rl_factory', 
                'from powerautomation_integration.rl_core'
            ).replace(
                'import powerautomation_integration.rl_factory', 
                'import powerautomation_integration.rl_core'
            )
            
            # 写回文件
            with open(test_file, 'w') as f:
                f.write(updated_content)
            
            print(f"已修复导入路径: {test_file}")
        
        # 修复相对导入
        if 'from enhancers.rl_enhancer' in content:
            updated_content = content.replace(
                'from enhancers.rl_enhancer', 
                'from powerautomation_integration.rl_core'
            )
            
            # 写回文件
            with open(test_file, 'w') as f:
                f.write(updated_content)
            
            print(f"已修复相对导入: {test_file}")
        
        if 'from rl_factory' in content:
            updated_content = content.replace(
                'from rl_factory', 
                'from powerautomation_integration.rl_core'
            )
            
            # 写回文件
            with open(test_file, 'w') as f:
                f.write(updated_content)
            
            print(f"已修复相对导入: {test_file}")

def main():
    """主函数"""
    print("开始修复导入路径问题...")
    
    # 修复测试导入
    fix_test_imports()
    
    print("导入路径修复完成！")

if __name__ == "__main__":
    main()
