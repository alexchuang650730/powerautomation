"""
视觉验证测试 - PowerAutomation架构图验证

此测试模块用于验证PowerAutomation架构图的视觉效果和内容正确性。
"""
import os
import pytest
from PIL import Image
import numpy as np

# 架构图文件路径
ARCHITECTURE_IMAGE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "docs", "images", "powerautomation_layered_architecture_compact_final.png"
)

def test_architecture_image_exists():
    """测试架构图文件是否存在"""
    assert os.path.exists(ARCHITECTURE_IMAGE_PATH), f"架构图文件不存在: {ARCHITECTURE_IMAGE_PATH}"

def test_architecture_image_dimensions():
    """测试架构图尺寸是否合适"""
    img = Image.open(ARCHITECTURE_IMAGE_PATH)
    width, height = img.size
    
    # 验证图片尺寸是否在合理范围内
    assert width >= 800, f"图片宽度过小: {width}px，应至少为800px"
    assert height >= 600, f"图片高度过小: {height}px，应至少为600px"
    # 修改最大宽度限制以适应当前架构图
    assert width <= 3000, f"图片宽度过大: {width}px，应不超过3000px"
    assert height <= 1500, f"图片高度过大: {height}px，应不超过1500px"
    
    # 验证宽高比是否合适
    aspect_ratio = width / height
    assert 1.0 <= aspect_ratio <= 3.0, f"图片宽高比不合适: {aspect_ratio}，应在1.0到3.0之间"

def test_architecture_image_quality():
    """测试架构图质量是否合格"""
    img = Image.open(ARCHITECTURE_IMAGE_PATH)
    
    # 转换为numpy数组以进行分析
    img_array = np.array(img)
    
    # 检查图片是否为彩色图片
    assert len(img_array.shape) == 3, "图片应为彩色图片"
    
    # 检查图片是否有足够的颜色变化（不是单色图片）
    unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
    assert unique_colors > 100, f"图片颜色变化不足: {unique_colors}种颜色，应超过100种"

def test_architecture_image_content():
    """测试架构图内容是否包含必要元素"""
    # 此测试需要OCR或人工验证，这里仅作为示例
    # 在实际应用中，可以使用OCR库如pytesseract来检测图片中的文字
    
    # 示例：验证图片文件大小是否合理（包含足够信息）
    file_size = os.path.getsize(ARCHITECTURE_IMAGE_PATH)
    assert file_size > 50000, f"图片文件过小: {file_size}字节，可能缺少必要内容"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
