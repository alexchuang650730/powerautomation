"""
工作流驱动集成验证脚本
版本: 1.0.0
更新日期: 2025-06-01
"""

import os
import sys
import json
import time
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# 导入工作流驱动器
from agents.workflow_driver.workflow_driver import get_instance as get_workflow_driver
from agents.general_agent.general_agent_features import get_instance as get_features

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("workflow_integration_test.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("WorkflowIntegrationTest")

class WorkflowIntegrationTest:
    """
    工作流驱动集成验证类
    用于验证工作流驱动器与核心Agent组件的集成
    """
    
    def __init__(self):
        """初始化工作流集成测试"""
        self.project_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.workflow_driver = get_workflow_driver(self.project_root)
        self.features = get_features()
        
        # 注册事件监听器
        self.workflow_driver.register_event_listener("node_created", self.on_node_created)
        self.workflow_driver.register_event_listener("node_updated", self.on_node_updated)
        self.workflow_driver.register_event_listener("workflow_completed", self.on_workflow_completed)
        
        # 初始化测试结果
        self.test_results = {
            "test_workflow": None,
            "rollback_workflow": None,
            "github_release_workflow": None
        }
        
        logger.info("工作流集成测试初始化完成")
    
    def on_node_created(self, event_data):
        """节点创建事件处理"""
        node = event_data["node"]
        logger.info(f"节点创建: {node['id']} - {node['name']} ({node['type']})")
    
    def on_node_updated(self, event_data):
        """节点更新事件处理"""
        node = event_data["node"]
        logger.info(f"节点更新: {node['id']} - {node['status']}")
    
    def on_workflow_completed(self, event_data):
        """工作流完成事件处理"""
        workflow_data = event_data["workflow_data"]
        nodes = workflow_data["nodes"]
        connections = workflow_data["connections"]
        
        logger.info(f"工作流完成: {len(nodes)} 个节点, {len(connections)} 个连接")
        
        # 保存工作流数据
        if nodes and nodes[0]["type"] == "trigger":
            trigger_node = nodes[0]
            if "test_type" in trigger_node["data"]:
                self.test_results["test_workflow"] = workflow_data
            elif "savepoint_id" in trigger_node["data"]:
                self.test_results["rollback_workflow"] = workflow_data
            elif "release_version" in trigger_node["data"]:
                self.test_results["github_release_workflow"] = workflow_data
    
    def run_test_workflow(self):
        """运行测试工作流"""
        logger.info("开始运行测试工作流")
        
        # 启动测试工作流
        self.workflow_driver.start_test_workflow("unit", "src/main.py")
        
        # 等待工作流完成
        while self.workflow_driver.workflow_status["is_running"]:
            time.sleep(1)
        
        logger.info("测试工作流执行完成")
        
        # 验证测试工作流结果
        workflow_data = self.test_results["test_workflow"]
        if not workflow_data:
            logger.error("未收到测试工作流完成事件")
            return False
        
        nodes = workflow_data["nodes"]
        if not nodes or len(nodes) < 3:
            logger.error(f"测试工作流节点数量不足: {len(nodes)}")
            return False
        
        # 验证节点状态
        success_count = sum(1 for node in nodes if node["status"] == "success")
        logger.info(f"测试工作流成功节点数: {success_count}/{len(nodes)}")
        
        return success_count >= 3
    
    def run_rollback_workflow(self):
        """运行回滚工作流"""
        logger.info("开始运行回滚工作流")
        
        # 启动回滚工作流
        self.workflow_driver.start_rollback_workflow(reason="集成测试")
        
        # 等待工作流完成
        while self.workflow_driver.workflow_status["is_running"]:
            time.sleep(1)
        
        logger.info("回滚工作流执行完成")
        
        # 验证回滚工作流结果
        workflow_data = self.test_results["rollback_workflow"]
        if not workflow_data:
            logger.error("未收到回滚工作流完成事件")
            return False
        
        nodes = workflow_data["nodes"]
        if not nodes or len(nodes) < 3:
            logger.error(f"回滚工作流节点数量不足: {len(nodes)}")
            return False
        
        # 验证节点状态
        success_count = sum(1 for node in nodes if node["status"] == "success")
        logger.info(f"回滚工作流成功节点数: {success_count}/{len(nodes)}")
        
        return success_count >= 2
    
    def run_github_release_workflow(self):
        """运行GitHub Release工作流"""
        logger.info("开始运行GitHub Release工作流")
        
        # 启动GitHub Release工作流
        self.workflow_driver.start_github_release_workflow(
            "v1.0.0",
            "https://github.com/example/repo/releases/tag/v1.0.0"
        )
        
        # 等待工作流完成
        while self.workflow_driver.workflow_status["is_running"]:
            time.sleep(1)
        
        logger.info("GitHub Release工作流执行完成")
        
        # 验证GitHub Release工作流结果
        workflow_data = self.test_results["github_release_workflow"]
        if not workflow_data:
            logger.error("未收到GitHub Release工作流完成事件")
            return False
        
        nodes = workflow_data["nodes"]
        if not nodes or len(nodes) < 3:
            logger.error(f"GitHub Release工作流节点数量不足: {len(nodes)}")
            return False
        
        # 验证节点状态
        success_count = sum(1 for node in nodes if node["status"] == "success")
        logger.info(f"GitHub Release工作流成功节点数: {success_count}/{len(nodes)}")
        
        return success_count >= 2
    
    def verify_feature_integration(self):
        """验证特性集成"""
        logger.info("开始验证特性集成")
        
        # 验证四大核心能力
        core_capabilities = self.features.get_core_capabilities()
        if len(core_capabilities) != 4:
            logger.error(f"核心能力数量不正确: {len(core_capabilities)}")
            return False
        
        # 验证自动化测试能力
        if "automated_testing" not in core_capabilities:
            logger.error("缺少自动化测试能力")
            return False
        
        # 验证自动化智能体生成能力
        if "agent_manufacturing" not in core_capabilities:
            logger.error("缺少自动化智能体生成能力")
            return False
        
        # 验证工作流可视化能力
        if "workflow_visualization" not in core_capabilities:
            logger.error("缺少工作流可视化能力")
            return False
        
        # 验证UI布局自动化能力
        if "ui_layout_automation" not in core_capabilities:
            logger.error("缺少UI布局自动化能力")
            return False
        
        logger.info("特性集成验证通过")
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("开始运行所有集成测试")
        
        # 验证特性集成
        feature_result = self.verify_feature_integration()
        
        # 运行测试工作流
        test_result = self.run_test_workflow()
        
        # 运行回滚工作流
        rollback_result = self.run_rollback_workflow()
        
        # 运行GitHub Release工作流
        github_result = self.run_github_release_workflow()
        
        # 汇总测试结果
        results = {
            "feature_integration": feature_result,
            "test_workflow": test_result,
            "rollback_workflow": rollback_result,
            "github_release_workflow": github_result,
            "overall": feature_result and test_result and rollback_result and github_result
        }
        
        # 输出测试结果
        logger.info("集成测试结果:")
        logger.info(f"  特性集成: {'通过' if feature_result else '失败'}")
        logger.info(f"  测试工作流: {'通过' if test_result else '失败'}")
        logger.info(f"  回滚工作流: {'通过' if rollback_result else '失败'}")
        logger.info(f"  GitHub Release工作流: {'通过' if github_result else '失败'}")
        logger.info(f"  总体结果: {'通过' if results['overall'] else '失败'}")
        
        # 保存测试结果
        with open("workflow_integration_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info("集成测试完成")
        return results


if __name__ == "__main__":
    # 运行工作流集成测试
    test = WorkflowIntegrationTest()
    results = test.run_all_tests()
    
    # 输出测试结果
    print("\n集成测试结果:")
    print(f"  特性集成: {'通过' if results['feature_integration'] else '失败'}")
    print(f"  测试工作流: {'通过' if results['test_workflow'] else '失败'}")
    print(f"  回滚工作流: {'通过' if results['rollback_workflow'] else '失败'}")
    print(f"  GitHub Release工作流: {'通过' if results['github_release_workflow'] else '失败'}")
    print(f"  总体结果: {'通过' if results['overall'] else '失败'}")
