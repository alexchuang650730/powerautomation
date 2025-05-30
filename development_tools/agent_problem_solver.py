"""
Agent问题解决驱动器模块 - AgentProblemSolver

该模块主要功能：
1. 版本回滚管理：支持每个版本的回滚，在持续出错时回滚至保存点
2. 自动回滚：当测试方案持续出错超过5次时自动回滚到前一个保存点
3. PowerAutomation集成：使用大模型+自动化工具将问题提交给PowerAutomation平台

注意：分析问题并生成解决方案功能已被标记为不可用

作者: PowerAutomation AI
日期: 2025-05-30
"""

import os
import re
import json
import time
import datetime
import logging
import requests
import shutil
import subprocess
import threading
import webbrowser
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from pathlib import Path

# 导入思考与操作记录器
from .thought_action_recorder import ThoughtActionRecorder

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AgentProblemSolver")

class AgentProblemSolver:
    """
    Agent问题解决驱动器，支持版本回滚功能，在持续出错时可回滚至保存点。
    集成PowerAutomation平台，通过大模型+自动化工具提交问题。
    
    注意：分析问题并生成解决方案功能已被标记为不可用
    """
    
    def __init__(self, 
                 repo_path: Optional[str] = None,
                 enhanced_recorder: Optional[Any] = None,
                 test_updater: Optional[Any] = None,
                 rules_checker: Optional[Any] = None,
                 platform_url: Optional[str] = "https://powerautomation.ai/app/dOwSylYaP4AL5S41JU3qO0"):
        """
        初始化Agent问题解决驱动器
        
        Args:
            repo_path: 代码仓库路径，如果为None则使用默认路径
            enhanced_recorder: 增强型记录器实例，如果为None则创建新实例
            test_updater: 测试更新器实例，如果为None则创建新实例
            rules_checker: 规则检查器实例，如果为None则创建新实例
            platform_url: PowerAutomation平台URL，默认为https://powerautomation.ai/app/dOwSylYaP4AL5S41JU3qO0
        """
        self.repo_path = repo_path or os.path.expanduser("~/powerassistant/powerautomation")
        
        # 确保目录存在
        os.makedirs(self.repo_path, exist_ok=True)
        
        # 保存点目录
        self.save_points_dir = os.path.join(self.repo_path, ".save_points")
        os.makedirs(self.save_points_dir, exist_ok=True)
        
        # 解决方案输出目录
        self.solutions_dir = os.path.join(self.repo_path, "agent_solutions")
        os.makedirs(self.solutions_dir, exist_ok=True)
        
        # 组件实例
        self.recorder = enhanced_recorder or ThoughtActionRecorder()
        self.test_updater = test_updater
        self.rules_checker = rules_checker
        
        # 保存点索引文件
        self.save_points_index_file = os.path.join(self.save_points_dir, "index.json")
        if not os.path.exists(self.save_points_index_file):
            with open(self.save_points_index_file, "w") as f:
                json.dump({"save_points": []}, f)
        
        # 错误计数器
        self.error_counter_file = os.path.join(self.repo_path, ".error_counter.json")
        if not os.path.exists(self.error_counter_file):
            with open(self.error_counter_file, "w") as f:
                json.dump({"error_count": 0, "last_error_time": None}, f)
        
        # PowerAutomation平台URL
        self.platform_url = platform_url
        
        # 自动化工具目录
        self.automation_tools_dir = os.path.join(self.repo_path, "automation_tools")
        os.makedirs(self.automation_tools_dir, exist_ok=True)
        
        # 问题提交历史
        self.submission_history_file = os.path.join(self.repo_path, ".submission_history.json")
        if not os.path.exists(self.submission_history_file):
            with open(self.submission_history_file, "w") as f:
                json.dump({"submissions": []}, f)
    
    def analyze_issues_and_generate_solutions(self, issues: Optional[List[Dict]] = None) -> Dict:
        """
        [已禁用] 分析问题并生成解决方案
        
        此功能已被标记为不可用，请使用自动回滚和问题提交功能。
        
        Args:
            issues: 问题列表，如果为None则从README和测试日志中提取
            
        Returns:
            Dict: 包含禁用状态信息的字典
        """
        self.recorder.record_thought("尝试调用已禁用的功能：分析问题并生成解决方案")
        
        return {
            "status": "disabled",
            "message": "此功能已被标记为不可用，请使用自动回滚和问题提交功能。",
            "timestamp": datetime.now().isoformat()
        }
    
    def save_solutions_to_file(self, solutions: Dict, output_dir: Optional[str] = None) -> str:
        """
        [已禁用] 将解决方案保存到文件
        
        此功能已被标记为不可用，请使用自动回滚和问题提交功能。
        
        Args:
            solutions: 解决方案字典
            output_dir: 输出目录，如果为None则使用默认目录
            
        Returns:
            str: 包含禁用状态信息的字符串
        """
        self.recorder.record_thought("尝试调用已禁用的功能：将解决方案保存到文件")
        
        return "此功能已被标记为不可用，请使用自动回滚和问题提交功能。"
    
    def create_save_point(self, name: Optional[str] = None) -> Dict:
        """
        创建版本保存点
        
        Args:
            name: 保存点名称，如果为None则使用时间戳
            
        Returns:
            Dict: 保存点信息
        """
        # 生成保存点ID和名称
        save_point_id = int(time.time())
        if name is None:
            name = f"save_point_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建保存点目录
        save_point_dir = os.path.join(self.save_points_dir, str(save_point_id))
        os.makedirs(save_point_dir, exist_ok=True)
        
        # 复制当前代码到保存点目录
        self._copy_code_to_save_point(save_point_dir)
        
        # 更新保存点索引
        save_point_info = {
            "id": save_point_id,
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "directory": save_point_dir
        }
        
        with open(self.save_points_index_file, "r") as f:
            index = json.load(f)
        
        index["save_points"].append(save_point_info)
        
        with open(self.save_points_index_file, "w") as f:
            json.dump(index, f, indent=2)
        
        self.recorder.record_action(
            "create_save_point", 
            {"name": name},
            save_point_info
        )
        
        return save_point_info
    
    def list_save_points(self) -> List[Dict]:
        """
        列出所有保存点
        
        Returns:
            List[Dict]: 保存点列表
        """
        with open(self.save_points_index_file, "r") as f:
            index = json.load(f)
        
        return index["save_points"]
    
    def rollback_to_save_point(self, save_point_id: Union[int, str]) -> Dict:
        """
        回滚到指定保存点
        
        Args:
            save_point_id: 保存点ID或名称
            
        Returns:
            Dict: 回滚结果
        """
        # 查找保存点
        save_point = self._find_save_point(save_point_id)
        if save_point is None:
            error_msg = f"未找到保存点: {save_point_id}"
            self.recorder.record_action(
                "rollback_to_save_point", 
                {"save_point_id": save_point_id},
                {"status": "error", "message": error_msg}
            )
            return {"status": "error", "message": error_msg}
        
        # 在回滚前创建当前状态的备份
        backup_info = self.create_save_point(f"auto_backup_before_rollback_to_{save_point['name']}")
        
        # 从保存点复制代码到当前目录
        self._copy_code_from_save_point(save_point["directory"])
        
        # 重置错误计数器
        self._reset_error_counter()
        
        result = {
            "status": "success",
            "message": f"成功回滚到保存点: {save_point['name']}",
            "save_point": save_point,
            "backup": backup_info,
            "timestamp": datetime.now().isoformat()
        }
        
        self.recorder.record_action(
            "rollback_to_save_point", 
            {"save_point_id": save_point_id},
            result
        )
        
        return result
    
    def rollback_to_previous_save_point(self) -> Dict:
        """
        回滚到前一个保存点
        
        Returns:
            Dict: 回滚结果
        """
        # 获取所有保存点
        save_points = self.list_save_points()
        
        if not save_points:
            error_msg = "没有可用的保存点"
            self.recorder.record_action(
                "rollback_to_previous_save_point", 
                {},
                {"status": "error", "message": error_msg}
            )
            return {"status": "error", "message": error_msg}
        
        # 按时间戳排序
        save_points.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # 如果只有一个保存点，则回滚到该保存点
        if len(save_points) == 1:
            return self.rollback_to_save_point(save_points[0]["id"])
        
        # 否则回滚到前一个保存点
        return self.rollback_to_save_point(save_points[1]["id"])
    
    def record_test_error(self) -> Dict:
        """
        记录测试错误，并在错误次数超过阈值时自动回滚
        
        Returns:
            Dict: 记录结果，包括是否触发自动回滚
        """
        # 读取当前错误计数
        with open(self.error_counter_file, "r") as f:
            counter_data = json.load(f)
        
        # 更新错误计数
        counter_data["error_count"] += 1
        counter_data["last_error_time"] = datetime.now().isoformat()
        
        # 保存更新后的错误计数
        with open(self.error_counter_file, "w") as f:
            json.dump(counter_data, f, indent=2)
        
        result = {
            "status": "recorded",
            "error_count": counter_data["error_count"],
            "last_error_time": counter_data["last_error_time"],
            "auto_rollback": False
        }
        
        # 检查是否需要自动回滚
        if counter_data["error_count"] >= 5:
            self.recorder.record_thought(f"错误次数({counter_data['error_count']})已超过阈值(5)，准备自动回滚到前一个保存点")
            
            # 执行自动回滚
            rollback_result = self.rollback_to_previous_save_point()
            
            result["auto_rollback"] = True
            result["rollback_result"] = rollback_result
            
            # 重置错误计数器
            self._reset_error_counter()
            
            # 将问题提交给PowerAutomation平台
            issues = self._extract_issues_from_readme_and_logs()
            if issues:
                submission_result = self.submit_issues_to_platform(issues)
                result["submission_result"] = submission_result
        
        self.recorder.record_action(
            "record_test_error", 
            {},
            result
        )
        
        return result
    
    def _reset_error_counter(self) -> None:
        """
        重置错误计数器
        """
        with open(self.error_counter_file, "w") as f:
            json.dump({"error_count": 0, "last_error_time": None}, f)
    
    def submit_issues_to_platform(self, issues: List[Dict]) -> Dict:
        """
        使用大模型+自动化工具将问题提交给PowerAutomation平台
        
        Args:
            issues: 问题列表
            
        Returns:
            Dict: 提交结果
        """
        self.recorder.record_thought("准备使用大模型+自动化工具将问题提交给PowerAutomation平台")
        
        # 准备问题摘要
        issues_summary = self._prepare_issues_summary(issues)
        
        # 生成自动化脚本
        script_path = self._generate_automation_script(issues_summary)
        
        # 执行自动化脚本
        result = self._execute_automation_script(script_path)
        
        # 记录提交历史
        submission_record = {
            "timestamp": datetime.now().isoformat(),
            "issues_count": len(issues),
            "issues_summary": issues_summary,
            "result": result
        }
        
        with open(self.submission_history_file, "r") as f:
            history = json.load(f)
        
        history["submissions"].append(submission_record)
        
        with open(self.submission_history_file, "w") as f:
            json.dump(history, f, indent=2)
        
        self.recorder.record_action(
            "submit_issues_to_platform", 
            {"issues_count": len(issues)},
            result
        )
        
        return result
    
    def _prepare_issues_summary(self, issues: List[Dict]) -> str:
        """
        准备问题摘要
        
        Args:
            issues: 问题列表
            
        Returns:
            str: 问题摘要
        """
        summary = "PowerAutomation MCP测试中发现以下问题：\n\n"
        
        for i, issue in enumerate(issues, 1):
            summary += f"{i}. {issue['description']}\n"
            
            # 添加问题来源
            if "source" in issue:
                summary += f"   来源: {issue['source']}\n"
            
            # 添加问题状态
            if "status" in issue:
                summary += f"   状态: {issue['status']}\n"
            
            summary += "\n"
        
        # 添加环境信息
        summary += "环境信息：\n"
        summary += f"- 仓库路径: {self.repo_path}\n"
        summary += f"- 时间戳: {datetime.now().isoformat()}\n"
        summary += f"- 错误计数: {self._get_error_count()}\n"
        
        return summary
    
    def _get_error_count(self) -> int:
        """
        获取当前错误计数
        
        Returns:
            int: 错误计数
        """
        with open(self.error_counter_file, "r") as f:
            counter_data = json.load(f)
        
        return counter_data["error_count"]
    
    def _generate_automation_script(self, issues_summary: str) -> str:
        """
        生成自动化脚本
        
        Args:
            issues_summary: 问题摘要
            
        Returns:
            str: 脚本路径
        """
        # 生成脚本文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_filename = f"platform_submit_{timestamp}.py"
        script_path = os.path.join(self.automation_tools_dir, script_filename)
        
        # 生成脚本内容
        script_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
