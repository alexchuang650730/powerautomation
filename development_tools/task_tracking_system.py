"""
端到端任务数据分类与追踪模块 - 整合Manus自动化和SuperMemory集成
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
from datetime import datetime

# 导入自定义模块
from manus_automation import ManusAutomation
from supermemory_integration import SuperMemoryIntegration

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("task_tracking.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("TaskTracking")

class TaskTrackingSystem:
    """
    端到端任务数据分类与追踪系统
    整合Manus自动化和SuperMemory集成
    """
    
    def __init__(self, supermemory_api_key: str = None):
        """
        初始化任务追踪系统
        
        Args:
            supermemory_api_key: SuperMemory API密钥
        """
        # 初始化Manus自动化
        self.manus = ManusAutomation()
        
        # 初始化SuperMemory集成
        self.supermemory = SuperMemoryIntegration(supermemory_api_key)
        
        # 任务缓存
        self.task_cache = {}
        
        logger.info("TaskTrackingSystem初始化完成")
    
    async def initialize(self, headless: bool = True):
        """
        初始化系统
        
        Args:
            headless: 是否使用无头模式
        """
        logger.info(f"初始化系统，headless={headless}")
        
        # 初始化Manus自动化
        await self.manus.initialize(headless=headless)
        
        logger.info("系统初始化完成")
    
    async def get_latest_task(self) -> Optional[Dict[str, Any]]:
        """
        获取最新任务
        
        Returns:
            最新任务信息
        """
        logger.info("获取最新任务")
        
        # 获取最新的PowerAutomation任务
        latest_task = await self.manus.get_latest_powerautomation_task()
        
        if latest_task:
            # 缓存任务
            self.task_cache[latest_task["id"]] = latest_task
            
            logger.info(f"找到最新任务: {latest_task['title']}")
            return latest_task
        
        logger.warning("未找到最新任务")
        return None
    
    async def execute_command(self, task_id: str, command: str, file_path: str = None) -> Dict[str, Any]:
        """
        执行命令并追踪
        
        Args:
            task_id: 任务ID
            command: 命令内容
            file_path: 文件路径（可选）
            
        Returns:
            执行结果
        """
        logger.info(f"执行命令: task_id={task_id}, command={command}, file_path={file_path}")
        
        # 记录命令作为动作记录
        action_record = f"执行命令: {command}"
        if file_path:
            action_record += f"，附带文件: {os.path.basename(file_path)}"
        
        action_result = self.supermemory.store_task_data(
            task_id=task_id,
            text=action_record,
            data_type="action_record"
        )
        
        # 执行命令
        success = await self.manus.execute_task_command(task_id, command, file_path)
        
        # 记录执行结果
        result_text = f"命令执行{'成功' if success else '失败'}: {command}"
        result = self.supermemory.store_task_data(
            task_id=task_id,
            text=result_text,
            data_type="task_progress"
        )
        
        return {
            "task_id": task_id,
            "command": command,
            "file_path": file_path,
            "success": success,
            "action_record": action_result,
            "progress_record": result
        }
    
    async def monitor_task_output(self, task_id: str, duration_seconds: int = 60) -> List[Dict[str, Any]]:
        """
        监控任务输出
        
        Args:
            task_id: 任务ID
            duration_seconds: 监控持续时间（秒）
            
        Returns:
            监控结果
        """
        logger.info(f"监控任务输出: task_id={task_id}, duration={duration_seconds}秒")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        results = []
        
        # 记录开始监控
        monitor_start = self.supermemory.store_task_data(
            task_id=task_id,
            text=f"开始监控任务输出，计划持续{duration_seconds}秒",
            data_type="task_progress"
        )
        
        try:
            # 选择任务
            await self.manus.select_task(task_id)
            
            # 监控循环
            while time.time() < end_time:
                # 获取最新消息
                messages = await self._get_latest_messages()
                
                for message in messages:
                    # 处理消息
                    result = self.supermemory.process_manus_output(task_id, message)
                    results.append(result)
                
                # 等待一段时间
                await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"监控任务输出失败: {str(e)}")
        finally:
            # 记录监控结束
            monitor_end = self.supermemory.store_task_data(
                task_id=task_id,
                text=f"结束监控任务输出，共处理{len(results)}条消息",
                data_type="task_progress"
            )
        
        return results
    
    async def _get_latest_messages(self) -> List[str]:
        """
        获取最新消息
        
        Returns:
            消息列表
        """
        # 这里应该实现从Manus.im获取最新消息的逻辑
        # 由于Playwright不直接支持获取动态更新的消息，这里使用模拟实现
        
        try:
            # 获取消息容器
            message_container = await self.manus.page.query_selector(".message-container")
            if not message_container:
                return []
            
            # 获取所有消息元素
            message_elements = await message_container.query_selector_all(".message-item")
            
            messages = []
            for element in message_elements:
                # 获取消息内容
                content_element = await element.query_selector(".message-content")
                if content_element:
                    content = await content_element.text_content()
                    messages.append(content)
            
            return messages
        except Exception as e:
            logger.error(f"获取最新消息失败: {str(e)}")
            return []
    
    async def process_task_with_mcpplanner(self, task_id: str, input_text: str, file_path: str = None) -> Dict[str, Any]:
        """
        使用MCPPlanner处理任务
        
        Args:
            task_id: 任务ID
            input_text: 输入文本
            file_path: 文件路径（可选）
            
        Returns:
            处理结果
        """
        logger.info(f"使用MCPPlanner处理任务: task_id={task_id}, input={input_text}")
        
        # 记录任务开始
        start_record = self.supermemory.store_task_data(
            task_id=task_id,
            text=f"开始使用MCPPlanner处理任务: {input_text}",
            data_type="task_progress",
            feature="platform"
        )
        
        # 这里应该实现调用MCPPlanner的逻辑
        # 由于MCPPlanner不在当前环境中，这里使用模拟实现
        
        # 模拟MCPPlanner处理
        planner_output = f"MCPPlanner处理结果: 已分析'{input_text}'，生成执行计划"
        
        # 记录MCPPlanner输出
        planner_record = self.supermemory.store_task_data(
            task_id=task_id,
            text=planner_output,
            data_type="action_record",
            feature="thinking"
        )
        
        # 执行命令
        execution_result = await self.execute_command(task_id, planner_output, file_path)
        
        # 监控输出
        monitoring_results = await self.monitor_task_output(task_id, 30)
        
        return {
            "task_id": task_id,
            "input": input_text,
            "planner_output": planner_output,
            "execution_result": execution_result,
            "monitoring_results": monitoring_results
        }
    
    async def process_task_with_mcpbrainstorm(self, task_id: str, input_text: str, file_path: str = None) -> Dict[str, Any]:
        """
        使用MCPBrainstorm处理任务
        
        Args:
            task_id: 任务ID
            input_text: 输入文本
            file_path: 文件路径（可选）
            
        Returns:
            处理结果
        """
        logger.info(f"使用MCPBrainstorm处理任务: task_id={task_id}, input={input_text}")
        
        # 记录任务开始
        start_record = self.supermemory.store_task_data(
            task_id=task_id,
            text=f"开始使用MCPBrainstorm处理任务: {input_text}",
            data_type="task_progress",
            feature="platform"
        )
        
        # 这里应该实现调用MCPBrainstorm的逻辑
        # 由于MCPBrainstorm不在当前环境中，这里使用模拟实现
        
        # 模拟MCPBrainstorm处理
        brainstorm_output = f"MCPBrainstorm处理结果: 已思考'{input_text}'，生成创意方案"
        
        # 记录MCPBrainstorm输出
        brainstorm_record = self.supermemory.store_task_data(
            task_id=task_id,
            text=brainstorm_output,
            data_type="action_record",
            feature="thinking"
        )
        
        # 执行命令
        execution_result = await self.execute_command(task_id, brainstorm_output, file_path)
        
        # 监控输出
        monitoring_results = await self.monitor_task_output(task_id, 30)
        
        return {
            "task_id": task_id,
            "input": input_text,
            "brainstorm_output": brainstorm_output,
            "execution_result": execution_result,
            "monitoring_results": monitoring_results
        }
    
    async def process_input_with_mcpcoordinator(self, input_text: str, file_path: str = None, has_tools: bool = None) -> Dict[str, Any]:
        """
        使用MCPCoordinator处理输入
        
        Args:
            input_text: 输入文本
            file_path: 文件路径（可选）
            has_tools: 是否有工具（如果为None则自动判断）
            
        Returns:
            处理结果
        """
        logger.info(f"使用MCPCoordinator处理输入: input={input_text}, has_tools={has_tools}")
        
        # 获取最新任务
        latest_task = await self.get_latest_task()
        
        if not latest_task:
            logger.error("未找到任务，无法处理输入")
            return {
                "success": False,
                "error": "未找到任务"
            }
        
        task_id = latest_task["id"]
        
        # 记录用户输入
        input_record = self.supermemory.store_task_data(
            task_id=task_id,
            text=f"用户输入: {input_text}",
            data_type="user_history",
            feature="prompt"
        )
        
        # 如果未指定是否有工具，进行自动判断
        if has_tools is None:
            # 这里应该实现自动判断是否有工具的逻辑
            # 简单实现：检查输入是否包含工具相关关键词
            tool_keywords = ["工具", "命令", "执行", "运行", "调用", "API", "函数"]
            has_tools = any(keyword in input_text for keyword in tool_keywords)
        
        # 根据是否有工具选择处理方式
        if has_tools:
            # 使用MCPPlanner处理
            result = await self.process_task_with_mcpplanner(task_id, input_text, file_path)
            processor = "MCPPlanner"
        else:
            # 使用MCPBrainstorm处理
            result = await self.process_task_with_mcpbrainstorm(task_id, input_text, file_path)
            processor = "MCPBrainstorm"
        
        # 记录处理完成
        completion_record = self.supermemory.store_task_data(
            task_id=task_id,
            text=f"使用{processor}处理完成: {input_text}",
            data_type="work_completion",
            feature="platform"
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "input": input_text,
            "processor": processor,
            "result": result
        }
    
    async def close(self):
        """关闭系统"""
        logger.info("关闭系统")
        
        # 关闭Manus自动化
        await self.manus.close()

# 示例用法
async def main():
    # 获取SuperMemory API密钥
    api_key = os.environ.get("SUPERMEMORY_API_KEY", "sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL")
    
    # 创建任务追踪系统
    system = TaskTrackingSystem(api_key)
    
    try:
        # 初始化系统
        await system.initialize(headless=False)
        
        # 处理输入
        result = await system.process_input_with_mcpcoordinator(
            "分析PowerAutomation项目的代码质量",
            "/path/to/file.txt",  # 可选
            has_tools=True  # 可选，如果为None则自动判断
        )
        
        print(f"处理结果: {result}")
    finally:
        # 关闭系统
        await system.close()

if __name__ == "__main__":
    asyncio.run(main())
