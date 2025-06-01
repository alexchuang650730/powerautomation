#!/usr/bin/env python3
"""
通用智能体驱动的TestAndIssueCollector自动化测试脚本

该脚本由通用智能体驱动，用于：
1. 执行指定的测试脚本
2. 分析测试日志，提取问题信息
3. 将问题信息结构化存储
4. 更新README文件，添加测试发现的问题
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("general_agent_test_collector.log")
    ]
)
logger = logging.getLogger("GeneralAgentTestCollector")

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# 导入TestAndIssueCollector
try:
    from development_tools.test_and_issue_collector import TestAndIssueCollector
    logger.info("成功导入TestAndIssueCollector")
except ImportError as e:
    logger.error(f"导入TestAndIssueCollector失败: {str(e)}")
    sys.exit(1)

class GeneralAgentTestDriver:
    """通用智能体驱动的测试执行器"""
    
    def __init__(self, output_dir: str = "test_results"):
        """
        初始化通用智能体驱动的测试执行器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self.collector = None
        self.test_results = None
        self.issues = []
        self.readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"通用智能体测试驱动初始化完成，输出目录: {self.output_dir}")
    
    def initialize_collector(self) -> None:
        """初始化TestAndIssueCollector"""
        try:
            logger.info("正在初始化TestAndIssueCollector...")
            self.collector = TestAndIssueCollector()
            logger.info("TestAndIssueCollector初始化成功")
        except Exception as e:
            logger.error(f"初始化TestAndIssueCollector失败: {str(e)}")
            raise
    
    def run_tests(self) -> Dict[str, Any]:
        """
        运行测试
        
        Returns:
            测试结果
        """
        logger.info("开始运行测试...")
        
        try:
            # 收集测试用例
            test_cases = self.collector.collect_test_cases()
            logger.info(f"收集到{len(test_cases)}个测试用例")
            
            # 生成测试计划
            test_plan = self.collector.generate_test_plan(test_cases)
            logger.info(f"生成测试计划: {test_plan['name']}")
            
            # 执行测试计划
            self.test_results = self.collector.execute_test_plan(test_plan)
            logger.info(f"测试执行完成，状态: {self.test_results['overall_status']}")
            
            # 保存测试结果
            self._save_test_results()
            
            return self.test_results
        except Exception as e:
            logger.error(f"运行测试失败: {str(e)}")
            raise
    
    def _save_test_results(self) -> None:
        """保存测试结果到文件"""
        if self.test_results:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            results_file = os.path.join(self.output_dir, f"test_results_{timestamp}.json")
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"测试结果已保存到: {results_file}")
    
    def analyze_test_logs(self) -> List[Dict[str, Any]]:
        """
        分析测试日志，提取问题信息
        
        Returns:
            问题列表
        """
        logger.info("开始分析测试日志...")
        
        if not self.test_results:
            logger.warning("没有测试结果可供分析")
            return []
        
        try:
            # 收集所有失败的测试
            failed_tests = []
            for group in self.test_results["groups_results"]:
                for test in group["test_results"]:
                    if test["status"] == "failed" or test["status"] == "error":
                        failed_tests.append(test)
            
            logger.info(f"发现{len(failed_tests)}个失败的测试")
            
            # 分析失败的测试
            self.issues = []
            for test in failed_tests:
                issue = self._analyze_test_failure(test)
                if issue:
                    self.issues.append(issue)
            
            logger.info(f"分析完成，提取了{len(self.issues)}个问题")
            
            # 保存问题信息
            self._save_issues()
            
            return self.issues
        except Exception as e:
            logger.error(f"分析测试日志失败: {str(e)}")
            raise
    
    def _analyze_test_failure(self, test: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        分析测试失败，提取问题信息
        
        Args:
            test: 测试结果
            
        Returns:
            问题信息
        """
        if not test.get("error"):
            return None
        
        # 提取问题信息
        issue = {
            "id": f"ISSUE-{len(self.issues) + 1}",
            "test_name": test["name"],
            "test_path": test["path"],
            "test_type": test["type"],
            "error": test["error"],
            "timestamp": datetime.now().isoformat(),
            "status": "open"
        }
        
        # 使用TestAndIssueCollector的模型分析问题
        if hasattr(self.collector, "_analyze_issue_with_model"):
            issue["analysis"] = self.collector._analyze_issue_with_model(issue)
        else:
            issue["analysis"] = f"问题分析: 测试 {test['name']} 失败，错误信息: {test['error']}"
        
        # 使用TestAndIssueCollector的模型生成解决方案
        if hasattr(self.collector, "_generate_solution_with_model"):
            issue["solution"] = self.collector._generate_solution_with_model(issue)
        else:
            issue["solution"] = "解决方案: 检查测试环境和测试代码，修复相关问题"
        
        logger.info(f"分析了问题: {issue['id']}")
        return issue
    
    def _save_issues(self) -> None:
        """保存问题信息到文件"""
        if self.issues:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            issues_file = os.path.join(self.output_dir, f"issues_{timestamp}.json")
            
            with open(issues_file, 'w', encoding='utf-8') as f:
                json.dump(self.issues, f, ensure_ascii=False, indent=2)
            
            logger.info(f"问题信息已保存到: {issues_file}")
    
    def update_readme(self) -> None:
        """更新README文件，添加测试发现的问题"""
        logger.info(f"开始更新README文件: {self.readme_path}")
        
        if not self.issues:
            logger.warning("没有问题信息可供更新README")
            return
        
        try:
            # 读取现有README内容
            readme_content = ""
            if os.path.exists(self.readme_path):
                with open(self.readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
            
            # 生成问题部分内容
            issues_section = self._generate_issues_section()
            
            # 检查README是否已有问题部分
            if "## 测试发现的问题" in readme_content:
                # 替换现有问题部分
                import re
                pattern = r"## 测试发现的问题[\s\S]*?(?=##|$)"
                readme_content = re.sub(pattern, issues_section, readme_content)
            else:
                # 添加问题部分到README末尾
                readme_content += "\n\n" + issues_section
            
            # 保存更新后的README
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            logger.info("README文件更新成功")
        except Exception as e:
            logger.error(f"更新README文件失败: {str(e)}")
            raise
    
    def _generate_issues_section(self) -> str:
        """
        生成问题部分内容
        
        Returns:
            问题部分内容
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"## 测试发现的问题\n\n"
        content += f"*最后更新时间: {timestamp}*\n\n"
        
        if not self.issues:
            content += "当前没有发现问题。\n"
            return content
        
        content += f"共发现 {len(self.issues)} 个问题:\n\n"
        
        for issue in self.issues:
            content += f"### {issue['id']}: {issue['test_name']}\n\n"
            content += f"- **类型**: {issue['test_type']}\n"
            content += f"- **状态**: {issue['status']}\n"
            content += f"- **错误**: {issue['error']}\n"
            content += f"- **分析**: {issue['analysis']}\n"
            content += f"- **解决方案**: {issue['solution']}\n\n"
        
        return content
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        生成测试摘要
        
        Returns:
            测试摘要
        """
        logger.info("生成测试摘要...")
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "test_results": None,
            "issues_count": len(self.issues),
            "issues": self.issues,
            "readme_updated": os.path.exists(self.readme_path)
        }
        
        if self.test_results:
            # 简化测试结果，只保留关键信息
            summary["test_results"] = {
                "plan_name": self.test_results.get("plan_name", "未知"),
                "overall_status": self.test_results.get("overall_status", "未知"),
                "groups_count": len(self.test_results.get("groups_results", [])),
                "passed_count": sum(1 for g in self.test_results.get("groups_results", [])
                                  for t in g.get("test_results", [])
                                  if t.get("status") == "passed"),
                "failed_count": sum(1 for g in self.test_results.get("groups_results", [])
                                  for t in g.get("test_results", [])
                                  if t.get("status") in ["failed", "error"])
            }
        
        # 保存摘要
        summary_file = os.path.join(self.output_dir, "test_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"测试摘要已保存到: {summary_file}")
        return summary

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="通用智能体驱动的TestAndIssueCollector自动化测试")
    parser.add_argument("--output-dir", default="test_results", help="输出目录")
    args = parser.parse_args()
    
    try:
        # 初始化通用智能体测试驱动
        driver = GeneralAgentTestDriver(output_dir=args.output_dir)
        
        # 初始化TestAndIssueCollector
        driver.initialize_collector()
        
        # 运行测试
        driver.run_tests()
        
        # 分析测试日志
        driver.analyze_test_logs()
        
        # 更新README
        driver.update_readme()
        
        # 生成摘要
        summary = driver.generate_summary()
        
        logger.info("通用智能体驱动的自动化测试完成")
        return 0
    except Exception as e:
        logger.error(f"自动化测试失败: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