PowerAutomation平台问题提交自动化脚本
生成时间: {datetime.now().isoformat()}
\"\"\"

import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='{os.path.join(self.automation_tools_dir, f"platform_submit_{timestamp}.log")}',
    filemode='w'
)
logger = logging.getLogger("PlatformSubmit")

# 问题摘要
ISSUES_SUMMARY = \"\"\"
{issues_summary}
\"\"\"

def main():
    \"\"\"主函数\"\"\"
    logger.info("开始执行PowerAutomation平台问题提交自动化脚本")
    
    try:
        # 初始化WebDriver
        logger.info("初始化WebDriver")
        driver = initialize_webdriver()
        
        # 打开PowerAutomation平台
        logger.info("打开PowerAutomation平台")
        driver.get("{self.platform_url}")
        
        # 等待页面加载
        logger.info("等待页面加载")
        time.sleep(5)
        
        # 定位消息输入框
        logger.info("定位消息输入框")
        message_input = locate_message_input(driver)
        
        # 输入问题摘要
        logger.info("输入问题摘要")
        input_issues_summary(message_input, ISSUES_SUMMARY)
        
        # 发送消息
        logger.info("发送消息")
        send_message(message_input)
        
        # 等待响应
        logger.info("等待响应")
        time.sleep(10)
        
        # 记录结果
        logger.info("记录结果")
        result = {{
            "status": "success",
            "message": "成功将问题提交给PowerAutomation平台",
            "timestamp": datetime.now().isoformat()
        }}
        
        # 保存结果
        save_result(result)
        
        # 关闭WebDriver
        logger.info("关闭WebDriver")
        driver.quit()
        
        return result
    
    except Exception as e:
        logger.error(f"执行过程中发生错误: {{e}}")
        
        result = {{
            "status": "error",
            "message": f"执行过程中发生错误: {{e}}",
            "timestamp": datetime.now().isoformat()
        }}
        
        # 保存结果
        save_result(result)
        
        return result

