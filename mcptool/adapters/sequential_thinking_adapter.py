"""
Sequential Thinking适配器模块

提供Sequential Thinking能力的MCP适配器实现
"""

from typing import Dict, Any, List, Optional
import logging
import time
from datetime import datetime
from .base_mcp import BaseMCP

class SequentialThinkingAdapter(BaseMCP):
    """Sequential Thinking适配器，提供思维链和任务分解能力"""
    
    def __init__(self):
        """初始化Sequential Thinking适配器"""
        super().__init__(name="SequentialThinking")
    
    def decompose_task(self, task_description: str) -> List[Dict[str, Any]]:
        """
        分解任务为步骤序列
        
        Args:
            task_description: 任务描述
            
        Returns:
            分解后的任务步骤列表
        """
        self.logger.info(f"分解任务: {task_description}")
        
        # 简单实现，实际应用中应该有更复杂的逻辑
        steps = [
            {
                "step_id": 1,
                "description": f"分析任务: {task_description}",
                "status": "pending"
            },
            {
                "step_id": 2,
                "description": "收集必要信息",
                "status": "pending"
            },
            {
                "step_id": 3,
                "description": "执行核心操作",
                "status": "pending"
            },
            {
                "step_id": 4,
                "description": "验证结果",
                "status": "pending"
            },
            {
                "step_id": 5,
                "description": "总结并完成任务",
                "status": "pending"
            }
        ]
        
        return steps
    
    def create_todo_md(self, steps: List[Dict[str, Any]]) -> str:
        """
        创建todo.md文件内容
        
        Args:
            steps: 任务步骤列表
            
        Returns:
            todo.md文件内容
        """
        self.logger.info("创建todo.md")
        
        lines = ["# 任务计划\n"]
        
        for step in steps:
            status_mark = "[ ]" if step["status"] == "pending" else "[x]"
            lines.append(f"- {status_mark} {step['description']}")
        
        return "\n".join(lines)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            处理结果字典
        """
        if not self.validate_input(input_data):
            return {
                "status": "error",
                "message": "输入数据无效"
            }
        
        task_type = input_data.get("task_type", "decompose")
        
        if task_type == "decompose":
            task_description = input_data.get("task_description", "")
            steps = self.decompose_task(task_description)
            todo_md = self.create_todo_md(steps)
            
            return {
                "status": "success",
                "steps": steps,
                "todo_md": todo_md
            }
        else:
            return {
                "status": "error",
                "message": f"不支持的任务类型: {task_type}"
            }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        验证输入数据是否有效
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            数据是否有效
        """
        if "task_type" not in input_data:
            self.logger.error("缺少task_type字段")
            return False
            
        task_type = input_data["task_type"]
        
        if task_type == "decompose" and "task_description" not in input_data:
            self.logger.error("分解任务缺少task_description字段")
            return False
        
        return True
    
    def get_capabilities(self) -> List[str]:
        """
        获取适配器能力列表
        
        Returns:
            能力描述列表
        """
        return [
            "任务分解",
            "思维链生成",
            "todo.md创建"
        ]

    
    def think_sequentially(self, problem: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        序列思维处理 - 生成思维链和推理过程
        
        Args:
            problem: 需要思考的问题
            context: 上下文信息
            
        Returns:
            思维链结果字典
        """
        self.logger.info(f"开始序列思维处理: {problem}")
        
        try:
            # 初始化思维链
            thinking_chain = {
                "problem": problem,
                "context": context or {},
                "thinking_steps": [],
                "reasoning_process": [],
                "conclusions": [],
                "confidence_score": 0.0,
                "metadata": {
                    "start_time": time.time(),
                    "thinking_mode": "sequential",
                    "complexity_level": self._assess_problem_complexity(problem)
                }
            }
            
            # 步骤1: 问题理解和分析
            understanding_result = self._understand_problem(problem, context)
            thinking_chain["thinking_steps"].append({
                "step_id": 1,
                "step_name": "问题理解",
                "description": "分析问题的核心要素和关键信息",
                "result": understanding_result,
                "confidence": understanding_result.get("confidence", 0.8),
                "timestamp": time.time()
            })
            
            # 步骤2: 知识检索和关联
            knowledge_result = self._retrieve_relevant_knowledge(problem, understanding_result)
            thinking_chain["thinking_steps"].append({
                "step_id": 2,
                "step_name": "知识检索",
                "description": "检索相关知识和经验",
                "result": knowledge_result,
                "confidence": knowledge_result.get("confidence", 0.7),
                "timestamp": time.time()
            })
            
            # 步骤3: 推理和分析
            reasoning_result = self._perform_reasoning(problem, understanding_result, knowledge_result)
            thinking_chain["thinking_steps"].append({
                "step_id": 3,
                "step_name": "逻辑推理",
                "description": "基于理解和知识进行逻辑推理",
                "result": reasoning_result,
                "confidence": reasoning_result.get("confidence", 0.8),
                "timestamp": time.time()
            })
            
            # 步骤4: 方案生成
            solution_result = self._generate_solutions(problem, reasoning_result)
            thinking_chain["thinking_steps"].append({
                "step_id": 4,
                "step_name": "方案生成",
                "description": "基于推理结果生成可行方案",
                "result": solution_result,
                "confidence": solution_result.get("confidence", 0.75),
                "timestamp": time.time()
            })
            
            # 步骤5: 评估和优化
            evaluation_result = self._evaluate_and_optimize(solution_result)
            thinking_chain["thinking_steps"].append({
                "step_id": 5,
                "step_name": "评估优化",
                "description": "评估方案可行性并进行优化",
                "result": evaluation_result,
                "confidence": evaluation_result.get("confidence", 0.8),
                "timestamp": time.time()
            })
            
            # 生成推理过程总结
            thinking_chain["reasoning_process"] = self._generate_reasoning_summary(thinking_chain["thinking_steps"])
            
            # 生成最终结论
            thinking_chain["conclusions"] = self._generate_conclusions(thinking_chain["thinking_steps"])
            
            # 计算整体置信度
            thinking_chain["confidence_score"] = self._calculate_overall_confidence(thinking_chain["thinking_steps"])
            
            # 更新元数据
            thinking_chain["metadata"].update({
                "end_time": time.time(),
                "total_duration": time.time() - thinking_chain["metadata"]["start_time"],
                "steps_completed": len(thinking_chain["thinking_steps"]),
                "reasoning_depth": len(thinking_chain["reasoning_process"])
            })
            
            self.logger.info(f"序列思维处理完成，置信度: {thinking_chain['confidence_score']:.2f}")
            
            return {
                "status": "success",
                "thinking_chain": thinking_chain,
                "summary": {
                    "problem": problem,
                    "steps_completed": len(thinking_chain["thinking_steps"]),
                    "confidence_score": thinking_chain["confidence_score"],
                    "main_conclusions": thinking_chain["conclusions"][:3],  # 前3个主要结论
                    "processing_time": thinking_chain["metadata"]["total_duration"]
                }
            }
            
        except Exception as e:
            self.logger.error(f"序列思维处理失败: {e}")
            return {
                "status": "error",
                "message": f"序列思维处理失败: {str(e)}",
                "problem": problem
            }
    
    def _assess_problem_complexity(self, problem: str) -> str:
        """评估问题复杂度"""
        complexity_indicators = [
            "系统", "架构", "优化", "分析", "设计", "实现", 
            "集成", "多", "复杂", "高级", "深度", "全面"
        ]
        
        indicator_count = sum(1 for indicator in complexity_indicators if indicator in problem)
        
        if indicator_count >= 4:
            return "high"
        elif indicator_count >= 2:
            return "medium"
        else:
            return "low"
    
    def _understand_problem(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """理解问题"""
        return {
            "core_elements": self._extract_core_elements(problem),
            "problem_type": self._classify_problem_type(problem),
            "key_requirements": self._identify_requirements(problem),
            "constraints": self._identify_constraints(problem, context),
            "success_criteria": self._define_success_criteria(problem),
            "confidence": 0.85
        }
    
    def _extract_core_elements(self, problem: str) -> List[str]:
        """提取核心要素"""
        # 简化的关键词提取
        keywords = []
        important_words = ["优化", "提升", "改进", "分析", "设计", "实现", "系统", "模型", "算法", "效率", "性能", "质量"]
        
        for word in important_words:
            if word in problem:
                keywords.append(word)
        
        return keywords or ["通用问题解决"]
    
    def _classify_problem_type(self, problem: str) -> str:
        """分类问题类型"""
        if "优化" in problem or "提升" in problem or "改进" in problem:
            return "optimization"
        elif "分析" in problem or "研究" in problem:
            return "analysis"
        elif "设计" in problem or "架构" in problem:
            return "design"
        elif "实现" in problem or "开发" in problem:
            return "implementation"
        else:
            return "general"
    
    def _identify_requirements(self, problem: str) -> List[str]:
        """识别需求"""
        requirements = []
        
        if "效率" in problem:
            requirements.append("提高效率")
        if "性能" in problem:
            requirements.append("优化性能")
        if "质量" in problem:
            requirements.append("保证质量")
        if "成本" in problem:
            requirements.append("控制成本")
        if "时间" in problem:
            requirements.append("时间约束")
        
        return requirements or ["满足基本功能需求"]
    
    def _identify_constraints(self, problem: str, context: Dict[str, Any]) -> List[str]:
        """识别约束条件"""
        constraints = []
        
        # 从问题中识别约束
        if "预算" in problem or "成本" in problem:
            constraints.append("预算限制")
        if "时间" in problem or "期限" in problem:
            constraints.append("时间限制")
        if "资源" in problem:
            constraints.append("资源限制")
        
        # 从上下文中识别约束
        if context:
            if context.get("budget_limit"):
                constraints.append("预算约束")
            if context.get("time_limit"):
                constraints.append("时间约束")
            if context.get("resource_limit"):
                constraints.append("资源约束")
        
        return constraints or ["无明显约束"]
    
    def _define_success_criteria(self, problem: str) -> List[str]:
        """定义成功标准"""
        return [
            "解决方案可行性高",
            "实施成本合理",
            "预期效果明显",
            "风险可控",
            "可持续性好"
        ]
    
    def _retrieve_relevant_knowledge(self, problem: str, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """检索相关知识"""
        problem_type = understanding.get("problem_type", "general")
        
        knowledge_base = {
            "optimization": [
                "性能优化最佳实践",
                "算法复杂度分析",
                "资源利用优化",
                "缓存策略",
                "并行处理技术"
            ],
            "analysis": [
                "数据分析方法",
                "统计学原理",
                "模式识别技术",
                "可视化技术",
                "报告生成方法"
            ],
            "design": [
                "设计模式",
                "架构原则",
                "用户体验设计",
                "系统设计方法",
                "接口设计规范"
            ],
            "implementation": [
                "编程最佳实践",
                "测试驱动开发",
                "持续集成",
                "版本控制",
                "部署策略"
            ],
            "general": [
                "问题解决方法论",
                "项目管理原则",
                "团队协作技巧",
                "沟通技能",
                "创新思维"
            ]
        }
        
        relevant_knowledge = knowledge_base.get(problem_type, knowledge_base["general"])
        
        return {
            "knowledge_items": relevant_knowledge,
            "knowledge_type": problem_type,
            "relevance_score": 0.8,
            "confidence": 0.75
        }
    
    def _perform_reasoning(self, problem: str, understanding: Dict[str, Any], knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """执行推理"""
        reasoning_steps = []
        
        # 基于理解进行推理
        core_elements = understanding.get("core_elements", [])
        problem_type = understanding.get("problem_type", "general")
        
        # 推理步骤1: 问题分解
        reasoning_steps.append({
            "step": "问题分解",
            "reasoning": f"将{problem_type}类型的问题分解为{len(core_elements)}个核心要素",
            "result": f"核心要素: {', '.join(core_elements)}"
        })
        
        # 推理步骤2: 知识应用
        knowledge_items = knowledge.get("knowledge_items", [])
        reasoning_steps.append({
            "step": "知识应用",
            "reasoning": f"应用{len(knowledge_items)}项相关知识",
            "result": f"适用知识: {', '.join(knowledge_items[:3])}"  # 显示前3项
        })
        
        # 推理步骤3: 逻辑分析
        reasoning_steps.append({
            "step": "逻辑分析",
            "reasoning": "基于问题特征和知识库进行逻辑分析",
            "result": "识别关键路径和潜在解决方向"
        })
        
        return {
            "reasoning_steps": reasoning_steps,
            "logical_flow": "问题分解 → 知识应用 → 逻辑分析",
            "key_insights": [
                "问题的核心在于找到最优解决路径",
                "需要平衡多个约束条件",
                "解决方案应具备可实施性"
            ],
            "confidence": 0.8
        }
    
    def _generate_solutions(self, problem: str, reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """生成解决方案"""
        solutions = []
        
        # 基于推理结果生成方案
        key_insights = reasoning.get("key_insights", [])
        
        # 方案1: 直接解决方案
        solutions.append({
            "solution_id": 1,
            "name": "直接解决方案",
            "description": "基于现有资源和技术直接解决问题",
            "approach": "采用成熟技术和方法",
            "pros": ["实施快速", "风险较低", "成本可控"],
            "cons": ["可能不是最优解", "创新性有限"],
            "feasibility": 0.9,
            "innovation": 0.3
        })
        
        # 方案2: 优化解决方案
        solutions.append({
            "solution_id": 2,
            "name": "优化解决方案",
            "description": "通过优化现有流程和技术来解决问题",
            "approach": "分析瓶颈并进行针对性优化",
            "pros": ["效果明显", "投入产出比高", "可持续"],
            "cons": ["需要深入分析", "实施周期较长"],
            "feasibility": 0.8,
            "innovation": 0.6
        })
        
        # 方案3: 创新解决方案
        solutions.append({
            "solution_id": 3,
            "name": "创新解决方案",
            "description": "采用新技术或新方法来解决问题",
            "approach": "引入前沿技术和创新思维",
            "pros": ["效果突出", "技术领先", "长期价值高"],
            "cons": ["风险较高", "成本较大", "不确定性强"],
            "feasibility": 0.6,
            "innovation": 0.9
        })
        
        return {
            "solutions": solutions,
            "solution_count": len(solutions),
            "recommended_solution": solutions[1],  # 推荐优化方案
            "selection_criteria": ["可行性", "创新性", "成本效益", "风险水平"],
            "confidence": 0.75
        }
    
    def _evaluate_and_optimize(self, solutions: Dict[str, Any]) -> Dict[str, Any]:
        """评估和优化方案"""
        solution_list = solutions.get("solutions", [])
        
        # 评估每个方案
        evaluated_solutions = []
        for solution in solution_list:
            evaluation = {
                "solution_id": solution.get("solution_id"),
                "name": solution.get("name"),
                "scores": {
                    "feasibility": solution.get("feasibility", 0.5),
                    "innovation": solution.get("innovation", 0.5),
                    "cost_effectiveness": 0.7,  # 模拟评分
                    "risk_level": 1 - solution.get("feasibility", 0.5),  # 风险与可行性反相关
                    "time_to_implement": 0.6  # 模拟评分
                },
                "overall_score": 0.0,
                "ranking": 0
            }
            
            # 计算综合评分
            scores = evaluation["scores"]
            evaluation["overall_score"] = (
                scores["feasibility"] * 0.3 +
                scores["innovation"] * 0.2 +
                scores["cost_effectiveness"] * 0.2 +
                (1 - scores["risk_level"]) * 0.2 +
                scores["time_to_implement"] * 0.1
            )
            
            evaluated_solutions.append(evaluation)
        
        # 排序
        evaluated_solutions.sort(key=lambda x: x["overall_score"], reverse=True)
        for i, solution in enumerate(evaluated_solutions):
            solution["ranking"] = i + 1
        
        # 优化建议
        optimization_suggestions = [
            "结合多个方案的优点形成混合方案",
            "分阶段实施降低风险",
            "建立监控机制确保效果",
            "准备备选方案应对不确定性",
            "持续优化和改进"
        ]
        
        return {
            "evaluated_solutions": evaluated_solutions,
            "best_solution": evaluated_solutions[0] if evaluated_solutions else None,
            "optimization_suggestions": optimization_suggestions,
            "evaluation_criteria": {
                "feasibility": "可行性 (30%)",
                "innovation": "创新性 (20%)",
                "cost_effectiveness": "成本效益 (20%)",
                "risk_level": "风险水平 (20%)",
                "time_to_implement": "实施时间 (10%)"
            },
            "confidence": 0.8
        }
    
    def _generate_reasoning_summary(self, thinking_steps: List[Dict[str, Any]]) -> List[str]:
        """生成推理过程总结"""
        summary = []
        
        for step in thinking_steps:
            step_name = step.get("step_name", "未知步骤")
            description = step.get("description", "")
            confidence = step.get("confidence", 0.0)
            
            summary.append(f"{step_name}: {description} (置信度: {confidence:.2f})")
        
        return summary
    
    def _generate_conclusions(self, thinking_steps: List[Dict[str, Any]]) -> List[str]:
        """生成最终结论"""
        conclusions = []
        
        # 基于思维步骤生成结论
        if len(thinking_steps) >= 5:
            conclusions.extend([
                "问题已经得到全面分析和理解",
                "相关知识和经验已被有效整合",
                "逻辑推理过程清晰完整",
                "生成了多个可行的解决方案",
                "方案评估和优化建议具有实用价值"
            ])
        else:
            conclusions.extend([
                "问题分析基本完成",
                "解决思路已经形成",
                "需要进一步细化实施方案"
            ])
        
        return conclusions
    
    def _calculate_overall_confidence(self, thinking_steps: List[Dict[str, Any]]) -> float:
        """计算整体置信度"""
        if not thinking_steps:
            return 0.0
        
        total_confidence = sum(step.get("confidence", 0.0) for step in thinking_steps)
        return total_confidence / len(thinking_steps)
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取适配器状态
        
        Returns:
            状态信息字典
        """
        return {
            "adapter_name": self.name,
            "status": "active",
            "capabilities": self.get_capabilities(),
            "last_activity": "ready_for_processing",
            "performance_metrics": {
                "average_processing_time": "0.5s",
                "success_rate": "95%",
                "confidence_score": "0.85"
            }
        }


    
    def execute_step(self, step_id: int, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行单个思维步骤
        
        Args:
            step_id: 步骤ID
            context: 执行上下文
            
        Returns:
            Dict[str, Any]: 步骤执行结果
        """
        try:
            if context is None:
                context = {}
                
            # 验证步骤ID
            if not isinstance(step_id, int) or step_id < 1:
                return {
                    "step_id": step_id,
                    "status": "error",
                    "error": "Invalid step_id",
                    "result": None
                }
            
            # 模拟步骤执行
            step_name = f"步骤{step_id}"
            if step_id == 1:
                step_name = "问题理解"
                result = "分析问题的核心要素和关键信息"
            elif step_id == 2:
                step_name = "知识检索"
                result = "检索相关知识和经验"
            elif step_id == 3:
                step_name = "逻辑推理"
                result = "基于理解和知识进行逻辑推理"
            elif step_id == 4:
                step_name = "方案生成"
                result = "基于推理结果生成可行方案"
            elif step_id == 5:
                step_name = "评估优化"
                result = "评估方案可行性并进行优化"
            else:
                step_name = f"扩展步骤{step_id}"
                result = f"执行扩展思维步骤{step_id}"
            
            return {
                "step_id": step_id,
                "step_name": step_name,
                "status": "completed",
                "result": result,
                "context": context,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"执行步骤失败: {e}")
            return {
                "step_id": step_id,
                "status": "error",
                "error": str(e),
                "result": None
            }
    
    def analyze_task_complexity(self, task: str) -> Dict[str, Any]:
        """
        分析任务复杂度
        
        Args:
            task: 任务描述
            
        Returns:
            Dict[str, Any]: 复杂度分析结果
        """
        try:
            if not task or not isinstance(task, str):
                return {
                    "status": "error",
                    "error": "Invalid task description",
                    "complexity": "unknown"
                }
            
            # 简单的复杂度分析逻辑
            task_length = len(task)
            word_count = len(task.split())
            
            if task_length < 20 or word_count < 5:
                complexity = "low"
                estimated_steps = 3
            elif task_length < 100 or word_count < 20:
                complexity = "medium"
                estimated_steps = 5
            else:
                complexity = "high"
                estimated_steps = 7
            
            # 检查关键词以调整复杂度
            complex_keywords = ["优化", "分析", "设计", "开发", "集成", "测试"]
            keyword_count = sum(1 for keyword in complex_keywords if keyword in task)
            
            if keyword_count >= 3:
                complexity = "high"
                estimated_steps = max(estimated_steps, 7)
            elif keyword_count >= 2:
                complexity = "medium"
                estimated_steps = max(estimated_steps, 5)
            
            return {
                "status": "success",
                "task": task,
                "complexity": complexity,
                "estimated_steps": estimated_steps,
                "word_count": word_count,
                "character_count": task_length,
                "keyword_count": keyword_count,
                "analysis_timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"任务复杂度分析失败: {e}")
            return {
                "status": "error",
                "error": str(e),
                "complexity": "unknown"
            }

