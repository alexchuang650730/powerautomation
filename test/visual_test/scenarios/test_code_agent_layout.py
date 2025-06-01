/**
 * 视觉测试 - 测试代码智能体UI布局
 * 验证两栏布局、任务进度和代码回放功能的视觉呈现
 */
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from PIL import Image, ImageChops
import numpy as np

class TestCodeAgentLayout:
    @pytest.fixture(scope="class")
    def driver(self):
        """设置Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()
    
    def test_two_column_layout(self, driver):
        """测试代码智能体的两栏布局"""
        # 导航到代码智能体页面
        driver.get("http://localhost:3000/code-agent")
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "code-agent-container"))
        )
        
        # 获取左右两栏元素
        left_column = driver.find_element(By.CLASS_NAME, "left-column")
        right_column = driver.find_element(By.CLASS_NAME, "right-column")
        
        # 验证两栏都存在
        assert left_column is not None, "左侧栏不存在"
        assert right_column is not None, "右侧栏不存在"
        
        # 验证左栏包含任务进度组件
        task_progress = left_column.find_element(By.CLASS_NAME, "task-progress-container")
        assert task_progress is not None, "左侧栏中没有任务进度组件"
        
        # 验证右栏包含代码编辑器和回放组件
        code_editor = right_column.find_element(By.CLASS_NAME, "code-editor-container")
        code_playback = right_column.find_element(By.CLASS_NAME, "code-playback-container")
        assert code_editor is not None, "右侧栏中没有代码编辑器组件"
        assert code_playback is not None, "右侧栏中没有代码回放组件"
        
        # 验证左右栏宽度比例（左栏约占40%，右栏约占60%）
        window_width = driver.execute_script("return window.innerWidth")
        left_width = left_column.size['width']
        right_width = right_column.size['width']
        
        left_ratio = left_width / window_width
        right_ratio = right_width / window_width
        
        assert 0.35 <= left_ratio <= 0.45, f"左侧栏宽度比例不正确: {left_ratio}"
        assert 0.55 <= right_ratio <= 0.65, f"右侧栏宽度比例不正确: {right_ratio}"
        
        # 截图保存
        driver.save_screenshot("code_agent_two_column_layout.png")
    
    def test_task_progress_component(self, driver):
        """测试任务进度组件的视觉呈现"""
        # 导航到代码智能体页面
        driver.get("http://localhost:3000/code-agent")
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "task-progress-container"))
        )
        
        # 获取任务进度组件
        task_progress = driver.find_element(By.CLASS_NAME, "task-progress-container")
        
        # 验证任务进度组件的标题
        header = task_progress.find_element(By.CLASS_NAME, "task-progress-header")
        assert "任务进度" in header.text, "任务进度组件标题不正确"
        
        # 验证任务列表存在
        task_list = task_progress.find_element(By.CLASS_NAME, "task-list")
        assert task_list is not None, "任务列表不存在"
        
        # 验证任务项目存在
        task_items = task_list.find_elements(By.CLASS_NAME, "task-item")
        assert len(task_items) > 0, "任务列表为空"
        
        # 验证当前任务高亮显示
        current_task = task_list.find_element(By.CLASS_NAME, "current")
        assert current_task is not None, "当前任务没有高亮显示"
        
        # 验证任务图标显示
        task_icons = task_list.find_elements(By.CLASS_NAME, "task-icon")
        assert len(task_icons) > 0, "任务图标不存在"
        
        # 截图保存
        task_progress.screenshot("task_progress_component.png")
    
    def test_code_playback_component(self, driver):
        """测试代码回放组件的视觉呈现"""
        # 导航到代码智能体页面
        driver.get("http://localhost:3000/code-agent")
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "code-playback-container"))
        )
        
        # 获取代码回放组件
        code_playback = driver.find_element(By.CLASS_NAME, "code-playback-container")
        
        # 验证代码回放组件的标题
        header = code_playback.find_element(By.CLASS_NAME, "playback-header")
        assert "代码回放" in header.text, "代码回放组件标题不正确"
        
        # 验证代码编辑器存在
        code_editor = code_playback.find_element(By.CLASS_NAME, "code-editor")
        assert code_editor is not None, "代码编辑器不存在"
        
        # 验证播放控制按钮存在
        play_button = code_playback.find_element(By.CLASS_NAME, "play-button")
        pause_button = code_playback.find_element(By.CLASS_NAME, "pause-button")
        step_forward_button = code_playback.find_element(By.CLASS_NAME, "step-forward-button")
        step_backward_button = code_playback.find_element(By.CLASS_NAME, "step-backward-button")
        
        assert play_button is not None, "播放按钮不存在"
        assert pause_button is not None, "暂停按钮不存在"
        assert step_forward_button is not None, "前进按钮不存在"
        assert step_backward_button is not None, "后退按钮不存在"
        
        # 验证进度条存在
        progress_bar = code_playback.find_element(By.CLASS_NAME, "playback-progress")
        assert progress_bar is not None, "进度条不存在"
        
        # 验证速度控制存在
        speed_control = code_playback.find_element(By.CLASS_NAME, "speed-control")
        assert speed_control is not None, "速度控制不存在"
        
        # 截图保存
        code_playback.screenshot("code_playback_component.png")
    
    def test_responsive_layout(self, driver):
        """测试响应式布局在不同屏幕尺寸下的表现"""
        # 测试桌面尺寸
        driver.set_window_size(1920, 1080)
        driver.get("http://localhost:3000/code-agent")
        time.sleep(2)  # 等待布局调整
        driver.save_screenshot("code_agent_desktop.png")
        
        # 验证桌面尺寸下的两栏布局
        left_column = driver.find_element(By.CLASS_NAME, "left-column")
        right_column = driver.find_element(By.CLASS_NAME, "right-column")
        assert left_column.is_displayed(), "桌面尺寸下左侧栏不可见"
        assert right_column.is_displayed(), "桌面尺寸下右侧栏不可见"
        
        # 测试平板尺寸
        driver.set_window_size(768, 1024)
        time.sleep(2)  # 等待布局调整
        driver.save_screenshot("code_agent_tablet.png")
        
        # 验证平板尺寸下的布局
        try:
            left_column = driver.find_element(By.CLASS_NAME, "left-column")
            right_column = driver.find_element(By.CLASS_NAME, "right-column")
            # 平板尺寸下可能是堆叠布局或仍保持两栏
            if left_column.is_displayed() and right_column.is_displayed():
                # 如果仍是两栏，验证宽度比例是否调整
                window_width = driver.execute_script("return window.innerWidth")
                left_width = left_column.size['width']
                right_width = right_column.size['width']
                
                # 平板尺寸下可能调整比例或变为堆叠
                if left_width + right_width > window_width * 0.9:
                    # 堆叠布局
                    left_top = left_column.location['y']
                    right_top = right_column.location['y']
                    assert abs(left_top - right_top) > 10, "平板尺寸下应为堆叠布局"
        except:
            # 可能布局已完全改变，无法通过相同的类名找到元素
            pass
        
        # 测试手机尺寸
        driver.set_window_size(375, 812)
        time.sleep(2)  # 等待布局调整
        driver.save_screenshot("code_agent_mobile.png")
        
        # 验证手机尺寸下的布局
        # 手机尺寸下应该是堆叠布局，且可能有折叠/展开功能
        try:
            # 检查是否有折叠/展开按钮
            toggle_button = driver.find_element(By.CLASS_NAME, "toggle-columns-button")
            assert toggle_button is not None, "手机尺寸下应有折叠/展开按钮"
        except:
            # 如果没有折叠/展开按钮，则验证是否为堆叠布局
            try:
                left_column = driver.find_element(By.CLASS_NAME, "left-column")
                right_column = driver.find_element(By.CLASS_NAME, "right-column")
                
                left_top = left_column.location['y']
                right_top = right_column.location['y']
                assert abs(left_top - right_top) > 10, "手机尺寸下应为堆叠布局"
            except:
                # 可能布局已完全改变，无法通过相同的类名找到元素
                pass
    
    def test_visual_regression(self, driver):
        """视觉回归测试，与基准图像比较"""
        # 导航到代码智能体页面
        driver.get("http://localhost:3000/code-agent")
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "code-agent-container"))
        )
        
        # 截取当前页面截图
        driver.save_screenshot("current_code_agent.png")
        
        # 如果存在基准图像，进行比较
        baseline_path = "baseline_code_agent.png"
        if os.path.exists(baseline_path):
            # 加载图像
            current_img = Image.open("current_code_agent.png")
            baseline_img = Image.open(baseline_path)
            
            # 确保尺寸一致
            if current_img.size != baseline_img.size:
                baseline_img = baseline_img.resize(current_img.size)
            
            # 计算差异
            diff = ImageChops.difference(current_img, baseline_img)
            diff_array = np.array(diff)
            
            # 计算差异百分比
            diff_percentage = np.sum(diff_array > 0) / (diff_array.size / 3) * 100
            
            # 保存差异图像
            diff.save("diff_code_agent.png")
            
            # 验证差异在可接受范围内（允许5%的差异）
            assert diff_percentage <= 5, f"视觉回归测试失败，差异百分比: {diff_percentage}%"
        else:
            # 如果不存在基准图像，将当前图像设为基准
            import shutil
            shutil.copy("current_code_agent.png", baseline_path)
            pytest.skip("基准图像不存在，已创建新的基准图像")
