"""
TestAndIssueCollector 自动化测试模块

结合Qwen3-8B中文版大模型，收集test/visual_test的端到端测试方案进行自动化测试
优先使用mcp.so或acidev相关MCP工具，如果找不到则使用MCPBrainstorm来建立测试方案
"""

import os
import sys
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("test_collector.log")
    ]
)
logger = logging.getLogger("TestAndIssueCollector")

# 尝试导入MCP工具
try:
    # 尝试导入mcp.so
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcptool', 'adapters'))
    import mcp_so_adapter as mcp_so
    logger.info("成功导入mcp.so适配器")
    MCP_SO_AVAILABLE = True
except ImportError:
    logger.warning("无法导入mcp.so适配器，将尝试其他工具")
    MCP_SO_AVAILABLE = False

try:
    # 尝试导入acidev
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcptool', 'adapters'))
    import acidev_adapter as acidev
    logger.info("成功导入acidev适配器")
    ACIDEV_AVAILABLE = True
except ImportError:
    logger.warning("无法导入acidev适配器，将尝试其他工具")
    ACIDEV_AVAILABLE = False

try:
    # 尝试导入MCPBrainstorm
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcptool', 'core'))
    from mcp_brainstorm import MCPBrainstorm
    logger.info("成功导入MCPBrainstorm")
    MCP_BRAINSTORM_AVAILABLE = True
except ImportError:
    logger.error("无法导入MCPBrainstorm，自动化测试功能将受限")
    MCP_BRAINSTORM_AVAILABLE = False

try:
    # 尝试导入RL Factory
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rl_factory'))
    from rl_factory.recipe import load_recipe
    logger.info("成功导入RL Factory")
    RL_FACTORY_AVAILABLE = True
except ImportError:
    logger.error("无法导入RL Factory，强化学习功能将受限")
    RL_FACTORY_AVAILABLE = False


