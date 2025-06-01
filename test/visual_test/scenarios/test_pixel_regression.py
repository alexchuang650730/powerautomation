/**
 * 像素级视觉回归测试实现
 * 用于确保UI细节符合设计要求
 */
import pytest
from playwright.sync_api import Page, expect
import os
import json
import cv2
import numpy as np
from datetime import datetime
from PIL import Image, ImageChops, ImageDraw

class TestPixelLevelVisualRegression:
    """像素级视觉回归测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前准备"""
        # 导航到首页
        page.goto("http://localhost:3000")
        # 等待页面加载完成
        page.wait_for_selector(".agent-grid-container", state="visible")
        
        # 创建测试结果目录
        self.results_dir = os.path.join(os.getcwd(), "test_results")
        self.snapshots_dir = os.path.join(self.results_dir, "snapshots")
        self.baseline_dir = os.path.join(self.results_dir, "baseline")
        self.diff_dir = os.path.join(self.results_dir, "diff")
        
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs(self.baseline_dir, exist_ok=True)
        os.makedirs(self.diff_dir, exist_ok=True)
    
    def compare_images(self, baseline_path, snapshot_path, diff_path, threshold=0.02):
        """比较两张图片的差异，并生成差异图"""
        if not os.path.exists(baseline_path):
            print(f"基线图片不存在: {baseline_path}")
            return False, 1.0  # 返回最大差异
        
        # 加载图片
        baseline_img = Image.open(baseline_path).convert('RGB')
        snapshot_img = Image.open(snapshot_path).convert('RGB')
        
        # 确保两张图片尺寸相同
        if baseline_img.size != snapshot_img.size:
            snapshot_img = snapshot_img.resize(baseline_img.size)
        
        # 计算差异
        diff_img = ImageChops.difference(baseline_img, snapshot_img)
        
        # 计算差异百分比
        stat = ImageChops.difference(baseline_img, snapshot_img).convert('L').point(lambda x: 255 if x > 0 else 0).getdata()
        diff_pixels = sum(1 for x in stat if x > 0)
        total_pixels = baseline_img.size[0] * baseline_img.size[1]
        diff_percentage = diff_pixels / total_pixels
        
        # 保存差异图片
        diff_with_highlight = snapshot_img.copy()
        draw = ImageDraw.Draw(diff_with_highlight)
        
        # 在差异处绘制红色标记
        diff_data = diff_img.getdata()
        width, height = diff_img.size
        for y in range(height):
            for x in range(width):
                pos = y * width + x
                if sum(diff_data[pos]) > 0:  # 如果有差异
                    draw.rectangle((x, y, x+1, y+1), fill=(255, 0, 0))
        
        diff_with_highlight.save(diff_path)
        
        # 返回比较结果
        return diff_percentage <= threshold, diff_percentage
    
    def test_homepage_pixel_level_regression(self, page: Page):
        """首页像素级回归测试"""
        # 设置桌面尺寸
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 等待页面完全加载
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)  # 额外等待以确保动画完成
        
        # 生成快照文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"homepage_full_{timestamp}.png"
        snapshot_path = os.path.join(self.snapshots_dir, snapshot_name)
        
        # 截取页面快照
        page.screenshot(path=snapshot_path, full_page=True)
        
        # 基线图片路径
        baseline_path = os.path.join(self.baseline_dir, "homepage_full_baseline.png")
        
        # 如果基线不存在，将当前快照设为基线
        if not os.path.exists(baseline_path):
            import shutil
            shutil.copy(snapshot_path, baseline_path)
            print(f"基线图片不存在，已将当前快照设为基线: {baseline_path}")
            return
        
        # 差异图片路径
        diff_path = os.path.join(self.diff_dir, f"homepage_full_diff_{timestamp}.png")
        
        # 比较图片
        is_pass, diff_percentage = self.compare_images(baseline_path, snapshot_path, diff_path)
        
        # 记录测试结果
        result = {
            "test": "homepage_pixel_level_regression",
            "timestamp": timestamp,
            "baseline_path": baseline_path,
            "snapshot_path": snapshot_path,
            "diff_path": diff_path,
            "diff_percentage": diff_percentage,
            "threshold": 0.02,
            "status": "pass" if is_pass else "fail"
        }
        
        # 保存测试结果
        results_file = os.path.join(self.results_dir, "pixel_regression_results.json")
        
        existing_results = []
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                try:
                    existing_results = json.load(f)
                except json.JSONDecodeError:
                    existing_results = []
        
        existing_results.append(result)
        
        with open(results_file, 'w') as f:
            json.dump(existing_results, f, indent=2)
        
        # 断言测试通过
        assert is_pass, f"像素级回归测试失败，差异百分比: {diff_percentage:.2%}"
    
    def test_agent_card_pixel_regression(self, page: Page):
        """智能体卡片像素级回归测试"""
        # 设置桌面尺寸
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 等待页面完全加载
        page.wait_for_load_state("networkidle")
        
        # 获取所有智能体卡片
        cards = page.locator(".agent-card").all()
        
        for i, card in enumerate(cards):
            # 等待卡片完全渲染
            card.wait_for(state="visible")
            
            # 生成快照文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_name = f"agent_card_{i}_{timestamp}.png"
            snapshot_path = os.path.join(self.snapshots_dir, snapshot_name)
            
            # 截取卡片快照
            card.screenshot(path=snapshot_path)
            
            # 基线图片路径
            baseline_path = os.path.join(self.baseline_dir, f"agent_card_{i}_baseline.png")
            
            # 如果基线不存在，将当前快照设为基线
            if not os.path.exists(baseline_path):
                import shutil
                shutil.copy(snapshot_path, baseline_path)
                print(f"基线图片不存在，已将当前快照设为基线: {baseline_path}")
                continue
            
            # 差异图片路径
            diff_path = os.path.join(self.diff_dir, f"agent_card_{i}_diff_{timestamp}.png")
            
            # 比较图片
            is_pass, diff_percentage = self.compare_images(baseline_path, snapshot_path, diff_path)
            
            # 记录测试结果
            result = {
                "test": f"agent_card_{i}_pixel_regression",
                "timestamp": timestamp,
                "baseline_path": baseline_path,
                "snapshot_path": snapshot_path,
                "diff_path": diff_path,
                "diff_percentage": diff_percentage,
                "threshold": 0.02,
                "status": "pass" if is_pass else "fail"
            }
            
            # 保存测试结果
            results_file = os.path.join(self.results_dir, "pixel_regression_results.json")
            
            existing_results = []
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    try:
                        existing_results = json.load(f)
                    except json.JSONDecodeError:
                        existing_results = []
            
            existing_results.append(result)
            
            with open(results_file, 'w') as f:
                json.dump(existing_results, f, indent=2)
            
            # 断言测试通过
            assert is_pass, f"卡片 {i} 像素级回归测试失败，差异百分比: {diff_percentage:.2%}"
    
    def test_two_column_layout_pixel_regression(self, page: Page):
        """两栏布局像素级回归测试"""
        # 设置桌面尺寸
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 等待页面完全加载
        page.wait_for_load_state("networkidle")
        
        # 等待两栏布局容器可见
        two_column = page.locator(".two-column-container")
        two_column.wait_for(state="visible")
        
        # 生成快照文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"two_column_layout_{timestamp}.png"
        snapshot_path = os.path.join(self.snapshots_dir, snapshot_name)
        
        # 截取两栏布局快照
        two_column.screenshot(path=snapshot_path)
        
        # 基线图片路径
        baseline_path = os.path.join(self.baseline_dir, "two_column_layout_baseline.png")
        
        # 如果基线不存在，将当前快照设为基线
        if not os.path.exists(baseline_path):
            import shutil
            shutil.copy(snapshot_path, baseline_path)
            print(f"基线图片不存在，已将当前快照设为基线: {baseline_path}")
            return
        
        # 差异图片路径
        diff_path = os.path.join(self.diff_dir, f"two_column_layout_diff_{timestamp}.png")
        
        # 比较图片
        is_pass, diff_percentage = self.compare_images(baseline_path, snapshot_path, diff_path)
        
        # 记录测试结果
        result = {
            "test": "two_column_layout_pixel_regression",
            "timestamp": timestamp,
            "baseline_path": baseline_path,
            "snapshot_path": snapshot_path,
            "diff_path": diff_path,
            "diff_percentage": diff_percentage,
            "threshold": 0.02,
            "status": "pass" if is_pass else "fail"
        }
        
        # 保存测试结果
        results_file = os.path.join(self.results_dir, "pixel_regression_results.json")
        
        existing_results = []
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                try:
                    existing_results = json.load(f)
                except json.JSONDecodeError:
                    existing_results = []
        
        existing_results.append(result)
        
        with open(results_file, 'w') as f:
            json.dump(existing_results, f, indent=2)
        
        # 断言测试通过
        assert is_pass, f"两栏布局像素级回归测试失败，差异百分比: {diff_percentage:.2%}"
