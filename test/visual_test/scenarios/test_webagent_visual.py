"""
WebAgentB视觉自动化测试
"""
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from test.visual_test.pages.home_page import HomePage
from test.visual_test.utils.test_utils import capture_screenshot, compare_screenshots

class TestWebAgentVisual:
    """WebAgentB视觉自动化测试类"""
    
    def setup_method(self):
        """测试前准备"""
        # 初始化WebDriver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
        # 初始化页面对象
        self.home_page = HomePage(self.driver)
        
        # 创建截图目录
        os.makedirs("test_results/screenshots", exist_ok=True)
    
    def teardown_method(self):
        """测试后清理"""
        if self.driver:
            self.driver.quit()
    
    def test_webagent_card_display(self):
        """测试网页智能体卡片显示"""
        # 打开首页
        self.home_page.open()
        
        # 等待页面加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-card"))
        )
        
        # 捕获网页智能体卡片截图
        web_agent_card = self.driver.find_element(By.CSS_SELECTOR, ".agent-card[data-agent-type='web']")
        screenshot_path = capture_screenshot(self.driver, web_agent_card, "webagent_card")
        
        # 比较截图与基准图
        baseline_path = "test/visual_test/baselines/webagent_card_baseline.png"
        if os.path.exists(baseline_path):
            comparison_result = compare_screenshots(screenshot_path, baseline_path)
            assert comparison_result["match_percentage"] > 95, f"网页智能体卡片显示异常，匹配度: {comparison_result['match_percentage']}%"
        else:
            # 首次运行，将当前截图设为基准图
            os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
            import shutil
            shutil.copy(screenshot_path, baseline_path)
    
    def test_webagent_search_functionality(self):
        """测试网页智能体搜索功能"""
        # 打开首页
        self.home_page.open()
        
        # 等待页面加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-card"))
        )
        
        # 选择网页智能体
        web_agent_card = self.driver.find_element(By.CSS_SELECTOR, ".agent-card[data-agent-type='web']")
        web_agent_card.click()
        
        # 等待输入框出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-input"))
        )
        
        # 输入搜索查询
        input_field = self.driver.find_element(By.CSS_SELECTOR, ".agent-input")
        input_field.clear()
        input_field.send_keys("人工智能最新发展")
        
        # 点击搜索按钮
        search_button = self.driver.find_element(By.CSS_SELECTOR, ".search-button")
        search_button.click()
        
        # 等待搜索结果出现
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results"))
        )
        
        # 捕获搜索结果截图
        search_results = self.driver.find_element(By.CSS_SELECTOR, ".search-results")
        screenshot_path = capture_screenshot(self.driver, search_results, "webagent_search_results")
        
        # 比较截图与基准图
        baseline_path = "test/visual_test/baselines/webagent_search_results_baseline.png"
        if os.path.exists(baseline_path):
            comparison_result = compare_screenshots(screenshot_path, baseline_path)
            assert comparison_result["match_percentage"] > 90, f"网页智能体搜索结果显示异常，匹配度: {comparison_result['match_percentage']}%"
        else:
            # 首次运行，将当前截图设为基准图
            os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
            import shutil
            shutil.copy(screenshot_path, baseline_path)
    
    def test_webagent_semantic_extract(self):
        """测试网页智能体语义提取功能"""
        # 打开首页
        self.home_page.open()
        
        # 等待页面加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-card"))
        )
        
        # 选择网页智能体
        web_agent_card = self.driver.find_element(By.CSS_SELECTOR, ".agent-card[data-agent-type='web']")
        web_agent_card.click()
        
        # 等待输入框出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-input"))
        )
        
        # 输入语义提取请求
        input_field = self.driver.find_element(By.CSS_SELECTOR, ".agent-input")
        input_field.clear()
        input_field.send_keys("分析网页 https://example.com/ai-article 的主要内容")
        
        # 点击提交按钮
        submit_button = self.driver.find_element(By.CSS_SELECTOR, ".submit-button")
        submit_button.click()
        
        # 等待分析结果出现
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".analysis-results"))
        )
        
        # 捕获分析结果截图
        analysis_results = self.driver.find_element(By.CSS_SELECTOR, ".analysis-results")
        screenshot_path = capture_screenshot(self.driver, analysis_results, "webagent_semantic_extract")
        
        # 比较截图与基准图
        baseline_path = "test/visual_test/baselines/webagent_semantic_extract_baseline.png"
        if os.path.exists(baseline_path):
            comparison_result = compare_screenshots(screenshot_path, baseline_path)
            assert comparison_result["match_percentage"] > 90, f"网页智能体语义提取结果显示异常，匹配度: {comparison_result['match_percentage']}%"
        else:
            # 首次运行，将当前截图设为基准图
            os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
            import shutil
            shutil.copy(screenshot_path, baseline_path)
    
    def test_webagent_integration_with_features(self):
        """测试网页智能体与六大特性的集成"""
        # 打开首页
        self.home_page.open()
        
        # 等待页面加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-card"))
        )
        
        # 选择网页智能体
        web_agent_card = self.driver.find_element(By.CSS_SELECTOR, ".agent-card[data-agent-type='web']")
        web_agent_card.click()
        
        # 等待输入框出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-input"))
        )
        
        # 输入特性更新请求
        input_field = self.driver.find_element(By.CSS_SELECTOR, ".agent-input")
        input_field.clear()
        input_field.send_keys("更新网页智能体的内容特性，添加更多结构化数据支持")
        
        # 点击提交按钮
        submit_button = self.driver.find_element(By.CSS_SELECTOR, ".submit-button")
        submit_button.click()
        
        # 等待特性更新结果出现
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".feature-update-results"))
        )
        
        # 捕获特性更新结果截图
        feature_update_results = self.driver.find_element(By.CSS_SELECTOR, ".feature-update-results")
        screenshot_path = capture_screenshot(self.driver, feature_update_results, "webagent_feature_integration")
        
        # 比较截图与基准图
        baseline_path = "test/visual_test/baselines/webagent_feature_integration_baseline.png"
        if os.path.exists(baseline_path):
            comparison_result = compare_screenshots(screenshot_path, baseline_path)
            assert comparison_result["match_percentage"] > 90, f"网页智能体与六大特性集成显示异常，匹配度: {comparison_result['match_percentage']}%"
        else:
            # 首次运行，将当前截图设为基准图
            os.makedirs(os.path.dirname(baseline_path), exist_ok=True)
            import shutil
            shutil.copy(screenshot_path, baseline_path)