def initialize_webdriver():
    \"\"\"初始化WebDriver\"\"\"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    return webdriver.Chrome(options=options)

def locate_message_input(driver):
    \"\"\"定位消息输入框\"\"\"
    try:
        # 等待消息输入框出现
        message_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[contenteditable='true']"))
        )
        return message_input
    except TimeoutException:
        logger.error("无法找到消息输入框")
        raise

def input_issues_summary(message_input, issues_summary):
    \"\"\"输入问题摘要\"\"\"
    # 清空输入框
    message_input.clear()
    
    # 输入问题摘要
    message_input.send_keys(issues_summary)

def send_message(message_input):
    \"\"\"发送消息\"\"\"
    # 按下Ctrl+Enter发送消息
    message_input.send_keys(Keys.CONTROL + Keys.RETURN)

def save_result(result):
    \"\"\"保存结果\"\"\"
    result_file = os.path.join('{self.automation_tools_dir}', 'platform_submit_result.json')
    
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"结果已保存到: {{result_file}}")

if __name__ == "__main__":
    main()
"""
        
        # 写入脚本文件
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        
        # 设置脚本可执行权限
        os.chmod(script_path, 0o755)
        
        return script_path
    
    def _execute_automation_script(self, script_path: str) -> Dict[str, Any]:
        """
        执行自动化脚本
        
        Args:
            script_path: 脚本路径
            
        Returns:
            Dict: 执行结果
        """
        self.recorder.record_thought(f"准备执行自动化脚本: {script_path}")
        
        try:
            # 在后台执行脚本
            process = subprocess.Popen(
                ["python3", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待脚本执行完成，最多等待60秒
            try:
                stdout, stderr = process.communicate(timeout=60)
                
                if process.returncode == 0:
                    self.recorder.record_thought("自动化脚本执行成功")
                    
                    # 读取结果文件
                    result_file = os.path.join(self.automation_tools_dir, 'platform_submit_result.json')
                    if os.path.exists(result_file):
                        with open(result_file, 'r', encoding='utf-8') as f:
                            result = json.load(f)
                    else:
                        result = {
                            "status": "success",
                            "message": "自动化脚本执行成功，但未找到结果文件",
                            "stdout": stdout.decode('utf-8', errors='ignore'),
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    self.recorder.record_thought(f"自动化脚本执行失败，返回码: {process.returncode}")
                    
                    result = {
                        "status": "error",
                        "message": f"自动化脚本执行失败，返回码: {process.returncode}",
                        "stdout": stdout.decode('utf-8', errors='ignore'),
                        "stderr": stderr.decode('utf-8', errors='ignore'),
                        "timestamp": datetime.now().isoformat()
                    }
            except subprocess.TimeoutExpired:
                # 如果超时，则终止进程
                process.kill()
                stdout, stderr = process.communicate()
                
                self.recorder.record_thought("自动化脚本执行超时")
                
                result = {
                    "status": "error",
                    "message": "自动化脚本执行超时",
                    "stdout": stdout.decode('utf-8', errors='ignore') if stdout else "",
                    "stderr": stderr.decode('utf-8', errors='ignore') if stderr else "",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            self.recorder.record_thought(f"执行自动化脚本时发生错误: {e}")
            
            result = {
                "status": "error",
                "message": f"执行自动化脚本时发生错误: {e}",
                "timestamp": datetime.now().isoformat()
            }
        
        return result
    
    def _find_save_point(self, save_point_id: Union[int, str]) -> Optional[Dict]:
        """
        查找保存点
        
        Args:
            save_point_id: 保存点ID或名称
            
        Returns:
            Dict: 保存点信息，如果未找到则返回None
        """
        with open(self.save_points_index_file, "r") as f:
            index = json.load(f)
        
        # 如果save_point_id是整数，则按ID查找
        if isinstance(save_point_id, int) or (isinstance(save_point_id, str) and save_point_id.isdigit()):
            save_point_id = int(save_point_id)
            for save_point in index["save_points"]:
                if save_point["id"] == save_point_id:
                    return save_point
        # 否则按名称查找
        else:
            for save_point in index["save_points"]:
                if save_point["name"] == save_point_id:
                    return save_point
        
        return None
    
    def _copy_code_to_save_point(self, save_point_dir: str) -> None:
        """
        复制当前代码到保存点目录
        
        Args:
            save_point_dir: 保存点目录
        """
        # 要复制的文件和目录列表
        items_to_copy = [
            "src",
            "tests",
            "docs",
            "README.md",
            "requirements.txt"
        ]
        
        for item in items_to_copy:
            src_path = os.path.join(self.repo_path, item)
            dst_path = os.path.join(save_point_dir, item)
            
            if os.path.exists(src_path):
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dst_path)
    
    def _copy_code_from_save_point(self, save_point_dir: str) -> None:
        """
        从保存点复制代码到当前目录
        
        Args:
            save_point_dir: 保存点目录
        """
        # 要复制的文件和目录列表
        items_to_copy = [
            "src",
            "tests",
            "docs",
            "README.md",
            "requirements.txt"
        ]
        
        for item in items_to_copy:
            src_path = os.path.join(save_point_dir, item)
            dst_path = os.path.join(self.repo_path, item)
            
            if os.path.exists(src_path):
                # 如果目标是目录，先删除再复制
                if os.path.isdir(src_path):
                    if os.path.exists(dst_path):
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                else:
                    shutil.copy2(src_path, dst_path)
    
    def _extract_issues_from_readme_and_logs(self) -> List[Dict]:
        """
        从README和测试日志中提取问题
        
        Returns:
            List[Dict]: 问题列表
        """
        issues = []
        
        # 从README中提取问题
        readme_path = os.path.join(self.repo_path, "README.md")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    readme_content = f.read()
                
                # 查找问题部分
                issues_section_match = re.search(r"## (已知问题|Known Issues|Issues|问题)([\s\S]*?)(?:^##|\Z)", readme_content, re.MULTILINE)
                if issues_section_match:
                    issues_section = issues_section_match.group(2).strip()
                    
                    # 提取问题列表
                    issue_matches = re.finditer(r"[-*] (.+?)(?:\n|$)", issues_section)
                    for match in issue_matches:
                        issue_description = match.group(1).strip()
                        issues.append({
                            "description": issue_description,
                            "source": "README.md"
                        })
            except Exception as e:
                self.recorder.record_thought(f"从README中提取问题时发生错误: {e}")
        
        # 从测试日志中提取问题
        logs_dir = os.path.join(self.repo_path, "logs")
        if os.path.exists(logs_dir):
            try:
                # 获取最新的日志文件
                log_files = [f for f in os.listdir(logs_dir) if f.endswith(".log")]
                if log_files:
                    latest_log = max(log_files, key=lambda f: os.path.getmtime(os.path.join(logs_dir, f)))
                    log_path = os.path.join(logs_dir, latest_log)
                    
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        log_content = f.read()
                    
                    # 提取错误信息
                    error_matches = re.finditer(r"ERROR.*?:(.*?)(?:\n|$)", log_content)
                    for match in error_matches:
                        error_description = match.group(1).strip()
                        issues.append({
                            "description": error_description,
                            "source": f"logs/{latest_log}"
                        })
            except Exception as e:
                self.recorder.record_thought(f"从测试日志中提取问题时发生错误: {e}")
        
        return issues
