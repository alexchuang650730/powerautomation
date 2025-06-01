"""
TestAndIssueCollector脚本 - 执行测试、收集问题并生成报告
通过MCP框架间接调用，确保与其他智能体调用方式一致
"""
import os
import sys
import json
import time
import logging
import subprocess
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入MCP模块
from agents.ppt_agent.core.mcp import mcpcoordinator
from agents.ppt_agent.core.mcp import mcpbrain
from agents.ppt_agent.core.mcp import mcpplanner

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/test_collector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TestAndIssueCollector")

class TestAndIssueCollector:
    """
    测试和问题收集器
    通过MCP框架执行测试、分析日志、提取问题并生成报告
    """
    
    def __init__(self):
        """初始化测试和问题收集器"""
        self.test_results = {}
        self.issues = []
        self.results_dir = os.path.join(os.getcwd(), "test_results")
        self.reports_dir = os.path.join(os.getcwd(), "reports")
        
        # 确保目录存在
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        
        logger.info("TestAndIssueCollector初始化完成")
    
    def run_tests(self):
        """执行测试脚本"""
        logger.info("开始执行测试...")
        
        # 通过MCP协调器执行测试
        test_params = {
            "test_types": ["unit", "visual", "pixel"],
            "parallel": True,
            "timeout": 300
        }
        
        try:
            # 使用MCP协调器调用测试工具
            result = mcpcoordinator.callTool(
                tool_name="test_runner",
                params=test_params,
                timeout=300
            )
            
            if result.get("success"):
                self.test_results = result.get("data", {})
                logger.info(f"测试执行完成，结果: {json.dumps(self.test_results, ensure_ascii=False)[:200]}...")
                return True
            else:
                logger.error(f"测试执行失败: {result.get('error')}")
                return False
        except Exception as e:
            logger.exception(f"执行测试时发生异常: {str(e)}")
            return False
    
    def analyze_test_logs(self):
        """分析测试日志，提取问题信息"""
        logger.info("开始分析测试日志...")
        
        # 通过MCP大脑分析日志
        analysis_params = {
            "log_files": [
                "logs/test_collector.log",
                "test_results/unit_test_results.log",
                "test_results/visual_test_results.log",
                "test_results/pixel_regression_results.json"
            ],
            "analysis_depth": "deep",
            "pattern_recognition": True
        }
        
        try:
            # 使用MCP大脑进行分析
            analysis_result = mcpbrain.analyze(
                data_type="test_logs",
                params=analysis_params
            )
            
            # 获取问题列表
            raw_issues = analysis_result.get("issues", [])
            
            # 使用MCP大脑进一步处理问题
            for issue in raw_issues:
                # 获取问题修复建议
                recommendations = mcpbrain.getRecommendation(
                    issue_type=issue.get("type"),
                    context=issue
                )
                
                # 丰富问题信息
                issue["recommendations"] = recommendations
                issue["timestamp"] = datetime.now().isoformat()
                
                # 添加到问题列表
                self.issues.append(issue)
            
            logger.info(f"测试日志分析完成，发现 {len(self.issues)} 个问题")
            return True
        except Exception as e:
            logger.exception(f"分析测试日志时发生异常: {str(e)}")
            return False
    
    def structure_issues(self):
        """将问题信息结构化存储"""
        logger.info("开始结构化存储问题信息...")
        
        if not self.issues:
            logger.info("没有发现问题，跳过结构化存储")
            return True
        
        try:
            # 按严重程度分类问题
            categorized_issues = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            for issue in self.issues:
                severity = issue.get("severity", "medium")
                if severity in categorized_issues:
                    categorized_issues[severity].append(issue)
                else:
                    categorized_issues["medium"].append(issue)
            
            # 保存结构化问题
            issues_file = os.path.join(self.reports_dir, "structured_issues.json")
            with open(issues_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "total_issues": len(self.issues),
                    "categorized_issues": categorized_issues
                }, f, ensure_ascii=False, indent=2)
            
            logger.info(f"问题信息已结构化存储到 {issues_file}")
            return True
        except Exception as e:
            logger.exception(f"结构化存储问题信息时发生异常: {str(e)}")
            return False
    
    def report_to_github(self):
        """将测试结果和问题报告到GitHub"""
        logger.info("开始向GitHub报告测试结果和问题...")
        
        # 通过MCP协调器调用GitHub API
        github_params = {
            "repo_owner": "alexchuang650730",
            "repo_name": "powerautomation",
            "title": f"自动化测试报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "test_results": self.test_results,
            "issues": self.issues,
            "labels": ["test-results", "automated"]
        }
        
        try:
            # 使用MCP协调器调用GitHub API
            result = mcpcoordinator.callTool(
                tool_name="github_reporter",
                params=github_params,
                timeout=60
            )
            
            if result.get("success"):
                logger.info(f"GitHub报告成功: {result.get('data', {}).get('html_url')}")
                return True
            else:
                logger.error(f"GitHub报告失败: {result.get('error')}")
                return False
        except Exception as e:
            logger.exception(f"向GitHub报告时发生异常: {str(e)}")
            return False
    
    def update_readme(self):
        """更新README文件，添加测试发现的问题"""
        logger.info("开始更新README文件...")
        
        readme_path = os.path.join(os.getcwd(), "README.md")
        if not os.path.exists(readme_path):
            logger.warning(f"README文件不存在: {readme_path}")
            return False
        
        try:
            # 读取现有README内容
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 准备测试状态部分
            test_status = "## 测试状态\n\n"
            test_status += f"最后更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # 添加测试结果摘要
            test_status += "### 测试结果摘要\n\n"
            test_status += "| 测试类型 | 总数 | 通过 | 失败 |\n"
            test_status += "|---------|------|------|------|\n"
            
            for test_type, result in self.test_results.items():
                total = result.get("total", 0)
                passed = result.get("passed", 0)
                failed = result.get("failed", 0)
                test_status += f"| {test_type} | {total} | {passed} | {failed} |\n"
            
            test_status += "\n"
            
            # 添加问题摘要
            if self.issues:
                test_status += "### 发现的问题\n\n"
                
                # 只显示最多5个关键问题
                critical_issues = [i for i in self.issues if i.get("severity") in ["critical", "high"]]
                display_issues = critical_issues[:5] if len(critical_issues) > 5 else critical_issues
                
                for issue in display_issues:
                    test_status += f"- **{issue.get('type')}**: {issue.get('message')}\n"
                    if issue.get('recommendations'):
                        test_status += f"  - 建议: {issue.get('recommendations')[0]}\n"
                
                if len(self.issues) > len(display_issues):
                    test_status += f"\n*还有 {len(self.issues) - len(display_issues)} 个其他问题未显示*\n"
            else:
                test_status += "### 未发现问题\n\n"
                test_status += "本次测试未发现任何问题，所有测试均已通过。\n"
            
            test_status += "\n详细测试报告请查看 [测试结果目录](./test_results) 和 [问题报告](./reports/structured_issues.json)。\n\n"
            
            # 更新README内容
            if "## 测试状态" in content:
                # 替换现有测试状态部分
                pattern = r"## 测试状态[\s\S]*?(?=##|$)"
                import re
                content = re.sub(pattern, test_status, content)
            else:
                # 添加到文件末尾
                content += "\n" + test_status
            
            # 写回README文件
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("README文件更新完成")
            return True
        except Exception as e:
            logger.exception(f"更新README文件时发生异常: {str(e)}")
            return False
    
    def notify_user(self):
        """通知用户测试完成和更新的文件"""
        logger.info("开始通知用户...")
        
        # 准备通知消息
        message = {
            "title": "自动化测试完成",
            "content": f"测试已完成，发现 {len(self.issues)} 个问题。",
            "test_summary": self.test_results,
            "updated_files": [
                "README.md",
                "reports/structured_issues.json"
            ]
        }
        
        try:
            # 使用MCP协调器发送通知
            result = mcpcoordinator.callTool(
                tool_name="user_notifier",
                params=message,
                timeout=30
            )
            
            if result.get("success"):
                logger.info("用户通知发送成功")
                return True
            else:
                logger.error(f"用户通知发送失败: {result.get('error')}")
                return False
        except Exception as e:
            logger.exception(f"通知用户时发生异常: {str(e)}")
            return False
    
    def run_workflow(self):
        """运行完整工作流程"""
        logger.info("开始运行TestAndIssueCollector工作流...")
        
        # 使用MCP规划器创建执行计划
        plan = mcpplanner.createPlan(
            task_type="test_and_collect",
            steps=[
                "run_tests",
                "analyze_test_logs",
                "structure_issues",
                "report_to_github",
                "update_readme",
                "notify_user"
            ]
        )
        
        logger.info(f"执行计划创建完成: {plan}")
        
        # 按计划执行步骤
        for step in plan.get("steps", []):
            logger.info(f"执行步骤: {step}")
            
            # 执行对应方法
            method = getattr(self, step, None)
            if method and callable(method):
                success = method()
                
                # 更新计划状态
                mcpplanner.updatePlan(
                    plan_id=plan.get("id"),
                    step=step,
                    status="completed" if success else "failed",
                    result={"success": success}
                )
                
                if not success:
                    logger.error(f"步骤 {step} 执行失败，中止工作流")
                    return False
            else:
                logger.error(f"未找到步骤对应的方法: {step}")
                return False
        
        logger.info("TestAndIssueCollector工作流执行完成")
        return True


if __name__ == "__main__":
    collector = TestAndIssueCollector()
    collector.run_workflow()
