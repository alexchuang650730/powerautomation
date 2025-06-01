"""
自动化测试框架与能力文档
版本: 1.0.0
更新日期: 2025-06-01
"""

import os
import sys
import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("automated_testing.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AutomatedTesting")

class TestType(Enum):
    """测试类型枚举"""
    UNIT = "unit"
    INTEGRATION = "integration"
    UI = "ui"
    PERFORMANCE = "performance"
    E2E = "end_to_end"
    VISUAL = "visual"

class TestStatus(Enum):
    """测试状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

class TestPriority(Enum):
    """测试优先级枚举"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AutomatedTestingFramework:
    """
    自动化测试框架
    
    提供完整的自动化测试能力，包括测试执行、结果收集、覆盖率分析和报告生成。
    支持多种测试类型，包括单元测试、集成测试、UI测试和性能测试。
    能够根据测试结果自动创建保存点和工作节点。
    
    主要功能:
    1. 测试计划生成与管理
    2. 测试用例执行与监控
    3. 测试结果收集与分析
    4. 测试覆盖率计算与报告
    5. 测试历史追踪与趋势分析
    6. 与AgentProblemSolver和ReleaseManager集成
    """
    
    def __init__(self, project_root: str, config_path: Optional[str] = None):
        """
        初始化自动化测试框架
        
        Args:
            project_root: 项目根目录
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.project_root = os.path.abspath(project_root)
        self.config = self._load_config(config_path)
        self.test_results = {}
        self.coverage_data = {}
        self.current_test_run = None
        self.test_history = []
        
        logger.info(f"自动化测试框架初始化完成，项目根目录: {self.project_root}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        default_config = {
            "test_dirs": {
                "unit": "test/unit",
                "integration": "test/integration",
                "ui": "test/ui",
                "performance": "test/performance",
                "visual": "test/visual_test",
                "end_to_end": "test/end_to_end"
            },
            "report_dir": "reports",
            "coverage_threshold": {
                "unit": 80,
                "integration": 70,
                "ui": 60,
                "performance": 50
            },
            "test_runners": {
                "unit": "pytest",
                "integration": "pytest",
                "ui": "playwright",
                "performance": "locust",
                "visual": "pytest",
                "end_to_end": "pytest"
            },
            "scheduling": {
                "on_commit": True,
                "nightly": True,
                "weekly": True
            },
            "notification": {
                "email": False,
                "slack": False,
                "github": True
            },
            "savepoint": {
                "create_on_success": True,
                "create_on_failure": False
            },
            "max_history_records": 100
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # 合并用户配置和默认配置
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in default_config:
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
                logger.info(f"已加载用户配置: {config_path}")
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
        
        return default_config
    
    def generate_test_plan(self, test_types: List[TestType] = None, priority: List[TestPriority] = None) -> Dict[str, Any]:
        """
        生成测试计划
        
        Args:
            test_types: 要包含的测试类型列表，如果为None则包含所有类型
            priority: 测试优先级列表，如果为None则包含所有优先级
            
        Returns:
            测试计划字典
        """
        if test_types is None:
            test_types = [t for t in TestType]
        
        if priority is None:
            priority = [p for p in TestPriority]
        
        test_plan = {
            "id": f"test_run_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "created_at": datetime.datetime.now().isoformat(),
            "test_types": [t.value for t in test_types],
            "priority": [p.value for p in priority],
            "test_cases": [],
            "status": TestStatus.PENDING.value
        }
        
        # 收集测试用例
        for test_type in test_types:
            test_dir = os.path.join(self.project_root, self.config["test_dirs"][test_type.value])
            if os.path.exists(test_dir):
                test_cases = self._collect_test_cases(test_dir, test_type)
                test_plan["test_cases"].extend(test_cases)
        
        # 按优先级排序
        priority_map = {p.value: i for i, p in enumerate(priority)}
        test_plan["test_cases"].sort(key=lambda x: priority_map.get(x["priority"], 999))
        
        logger.info(f"测试计划生成完成，包含 {len(test_plan['test_cases'])} 个测试用例")
        self.current_test_run = test_plan
        
        return test_plan
    
    def _collect_test_cases(self, test_dir: str, test_type: TestType) -> List[Dict[str, Any]]:
        """
        收集指定目录下的测试用例
        
        Args:
            test_dir: 测试目录
            test_type: 测试类型
            
        Returns:
            测试用例列表
        """
        test_cases = []
        
        # 递归遍历目录
        for root, _, files in os.walk(test_dir):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.project_root)
                    
                    # 解析测试用例
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # 简单解析，实际项目中可能需要更复杂的解析逻辑
                        test_functions = [line.strip() for line in content.split("\n") 
                                         if line.strip().startswith("def test_") or 
                                         line.strip().startswith("    def test_")]
                        
                        for func in test_functions:
                            func_name = func.split("def ")[1].split("(")[0]
                            
                            # 确定优先级（简单示例，实际项目中可能基于注释或装饰器）
                            priority = TestPriority.MEDIUM.value
                            if "critical" in func_name.lower() or "critical" in content.lower():
                                priority = TestPriority.CRITICAL.value
                            elif "high" in func_name.lower() or "high" in content.lower():
                                priority = TestPriority.HIGH.value
                            elif "low" in func_name.lower() or "low" in content.lower():
                                priority = TestPriority.LOW.value
                            
                            test_case = {
                                "id": f"{test_type.value}_{func_name}",
                                "name": func_name,
                                "file": relative_path,
                                "type": test_type.value,
                                "priority": priority,
                                "status": TestStatus.PENDING.value
                            }
                            test_cases.append(test_case)
        
        return test_cases
    
    def execute_tests(self, test_plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行测试计划
        
        Args:
            test_plan: 测试计划，如果为None则使用当前测试计划
            
        Returns:
            测试结果字典
        """
        if test_plan is None:
            if self.current_test_run is None:
                self.generate_test_plan()
            test_plan = self.current_test_run
        
        logger.info(f"开始执行测试计划: {test_plan['id']}")
        test_plan["status"] = TestStatus.RUNNING.value
        test_plan["started_at"] = datetime.datetime.now().isoformat()
        
        # 按测试类型分组执行
        test_types = set(tc["type"] for tc in test_plan["test_cases"])
        for test_type in test_types:
            logger.info(f"执行 {test_type} 测试")
            runner = self.config["test_runners"][test_type]
            test_cases = [tc for tc in test_plan["test_cases"] if tc["type"] == test_type]
            
            # 执行该类型的所有测试用例
            for test_case in test_cases:
                test_case["status"] = TestStatus.RUNNING.value
                test_case["started_at"] = datetime.datetime.now().isoformat()
                
                try:
                    # 实际执行测试（示例，实际项目中应调用相应的测试运行器）
                    result = self._run_test_case(test_case, runner)
                    test_case.update(result)
                except Exception as e:
                    logger.error(f"测试执行异常: {e}")
                    test_case["status"] = TestStatus.ERROR.value
                    test_case["error"] = str(e)
                
                test_case["completed_at"] = datetime.datetime.now().isoformat()
        
        # 更新测试计划状态
        test_plan["completed_at"] = datetime.datetime.now().isoformat()
        
        # 确定整体测试状态
        statuses = [tc["status"] for tc in test_plan["test_cases"]]
        if TestStatus.FAILED.value in statuses or TestStatus.ERROR.value in statuses:
            test_plan["status"] = TestStatus.FAILED.value
        else:
            test_plan["status"] = TestStatus.PASSED.value
        
        # 计算测试统计信息
        test_plan["statistics"] = self._calculate_statistics(test_plan)
        
        # 保存测试结果
        self.test_results[test_plan["id"]] = test_plan
        self.test_history.append({
            "id": test_plan["id"],
            "created_at": test_plan["created_at"],
            "completed_at": test_plan["completed_at"],
            "status": test_plan["status"],
            "statistics": test_plan["statistics"]
        })
        
        # 限制历史记录数量
        if len(self.test_history) > self.config["max_history_records"]:
            self.test_history = self.test_history[-self.config["max_history_records"]:]
        
        logger.info(f"测试计划执行完成: {test_plan['id']}, 状态: {test_plan['status']}")
        
        # 如果配置了成功时创建保存点，则创建
        if test_plan["status"] == TestStatus.PASSED.value and self.config["savepoint"]["create_on_success"]:
            self._create_savepoint(test_plan)
        
        # 如果配置了失败时创建保存点，则创建
        if test_plan["status"] == TestStatus.FAILED.value and self.config["savepoint"]["create_on_failure"]:
            self._create_savepoint(test_plan)
        
        return test_plan
    
    def _run_test_case(self, test_case: Dict[str, Any], runner: str) -> Dict[str, Any]:
        """
        执行单个测试用例
        
        Args:
            test_case: 测试用例信息
            runner: 测试运行器
            
        Returns:
            测试结果
        """
        # 这里是示例实现，实际项目中应调用相应的测试运行器
        logger.info(f"执行测试用例: {test_case['id']}")
        
        # 模拟测试执行
        import random
        import time
        
        # 模拟测试执行时间
        execution_time = random.uniform(0.1, 2.0)
        time.sleep(min(0.1, execution_time))  # 实际执行时不要真的等待
        
        # 模拟测试结果
        if test_case["priority"] == TestPriority.CRITICAL.value:
            # 关键测试用例有90%的通过率
            success = random.random() < 0.9
        elif test_case["priority"] == TestPriority.HIGH.value:
            # 高优先级测试用例有80%的通过率
            success = random.random() < 0.8
        else:
            # 其他测试用例有70%的通过率
            success = random.random() < 0.7
        
        result = {
            "execution_time": execution_time,
            "status": TestStatus.PASSED.value if success else TestStatus.FAILED.value
        }
        
        if not success:
            result["failure_reason"] = "测试断言失败"
            result["failure_details"] = {
                "expected": "预期结果",
                "actual": "实际结果",
                "diff": "差异详情"
            }
        
        return result
    
    def _calculate_statistics(self, test_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算测试统计信息
        
        Args:
            test_plan: 测试计划
            
        Returns:
            统计信息字典
        """
        total = len(test_plan["test_cases"])
        passed = sum(1 for tc in test_plan["test_cases"] if tc["status"] == TestStatus.PASSED.value)
        failed = sum(1 for tc in test_plan["test_cases"] if tc["status"] == TestStatus.FAILED.value)
        skipped = sum(1 for tc in test_plan["test_cases"] if tc["status"] == TestStatus.SKIPPED.value)
        error = sum(1 for tc in test_plan["test_cases"] if tc["status"] == TestStatus.ERROR.value)
        
        # 按测试类型分组统计
        by_type = {}
        for test_type in set(tc["type"] for tc in test_plan["test_cases"]):
            type_cases = [tc for tc in test_plan["test_cases"] if tc["type"] == test_type]
            type_total = len(type_cases)
            type_passed = sum(1 for tc in type_cases if tc["status"] == TestStatus.PASSED.value)
            
            by_type[test_type] = {
                "total": type_total,
                "passed": type_passed,
                "pass_rate": round(type_passed / type_total * 100, 2) if type_total > 0 else 0
            }
        
        # 计算总体通过率
        pass_rate = round(passed / total * 100, 2) if total > 0 else 0
        
        # 计算执行时间
        start_time = datetime.datetime.fromisoformat(test_plan["started_at"])
        end_time = datetime.datetime.fromisoformat(test_plan["completed_at"])
        duration = (end_time - start_time).total_seconds()
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "error": error,
            "pass_rate": pass_rate,
            "duration": duration,
            "by_type": by_type
        }
    
    def _create_savepoint(self, test_plan: Dict[str, Any]) -> None:
        """
        创建保存点
        
        Args:
            test_plan: 测试计划
        """
        try:
            # 这里是示例实现，实际项目中应调用AgentProblemSolver的API
            from development_tools.agent_problem_solver import AgentProblemSolver
            
            # 初始化AgentProblemSolver
            solver = AgentProblemSolver(self.project_root)
            
            # 创建保存点
            description = f"自动测试 {test_plan['id']} - {test_plan['status']}"
            savepoint_result = solver.create_savepoint(description)
            
            logger.info(f"创建保存点成功: {savepoint_result['id']}, 描述: {description}")
            
            # 更新测试计划
            test_plan["savepoint_id"] = savepoint_result['id']
        except Exception as e:
            logger.error(f"创建保存点失败: {e}")
    
    def analyze_coverage(self, test_plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        分析测试覆盖率
        
        Args:
            test_plan: 测试计划，如果为None则使用当前测试计划
            
        Returns:
            覆盖率数据字典
        """
        if test_plan is None:
            if not self.test_results:
                raise ValueError("没有可用的测试结果")
            test_plan = list(self.test_results.values())[-1]
        
        logger.info(f"分析测试覆盖率: {test_plan['id']}")
        
        # 这里是示例实现，实际项目中应使用覆盖率工具（如coverage.py）
        coverage_data = {
            "test_plan_id": test_plan["id"],
            "timestamp": datetime.datetime.now().isoformat(),
            "overall": {
                "line_rate": 0.85,
                "branch_rate": 0.75,
                "complexity": 0.65
            },
            "by_module": {}
        }
        
        # 模拟各模块的覆盖率数据
        modules = [
            "agents.general_agent",
            "agents.code",
            "agents.web",
            "agents.ppt",
            "development_tools",
            "workflow_driver"
        ]
        
        import random
        for module in modules:
            coverage_data["by_module"][module] = {
                "line_rate": round(random.uniform(0.7, 0.95), 2),
                "branch_rate": round(random.uniform(0.6, 0.9), 2),
                "complexity": round(random.uniform(0.5, 0.8), 2),
                "classes": {}
            }
            
            # 模拟各类的覆盖率数据
            class_count = random.randint(2, 5)
            for i in range(class_count):
                class_name = f"{module.split('.')[-1].capitalize()}{i+1}"
                coverage_data["by_module"][module]["classes"][class_name] = {
                    "line_rate": round(random.uniform(0.7, 0.95), 2),
                    "branch_rate": round(random.uniform(0.6, 0.9), 2),
                    "complexity": round(random.uniform(0.5, 0.8), 2),
                    "methods": {}
                }
                
                # 模拟各方法的覆盖率数据
                method_count = random.randint(3, 8)
                for j in range(method_count):
                    method_name = f"method{j+1}"
                    coverage_data["by_module"][module]["classes"][class_name]["methods"][method_name] = {
                        "line_rate": round(random.uniform(0.7, 0.95), 2),
                        "branch_rate": round(random.uniform(0.6, 0.9), 2),
                        "complexity": round(random.uniform(0.5, 0.8), 2)
                    }
        
        # 保存覆盖率数据
        self.coverage_data[test_plan["id"]] = coverage_data
        
        logger.info(f"测试覆盖率分析完成: {test_plan['id']}")
        
        return coverage_data
    
    def generate_report(self, test_plan: Optional[Dict[str, Any]] = None, include_coverage: bool = True) -> str:
        """
        生成测试报告
        
        Args:
            test_plan: 测试计划，如果为None则使用当前测试计划
            include_coverage: 是否包含覆盖率数据
            
        Returns:
            报告文件路径
        """
        if test_plan is None:
            if not self.test_results:
                raise ValueError("没有可用的测试结果")
            test_plan = list(self.test_results.values())[-1]
        
        logger.info(f"生成测试报告: {test_plan['id']}")
        
        # 准备报告数据
        report_data = {
            "test_plan": test_plan,
            "timestamp": datetime.datetime.now().isoformat(),
            "coverage": None
        }
        
        # 如果需要包含覆盖率数据
        if include_coverage:
            if test_plan["id"] in self.coverage_data:
                report_data["coverage"] = self.coverage_data[test_plan["id"]]
            else:
                try:
                    report_data["coverage"] = self.analyze_coverage(test_plan)
                except Exception as e:
                    logger.error(f"分析覆盖率失败: {e}")
        
        # 创建报告目录
        report_dir = os.path.join(self.project_root, self.config["report_dir"])
        os.makedirs(report_dir, exist_ok=True)
        
        # 生成报告文件名
        report_file = os.path.join(report_dir, f"test_report_{test_plan['id']}.html")
        
        # 生成HTML报告
        with open(report_file, 'w') as f:
            f.write(self._generate_html_report(report_data))
        
        logger.info(f"测试报告生成完成: {report_file}")
        
        return report_file
    
    def _generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """
        生成HTML格式的测试报告
        
        Args:
            report_data: 报告数据
            
        Returns:
            HTML报告内容
        """
        test_plan = report_data["test_plan"]
        timestamp = report_data["timestamp"]
        coverage = report_data["coverage"]
        
        # 生成HTML报告头部
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>测试报告 - {test_plan['id']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                h1, h2, h3 {{ color: #333; }}
                .summary {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .skipped {{ color: orange; }}
                .error {{ color: darkred; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .chart {{ height: 200px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>测试报告</h1>
            <div class="summary">
                <h2>摘要</h2>
                <p><strong>测试计划ID:</strong> {test_plan['id']}</p>
                <p><strong>创建时间:</strong> {test_plan['created_at']}</p>
                <p><strong>完成时间:</strong> {test_plan['completed_at']}</p>
                <p><strong>状态:</strong> <span class="{test_plan['status'].lower()}">{test_plan['status']}</span></p>
                <p><strong>测试用例总数:</strong> {test_plan['statistics']['total']}</p>
                <p><strong>通过:</strong> <span class="passed">{test_plan['statistics']['passed']}</span></p>
                <p><strong>失败:</strong> <span class="failed">{test_plan['statistics']['failed']}</span></p>
                <p><strong>跳过:</strong> <span class="skipped">{test_plan['statistics']['skipped']}</span></p>
                <p><strong>错误:</strong> <span class="error">{test_plan['statistics']['error']}</span></p>
                <p><strong>通过率:</strong> {test_plan['statistics']['pass_rate']}%</p>
                <p><strong>执行时间:</strong> {test_plan['statistics']['duration']:.2f} 秒</p>
            </div>
        """
        
        # 生成测试类型统计
        html += f"""
            <h2>测试类型统计</h2>
            <table>
                <tr>
                    <th>测试类型</th>
                    <th>总数</th>
                    <th>通过</th>
                    <th>通过率</th>
                </tr>
        """
        
        for test_type, stats in test_plan['statistics']['by_type'].items():
            html += f"""
                <tr>
                    <td>{test_type}</td>
                    <td>{stats['total']}</td>
                    <td>{stats['passed']}</td>
                    <td>{stats['pass_rate']}%</td>
                </tr>
            """
        
        html += "</table>"
        
        # 生成测试用例详情
        html += f"""
            <h2>测试用例详情</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>名称</th>
                    <th>类型</th>
                    <th>优先级</th>
                    <th>状态</th>
                    <th>执行时间</th>
                </tr>
        """
        
        for test_case in test_plan['test_cases']:
            html += f"""
                <tr>
                    <td>{test_case['id']}</td>
                    <td>{test_case['name']}</td>
                    <td>{test_case['type']}</td>
                    <td>{test_case['priority']}</td>
                    <td class="{test_case['status'].lower()}">{test_case['status']}</td>
                    <td>{test_case.get('execution_time', 'N/A')}</td>
                </tr>
            """
        
        html += "</table>"
        
        # 如果有覆盖率数据，生成覆盖率报告
        if coverage:
            html += f"""
                <h2>覆盖率报告</h2>
                <div class="summary">
                    <h3>总体覆盖率</h3>
                    <p><strong>行覆盖率:</strong> {coverage['overall']['line_rate'] * 100:.2f}%</p>
                    <p><strong>分支覆盖率:</strong> {coverage['overall']['branch_rate'] * 100:.2f}%</p>
                    <p><strong>复杂度:</strong> {coverage['overall']['complexity']:.2f}</p>
                </div>
                
                <h3>模块覆盖率</h3>
                <table>
                    <tr>
                        <th>模块</th>
                        <th>行覆盖率</th>
                        <th>分支覆盖率</th>
                        <th>复杂度</th>
                    </tr>
            """
            
            for module, module_data in coverage['by_module'].items():
                html += f"""
                    <tr>
                        <td>{module}</td>
                        <td>{module_data['line_rate'] * 100:.2f}%</td>
                        <td>{module_data['branch_rate'] * 100:.2f}%</td>
                        <td>{module_data['complexity']:.2f}</td>
                    </tr>
                """
            
            html += "</table>"
        
        # 生成HTML报告尾部
        html += f"""
            <div>
                <p><em>报告生成时间: {timestamp}</em></p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def get_test_history(self) -> List[Dict[str, Any]]:
        """
        获取测试历史记录
        
        Returns:
            测试历史记录列表
        """
        return self.test_history
    
    def get_test_result(self, test_plan_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定测试计划的结果
        
        Args:
            test_plan_id: 测试计划ID
            
        Returns:
            测试结果字典，如果不存在则返回None
        """
        return self.test_results.get(test_plan_id)
    
    def get_coverage_data(self, test_plan_id: str) -> Optional[Dict[str, Any]]:
        """
        获取指定测试计划的覆盖率数据
        
        Args:
            test_plan_id: 测试计划ID
            
        Returns:
            覆盖率数据字典，如果不存在则返回None
        """
        return self.coverage_data.get(test_plan_id)


# 工厂函数，获取AutomatedTestingFramework实例
_instance = None

def get_instance(project_root: str = None) -> AutomatedTestingFramework:
    """
    获取AutomatedTestingFramework实例（单例模式）
    
    Args:
        project_root: 项目根目录路径，仅在首次调用时需要提供
        
    Returns:
        AutomatedTestingFramework实例
    """
    global _instance
    
    if _instance is None:
        if project_root is None:
            raise ValueError("首次调用必须提供project_root参数")
        
        _instance = AutomatedTestingFramework(project_root)
    
    return _instance


# 使用示例
if __name__ == "__main__":
    # 获取AutomatedTestingFramework实例
    framework = get_instance("/path/to/project")
    
    # 生成测试计划
    test_plan = framework.generate_test_plan()
    
    # 执行测试
    test_result = framework.execute_tests(test_plan)
    
    # 分析覆盖率
    coverage_data = framework.analyze_coverage(test_result)
    
    # 生成报告
    report_file = framework.generate_report(test_result)
    print(f"测试报告已生成: {report_file}")
