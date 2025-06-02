"""
任务追踪系统测试模块 - 验证端到端自动化流程和数据同步
版本: 1.0.0
更新日期: 2025-06-02
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, List, Any

# 导入任务追踪系统
from task_tracking_system import TaskTrackingSystem

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_task_tracking.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("TestTaskTracking")

class TaskTrackingTester:
    """
    任务追踪系统测试类
    验证端到端自动化流程和数据同步
    """
    
    def __init__(self, api_key: str = None):
        """
        初始化测试类
        
        Args:
            api_key: SuperMemory API密钥
        """
        self.api_key = api_key or os.environ.get("SUPERMEMORY_API_KEY")
        self.system = None
        
        logger.info("TaskTrackingTester初始化完成")
    
    async def setup(self):
        """设置测试环境"""
        logger.info("设置测试环境")
        
        # 创建任务追踪系统
        self.system = TaskTrackingSystem(self.api_key)
        
        # 初始化系统
        await self.system.initialize(headless=False)
        
        logger.info("测试环境设置完成")
    
    async def teardown(self):
        """清理测试环境"""
        logger.info("清理测试环境")
        
        if self.system:
            await self.system.close()
        
        logger.info("测试环境清理完成")
    
    async def test_get_latest_task(self):
        """测试获取最新任务"""
        logger.info("测试获取最新任务")
        
        # 获取最新任务
        latest_task = await self.system.get_latest_task()
        
        # 验证结果
        assert latest_task is not None, "未找到最新任务"
        assert "id" in latest_task, "任务缺少ID"
        assert "title" in latest_task, "任务缺少标题"
        
        logger.info(f"最新任务: {latest_task['title']}")
        return latest_task
    
    async def test_execute_command(self, task_id: str):
        """
        测试执行命令
        
        Args:
            task_id: 任务ID
        """
        logger.info(f"测试执行命令: {task_id}")
        
        # 执行命令
        command = "测试命令：验证任务追踪系统"
        result = await self.system.execute_command(task_id, command)
        
        # 验证结果
        assert result["success"] is True, "命令执行失败"
        assert "action_record" in result, "缺少动作记录"
        assert "progress_record" in result, "缺少进度记录"
        
        logger.info("命令执行成功")
        return result
    
    async def test_monitor_task_output(self, task_id: str):
        """
        测试监控任务输出
        
        Args:
            task_id: 任务ID
        """
        logger.info(f"测试监控任务输出: {task_id}")
        
        # 监控任务输出
        results = await self.system.monitor_task_output(task_id, 10)
        
        # 验证结果
        logger.info(f"监控结果: {len(results)}条消息")
        return results
    
    async def test_process_with_mcpplanner(self, task_id: str):
        """
        测试使用MCPPlanner处理任务
        
        Args:
            task_id: 任务ID
        """
        logger.info(f"测试使用MCPPlanner处理任务: {task_id}")
        
        # 使用MCPPlanner处理任务
        input_text = "分析PowerAutomation项目的代码质量"
        result = await self.system.process_task_with_mcpplanner(task_id, input_text)
        
        # 验证结果
        assert "planner_output" in result, "缺少规划器输出"
        assert "execution_result" in result, "缺少执行结果"
        assert "monitoring_results" in result, "缺少监控结果"
        
        logger.info("MCPPlanner处理成功")
        return result
    
    async def test_process_with_mcpbrainstorm(self, task_id: str):
        """
        测试使用MCPBrainstorm处理任务
        
        Args:
            task_id: 任务ID
        """
        logger.info(f"测试使用MCPBrainstorm处理任务: {task_id}")
        
        # 使用MCPBrainstorm处理任务
        input_text = "为PowerAutomation项目提供创意改进方案"
        result = await self.system.process_task_with_mcpbrainstorm(task_id, input_text)
        
        # 验证结果
        assert "brainstorm_output" in result, "缺少头脑风暴输出"
        assert "execution_result" in result, "缺少执行结果"
        assert "monitoring_results" in result, "缺少监控结果"
        
        logger.info("MCPBrainstorm处理成功")
        return result
    
    async def test_process_with_mcpcoordinator(self):
        """测试使用MCPCoordinator处理输入"""
        logger.info("测试使用MCPCoordinator处理输入")
        
        # 使用MCPCoordinator处理输入
        input_text = "优化PowerAutomation项目的性能"
        result = await self.system.process_input_with_mcpcoordinator(input_text)
        
        # 验证结果
        assert result["success"] is True, "处理失败"
        assert "task_id" in result, "缺少任务ID"
        assert "processor" in result, "缺少处理器信息"
        assert "result" in result, "缺少处理结果"
        
        logger.info(f"使用{result['processor']}处理成功")
        return result
    
    async def run_all_tests(self):
        """运行所有测试"""
        logger.info("运行所有测试")
        
        try:
            # 设置测试环境
            await self.setup()
            
            # 获取最新任务
            latest_task = await self.test_get_latest_task()
            task_id = latest_task["id"]
            
            # 执行命令
            await self.test_execute_command(task_id)
            
            # 监控任务输出
            await self.test_monitor_task_output(task_id)
            
            # 使用MCPPlanner处理任务
            await self.test_process_with_mcpplanner(task_id)
            
            # 使用MCPBrainstorm处理任务
            await self.test_process_with_mcpbrainstorm(task_id)
            
            # 使用MCPCoordinator处理输入
            await self.test_process_with_mcpcoordinator()
            
            logger.info("所有测试通过")
            return True
        except AssertionError as e:
            logger.error(f"测试失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"测试异常: {str(e)}")
            return False
        finally:
            # 清理测试环境
            await self.teardown()

# 主函数
async def main():
    # 获取SuperMemory API密钥
    api_key = os.environ.get("SUPERMEMORY_API_KEY", "sm_ohYKVYxdyurx5qGri5VqCi_BAzZRzHUyqFnueoSOCMPyIQbIfbvdJuQZmTgYpGAgMyCbgzTECRyoQnMviFbsYuL")
    
    # 创建测试类
    tester = TaskTrackingTester(api_key)
    
    # 运行所有测试
    success = await tester.run_all_tests()
    
    # 输出结果
    if success:
        print("✅ 所有测试通过")
    else:
        print("❌ 测试失败")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())
