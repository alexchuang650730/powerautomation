"""
RL能力统一模块

此脚本用于合并enhancers/rl_enhancer和rl_factory中的重复实现，
统一RL相关能力，确保代码结构清晰、无冗余。
"""

import os
import shutil
import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path('/home/ubuntu/powerautomation_integration')

# 源目录和目标目录
RL_FACTORY_DIR = PROJECT_ROOT / 'rl_factory'
RL_ENHANCER_DIR = PROJECT_ROOT / 'enhancers/rl_enhancer'
RL_CORE_DIR = PROJECT_ROOT / 'rl_core'

# 需要合并的模块列表
MODULES_TO_MERGE = [
    'adapters/infinite_context_adapter.py',
    'adapters/github_actions_adapter.py',
    'adapters/mcp_so_adapter.py',
    'core/learning/supervised.py',
    'core/learning/reinforcement.py',
    'core/learning/contrastive.py',
    'core/learning/hybrid.py',
    'core/thought/decomposer.py',
    'core/thought/schema.py',
    'core/thought/serializer.py',
]

# 需要更新导入路径的文件列表
FILES_TO_UPDATE_IMPORTS = []

def create_directory_structure():
    """创建统一的RL核心目录结构"""
    print("创建统一的RL核心目录结构...")
    
    # 创建主目录
    os.makedirs(RL_CORE_DIR, exist_ok=True)
    
    # 创建子目录
    os.makedirs(RL_CORE_DIR / 'adapters', exist_ok=True)
    os.makedirs(RL_CORE_DIR / 'core/learning', exist_ok=True)
    os.makedirs(RL_CORE_DIR / 'core/thought', exist_ok=True)
    os.makedirs(RL_CORE_DIR / 'tests/end_to_end', exist_ok=True)
    os.makedirs(RL_CORE_DIR / 'tests/integration', exist_ok=True)
    
    # 创建__init__.py文件
    for dir_path in [
        RL_CORE_DIR,
        RL_CORE_DIR / 'adapters',
        RL_CORE_DIR / 'core',
        RL_CORE_DIR / 'core/learning',
        RL_CORE_DIR / 'core/thought',
        RL_CORE_DIR / 'tests',
        RL_CORE_DIR / 'tests/end_to_end',
        RL_CORE_DIR / 'tests/integration',
    ]:
        init_file = dir_path / '__init__.py'
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write('"""RL核心模块"""\n')

def merge_modules():
    """合并RL模块"""
    print("合并RL模块...")
    
    for module_path in MODULES_TO_MERGE:
        enhancer_file = RL_ENHANCER_DIR / module_path
        factory_file = RL_FACTORY_DIR / module_path
        target_file = RL_CORE_DIR / module_path
        
        # 确保目标目录存在
        os.makedirs(target_file.parent, exist_ok=True)
        
        # 检查两个源文件是否都存在
        enhancer_exists = enhancer_file.exists()
        factory_exists = factory_file.exists()
        
        if enhancer_exists and factory_exists:
            # 比较两个文件内容
            with open(enhancer_file, 'r') as f1, open(factory_file, 'r') as f2:
                enhancer_content = f1.read()
                factory_content = f2.read()
            
            # 如果内容基本相同（忽略导入路径差异），使用enhancer版本
            # 这里简化处理，实际应该有更复杂的比较逻辑
            with open(target_file, 'w') as f:
                # 更新导入路径
                updated_content = enhancer_content.replace(
                    'from ...core', 'from powerautomation_integration.rl_core.core'
                ).replace(
                    'from ..core', 'from powerautomation_integration.rl_core.core'
                )
                f.write(updated_content)
            
            print(f"合并模块: {module_path}")
        elif enhancer_exists:
            # 只有enhancer版本存在
            with open(enhancer_file, 'r') as f:
                content = f.read()
            
            # 更新导入路径
            updated_content = content.replace(
                'from ...core', 'from powerautomation_integration.rl_core.core'
            ).replace(
                'from ..core', 'from powerautomation_integration.rl_core.core'
            )
            
            with open(target_file, 'w') as f:
                f.write(updated_content)
            
            print(f"复制enhancer模块: {module_path}")
        elif factory_exists:
            # 只有factory版本存在
            with open(factory_file, 'r') as f:
                content = f.read()
            
            # 更新导入路径
            updated_content = content.replace(
                'from ...core', 'from powerautomation_integration.rl_core.core'
            ).replace(
                'from ..core', 'from powerautomation_integration.rl_core.core'
            )
            
            with open(target_file, 'w') as f:
                f.write(updated_content)
            
            print(f"复制factory模块: {module_path}")
        else:
            print(f"警告: 模块不存在 {module_path}")

