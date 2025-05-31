"""
修复ThoughtDecomposer类的decompose方法

此脚本用于修复ThoughtDecomposer类的decompose方法，
将其从静态方法改为实例方法，确保测试用例能顺利通过。
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path('/home/ubuntu/powerautomation_integration')

# RL核心目录
RL_CORE_DIR = PROJECT_ROOT / 'rl_core'

def fix_decomposer_method():
    """修复ThoughtDecomposer类的decompose方法"""
    print("修复ThoughtDecomposer类的decompose方法...")
    
    # 修改decomposer.py
    decomposer_path = RL_CORE_DIR / 'core/thought/decomposer.py'
    if decomposer_path.exists():
        with open(decomposer_path, 'r') as f:
            content = f.read()
        
        # 修复decompose方法
        # 1. 移除@staticmethod装饰器
        # 2. 修正参数列表，只保留self和thought_process
        if '@staticmethod\n    def decompose(self, thought_process):' in content:
            content = content.replace(
                '@staticmethod\n    def decompose(self, thought_process):',
                'def decompose(self, thought_process):'
            )
        
        # 写回文件
        with open(decomposer_path, 'w') as f:
            f.write(content)
        
        print(f"已修复ThoughtDecomposer类的decompose方法: {decomposer_path}")
        return True
    else:
        print(f"错误: 找不到文件 {decomposer_path}")
        return False

def main():
    """主函数"""
    print("开始修复ThoughtDecomposer类的decompose方法...")
    
    # 修复decompose方法
    success = fix_decomposer_method()
    
    if success:
        print("ThoughtDecomposer类的decompose方法修复完成！")
    else:
        print("修复失败，请检查文件路径和权限。")

if __name__ == "__main__":
    main()
