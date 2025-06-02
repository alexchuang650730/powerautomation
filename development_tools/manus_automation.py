"""
Manus.im自动化访问模块 - 使用Playwright实现自动访问、任务获取和指令发送
版本: 1.0.0
更新日期: 2025-06-02
"""

import os
import sys
import json
import time
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("manus_automation.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ManusAutomation")

class ManusAutomation:
    """
    Manus.im自动化访问类
    负责自动访问manus.im、获取任务和发送指令
    """
    
    def __init__(self, manus_url: str = "https://manus.im/app/cE2WJJSUHuhRTdnphepSdi"):
        """
        初始化Manus自动化访问
        
        Args:
            manus_url: Manus.im的URL
        """
        self.manus_url = manus_url
        self.browser = None
        self.context = None
        self.page = None
        self.is_initialized = False
        
        logger.info(f"ManusAutomation初始化完成，目标URL: {manus_url}")
    
    async def initialize(self, headless: bool = True):
        """
        初始化Playwright浏览器
        
        Args:
            headless: 是否使用无头模式
        """
        if self.is_initialized:
            logger.info("浏览器已初始化，跳过")
            return
        
        logger.info(f"初始化Playwright浏览器，headless={headless}")
        
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=headless)
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            self.page = await self.context.new_page()
            self.is_initialized = True
            
            logger.info("Playwright浏览器初始化成功")
        except Exception as e:
            logger.error(f"初始化Playwright浏览器失败: {str(e)}")
            raise
    
    async def navigate_to_manus(self, wait_for_load: bool = True):
        """
        导航到Manus.im
        
        Args:
            wait_for_load: 是否等待页面加载完成
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"导航到Manus.im: {self.manus_url}")
        
        try:
            await self.page.goto(self.manus_url)
            
            if wait_for_load:
                # 等待页面加载完成
                await self.page.wait_for_load_state("networkidle")
                
                # 等待主要内容加载
                await self.page.wait_for_selector(".main-content", timeout=30000)
                
                logger.info("Manus.im页面加载完成")
            
            return True
        except Exception as e:
            logger.error(f"导航到Manus.im失败: {str(e)}")
            return False
    
    async def get_task_list(self, keyword: str = "powerautomation") -> List[Dict[str, Any]]:
        """
        获取任务列表
        
        Args:
            keyword: 任务关键词
            
        Returns:
            任务列表
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"获取任务列表，关键词: {keyword}")
        
        try:
            # 等待任务列表加载
            await self.page.wait_for_selector(".task-list", timeout=30000)
            
            # 获取所有任务元素
            task_elements = await self.page.query_selector_all(".task-item")
            
            tasks = []
            for element in task_elements:
                # 获取任务标题
                title_element = await element.query_selector(".task-title")
                title = await title_element.text_content() if title_element else "无标题"
                
                # 获取任务描述
                desc_element = await element.query_selector(".task-description")
                description = await desc_element.text_content() if desc_element else ""
                
                # 获取任务状态
                status_element = await element.query_selector(".task-status")
                status = await status_element.text_content() if status_element else "未知"
                
                # 获取任务ID
                task_id = await element.get_attribute("data-task-id") or "unknown"
                
                # 检查是否包含关键词
                if keyword.lower() in title.lower() or keyword.lower() in description.lower():
                    tasks.append({
                        "id": task_id,
                        "title": title,
                        "description": description,
                        "status": status,
                        "element": element
                    })
            
            logger.info(f"找到{len(tasks)}个包含关键词'{keyword}'的任务")
            return tasks
        except Exception as e:
            logger.error(f"获取任务列表失败: {str(e)}")
            return []
    
    async def select_task(self, task_id: str) -> bool:
        """
        选择任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"选择任务: {task_id}")
        
        try:
            # 查找任务元素
            task_selector = f".task-item[data-task-id='{task_id}']"
            await self.page.wait_for_selector(task_selector, timeout=10000)
            
            # 点击任务
            await self.page.click(task_selector)
            
            # 等待任务详情加载
            await self.page.wait_for_selector(".task-detail", timeout=10000)
            
            logger.info(f"成功选择任务: {task_id}")
            return True
        except Exception as e:
            logger.error(f"选择任务失败: {str(e)}")
            return False
    
    async def send_message(self, message: str) -> bool:
        """
        发送消息
        
        Args:
            message: 消息内容
            
        Returns:
            是否成功
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"发送消息: {message}")
        
        try:
            # 查找输入框
            input_selector = ".message-input"
            await self.page.wait_for_selector(input_selector, timeout=10000)
            
            # 清空输入框
            await self.page.click(input_selector)
            await self.page.keyboard.press("Control+A")
            await self.page.keyboard.press("Delete")
            
            # 输入消息
            await self.page.fill(input_selector, message)
            
            # 点击发送按钮
            send_button_selector = ".send-button"
            await self.page.click(send_button_selector)
            
            # 等待消息发送完成
            await self.page.wait_for_timeout(1000)
            
            logger.info("消息发送成功")
            return True
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
            return False
    
    async def upload_file(self, file_path: str) -> bool:
        """
        上传文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否成功
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"上传文件: {file_path}")
        
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                return False
            
            # 查找文件上传按钮
            upload_button_selector = ".file-upload-button"
            await self.page.wait_for_selector(upload_button_selector, timeout=10000)
            
            # 设置文件输入
            file_input_selector = "input[type=file]"
            await self.page.set_input_files(file_input_selector, file_path)
            
            # 等待文件上传完成
            await self.page.wait_for_selector(".file-upload-complete", timeout=30000)
            
            logger.info("文件上传成功")
            return True
        except Exception as e:
            logger.error(f"上传文件失败: {str(e)}")
            return False
    
    async def send_message_with_file(self, message: str, file_path: str) -> bool:
        """
        发送消息和文件
        
        Args:
            message: 消息内容
            file_path: 文件路径
            
        Returns:
            是否成功
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"发送消息和文件: {message}, {file_path}")
        
        try:
            # 上传文件
            file_success = await self.upload_file(file_path)
            if not file_success:
                logger.error("文件上传失败，无法发送消息")
                return False
            
            # 发送消息
            message_success = await self.send_message(message)
            if not message_success:
                logger.error("消息发送失败")
                return False
            
            logger.info("消息和文件发送成功")
            return True
        except Exception as e:
            logger.error(f"发送消息和文件失败: {str(e)}")
            return False
    
    async def get_latest_powerautomation_task(self) -> Optional[Dict[str, Any]]:
        """
        获取最新的PowerAutomation任务
        
        Returns:
            最新任务信息
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info("获取最新的PowerAutomation任务")
        
        try:
            # 导航到Manus.im
            await self.navigate_to_manus()
            
            # 获取PowerAutomation相关任务
            tasks = await self.get_task_list("powerautomation")
            
            if not tasks:
                logger.warning("未找到PowerAutomation相关任务")
                return None
            
            # 按时间排序（假设最新的任务在列表前面）
            latest_task = tasks[0]
            
            logger.info(f"找到最新的PowerAutomation任务: {latest_task['title']}")
            return latest_task
        except Exception as e:
            logger.error(f"获取最新的PowerAutomation任务失败: {str(e)}")
            return None
    
    async def execute_task_command(self, task_id: str, command: str, file_path: str = None) -> bool:
        """
        执行任务命令
        
        Args:
            task_id: 任务ID
            command: 命令内容
            file_path: 文件路径（可选）
            
        Returns:
            是否成功
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"执行任务命令: {task_id}, {command}, {file_path}")
        
        try:
            # 选择任务
            select_success = await self.select_task(task_id)
            if not select_success:
                logger.error(f"选择任务失败: {task_id}")
                return False
            
            # 发送命令
            if file_path:
                return await self.send_message_with_file(command, file_path)
            else:
                return await self.send_message(command)
        except Exception as e:
            logger.error(f"执行任务命令失败: {str(e)}")
            return False
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            logger.info("关闭浏览器")
            await self.browser.close()
            self.is_initialized = False

# 示例用法
async def main():
    # 创建Manus自动化实例
    manus = ManusAutomation()
    
    try:
        # 初始化浏览器
        await manus.initialize(headless=False)
        
        # 获取最新的PowerAutomation任务
        latest_task = await manus.get_latest_powerautomation_task()
        
        if latest_task:
            # 执行任务命令
            await manus.execute_task_command(
                latest_task["id"],
                "执行PowerAutomation任务测试",
                "/path/to/file.txt"  # 可选
            )
    finally:
        # 关闭浏览器
        await manus.close()

if __name__ == "__main__":
    asyncio.run(main())
