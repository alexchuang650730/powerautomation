"""
更新通用智能体六大特性中的UI布局特性，集成新的图标和模式样式切换功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.features.agent_features import update_agent_features, get_agent_features

def update_general_agent_ui_features():
    """更新通用智能体的UI布局特性，集成新的图标和模式样式切换功能"""
    
    # 获取当前通用智能体特性
    current_features = get_agent_features('general_agent')
    
    # 更新UI布局特性，集成新的图标和模式样式切换
    updated_ui_layout = """通用智能体的UI布局特性：
    1. 横向四等分智能体卡片布局，支持响应式设计
    2. 每种模式选中时显示专属图标和样式：
       - PPT模式：使用自定义图标，选中时显示红色主题
       - 代码模式：选中时显示蓝色主题
       - 网页模式：选中时显示绿色主题
       - 通用模式：选中时显示紫色主题
    3. 平台标题使用渐变色和优化字体，提升视觉效果
    4. 输入区支持场景选择和联网开关
    """
    
    # 准备更新的特性字典
    features_to_update = {
        'ui_layout': updated_ui_layout
    }
    
    # 更新通用智能体特性
    result = update_agent_features('general_agent', features_to_update)
    
    return result

if __name__ == '__main__':
    # 执行更新
    result = update_general_agent_ui_features()
    print("通用智能体UI布局特性更新结果:")
    print(f"更新特性数量: {result['updated_count']}")
    print(f"更新后的UI布局特性: {result['features']['ui_layout']}")
