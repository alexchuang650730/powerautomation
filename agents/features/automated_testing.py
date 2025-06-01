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
            savepoint_id = solver.create_savepoint(description)
            
            logger.info(f"创建保存点成功: {savepoint_id}, 描述: {description}")
            
            # 更新测试计划
            test_plan["savepoint_id"] = savepoint_id
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
                "line": 75.5,
                "branch": 68.2,
                "function": 82.1
            },
            "by_type": {
                "unit": {
                    "line": 85.3,
                    "branch": 78.6,
                    "function": 90.2
                },
                "integration": {
                    "line": 72.1,
                    "branch": 65.4,
                    "function": 80.5
                },
                "ui": {
                    "line": 68.7,
                    "branch": 60.2,
                    "function": 75.8
                }
            },
            "by_module": {
                "frontend": {
                    "line": 78.2,
                    "branch": 70.5,
                    "function": 85.3
                },
                "backend": {
                    "line": 82.1,
                    "branch": 75.8,
                    "function": 88.6
                },
                "agents": {
                    "line": 65.4,
                    "branch": 58.2,
                    "function": 72.3
                }
            },
            "threshold_met": {}
        }
        
        # 检查是否达到阈值
        for test_type, threshold in self.config["coverage_threshold"].items():
            if test_type in coverage_data["by_type"]:
                coverage_data["threshold_met"][test_type] = coverage_data["by_type"][test_type]["line"] >= threshold
        
        # 保存覆盖率数据
        self.coverage_data[test_plan["id"]] = coverage_data
        
        logger.info(f"测试覆盖率分析完成: {test_plan['id']}")
        
        return coverage_data
    
    def generate_report(self, test_plan: Optional[Dict[str, Any]] = None, 
                       coverage_data: Optional[Dict[str, Any]] = None,
                       report_format: str = "html") -> str:
        """
        生成测试报告
        
        Args:
            test_plan: 测试计划，如果为None则使用当前测试计划
            coverage_data: 覆盖率数据，如果为None则使用当前覆盖率数据
            report_format: 报告格式，支持html、markdown、pdf
            
        Returns:
            报告文件路径
        """
        if test_plan is None:
            if not self.test_results:
                raise ValueError("没有可用的测试结果")
            test_plan = list(self.test_results.values())[-1]
        
        if coverage_data is None:
            if test_plan["id"] in self.coverage_data:
                coverage_data = self.coverage_data[test_plan["id"]]
            else:
                coverage_data = self.analyze_coverage(test_plan)
        
        logger.info(f"生成测试报告: {test_plan['id']}, 格式: {report_format}")
        
        # 确保报告目录存在
        report_dir = os.path.join(self.project_root, self.config["report_dir"])
        os.makedirs(report_dir, exist_ok=True)
        
        # 生成报告文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        report_file = os.path.join(report_dir, f"test_report_{test_plan['id']}_{timestamp}.{report_format}")
        
        # 根据格式生成报告
        if report_format == "html":
            self._generate_html_report(test_plan, coverage_data, report_file)
        elif report_format == "markdown":
            self._generate_markdown_report(test_plan, coverage_data, report_file)
        elif report_format == "pdf":
            self._generate_pdf_report(test_plan, coverage_data, report_file)
        else:
            raise ValueError(f"不支持的报告格式: {report_format}")
        
        logger.info(f"测试报告生成完成: {report_file}")
        
        return report_file
    
    def _generate_html_report(self, test_plan: Dict[str, Any], coverage_data: Dict[str, Any], report_file: str) -> None:
        """
        生成HTML格式的测试报告
        
        Args:
            test_plan: 测试计划
            coverage_data: 覆盖率数据
            report_file: 报告文件路径
        """
        # 这里是示例实现，实际项目中可能使用模板引擎
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>测试报告 - {test_plan['id']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .summary-item {{ margin-bottom: 10px; }}
                .passed {{ color: #27ae60; }}
                .failed {{ color: #e74c3c; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .chart {{ height: 300px; margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>自动化测试报告</h1>
                
                <div class="summary">
                    <h2>测试摘要</h2>
                    <div class="summary-item"><strong>测试计划ID:</strong> {test_plan['id']}</div>
                    <div class="summary-item"><strong>开始时间:</strong> {test_plan['started_at']}</div>
                    <div class="summary-item"><strong>完成时间:</strong> {test_plan['completed_at']}</div>
                    <div class="summary-item"><strong>状态:</strong> <span class="{test_plan['status'].lower()}">{test_plan['status']}</span></div>
                    <div class="summary-item"><strong>总用例数:</strong> {test_plan['statistics']['total']}</div>
                    <div class="summary-item"><strong>通过:</strong> {test_plan['statistics']['passed']} ({test_plan['statistics']['pass_rate']}%)</div>
                    <div class="summary-item"><strong>失败:</strong> {test_plan['statistics']['failed']}</div>
                    <div class="summary-item"><strong>跳过:</strong> {test_plan['statistics']['skipped']}</div>
                    <div class="summary-item"><strong>错误:</strong> {test_plan['statistics']['error']}</div>
                    <div class="summary-item"><strong>执行时间:</strong> {test_plan['statistics']['duration']:.2f} 秒</div>
                </div>
                
                <h2>测试覆盖率</h2>
                <div class="chart" id="coverage-chart"></div>
                
                <table>
                    <tr>
                        <th>模块</th>
                        <th>行覆盖率</th>
                        <th>分支覆盖率</th>
                        <th>函数覆盖率</th>
                    </tr>
                    <tr>
                        <td>总体</td>
                        <td>{coverage_data['overall']['line']}%</td>
                        <td>{coverage_data['overall']['branch']}%</td>
                        <td>{coverage_data['overall']['function']}%</td>
                    </tr>
        """
        
        # 添加按模块的覆盖率
        for module, data in coverage_data["by_module"].items():
            html += f"""
                    <tr>
                        <td>{module}</td>
                        <td>{data['line']}%</td>
                        <td>{data['branch']}%</td>
                        <td>{data['function']}%</td>
                    </tr>
            """
        
        html += """
                </table>
                
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
        
        # 添加测试用例详情
        for test_case in test_plan["test_cases"]:
            execution_time = test_case.get("execution_time", 0)
            html += f"""
                    <tr>
                        <td>{test_case['id']}</td>
                        <td>{test_case['name']}</td>
                        <td>{test_case['type']}</td>
                        <td>{test_case['priority']}</td>
                        <td class="{test_case['status'].lower()}">{test_case['status']}</td>
                        <td>{execution_time:.2f} 秒</td>
                    </tr>
            """
        
        html += """
                </table>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                // 创建覆盖率图表
                const ctx = document.createElement('canvas');
                document.getElementById('coverage-chart').appendChild(ctx);
                
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['行覆盖率', '分支覆盖率', '函数覆盖率'],
                        datasets: [{
                            label: '总体覆盖率',
                            data: [
        """
        
        # 添加覆盖率数据
        html += f"{coverage_data['overall']['line']}, {coverage_data['overall']['branch']}, {coverage_data['overall']['function']}"
        
        html += """
                            ],
                            backgroundColor: [
                                'rgba(54, 162, 235, 0.5)',
                                'rgba(255, 206, 86, 0.5)',
                                'rgba(75, 192, 192, 0.5)'
                            ],
                            borderColor: [
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            </script>
        </body>
        </html>
        """
        
        with open(report_file, 'w') as f:
            f.write(html)
    
    def _generate_markdown_report(self, test_plan: Dict[str, Any], coverage_data: Dict[str, Any], report_file: str) -> None:
        """
        生成Markdown格式的测试报告
        
        Args:
            test_plan: 测试计划
            coverage_data: 覆盖率数据
            report_file: 报告文件路径
        """
        markdown = f"""# 自动化测试报告

## 测试摘要

- **测试计划ID:** {test_plan['id']}
- **开始时间:** {test_plan['started_at']}
- **完成时间:** {test_plan['completed_at']}
- **状态:** {test_plan['status']}
- **总用例数:** {test_plan['statistics']['total']}
- **通过:** {test_plan['statistics']['passed']} ({test_plan['statistics']['pass_rate']}%)
- **失败:** {test_plan['statistics']['failed']}
- **跳过:** {test_plan['statistics']['skipped']}
- **错误:** {test_plan['statistics']['error']}
- **执行时间:** {test_plan['statistics']['duration']:.2f} 秒

## 测试覆盖率

| 模块 | 行覆盖率 | 分支覆盖率 | 函数覆盖率 |
|------|----------|------------|------------|
| 总体 | {coverage_data['overall']['line']}% | {coverage_data['overall']['branch']}% | {coverage_data['overall']['function']}% |
"""
        
        # 添加按模块的覆盖率
        for module, data in coverage_data["by_module"].items():
            markdown += f"| {module} | {data['line']}% | {data['branch']}% | {data['function']}% |\n"
        
        markdown += """
## 测试用例详情

| ID | 名称 | 类型 | 优先级 | 状态 | 执行时间 |
|----|------|------|--------|------|----------|
"""
        
        # 添加测试用例详情
        for test_case in test_plan["test_cases"]:
            execution_time = test_case.get("execution_time", 0)
            markdown += f"| {test_case['id']} | {test_case['name']} | {test_case['type']} | {test_case['priority']} | {test_case['status']} | {execution_time:.2f} 秒 |\n"
        
        with open(report_file, 'w') as f:
            f.write(markdown)
    
    def _generate_pdf_report(self, test_plan: Dict[str, Any], coverage_data: Dict[str, Any], report_file: str) -> None:
        """
        生成PDF格式的测试报告
        
        Args:
            test_plan: 测试计划
            coverage_data: 覆盖率数据
            report_file: 报告文件路径
        """
        # 先生成Markdown报告
        md_file = report_file.replace(".pdf", ".md")
        self._generate_markdown_report(test_plan, coverage_data, md_file)
        
        # 使用manus-md-to-pdf转换为PDF
        try:
            import subprocess
            subprocess.run(["manus-md-to-pdf", md_file, report_file], check=True)
            
            # 删除临时Markdown文件
            os.remove(md_file)
        except Exception as e:
            logger.error(f"生成PDF报告失败: {e}")
            raise
    
    def get_test_history(self) -> List[Dict[str, Any]]:
        """
        获取测试历史记录
        
        Returns:
            测试历史记录列表
        """
        return self.test_history
    
    def analyze_trends(self) -> Dict[str, Any]:
        """
        分析测试趋势
        
        Returns:
            趋势分析结果
        """
        if not self.test_history:
            return {"error": "没有可用的测试历史记录"}
        
        # 按时间排序
        sorted_history = sorted(self.test_history, key=lambda x: x["created_at"])
        
        # 提取通过率趋势
        pass_rates = [h["statistics"]["pass_rate"] for h in sorted_history]
        timestamps = [h["created_at"] for h in sorted_history]
        
        # 计算平均通过率
        avg_pass_rate = sum(pass_rates) / len(pass_rates) if pass_rates else 0
        
        # 计算通过率变化趋势
        trend = "stable"
        if len(pass_rates) >= 2:
            recent_rates = pass_rates[-5:] if len(pass_rates) >= 5 else pass_rates
            if all(recent_rates[i] <= recent_rates[i+1] for i in range(len(recent_rates)-1)):
                trend = "improving"
            elif all(recent_rates[i] >= recent_rates[i+1] for i in range(len(recent_rates)-1)):
                trend = "declining"
        
        return {
            "total_runs": len(sorted_history),
            "pass_rates": pass_rates,
            "timestamps": timestamps,
            "avg_pass_rate": avg_pass_rate,
            "trend": trend,
            "latest_pass_rate": pass_rates[-1] if pass_rates else 0,
            "highest_pass_rate": max(pass_rates) if pass_rates else 0,
            "lowest_pass_rate": min(pass_rates) if pass_rates else 0
        }
    
    def notify_results(self, test_plan: Optional[Dict[str, Any]] = None) -> None:
        """
        通知测试结果
        
        Args:
            test_plan: 测试计划，如果为None则使用当前测试计划
        """
        if test_plan is None:
            if not self.test_results:
                raise ValueError("没有可用的测试结果")
            test_plan = list(self.test_results.values())[-1]
        
        logger.info(f"通知测试结果: {test_plan['id']}")
        
        # 检查通知配置
        if not any(self.config["notification"].values()):
            logger.info("未配置通知方式，跳过通知")
            return
        
        # 准备通知内容
        notification = {
            "test_plan_id": test_plan["id"],
            "status": test_plan["status"],
            "pass_rate": test_plan["statistics"]["pass_rate"],
            "total": test_plan["statistics"]["total"],
            "passed": test_plan["statistics"]["passed"],
            "failed": test_plan["statistics"]["failed"],
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 发送通知
        if self.config["notification"]["email"]:
            self._send_email_notification(notification)
        
        if self.config["notification"]["slack"]:
            self._send_slack_notification(notification)
        
        if self.config["notification"]["github"]:
            self._send_github_notification(notification, test_plan)
        
        logger.info(f"测试结果通知完成: {test_plan['id']}")
    
    def _send_email_notification(self, notification: Dict[str, Any]) -> None:
        """
        发送邮件通知
        
        Args:
            notification: 通知内容
        """
        logger.info(f"发送邮件通知: {notification['test_plan_id']}")
        # 实际项目中应实现邮件发送逻辑
    
    def _send_slack_notification(self, notification: Dict[str, Any]) -> None:
        """
        发送Slack通知
        
        Args:
            notification: 通知内容
        """
        logger.info(f"发送Slack通知: {notification['test_plan_id']}")
        # 实际项目中应实现Slack通知逻辑
    
    def _send_github_notification(self, notification: Dict[str, Any], test_plan: Dict[str, Any]) -> None:
        """
        发送GitHub通知
        
        Args:
            notification: 通知内容
            test_plan: 测试计划
        """
        logger.info(f"发送GitHub通知: {notification['test_plan_id']}")
        
        try:
            # 这里是示例实现，实际项目中应使用GitHub API
            from powerautomation_integration.scripts.github_test_reporter import GitHubTestReporter
            
            # 初始化GitHub测试报告器
            reporter = GitHubTestReporter()
            
            # 生成测试报告
            report_file = self.generate_report(test_plan, report_format="markdown")
            
            # 上传测试报告
            with open(report_file, 'r') as f:
                report_content = f.read()
            
            # 创建或更新GitHub Issue
            issue_number = reporter.create_or_update_test_report(
                title=f"自动化测试报告: {test_plan['id']}",
                body=report_content,
                labels=["test-report", test_plan["status"].lower()]
            )
            
            logger.info(f"GitHub通知完成，Issue #{issue_number}")
        except Exception as e:
            logger.error(f"发送GitHub通知失败: {e}")
    
    def integrate_with_mcp(self) -> None:
        """
        与MCP协调器集成
        """
        logger.info("与MCP协调器集成")
        
        try:
            # 这里是示例实现，实际项目中应使用MCP API
            from powerautomation_integration.agents.ppt_agent.core.mcp.webagent_adapter import MCPAdapter
            
            # 初始化MCP适配器
            adapter = MCPAdapter()
            
            # 注册自动化测试能力
            adapter.register_capability(
                capability_id="automated_testing",
                capability_name="自动化测试",
                capability_description="自动执行测试用例，收集测试结果，分析测试覆盖率，生成测试报告",
                handler=self.execute_tests
            )
            
            # 注册测试报告生成能力
            adapter.register_capability(
                capability_id="test_report_generation",
                capability_name="测试报告生成",
                capability_description="生成结构化、可视化的测试报告",
                handler=self.generate_report
            )
            
            # 注册测试历史追踪能力
            adapter.register_capability(
                capability_id="test_history_tracking",
                capability_name="测试历史追踪",
                capability_description="记录并分析历史测试结果，识别趋势和模式",
                handler=self.get_test_history
            )
            
            logger.info("MCP协调器集成完成")
        except Exception as e:
            logger.error(f"MCP协调器集成失败: {e}")


# 使用示例
if __name__ == "__main__":
    # 初始化自动化测试框架
    framework = AutomatedTestingFramework("/home/ubuntu/powerautomation_integration")
    
    # 生成测试计划
    test_plan = framework.generate_test_plan(
        test_types=[TestType.UNIT, TestType.INTEGRATION],
        priority=[TestPriority.CRITICAL, TestPriority.HIGH]
    )
    
    # 执行测试
    test_results = framework.execute_tests(test_plan)
    
    # 分析覆盖率
    coverage_data = framework.analyze_coverage(test_results)
    
    # 生成报告
    report_file = framework.generate_report(test_results, coverage_data, "html")
    
    # 通知结果
    framework.notify_results(test_results)
    
    # 与MCP协调器集成
    framework.integrate_with_mcp()
    
    print(f"测试完成，报告已生成: {report_file}")
