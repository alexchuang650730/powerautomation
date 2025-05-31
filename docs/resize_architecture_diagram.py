"""
调整架构图尺寸以符合视觉测试要求
"""
import os
from PIL import Image

# 架构图文件路径
ARCHITECTURE_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), 
    "images", 
    "powerautomation_layered_architecture_compact_final.png"
)

# 调整后的架构图文件路径
RESIZED_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__), 
    "images", 
    "powerautomation_layered_architecture_compact_final_resized.png"
)

def resize_image():
    """调整架构图尺寸以符合视觉测试要求"""
    # 打开原始图片
    img = Image.open(ARCHITECTURE_IMAGE_PATH)
    width, height = img.size
    
    # 计算新的尺寸，保持宽高比
    max_height = 1400  # 设置最大高度为1400px，低于测试要求的1500px
    max_width = 2800   # 设置最大宽度为2800px，低于测试要求的3000px
    
    # 计算缩放比例
    scale_width = max_width / width if width > max_width else 1
    scale_height = max_height / height if height > max_height else 1
    scale = min(scale_width, scale_height)  # 选择较小的缩放比例以确保两个维度都不超过限制
    
    # 计算新的尺寸
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # 调整图片尺寸
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)
    
    # 保存调整后的图片
    resized_img.save(RESIZED_IMAGE_PATH)
    
    print(f"原始尺寸: {width}x{height}")
    print(f"调整后尺寸: {new_width}x{new_height}")
    print(f"调整后的图片已保存至: {RESIZED_IMAGE_PATH}")
    
    # 替换原始图片
    os.replace(RESIZED_IMAGE_PATH, ARCHITECTURE_IMAGE_PATH)
    print(f"已用调整后的图片替换原始图片")
    
    return new_width, new_height

if __name__ == "__main__":
    resize_image()
