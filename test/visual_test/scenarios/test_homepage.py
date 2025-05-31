"""
端到端视觉自动化测试：主页和智能体选择
"""
import os
import sys
import pytest
from playwright.sync_api import Page, expect

# 测试配置
BASE_URL = "http://localhost:5173"

def test_homepage_visual(page: Page):
    """测试首页视觉效果"""
    # 导航到首页
    page.goto(BASE_URL)
    
    # 等待页面加载完成
    page.wait_for_selector(".agent-card", state="visible")
    
    # 截取屏幕截图
    screenshot_path = os.path.join("reports", "homepage.png")
    page.screenshot(path=screenshot_path)
    
    # 验证关键元素存在
    expect(page.locator(".agent-card")).to_have_count(4)
    expect(page.locator("text=代码智能体")).to_be_visible()
    expect(page.locator("text=PPT智能体")).to_be_visible()
    expect(page.locator("text=网页智能体")).to_be_visible()
    expect(page.locator("text=通用智能体")).to_be_visible()


def test_agent_selection(page: Page):
    """测试智能体选择功能"""
    # 导航到首页
    page.goto(BASE_URL)
    
    # 等待页面加载完成
    page.wait_for_selector(".agent-card", state="visible")
    
    # 选择代码智能体
    page.click("text=代码智能体")
    
    # 验证选择状态
    expect(page.locator(".agent-card.selected")).to_contain_text("代码智能体")
    
    # 截取屏幕截图
    screenshot_path = os.path.join("reports", "code_agent_selected.png")
    page.screenshot(path=screenshot_path)
    
    # 选择PPT智能体
    page.click("text=PPT智能体")
    
    # 验证选择状态
    expect(page.locator(".agent-card.selected")).to_contain_text("PPT智能体")
    
    # 截取屏幕截图
    screenshot_path = os.path.join("reports", "ppt_agent_selected.png")
    page.screenshot(path=screenshot_path)


def test_input_and_response(page: Page):
    """测试输入和响应功能"""
    # 导航到首页
    page.goto(BASE_URL)
    
    # 等待页面加载完成
    page.wait_for_selector(".agent-card", state="visible")
    
    # 选择代码智能体
    page.click("text=代码智能体")
    
    # 输入查询
    page.fill("textarea[placeholder='请输入您的需求...']", "帮我写一个Python函数计算斐波那契数列")
    
    # 点击发送按钮
    page.click("button.send-button")
    
    # 等待响应
    page.wait_for_selector(".response-content", state="visible", timeout=30000)
    
    # 验证响应内容
    response_content = page.locator(".response-content").inner_text()
    assert "def fibonacci" in response_content
    
    # 截取屏幕截图
    screenshot_path = os.path.join("reports", "code_response.png")
    page.screenshot(path=screenshot_path)


def test_feature_update(page: Page):
    """测试特性更新功能"""
    # 导航到首页
    page.goto(BASE_URL)
    
    # 等待页面加载完成
    page.wait_for_selector(".agent-card", state="visible")
    
    # 选择通用智能体
    page.click("text=通用智能体")
    
    # 输入特性更新查询
    page.fill("textarea[placeholder='请输入您的需求...']", "优化PowerAutomation的UI布局特性，使用两栏设计")
    
    # 点击发送按钮
    page.click("button.send-button")
    
    # 等待响应
    page.wait_for_selector(".response-content", state="visible", timeout=30000)
    
    # 验证响应内容
    response_content = page.locator(".response-content").inner_text()
    assert "UI布局特性已更新" in response_content
    
    # 截取屏幕截图
    screenshot_path = os.path.join("reports", "feature_update.png")
    page.screenshot(path=screenshot_path)
