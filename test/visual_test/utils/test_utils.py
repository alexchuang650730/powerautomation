"""
端到端视觉自动化测试：工具类
"""
import os
import sys
import json
import shutil
from PIL import Image, ImageChops
import numpy as np

class ScreenshotComparison:
    """截图比较工具类"""
    
    def __init__(self, baseline_dir=None, diff_dir=None):
        """初始化截图比较工具
        
        Args:
            baseline_dir: 基准图像目录
            diff_dir: 差异图像目录
        """
        self.baseline_dir = baseline_dir or os.path.join(os.path.dirname(__file__), '../baseline')
        self.diff_dir = diff_dir or os.path.join(os.path.dirname(__file__), '../reports/diff')
        
        # 确保目录存在
        os.makedirs(self.baseline_dir, exist_ok=True)
        os.makedirs(self.diff_dir, exist_ok=True)
    
    def compare(self, screenshot, baseline_name, threshold=0.1):
        """比较截图与基准图像
        
        Args:
            screenshot: 截图数据或路径
            baseline_name: 基准图像名称
            threshold: 差异阈值
        
        Returns:
            差异比例
        """
        # 加载截图
        if isinstance(screenshot, str):
            screenshot_img = Image.open(screenshot)
        elif isinstance(screenshot, bytes):
            screenshot_img = Image.open(io.BytesIO(screenshot))
        else:
            screenshot_img = screenshot
        
        # 基准图像路径
        baseline_path = os.path.join(self.baseline_dir, baseline_name)
        
        # 如果基准图像不存在，则保存当前截图作为基准
        if not os.path.exists(baseline_path):
            screenshot_img.save(baseline_path)
            return 0.0
        
        # 加载基准图像
        baseline_img = Image.open(baseline_path)
        
        # 确保两张图片尺寸相同
        if screenshot_img.size != baseline_img.size:
            screenshot_img = screenshot_img.resize(baseline_img.size)
        
        # 计算差异
        diff_img = ImageChops.difference(screenshot_img, baseline_img)
        
        # 计算差异比例
        diff_array = np.array(diff_img)
        diff_ratio = np.count_nonzero(diff_array) / diff_array.size
        
        # 如果差异超过阈值，保存差异图像
        if diff_ratio > threshold:
            diff_path = os.path.join(self.diff_dir, f"diff_{baseline_name}")
            diff_img.save(diff_path)
        
        return diff_ratio
    
    def update_baseline(self, screenshot, baseline_name):
        """更新基准图像
        
        Args:
            screenshot: 截图数据或路径
            baseline_name: 基准图像名称
        """
        # 加载截图
        if isinstance(screenshot, str):
            screenshot_img = Image.open(screenshot)
        elif isinstance(screenshot, bytes):
            screenshot_img = Image.open(io.BytesIO(screenshot))
        else:
            screenshot_img = screenshot
        
        # 保存为基准图像
        baseline_path = os.path.join(self.baseline_dir, baseline_name)
        screenshot_img.save(baseline_path)


class TestConfig:
    """测试配置类"""
    
    def __init__(self, config_path=None):
        """初始化测试配置
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '../config.json')
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 默认配置
            default_config = {
                "baseUrl": "http://localhost:5173",
                "apiUrl": "http://localhost:5000",
                "headless": True,
                "slowMo": 50,
                "viewport": {
                    "width": 1280,
                    "height": 720
                },
                "screenshotDir": "./screenshots",
                "baselineDir": "./baseline",
                "diffDir": "./diff",
                "threshold": 0.1,
                "timeout": 30000
            }
            
            # 保存默认配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            
            return default_config
    
    def get(self, key, default=None):
        """获取配置项
        
        Args:
            key: 配置项键名
            default: 默认值
        
        Returns:
            配置项值
        """
        return self.config.get(key, default)
    
    def update(self, key, value):
        """更新配置项
        
        Args:
            key: 配置项键名
            value: 配置项值
        """
        self.config[key] = value
        
        # 保存配置
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)


class AssertStorage:
    """存储断言工具类"""
    
    def __init__(self, api_url=None):
        """初始化存储断言工具
        
        Args:
            api_url: API URL
        """
        config = TestConfig()
        self.api_url = api_url or config.get("apiUrl")
    
    def verify_feature_stored(self, agent_type, feature_name, contains_text):
        """验证特性是否已存储
        
        Args:
            agent_type: 智能体类型
            feature_name: 特性名称
            contains_text: 包含的文本
        
        Returns:
            验证结果对象
        """
        import requests
        
        # 构建API URL
        url = f"{self.api_url}/api/features/{agent_type}/{feature_name}"
        
        try:
            # 发送请求
            response = requests.get(url)
            
            # 检查响应状态码
            if response.status_code != 200:
                return StorageResult(False, f"API返回错误状态码: {response.status_code}")
            
            # 解析响应
            data = response.json()
            
            # 检查特性值
            feature_value = data.get("value", "")
            if contains_text.lower() in feature_value.lower():
                return StorageResult(True, "特性已正确存储")
            else:
                return StorageResult(False, f"特性值不包含预期文本. 预期: {contains_text}, 实际: {feature_value}")
        
        except Exception as e:
            return StorageResult(False, f"验证特性存储时发生错误: {str(e)}")


class StorageResult:
    """存储验证结果类"""
    
    def __init__(self, stored, message):
        """初始化存储验证结果
        
        Args:
            stored: 是否已存储
            message: 消息
        """
        self.stored = stored
        self.message = message
