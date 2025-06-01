"""
测试与问题收集器模块 - TestAndIssueCollector

该模块用于执行自动化测试、收集问题并更新README文件。
主要功能：
1. 执行自动化测试脚本
2. 收集测试过程中的问题
3. 更新README文件
4. 生成测试报告
5. 支持截图和日志收集

作者: PowerAutomation AI
日期: 2025-05-30
"""

import os
import re
import glob
import json
import time
import datetime
import subprocess
import logging
import shutil
from typing import Dict, List, Any, Optional, Union

# 导入思考与操作记录器
from .thought_action_recorder import ThoughtActionRecorder

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TestAndIssueCollector")

class TestAndIssueCollector:
    """
    测试与问题收集器类，用于执行自动化测试、收集问题并更新README文件
    """
    
    def __init__(self, 
                 repo_path: str,
                 test_script: str = "start_and_test.sh",
                 readme_path: str = "README.md",
                 recorder: ThoughtActionRecorder = None):
        """
        初始化测试与问题收集器
        
        Args:
            repo_path: 仓库路径
            test_script: 测试脚本名称，默认为"start_and_test.sh"
            readme_path: README文件路径，默认为"README.md"
            recorder: 思考与操作记录器实例，如果为None则创建新实例
        """
        self.repo_path = repo_path
        self.test_script = test_script
        self.readme_path = os.path.join(repo_path, readme_path)
        
        # 初始化记录器
        self.recorder = recorder or ThoughtActionRecorder(
            log_dir=os.path.join(repo_path, "logs")
        )
        
        # 创建输出目录
        self.output_dir = os.path.join(repo_path, "output")
        self.logs_dir = os.path.join(repo_path, "logs")
        self.screenshots_dir = os.path.join(self.output_dir, "screenshots")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        logger.info(f"TestAndIssueCollector initialized with repo path: {repo_path}")
        logger.info(f"Test script: {test_script}")
        logger.info(f"README path: {self.readme_path}")
    
    def run_tests(self) -> Dict[str, Any]:
        """
        运行测试脚本并收集结果
        
        Returns:
            测试结果
        """
        self.recorder.record_thought("运行测试脚本并收集结果")
        
        # 确保测试脚本有执行权限
        test_script_path = os.path.join(self.repo_path, self.test_script)
        
        if not os.path.exists(test_script_path):
            error_msg = f"Test script {test_script_path} does not exist"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "run_tests", 
                {"test_script": self.test_script},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
        
        try:
            # 确保测试脚本有执行权限
            os.chmod(test_script_path, 0o755)
            logger.info(f"Set execute permission for {test_script_path}")
        except Exception as e:
            logger.warning(f"Failed to set execute permission for {test_script_path}: {e}")
        
        # 创建测试日志文件
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        test_log_file = os.path.join(self.logs_dir, f"test_{timestamp}.log")
        
        # 运行测试脚本
        logger.info(f"Running test script: {self.test_script}")
        self.recorder.record_action("run_test_script", {"script": self.test_script})
        
        try:
            # 使用subprocess.Popen运行测试脚本
            process = subprocess.Popen(
                f"./{self.test_script}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.repo_path
            )
            
            # 实时获取输出
            stdout_lines = []
            stderr_lines = []
            
            # 非阻塞读取输出
            for stdout_line in iter(process.stdout.readline, b""):
                line = stdout_line.decode("utf-8").strip()
                stdout_lines.append(line)
                logger.info(f"[TEST] {line}")
                
                # 将输出写入日志文件
                with open(test_log_file, "a", encoding="utf-8") as f:
                    f.write(f"[OUT] {line}\n")
            
            for stderr_line in iter(process.stderr.readline, b""):
                line = stderr_line.decode("utf-8").strip()
                stderr_lines.append(line)
                logger.error(f"[TEST ERROR] {line}")
                
                # 将错误输出写入日志文件
                with open(test_log_file, "a", encoding="utf-8") as f:
                    f.write(f"[ERR] {line}\n")
            
            # 等待进程完成
            process.wait()
            success = process.returncode == 0
            
            # 记录测试结果
            test_result = {
                "success": success,
                "stdout": "\n".join(stdout_lines),
                "stderr": "\n".join(stderr_lines),
                "return_code": process.returncode,
                "log_file": test_log_file,
                "timestamp": timestamp
            }
            
            logger.info(f"Test completed with return code {process.returncode}")
            
            self.recorder.record_action(
                "test_completed", 
                {"script": self.test_script},
                test_result
            )
            
            return test_result
            
        except Exception as e:
            error_msg = f"Error running test script: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "run_tests", 
                {"test_script": self.test_script},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
    
    def collect_issues(self) -> List[Dict[str, Any]]:
        """
        从测试日志中收集问题
        
        Returns:
            问题列表
        """
        self.recorder.record_thought("从测试日志中收集问题")
        
        issues = []
        
        # 收集日志文件
        log_files = glob.glob(os.path.join(self.logs_dir, "*.log"))
        
        logger.info(f"Found {len(log_files)} log files")
        
        for log_file in log_files:
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    log_content = f.read()
                
                # 查找错误和警告
                error_pattern = re.compile(r"(error|exception|fail|traceback)", re.IGNORECASE)
                warning_pattern = re.compile(r"warning", re.IGNORECASE)
                
                # 提取错误
                for match in error_pattern.finditer(log_content):
                    # 获取错误上下文（前后各200个字符）
                    start = max(0, match.start() - 200)
                    end = min(len(log_content), match.end() + 200)
                    context = log_content[start:end]
                    
                    issues.append({
                        "type": "error",
                        "file": os.path.basename(log_file),
                        "context": context,
                        "position": match.start()
                    })
                
                # 提取警告
                for match in warning_pattern.finditer(log_content):
                    # 获取警告上下文（前后各150个字符）
                    start = max(0, match.start() - 150)
                    end = min(len(log_content), match.end() + 150)
                    context = log_content[start:end]
                    
                    issues.append({
                        "type": "warning",
                        "file": os.path.basename(log_file),
                        "context": context,
                        "position": match.start()
                    })
            except Exception as e:
                logger.error(f"Error processing log file {log_file}: {e}")
        
        # 检查是否生成了PPT文件
        ppt_files = glob.glob(os.path.join(self.repo_path, "final_release/static/ppt/*.pptx"))
        if not ppt_files:
            issues.append({
                "type": "error",
                "file": "PPT Generation",
                "context": "No PPT files were generated during the test",
                "position": 0
            })
        
        logger.info(f"Collected {len(issues)} issues")
        
        self.recorder.record_action(
            "collect_issues", 
            {"log_files": log_files},
            {"issues_count": len(issues)}
        )
        
        return issues
    
    def update_readme(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        更新README文件，添加发现的问题
        
        Args:
            issues: 问题列表
            
        Returns:
            更新结果
        """
        self.recorder.record_thought("更新README文件，添加发现的问题")
        
        if not os.path.exists(self.readme_path):
            error_msg = f"README file {self.readme_path} does not exist"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "update_readme", 
                {"readme_path": self.readme_path},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
        
        try:
            # 读取当前README内容
            with open(self.readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
            
            # 生成问题报告
            issues_report = "\n\n## 测试发现的问题\n\n"
            
            if not issues:
                issues_report += "测试未发现任何问题，所有功能正常工作。\n"
            else:
                issues_report += "测试发现以下问题：\n\n"
                
                for i, issue in enumerate(issues, 1):
                    issues_report += f"{i}. **{issue['type'].upper()}**: {issue['file']}\n"
                    issues_report += f"   ```\n   {issue['context']}\n   ```\n\n"
            
            # 添加测试时间戳
            issues_report += f"\n*测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
            
            # 检查README是否已包含问题部分
            if "## 测试发现的问题" in readme_content:
                # 替换现有问题部分
                pattern = r"## 测试发现的问题.*?(?=\n## |$)"
                readme_content = re.sub(pattern, issues_report.strip(), readme_content, flags=re.DOTALL)
            else:
                # 添加问题部分到README末尾
                readme_content += issues_report
            
            # 写回README文件
            with open(self.readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            logger.info(f"Updated README with {len(issues)} issues")
            
            self.recorder.record_action(
                "update_readme", 
                {"readme_path": self.readme_path},
                {"success": True, "issues_count": len(issues)}
            )
            
            return {"success": True, "issues_count": len(issues)}
            
        except Exception as e:
            error_msg = f"Error updating README: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "update_readme", 
                {"readme_path": self.readme_path},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
    
    def generate_test_report(self, test_result: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成测试报告
        
        Args:
            test_result: 测试结果
            issues: 问题列表
            
        Returns:
            报告生成结果
        """
        self.recorder.record_thought("生成测试报告")
        
        # 创建报告文件
        timestamp = test_result.get("timestamp") or datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.output_dir, f"TEST_REPORT_{timestamp}.md")
        
        try:
            report_content = "# PowerAutomation 测试报告\n\n"
            report_content += f"测试时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # 测试结果摘要
            report_content += "## 测试结果摘要\n\n"
            report_content += f"- **测试状态**: {'成功' if test_result.get('success') else '失败'}\n"
            report_content += f"- **发现问题数**: {len(issues)}\n"
            report_content += f"- **返回代码**: {test_result.get('return_code')}\n\n"
            
            # 问题详情
            report_content += "## 问题详情\n\n"
            
            if not issues:
                report_content += "测试未发现任何问题，所有功能正常工作。\n"
            else:
                for i, issue in enumerate(issues, 1):
                    report_content += f"### 问题 {i}: {issue['type'].upper()} in {issue['file']}\n\n"
                    report_content += f"```\n{issue['context']}\n```\n\n"
            
            # 测试日志
            report_content += "## 测试日志\n\n"
            report_content += "### 标准输出\n\n"
            report_content += f"```\n{test_result.get('stdout', '')}\n```\n\n"
            
            if test_result.get('stderr'):
                report_content += "### 标准错误\n\n"
                report_content += f"```\n{test_result.get('stderr', '')}\n```\n\n"
            
            # 写入报告文件
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report_content)
            
            logger.info(f"Generated test report: {report_path}")
            
            self.recorder.record_action(
                "generate_test_report", 
                {"report_path": report_path},
                {"success": True}
            )
            
            return {"success": True, "report_path": report_path}
            
        except Exception as e:
            error_msg = f"Error generating test report: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "generate_test_report", 
                {"report_path": report_path},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
    
    def collect_test_artifacts(self) -> Dict[str, Any]:
        """
        收集测试产物
        
        Returns:
            收集结果
        """
        self.recorder.record_thought("收集测试产物")
        
        artifacts = {
            "logs": [],
            "screenshots": [],
            "ppt_files": [],
            "other_files": []
        }
        
        try:
            # 收集日志文件
            log_files = glob.glob(os.path.join(self.logs_dir, "*.log"))
            artifacts["logs"] = log_files
            
            # 收集截图
            screenshot_files = glob.glob(os.path.join(self.screenshots_dir, "*.png"))
            screenshot_files.extend(glob.glob(os.path.join(self.screenshots_dir, "*.jpg")))
            screenshot_files.extend(glob.glob(os.path.join(self.screenshots_dir, "*.jpeg")))
            artifacts["screenshots"] = screenshot_files
            
            # 收集PPT文件
            ppt_files = glob.glob(os.path.join(self.repo_path, "final_release/static/ppt/*.pptx"))
            artifacts["ppt_files"] = ppt_files
            
            # 收集其他文件
            other_files = glob.glob(os.path.join(self.output_dir, "*.md"))
            other_files.extend(glob.glob(os.path.join(self.output_dir, "*.json")))
            other_files.extend(glob.glob(os.path.join(self.output_dir, "*.txt")))
            artifacts["other_files"] = other_files
            
            logger.info(f"Collected {len(log_files)} logs, {len(screenshot_files)} screenshots, {len(ppt_files)} PPT files, {len(other_files)} other files")
            
            self.recorder.record_action(
                "collect_test_artifacts", 
                {},
                {
                    "success": True,
                    "logs_count": len(log_files),
                    "screenshots_count": len(screenshot_files),
                    "ppt_files_count": len(ppt_files),
                    "other_files_count": len(other_files)
                }
            )
            
            return artifacts
            
        except Exception as e:
            error_msg = f"Error collecting test artifacts: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "collect_test_artifacts", 
                {},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
    
    def take_screenshot(self, name: str) -> Dict[str, Any]:
        """
        截取屏幕截图
        
        Args:
            name: 截图名称
            
        Returns:
            截图结果
        """
        self.recorder.record_thought(f"截取屏幕截图: {name}")
        
        try:
            # 生成截图文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(self.screenshots_dir, f"{name}_{timestamp}.png")
            
            # 使用系统截图工具
            if os.name == "posix":  # Linux/Mac
                if shutil.which("screencapture"):  # Mac
                    subprocess.run(["screencapture", "-x", screenshot_path], check=True)
                elif shutil.which("import"):  # Linux with ImageMagick
                    subprocess.run(["import", "-window", "root", screenshot_path], check=True)
                else:
                    return {"success": False, "error": "No screenshot tool available"}
            elif os.name == "nt":  # Windows
                # 使用PIL库截图
                try:
                    from PIL import ImageGrab
                    screenshot = ImageGrab.grab()
                    screenshot.save(screenshot_path)
                except ImportError:
                    return {"success": False, "error": "PIL library not available"}
            
            logger.info(f"Screenshot saved to: {screenshot_path}")
            
            self.recorder.record_action(
                "take_screenshot", 
                {"name": name},
                {"success": True, "path": screenshot_path}
            )
            
            return {"success": True, "path": screenshot_path}
            
        except Exception as e:
            error_msg = f"Error taking screenshot: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "take_screenshot", 
                {"name": name},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
    
    def compare_screenshots(self, screenshot1: str, screenshot2: str) -> Dict[str, Any]:
        """
        比较两张截图
        
        Args:
            screenshot1: 第一张截图路径
            screenshot2: 第二张截图路径
            
        Returns:
            比较结果
        """
        self.recorder.record_thought(f"比较截图: {screenshot1} vs {screenshot2}")
        
        try:
            # 使用PIL库比较截图
            try:
                from PIL import Image, ImageChops
                import numpy as np
            except ImportError:
                return {"success": False, "error": "PIL or numpy library not available"}
            
            # 打开截图
            img1 = Image.open(screenshot1)
            img2 = Image.open(screenshot2)
            
            # 确保尺寸一致
            if img1.size != img2.size:
                return {
                    "success": True,
                    "match": False,
                    "reason": "Size mismatch",
                    "diff_percentage": 100.0
                }
            
            # 计算差异
            diff = ImageChops.difference(img1, img2)
            
            # 转换为numpy数组
            diff_array = np.array(diff)
            
            # 计算差异百分比
            total_pixels = diff_array.size / 3  # RGB图像每个像素有3个值
            diff_pixels = np.count_nonzero(diff_array)
            diff_percentage = (diff_pixels / total_pixels) * 100
            
            # 生成差异图
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            diff_path = os.path.join(self.screenshots_dir, f"diff_{timestamp}.png")
            diff.save(diff_path)
            
            # 判断是否匹配
            match = diff_percentage < 1.0  # 差异小于1%认为匹配
            
            result = {
                "success": True,
                "match": match,
                "diff_percentage": diff_percentage,
                "diff_path": diff_path
            }
            
            logger.info(f"Screenshot comparison: match={match}, diff_percentage={diff_percentage:.2f}%")
            
            self.recorder.record_action(
                "compare_screenshots", 
                {"screenshot1": screenshot1, "screenshot2": screenshot2},
                result
            )
            
            return result
            
        except Exception as e:
            error_msg = f"Error comparing screenshots: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "compare_screenshots", 
                {"screenshot1": screenshot1, "screenshot2": screenshot2},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
    
    def run_visual_test(self, test_name: str, expected_screenshot: str = None) -> Dict[str, Any]:
        """
        运行视觉测试
        
        Args:
            test_name: 测试名称
            expected_screenshot: 预期截图路径，如果为None则只截图不比较
            
        Returns:
            测试结果
        """
        self.recorder.record_thought(f"运行视觉测试: {test_name}")
        
        # 截取当前屏幕
        screenshot_result = self.take_screenshot(test_name)
        
        if not screenshot_result["success"]:
            return screenshot_result
        
        current_screenshot = screenshot_result["path"]
        
        # 如果没有提供预期截图，则只返回当前截图
        if expected_screenshot is None:
            return {
                "success": True,
                "screenshot": current_screenshot,
                "comparison": None
            }
        
        # 比较截图
        comparison_result = self.compare_screenshots(current_screenshot, expected_screenshot)
        
        if not comparison_result["success"]:
            return comparison_result
        
        return {
            "success": True,
            "screenshot": current_screenshot,
            "comparison": comparison_result
        }
    
    def submit_issues_to_problem_solver(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        将问题提交给问题解决器
        
        Args:
            issues: 问题列表
            
        Returns:
            提交结果
        """
        self.recorder.record_thought("将问题提交给问题解决器")
        
        try:
            # 导入问题解决器
            from ..development_tools import AgentProblemSolver
            
            # 创建问题解决器实例
            problem_solver = AgentProblemSolver(repo_path=self.repo_path)
            
            # 记录测试错误
            problem_solver.record_test_error()
            
            # 提交问题
            result = problem_solver.submit_issues_to_platform(issues)
            
            logger.info(f"Submitted {len(issues)} issues to problem solver")
            
            self.recorder.record_action(
                "submit_issues_to_problem_solver", 
                {"issues_count": len(issues)},
                result
            )
            
            return result
            
        except Exception as e:
            error_msg = f"Error submitting issues to problem solver: {str(e)}"
            logger.error(error_msg)
            
            self.recorder.record_action(
                "submit_issues_to_problem_solver", 
                {"issues_count": len(issues)},
                {"success": False, "error": error_msg}
            )
            
            return {"success": False, "error": error_msg}
