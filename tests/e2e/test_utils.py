"""
测试辅助函数模块 - 提供可视化页面创建、图像比较等测试辅助功能
"""
import os
import cv2
import json
import numpy as np
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestUtils")

class VisualTestHelper:
    """视觉测试辅助类，提供图像比较和可视化功能"""
    
    def __init__(self, output_dir: str, template_dir: str):
        """
        初始化视觉测试辅助类
        
        Args:
            output_dir: 输出目录
            template_dir: 模板目录
        """
        self.output_dir = output_dir
        self.template_dir = template_dir
        
        # 确保目录存在
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(template_dir, exist_ok=True)
        
        logger.info(f"初始化视觉测试辅助类: 输出目录={output_dir}, 模板目录={template_dir}")
    
    def compare_images(self, expected_image_path: str, actual_image_path: str, threshold: float = 0.95) -> Dict:
        """
        比较两个图像的相似度
        
        Args:
            expected_image_path: 预期图像路径
            actual_image_path: 实际图像路径
            threshold: 相似度阈值，默认0.95
            
        Returns:
            Dict: 比较结果
        """
        logger.info(f"比较图像: 预期={expected_image_path}, 实际={actual_image_path}, 阈值={threshold}")
        
        try:
            # 读取图像
            expected_img = cv2.imread(expected_image_path)
            actual_img = cv2.imread(actual_image_path)
            
            if expected_img is None:
                return {"success": False, "error": f"无法读取预期图像: {expected_image_path}"}
            
            if actual_img is None:
                return {"success": False, "error": f"无法读取实际图像: {actual_image_path}"}
            
            # 调整大小
            if expected_img.shape != actual_img.shape:
                logger.info(f"图像尺寸不同，调整大小: 预期={expected_img.shape}, 实际={actual_img.shape}")
                actual_img = cv2.resize(actual_img, (expected_img.shape[1], expected_img.shape[0]))
            
            # 计算相似度
            result = cv2.matchTemplate(actual_img, expected_img, cv2.TM_CCOEFF_NORMED)
            similarity = result[0][0]
            
            # 生成差异图像
            diff_image_path = self._generate_diff_image(expected_img, actual_img, expected_image_path)
            
            logger.info(f"图像相似度: {similarity}")
            
            return {
                "success": similarity >= threshold,
                "similarity": float(similarity),
                "threshold": threshold,
                "diff_image": diff_image_path
            }
        except Exception as e:
            logger.error(f"比较图像失败: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_diff_image(self, expected_img: np.ndarray, actual_img: np.ndarray, expected_image_path: str) -> str:
        """生成差异图像"""
        # 计算差异
        diff = cv2.absdiff(expected_img, actual_img)
        
        # 生成差异图像路径
        base_name = os.path.basename(expected_image_path)
        name_without_ext = os.path.splitext(base_name)[0]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        diff_image_path = os.path.join(self.output_dir, f"{name_without_ext}_diff_{timestamp}.png")
        
        # 保存差异图像
        cv2.imwrite(diff_image_path, diff)
        
        return diff_image_path
    
    def create_visual_report(self, test_results: List[Dict], report_path: Optional[str] = None) -> str:
        """
        创建视觉测试报告
        
        Args:
            test_results: 测试结果列表
            report_path: 报告路径，如果为None则使用默认路径
            
        Returns:
            str: 报告路径
        """
        if report_path is None:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            report_path = os.path.join(self.output_dir, f"visual_report_{timestamp}.html")
        
        logger.info(f"创建视觉测试报告: {report_path}")
        
        # 生成HTML报告
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Visual Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .test-case { margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
                .success { background-color: #dff0d8; }
                .failure { background-color: #f2dede; }
                .image-container { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
                .image-item { text-align: center; }
                img { max-width: 300px; border: 1px solid #ddd; }
                h1, h2 { color: #333; }
                .summary { margin-bottom: 20px; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Visual Test Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Tests: {total}</p>
                <p>Passed: {passed}</p>
                <p>Failed: {failed}</p>
                <p>Success Rate: {success_rate}%</p>
            </div>
            <h2>Test Cases</h2>
            {test_cases}
        </body>
        </html>
        """
        
        # 生成测试用例HTML
        test_cases_html = ""
        passed = 0
        failed = 0
        
        for i, result in enumerate(test_results):
            status_class = "success" if result.get("success", False) else "failure"
            status_text = "PASS" if result.get("success", False) else "FAIL"
            
            if result.get("success", False):
                passed += 1
            else:
                failed += 1
            
            test_case_html = f"""
            <div class="test-case {status_class}">
                <h3>Test Case #{i+1}: {result.get("name", "Unnamed Test")} - {status_text}</h3>
                <p>Similarity: {result.get("similarity", "N/A")}</p>
                <p>Threshold: {result.get("threshold", "N/A")}</p>
                <div class="image-container">
            """
            
            # 添加预期图像
            if "expected_image" in result:
                test_case_html += f"""
                    <div class="image-item">
                        <p>Expected</p>
                        <img src="{result['expected_image']}" alt="Expected Image">
                    </div>
                """
            
            # 添加实际图像
            if "actual_image" in result:
                test_case_html += f"""
                    <div class="image-item">
                        <p>Actual</p>
                        <img src="{result['actual_image']}" alt="Actual Image">
                    </div>
                """
            
            # 添加差异图像
            if "diff_image" in result:
                test_case_html += f"""
                    <div class="image-item">
                        <p>Difference</p>
                        <img src="{result['diff_image']}" alt="Difference Image">
                    </div>
                """
            
            test_case_html += """
                </div>
            </div>
            """
            
            test_cases_html += test_case_html
        
        # 计算成功率
        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        # 替换模板变量
        html_content = html_content.format(
            total=total,
            passed=passed,
            failed=failed,
            success_rate=round(success_rate, 2),
            test_cases=test_cases_html
        )
        
        # 保存报告
        with open(report_path, "w") as f:
            f.write(html_content)
        
        logger.info(f"视觉测试报告已创建: {report_path}")
        
        return report_path

class TestDataHelper:
    """测试数据辅助类，提供测试数据加载和管理功能"""
    
    def __init__(self, fixtures_dir: str):
        """
        初始化测试数据辅助类
        
        Args:
            fixtures_dir: 测试数据目录
        """
        self.fixtures_dir = fixtures_dir
        
        # 确保目录存在
        os.makedirs(fixtures_dir, exist_ok=True)
        
        logger.info(f"初始化测试数据辅助类: 测试数据目录={fixtures_dir}")
    
    def load_json_fixture(self, fixture_name: str) -> Any:
        """
        加载JSON测试数据
        
        Args:
            fixture_name: 测试数据文件名
            
        Returns:
            Any: 加载的测试数据
        """
        fixture_path = os.path.join(self.fixtures_dir, fixture_name)
        
        logger.info(f"加载JSON测试数据: {fixture_path}")
        
        try:
            with open(fixture_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载JSON测试数据失败: {e}")
            return None
    
    def save_json_fixture(self, fixture_name: str, data: Any) -> bool:
        """
        保存JSON测试数据
        
        Args:
            fixture_name: 测试数据文件名
            data: 要保存的数据
            
        Returns:
            bool: 是否成功
        """
        fixture_path = os.path.join(self.fixtures_dir, fixture_name)
        
        logger.info(f"保存JSON测试数据: {fixture_path}")
        
        try:
            with open(fixture_path, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存JSON测试数据失败: {e}")
            return False
    
    def get_fixture_path(self, fixture_name: str) -> str:
        """
        获取测试数据文件路径
        
        Args:
            fixture_name: 测试数据文件名
            
        Returns:
            str: 测试数据文件路径
        """
        return os.path.join(self.fixtures_dir, fixture_name)

class MockWebServer:
    """模拟Web服务器，用于测试网页相关功能"""
    
    def __init__(self, port: int = 8000, content_dir: str = None):
        """
        初始化模拟Web服务器
        
        Args:
            port: 端口号
            content_dir: 内容目录
        """
        self.port = port
        self.content_dir = content_dir or os.path.join(os.path.dirname(__file__), "mock_web_content")
        self.server_process = None
        
        # 确保目录存在
        os.makedirs(self.content_dir, exist_ok=True)
        
        logger.info(f"初始化模拟Web服务器: 端口={port}, 内容目录={self.content_dir}")
    
    def start(self) -> bool:
        """
        启动服务器
        
        Returns:
            bool: 是否成功
        """
        import subprocess
        import time
        
        logger.info(f"启动模拟Web服务器: 端口={self.port}")
        
        try:
            # 使用Python内置的HTTP服务器
            cmd = ["python", "-m", "http.server", str(self.port)]
            
            # 在内容目录中启动服务器
            self.server_process = subprocess.Popen(
                cmd,
                cwd=self.content_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待服务器启动
            time.sleep(1)
            
            # 检查服务器是否成功启动
            if self.server_process.poll() is not None:
                stderr = self.server_process.stderr.read().decode()
                logger.error(f"启动模拟Web服务器失败: {stderr}")
                return False
            
            logger.info(f"模拟Web服务器已启动: 端口={self.port}")
            return True
        except Exception as e:
            logger.error(f"启动模拟Web服务器失败: {e}")
            return False
    
    def stop(self) -> bool:
        """
        停止服务器
        
        Returns:
            bool: 是否成功
        """
        logger.info("停止模拟Web服务器")
        
        if self.server_process is None:
            logger.warning("模拟Web服务器未启动")
            return True
        
        try:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            self.server_process = None
            logger.info("模拟Web服务器已停止")
            return True
        except Exception as e:
            logger.error(f"停止模拟Web服务器失败: {e}")
            return False
    
    def create_test_page(self, page_name: str, content: str) -> str:
        """
        创建测试页面
        
        Args:
            page_name: 页面名称
            content: 页面内容
            
        Returns:
            str: 页面URL
        """
        page_path = os.path.join(self.content_dir, page_name)
        
        logger.info(f"创建测试页面: {page_path}")
        
        try:
            with open(page_path, "w") as f:
                f.write(content)
            
            page_url = f"http://localhost:{self.port}/{page_name}"
            logger.info(f"测试页面已创建: {page_url}")
            
            return page_url
        except Exception as e:
            logger.error(f"创建测试页面失败: {e}")
            return None

# 辅助函数
def setup_test_environment(base_dir: Optional[str] = None) -> Dict:
    """
    设置测试环境
    
    Args:
        base_dir: 基础目录，如果为None则使用当前目录
        
    Returns:
        Dict: 测试环境配置
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建测试目录
    test_dirs = {
        "output": os.path.join(base_dir, "output"),
        "templates": os.path.join(base_dir, "templates"),
        "fixtures": os.path.join(base_dir, "fixtures"),
        "mock_web": os.path.join(base_dir, "mock_web_content")
    }
    
    for dir_name, dir_path in test_dirs.items():
        os.makedirs(dir_path, exist_ok=True)
    
    # 创建辅助对象
    visual_helper = VisualTestHelper(test_dirs["output"], test_dirs["templates"])
    data_helper = TestDataHelper(test_dirs["fixtures"])
    mock_server = MockWebServer(port=8000, content_dir=test_dirs["mock_web"])
    
    return {
        "base_dir": base_dir,
        "dirs": test_dirs,
        "visual_helper": visual_helper,
        "data_helper": data_helper,
        "mock_server": mock_server
    }

def cleanup_test_environment(env: Dict) -> bool:
    """
    清理测试环境
    
    Args:
        env: 测试环境配置
        
    Returns:
        bool: 是否成功
    """
    logger.info("清理测试环境")
    
    try:
        # 停止模拟Web服务器
        if "mock_server" in env:
            env["mock_server"].stop()
        
        return True
    except Exception as e:
        logger.error(f"清理测试环境失败: {e}")
        return False