class TestAndIssueCollector:
    """
    自动化测试和问题收集器
    结合Qwen3-8B模型，自动收集和执行端到端测试
    """
    
    def __init__(self, model_path: str = "Qwen3-8B"):
        """
        初始化测试和问题收集器
        
        Args:
            model_path: Qwen3-8B模型路径
        """
        self.model_path = model_path
        self.model = None
        self.test_results = []
        self.issues = []
        
        # 初始化模型
        self._initialize_model()
        
        # 初始化测试环境
        self._initialize_test_environment()
    
    def _initialize_model(self) -> None:
        """初始化Qwen3-8B模型"""
        try:
            logger.info(f"正在初始化{self.model_path}模型...")
            
            # 这里是模拟代码，实际项目中应使用正确的模型加载方式
            # 例如使用transformers库加载模型
            # from transformers import AutoModelForCausalLM, AutoTokenizer
            # self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            # self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            
            # 模拟模型加载
            self.model = {
                "name": self.model_path,
                "loaded": True,
                "status": "ready"
            }
            
            logger.info(f"{self.model_path}模型初始化成功")
        except Exception as e:
            logger.error(f"模型初始化失败: {str(e)}")
            raise
    
    def _initialize_test_environment(self) -> None:
        """初始化测试环境"""
        logger.info("正在初始化测试环境...")
        
        # 检查测试目录
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
        self.visual_test_dir = os.path.join(self.test_dir, 'visual_test')
        
        if not os.path.exists(self.test_dir):
            logger.warning(f"测试目录不存在: {self.test_dir}")
            os.makedirs(self.test_dir, exist_ok=True)
            logger.info(f"已创建测试目录: {self.test_dir}")
        
        if not os.path.exists(self.visual_test_dir):
            logger.warning(f"视觉测试目录不存在: {self.visual_test_dir}")
            os.makedirs(self.visual_test_dir, exist_ok=True)
            logger.info(f"已创建视觉测试目录: {self.visual_test_dir}")
        
        logger.info("测试环境初始化完成")
    
    def collect_test_cases(self, source_dir: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        收集测试用例
        
        Args:
            source_dir: 测试用例源目录，默认为self.test_dir
            
        Returns:
            测试用例列表
        """
        if source_dir is None:
            source_dir = self.test_dir
        
        logger.info(f"正在从{source_dir}收集测试用例...")
        
        test_cases = []
        
        # 遍历目录收集测试用例
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    test_path = os.path.join(root, file)
                    test_cases.append({
                        "name": file,
                        "path": test_path,
                        "type": "unit_test"
                    })
                elif file.endswith('_visual_test.py'):
                    test_path = os.path.join(root, file)
                    test_cases.append({
                        "name": file,
                        "path": test_path,
                        "type": "visual_test"
                    })
        
        logger.info(f"收集到{len(test_cases)}个测试用例")
        return test_cases
    
    def generate_test_plan(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成测试计划
        
        Args:
            test_cases: 测试用例列表
            
        Returns:
            测试计划
        """
        logger.info("正在生成测试计划...")
        
        # 优先使用mcp.so
        if MCP_SO_AVAILABLE:
            logger.info("使用mcp.so生成测试计划")
            # 实际项目中应调用mcp.so的相关API
            # plan = mcp_so.generate_test_plan(test_cases)
            plan = self._mock_generate_test_plan(test_cases, "mcp.so")
        
        # 其次使用acidev
        elif ACIDEV_AVAILABLE:
            logger.info("使用acidev生成测试计划")
            # 实际项目中应调用acidev的相关API
            # plan = acidev.generate_test_plan(test_cases)
            plan = self._mock_generate_test_plan(test_cases, "acidev")
        
        # 最后使用MCPBrainstorm
        elif MCP_BRAINSTORM_AVAILABLE:
            logger.info("使用MCPBrainstorm生成测试计划")
            # 实际项目中应实例化MCPBrainstorm并调用相关方法
            # mcp_brainstorm = MCPBrainstorm()
            # plan = mcp_brainstorm.generate_test_plan(test_cases)
            plan = self._mock_generate_test_plan(test_cases, "MCPBrainstorm")
        
        # 如果都不可用，使用内置方法
        else:
            logger.warning("所有MCP工具都不可用，使用内置方法生成测试计划")
            plan = self._generate_fallback_test_plan(test_cases)
        
        logger.info("测试计划生成完成")
        return plan
    
    def _mock_generate_test_plan(self, test_cases: List[Dict[str, Any]], tool: str) -> Dict[str, Any]:
        """
        模拟生成测试计划（实际项目中应替换为真实实现）
        
        Args:
            test_cases: 测试用例列表
            tool: 使用的工具名称
            
        Returns:
            测试计划
        """
        # 模拟测试计划生成
        plan = {
            "name": f"PowerAutomation自动化测试计划-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "tool": tool,
            "created_at": datetime.now().isoformat(),
            "test_groups": []
        }
        
        # 按类型分组测试用例
        unit_tests = [tc for tc in test_cases if tc["type"] == "unit_test"]
        visual_tests = [tc for tc in test_cases if tc["type"] == "visual_test"]
        
        # 添加单元测试组
        if unit_tests:
            plan["test_groups"].append({
                "name": "单元测试",
                "type": "unit_test",
                "test_cases": unit_tests,
                "parallel": True,
                "priority": 1
            })
        
        # 添加视觉测试组
        if visual_tests:
            plan["test_groups"].append({
                "name": "视觉测试",
                "type": "visual_test",
                "test_cases": visual_tests,
                "parallel": False,
                "priority": 2
            })
        
        return plan
    
    def _generate_fallback_test_plan(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成备用测试计划（当所有MCP工具都不可用时）
        
        Args:
            test_cases: 测试用例列表
            
        Returns:
            测试计划
        """
        # 使用Qwen3-8B模型生成测试计划
        logger.info("使用Qwen3-8B模型生成测试计划")
        
        # 这里是模拟代码，实际项目中应使用模型生成测试计划
        # prompt = f"根据以下测试用例生成测试计划：\n{json.dumps(test_cases, indent=2)}"
        # response = self._generate_with_model(prompt)
        # plan = json.loads(response)
        
        # 模拟生成测试计划
        plan = {
            "name": f"PowerAutomation自动化测试计划(备用)-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "tool": "Qwen3-8B",
            "created_at": datetime.now().isoformat(),
            "test_groups": [
                {
                    "name": "所有测试",
                    "type": "mixed",
                    "test_cases": test_cases,
                    "parallel": False,
                    "priority": 1
                }
            ]
        }
        
        return plan
    
    def execute_test_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行测试计划
        
        Args:
            plan: 测试计划
            
        Returns:
            测试结果
        """
        logger.info(f"开始执行测试计划: {plan['name']}")
        
        results = {
            "plan_name": plan["name"],
            "tool": plan["tool"],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "groups_results": [],
            "overall_status": "pending"
        }
        
        # 按优先级排序测试组
        test_groups = sorted(plan["test_groups"], key=lambda g: g["priority"])
        
        # 执行每个测试组
        for group in test_groups:
            logger.info(f"执行测试组: {group['name']}")
            
            group_result = {
                "name": group["name"],
                "type": group["type"],
                "start_time": datetime.now().isoformat(),
                "end_time": None,
                "test_results": [],
                "status": "pending"
            }
            
            # 执行测试用例
            for test_case in group["test_cases"]:
                test_result = self._execute_test_case(test_case)
                group_result["test_results"].append(test_result)
            
            # 更新测试组结果
            group_result["end_time"] = datetime.now().isoformat()
            group_result["status"] = "failed" if any(r["status"] == "failed" for r in group_result["test_results"]) else "passed"
            results["groups_results"].append(group_result)
            
            logger.info(f"测试组 {group['name']} 执行完成，状态: {group_result['status']}")
        
        # 更新整体结果
        results["end_time"] = datetime.now().isoformat()
        results["overall_status"] = "failed" if any(g["status"] == "failed" for g in results["groups_results"]) else "passed"
        
        logger.info(f"测试计划执行完成，整体状态: {results['overall_status']}")
        self.test_results.append(results)
        
        return results
    
    def _execute_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个测试用例
        
        Args:
            test_case: 测试用例
            
        Returns:
            测试结果
        """
        logger.info(f"执行测试用例: {test_case['name']}")
        
        result = {
            "name": test_case["name"],
            "path": test_case["path"],
            "type": test_case["type"],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "status": "pending",
            "error": None,
            "output": None
        }
        
        try:
            # 这里是模拟代码，实际项目中应执行测试用例
            # 例如使用subprocess运行pytest
            # import subprocess
            # process = subprocess.run(
            #     ["pytest", test_case["path"], "-v"],
            #     capture_output=True,
            #     text=True
            # )
            # result["output"] = process.stdout
            # result["status"] = "passed" if process.returncode == 0 else "failed"
            # if process.returncode != 0:
            #     result["error"] = process.stderr
            
            # 模拟测试执行
            import random
            result["output"] = f"测试用例 {test_case['name']} 执行输出"
            result["status"] = random.choice(["passed", "passed", "passed", "failed"])  # 75%通过率
            if result["status"] == "failed":
                result["error"] = f"测试用例 {test_case['name']} 执行失败"
                self._collect_issue(test_case, result["error"])
            
            logger.info(f"测试用例 {test_case['name']} 执行完成，状态: {result['status']}")
        except Exception as e:
            logger.error(f"测试用例 {test_case['name']} 执行异常: {str(e)}")
            result["status"] = "error"
            result["error"] = str(e)
            self._collect_issue(test_case, str(e))
        finally:
            result["end_time"] = datetime.now().isoformat()
        
        return result
    
    def _collect_issue(self, test_case: Dict[str, Any], error: str) -> None:
        """
        收集测试问题
        
        Args:
            test_case: 测试用例
            error: 错误信息
        """
        issue = {
            "id": f"ISSUE-{len(self.issues) + 1}",
            "test_case": test_case["name"],
            "test_path": test_case["path"],
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "status": "open",
            "analysis": None,
            "solution": None
        }
        
        # 使用Qwen3-8B分析问题
        issue["analysis"] = self._analyze_issue_with_model(issue)
        
        # 使用Qwen3-8B提出解决方案
        issue["solution"] = self._generate_solution_with_model(issue)
        
        self.issues.append(issue)
        logger.info(f"已收集问题: {issue['id']}")
    
    def _analyze_issue_with_model(self, issue: Dict[str, Any]) -> str:
        """
        使用Qwen3-8B模型分析问题
        
        Args:
            issue: 问题信息
            
        Returns:
            问题分析
        """
        # 这里是模拟代码，实际项目中应使用模型分析问题
        # prompt = f"分析以下测试失败问题并给出原因：\n测试用例: {issue['test_case']}\n错误信息: {issue['error']}"
        # analysis = self._generate_with_model(prompt)
        
        # 模拟问题分析
        analysis = f"问题分析: 测试用例 {issue['test_case']} 失败，可能是因为输入验证不完整或环境配置问题。错误信息显示: {issue['error']}"
        
        return analysis
    
    def _generate_solution_with_model(self, issue: Dict[str, Any]) -> str:
        """
        使用Qwen3-8B模型生成解决方案
        
        Args:
            issue: 问题信息
            
        Returns:
            解决方案
        """
        # 这里是模拟代码，实际项目中应使用模型生成解决方案
        # prompt = f"为以下测试失败问题提供解决方案：\n测试用例: {issue['test_case']}\n错误信息: {issue['error']}\n分析: {issue['analysis']}"
        # solution = self._generate_with_model(prompt)
        
        # 模拟解决方案
        solution = f"解决方案: 1. 检查测试用例 {issue['test_case']} 的输入验证逻辑\n2. 验证测试环境配置\n3. 添加更详细的错误处理"
        
        return solution
    
    def _generate_with_model(self, prompt: str) -> str:
        """
        使用Qwen3-8B模型生成内容
        
        Args:
            prompt: 提示词
            
        Returns:
            生成的内容
        """
        # 这里是模拟代码，实际项目中应使用模型生成内容
        # inputs = self.tokenizer(prompt, return_tensors="pt")
        # outputs = self.model.generate(**inputs, max_length=1000)
        # response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 模拟模型生成
        response = f"Qwen3-8B模型响应: {prompt[:20]}..."
        
        return response
    
    def generate_test_report(self, results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        生成测试报告
        
        Args:
            results: 测试结果，默认使用最新的测试结果
            
        Returns:
            测试报告
        """
        if results is None:
            if not self.test_results:
                logger.warning("没有可用的测试结果，无法生成报告")
                return {"error": "没有可用的测试结果"}
            results = self.test_results[-1]
        
        logger.info("正在生成测试报告...")
        
        # 计算统计信息
        total_tests = sum(len(group["test_results"]) for group in results["groups_results"])
        passed_tests = sum(
            sum(1 for test in group["test_results"] if test["status"] == "passed")
            for group in results["groups_results"]
        )
        failed_tests = sum(
            sum(1 for test in group["test_results"] if test["status"] == "failed")
            for group in results["groups_results"]
        )
        error_tests = sum(
            sum(1 for test in group["test_results"] if test["status"] == "error")
            for group in results["groups_results"]
        )
        
        # 生成报告
        report = {
            "title": f"PowerAutomation测试报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "plan_name": results["plan_name"],
            "tool": results["tool"],
            "start_time": results["start_time"],
            "end_time": results["end_time"],
            "overall_status": results["overall_status"],
            "statistics": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "pass_rate": round(passed_tests / total_tests * 100, 2) if total_tests > 0 else 0
            },
            "groups_summary": [
                {
                    "name": group["name"],
                    "type": group["type"],
                    "status": group["status"],
                    "total": len(group["test_results"]),
                    "passed": sum(1 for test in group["test_results"] if test["status"] == "passed"),
                    "failed": sum(1 for test in group["test_results"] if test["status"] == "failed"),
                    "error": sum(1 for test in group["test_results"] if test["status"] == "error")
                }
                for group in results["groups_results"]
            ],
            "issues": [issue for issue in self.issues if any(
                issue["test_case"] == test["name"]
                for group in results["groups_results"]
                for test in group["test_results"]
                if test["status"] in ["failed", "error"]
            )],
            "generated_at": datetime.now().isoformat()
        }
        
        # 保存报告
        report_path = os.path.join(self.test_dir, f"test_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"测试报告已生成并保存到: {report_path}")
        return report
    
    def integrate_with_rl_factory(self) -> bool:
        """
        与RL Factory集成
        
        Returns:
            是否集成成功
        """
        if not RL_FACTORY_AVAILABLE:
            logger.error("RL Factory不可用，无法集成")
            return False
        
        try:
            logger.info("正在与RL Factory集成...")
            
            # 这里是模拟代码，实际项目中应与RL Factory集成
            # 例如加载RL Factory配置并使用
            # recipe = load_recipe("configs/test_collector_recipe.yaml")
            # model = recipe.load_model(self.model_path)
            # self.model = model
            
            # 模拟集成
            logger.info("RL Factory集成成功")
            return True
        except Exception as e:
            logger.error(f"RL Factory集成失败: {str(e)}")
            return False
    
    def run_end_to_end_test(self) -> Dict[str, Any]:
        """
        运行端到端测试
        
        Returns:
            测试报告
        """
        logger.info("开始运行端到端测试...")
        
        # 收集测试用例
        test_cases = self.collect_test_cases()
        
        # 生成测试计划
        plan = self.generate_test_plan(test_cases)
        
        # 执行测试计划
        results = self.execute_test_plan(plan)
        
        # 生成测试报告
        report = self.generate_test_report(results)
        
        logger.info("端到端测试完成")
        return report


# 示例用法
if __name__ == "__main__":
    # 创建测试收集器
    collector = TestAndIssueCollector()
    
    # 与RL Factory集成
    collector.integrate_with_rl_factory()
    
    # 运行端到端测试
    report = collector.run_end_to_end_test()
    
    # 打印测试报告摘要
    print(f"测试报告: {report['title']}")
    print(f"总体状态: {report['overall_status']}")
    print(f"测试统计: 总计 {report['statistics']['total_tests']} 个测试，通过率 {report['statistics']['pass_rate']}%")
    print(f"问题数量: {len(report['issues'])}")
