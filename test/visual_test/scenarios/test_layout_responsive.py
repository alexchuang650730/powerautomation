/**
 * 视觉测试增强：布局方向和响应式断言
 * 用于验证UI布局的方向性和响应式表现
 */
import pytest
from playwright.sync_api import Page, expect
import re
import os
import json
from datetime import datetime

class TestLayoutAndResponsive:
    """测试UI布局方向和响应式表现"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前准备"""
        # 导航到首页
        page.goto("http://localhost:3000")
        # 等待页面加载完成
        page.wait_for_selector(".agent-grid-container", state="visible")
    
    def test_agent_cards_horizontal_layout(self, page: Page):
        """测试智能体卡片的横向布局"""
        # 获取智能体卡片容器
        agent_grid = page.locator(".agent-grid-container")
        
        # 验证容器使用了网格布局
        expect(agent_grid).to_have_css("display", "grid")
        
        # 验证网格列数为4（横向布局）
        grid_template_columns = page.evaluate("""() => {
            const container = document.querySelector('.agent-grid-container');
            return window.getComputedStyle(container).gridTemplateColumns;
        }""")
        
        # 检查是否有4列（会返回类似 "1fr 1fr 1fr 1fr" 的值）
        columns_count = len(grid_template_columns.split())
        assert columns_count == 4, f"期望4列横向布局，实际为{columns_count}列"
        
        # 验证卡片排列方向
        cards = page.locator(".agent-card").all()
        assert len(cards) == 4, "应该有4个智能体卡片"
        
        # 获取第一个和第二个卡片的位置
        first_card_box = cards[0].bounding_box()
        second_card_box = cards[1].bounding_box()
        
        # 横向布局中，第二个卡片应该在第一个卡片的右侧
        # 即第二个卡片的x坐标应该大于第一个卡片的x坐标
        assert second_card_box['x'] > first_card_box['x'], "卡片未按横向排列"
    
    def test_responsive_layout_desktop(self, page: Page):
        """测试桌面端响应式布局"""
        # 设置桌面尺寸
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 等待布局调整
        page.wait_for_timeout(500)
        
        # 验证智能体卡片容器的网格列数
        grid_template_columns = page.evaluate("""() => {
            const container = document.querySelector('.agent-grid-container');
            return window.getComputedStyle(container).gridTemplateColumns;
        }""")
        
        # 桌面端应该是4列布局
        columns_count = len(grid_template_columns.split())
        assert columns_count == 4, f"桌面端期望4列布局，实际为{columns_count}列"
    
    def test_responsive_layout_tablet(self, page: Page):
        """测试平板端响应式布局"""
        # 设置平板尺寸
        page.set_viewport_size({"width": 768, "height": 1024})
        
        # 等待布局调整
        page.wait_for_timeout(500)
        
        # 验证智能体卡片容器的网格列数
        grid_template_columns = page.evaluate("""() => {
            const container = document.querySelector('.agent-grid-container');
            return window.getComputedStyle(container).gridTemplateColumns;
        }""")
        
        # 平板端应该是2列布局
        columns_count = len(grid_template_columns.split())
        assert columns_count == 2, f"平板端期望2列布局，实际为{columns_count}列"
    
    def test_responsive_layout_mobile(self, page: Page):
        """测试移动端响应式布局"""
        # 设置移动端尺寸
        page.set_viewport_size({"width": 375, "height": 667})
        
        # 等待布局调整
        page.wait_for_timeout(500)
        
        # 验证智能体卡片容器的网格列数
        grid_template_columns = page.evaluate("""() => {
            const container = document.querySelector('.agent-grid-container');
            return window.getComputedStyle(container).gridTemplateColumns;
        }""")
        
        # 移动端应该是1列布局
        columns_count = len(grid_template_columns.split())
        assert columns_count == 1, f"移动端期望1列布局，实际为{columns_count}列"
    
    def test_two_column_layout_below_agents(self, page: Page):
        """测试智能体下方的两栏布局"""
        # 设置桌面尺寸
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 等待布局调整
        page.wait_for_timeout(500)
        
        # 验证两栏布局容器存在
        two_column_container = page.locator(".two-column-container")
        expect(two_column_container).to_be_visible()
        
        # 验证左侧任务进度栏
        task_progress = page.locator(".task-progress-container")
        expect(task_progress).to_be_visible()
        
        # 验证右侧任务回放栏
        task_playback = page.locator(".task-playback-container")
        expect(task_playback).to_be_visible()
        
        # 获取两栏的位置信息
        progress_box = task_progress.bounding_box()
        playback_box = task_playback.bounding_box()
        
        # 验证左右布局：任务进度在左，任务回放在右
        assert progress_box['x'] < playback_box['x'], "两栏布局错误：任务进度应在左侧，任务回放应在右侧"
        
        # 验证两栏宽度比例（大致为1:1）
        progress_width = progress_box['width']
        playback_width = playback_box['width']
        width_ratio = progress_width / playback_width
        
        assert 0.8 <= width_ratio <= 1.2, f"两栏宽度比例不均衡，当前比例为{width_ratio}"
    
    def test_platform_title_centered(self, page: Page):
        """测试平台标题居中"""
        # 获取平台标题元素
        platform_title = page.locator(".platform-title")
        expect(platform_title).to_be_visible()
        
        # 获取标题和页面的位置信息
        title_box = platform_title.bounding_box()
        page_width = page.viewport_size['width']
        
        # 计算标题中心点
        title_center = title_box['x'] + title_box['width'] / 2
        page_center = page_width / 2
        
        # 验证标题居中（允许5像素误差）
        assert abs(title_center - page_center) <= 5, "平台标题未居中显示"
    
    def test_visual_regression_with_snapshot(self, page: Page):
        """使用快照进行视觉回归测试"""
        # 设置桌面尺寸
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        # 等待页面完全加载
        page.wait_for_load_state("networkidle")
        
        # 创建快照目录
        snapshot_dir = os.path.join(os.getcwd(), "test_results", "snapshots")
        os.makedirs(snapshot_dir, exist_ok=True)
        
        # 生成快照文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = os.path.join(snapshot_dir, f"homepage_snapshot_{timestamp}.png")
        
        # 截取页面快照
        page.screenshot(path=snapshot_path, full_page=True)
        
        # 记录测试结果
        result = {
            "test": "visual_regression_with_snapshot",
            "timestamp": timestamp,
            "snapshot_path": snapshot_path,
            "viewport": {"width": 1920, "height": 1080},
            "status": "completed"
        }
        
        # 保存测试结果
        results_file = os.path.join(os.getcwd(), "test_results", "visual_test_results.json")
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
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
        
        # 验证快照文件已创建
        assert os.path.exists(snapshot_path), "快照文件未创建成功"