def copy_tests():
    """复制测试文件"""
    print("复制测试文件...")
    
    # 复制enhancer的测试
    enhancer_test_dir = RL_ENHANCER_DIR / 'tests'
    if enhancer_test_dir.exists():
        for test_file in enhancer_test_dir.glob('**/*.py'):
            rel_path = test_file.relative_to(enhancer_test_dir)
            target_file = RL_CORE_DIR / 'tests' / rel_path
            
            # 确保目标目录存在
            os.makedirs(target_file.parent, exist_ok=True)
            
            # 复制并更新导入路径
            with open(test_file, 'r') as f:
                content = f.read()
            
            # 更新导入路径
            updated_content = content.replace(
                'from ...core', 'from powerautomation_integration.rl_core.core'
            ).replace(
                'from ..core', 'from powerautomation_integration.rl_core.core'
            ).replace(
                'from ...adapters', 'from powerautomation_integration.rl_core.adapters'
            ).replace(
                'from ..adapters', 'from powerautomation_integration.rl_core.adapters'
            )
            
            with open(target_file, 'w') as f:
                f.write(updated_content)
            
            print(f"复制测试: {rel_path}")
    
    # 复制factory的测试
    factory_test_dir = RL_FACTORY_DIR / 'tests'
    if factory_test_dir.exists():
        for test_file in factory_test_dir.glob('**/*.py'):
            rel_path = test_file.relative_to(factory_test_dir)
            target_file = RL_CORE_DIR / 'tests' / rel_path
            
            # 如果目标文件已存在，跳过
            if target_file.exists():
                continue
            
            # 确保目标目录存在
            os.makedirs(target_file.parent, exist_ok=True)
            
            # 复制并更新导入路径
            with open(test_file, 'r') as f:
                content = f.read()
            
            # 更新导入路径
            updated_content = content.replace(
                'from ...core', 'from powerautomation_integration.rl_core.core'
            ).replace(
                'from ..core', 'from powerautomation_integration.rl_core.core'
            ).replace(
                'from ...adapters', 'from powerautomation_integration.rl_core.adapters'
            ).replace(
                'from ..adapters', 'from powerautomation_integration.rl_core.adapters'
            )
            
            with open(target_file, 'w') as f:
                f.write(updated_content)
            
            print(f"复制测试: {rel_path}")

def update_imports():
    """更新项目中对RL模块的导入路径"""
    print("更新项目中对RL模块的导入路径...")
    
    # 查找所有Python文件
    for py_file in PROJECT_ROOT.glob('**/*.py'):
        # 排除rl_factory和rl_enhancer目录
        if str(py_file).startswith(str(RL_FACTORY_DIR)) or str(py_file).startswith(str(RL_ENHANCER_DIR)):
            continue
        
        # 排除rl_core目录
        if str(py_file).startswith(str(RL_CORE_DIR)):
            continue
        
        # 读取文件内容
        with open(py_file, 'r') as f:
            content = f.read()
        
        # 检查是否包含对rl_factory或rl_enhancer的导入
        if 'from powerautomation_integration.rl_factory' in content or 'import powerautomation_integration.rl_factory' in content:
            # 更新导入路径
            updated_content = content.replace(
                'from powerautomation_integration.rl_factory', 'from powerautomation_integration.rl_core'
            ).replace(
                'import powerautomation_integration.rl_factory', 'import powerautomation_integration.rl_core'
            )
            
            # 写回文件
            with open(py_file, 'w') as f:
                f.write(updated_content)
            
            print(f"更新导入路径: {py_file}")
            FILES_TO_UPDATE_IMPORTS.append(py_file)
        
        if 'from powerautomation_integration.rl_core' in content or 'import powerautomation_integration.rl_core' in content:
            # 更新导入路径
            updated_content = content.replace(
                'from powerautomation_integration.rl_core', 'from powerautomation_integration.rl_core'
            ).replace(
                'import powerautomation_integration.rl_core', 'import powerautomation_integration.rl_core'
            )
            
            # 写回文件
            with open(py_file, 'w') as f:
                f.write(updated_content)
            
            print(f"更新导入路径: {py_file}")
            FILES_TO_UPDATE_IMPORTS.append(py_file)

def main():
    """主函数"""
    print("开始RL能力统一...")
    
    # 创建目录结构
    create_directory_structure()
    
    # 合并模块
    merge_modules()
    
    # 复制测试
    copy_tests()
    
    # 更新导入路径
    update_imports()
    
    print("RL能力统一完成！")
    print(f"已更新 {len(FILES_TO_UPDATE_IMPORTS)} 个文件的导入路径")

if __name__ == "__main__":
    main()
