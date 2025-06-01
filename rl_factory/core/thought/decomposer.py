"""
思考过程分解器，负责将思考过程分解为多个阶段
"""
from typing import Dict, List, Any, Optional, Tuple
from .schema import (
    ThoughtProcess, ThoughtStage, 
    ProblemAnalysisStage, SolutionDesignStage,
    ImplementationPlanningStage, ValidationEvaluationStage
)


class ThoughtDecomposer:
    """思考过程分解器"""
    
    @staticmethod
    def decompose_raw_thought(raw_thought: str) -> ThoughtProcess:
        """
        将原始文本思考过程分解为结构化的ThoughtProcess对象
        
        Args:
            raw_thought: 原始文本思考过程
            
        Returns:
            结构化的ThoughtProcess对象
        """
        # 提取基本信息
        import uuid
        import datetime
        
        process_id = f"TP-{uuid.uuid4().hex[:8]}"
        now = datetime.datetime.now().isoformat()
        
        # 提取任务描述（假设第一行是任务描述）
        lines = raw_thought.strip().split('\n')
        task_description = lines[0] if lines else "未指定任务"
        
        # 创建思考过程对象
        thought_process = ThoughtProcess(
            process_id=process_id,
            task_description=task_description,
            created_at=now,
            updated_at=now,
            author="Manus",
            stages={},
            overall_quality=0.0,
            tags=[],
            references=[]
        )
        
        # 分解思考阶段
        stages = ThoughtDecomposer._extract_stages(raw_thought)
        
        # 添加各个阶段
        for stage_id, stage_data in stages.items():
            if "problem_analysis" in stage_id:
                stage = ThoughtDecomposer._create_problem_analysis_stage(stage_id, stage_data)
            elif "solution_design" in stage_id:
                stage = ThoughtDecomposer._create_solution_design_stage(stage_id, stage_data)
            elif "implementation_planning" in stage_id:
                stage = ThoughtDecomposer._create_implementation_planning_stage(stage_id, stage_data)
            elif "validation_evaluation" in stage_id:
                stage = ThoughtDecomposer._create_validation_evaluation_stage(stage_id, stage_data)
            else:
                # 创建通用阶段
                stage = ThoughtStage(
                    stage_id=stage_id,
                    stage_name=stage_data.get("name", "未命名阶段"),
                    stage_description=stage_data.get("description", ""),
                    inputs=stage_data.get("inputs", {}),
                    outputs=stage_data.get("outputs", {}),
                    quality_metrics={}
                )
            
            thought_process.stages[stage_id] = stage
        
        return thought_process
    
    @staticmethod
    def _extract_stages(raw_thought: str) -> Dict[str, Dict[str, Any]]:
        """
        从原始思考文本中提取各个阶段
        
        这里使用简单的启发式方法，实际应用中可能需要更复杂的NLP技术
        """
        stages = {}
        
        # 定义阶段关键词和对应的阶段ID
        stage_keywords = {
            "问题分析": "problem_analysis",
            "需求分析": "problem_analysis",
            "问题定义": "problem_analysis",
            "方案设计": "solution_design",
            "解决方案": "solution_design",
            "设计方案": "solution_design",
            "实现规划": "implementation_planning",
            "实施计划": "implementation_planning",
            "开发计划": "implementation_planning",
            "验证评估": "validation_evaluation",
            "测试验证": "validation_evaluation",
            "评估方案": "validation_evaluation"
        }
        
        # 分割文本为段落
        paragraphs = raw_thought.split('\n\n')
        
        current_stage = None
        current_stage_content = []
        
        for para in paragraphs:
            # 检查是否是新阶段的开始
            is_new_stage = False
            for keyword, stage_type in stage_keywords.items():
                if keyword in para[:20]:  # 只检查段落开头
                    # 保存当前阶段
                    if current_stage:
                        stage_id = f"{current_stage}_{len([s for s in stages if current_stage in s])}"
                        stages[stage_id] = {
                            "name": current_stage.replace("_", " ").title(),
                            "description": "\n\n".join(current_stage_content[:1]),
                            "content": "\n\n".join(current_stage_content),
                            "inputs": {},
                            "outputs": {}
                        }
                    
                    # 开始新阶段
                    current_stage = stage_type
                    current_stage_content = [para]
                    is_new_stage = True
                    break
            
            if not is_new_stage and current_stage:
                current_stage_content.append(para)
        
        # 保存最后一个阶段
        if current_stage:
            stage_id = f"{current_stage}_{len([s for s in stages if current_stage in s])}"
            stages[stage_id] = {
                "name": current_stage.replace("_", " ").title(),
                "description": "\n\n".join(current_stage_content[:1]),
                "content": "\n\n".join(current_stage_content),
                "inputs": {},
                "outputs": {}
            }
        
        # 如果没有识别出任何阶段，创建一个默认阶段
        if not stages:
            stages["general_thought_0"] = {
                "name": "General Thought",
                "description": "Complete thought process",
                "content": raw_thought,
                "inputs": {},
                "outputs": {}
            }
        
        return stages
    
    @staticmethod
    def _create_problem_analysis_stage(stage_id: str, stage_data: Dict[str, Any]) -> ProblemAnalysisStage:
        """创建问题分析阶段"""
        content = stage_data.get("content", "")
        
        # 提取关键约束条件（假设以"约束:"或"限制:"开头的行）
        constraints = []
        for line in content.split('\n'):
            if line.strip().startswith(("约束:", "限制:", "约束条件:", "Constraint:")):
                constraint = line.split(':', 1)[1].strip()
                if constraint:
                    constraints.append(constraint)
        
        # 提取识别的挑战（假设以"挑战:"或"难点:"开头的行）
        challenges = []
        for line in content.split('\n'):
            if line.strip().startswith(("挑战:", "难点:", "Challenge:")):
                challenge_text = line.split(':', 1)[1].strip()
                if challenge_text:
                    challenges.append({"name": challenge_text, "description": ""})
        
        return ProblemAnalysisStage(
            stage_id=stage_id,
            stage_name=stage_data.get("name", "问题分析"),
            stage_description=stage_data.get("description", ""),
            problem_statement=stage_data.get("description", "")[:100],  # 使用描述的前100个字符作为问题陈述
            key_constraints=constraints,
            identified_challenges=challenges,
            background_knowledge={}
        )
    
    @staticmethod
    def _create_solution_design_stage(stage_id: str, stage_data: Dict[str, Any]) -> SolutionDesignStage:
        """创建方案设计阶段"""
        content = stage_data.get("content", "")
        
        # 提取设计原则（假设以"原则:"或"设计原则:"开头的行）
        principles = []
        for line in content.split('\n'):
            if line.strip().startswith(("原则:", "设计原则:", "Principle:")):
                principle = line.split(':', 1)[1].strip()
                if principle:
                    principles.append(principle)
        
        # 提取备选方案（假设以"方案:"或"备选方案:"开头的段落）
        alternatives = []
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip().startswith(("方案:", "备选方案:", "Alternative:")):
                alt_text = para.split(':', 1)[1].strip()
                if alt_text:
                    alternatives.append({"name": alt_text[:50], "description": alt_text})
        
        return SolutionDesignStage(
            stage_id=stage_id,
            stage_name=stage_data.get("name", "方案设计"),
            stage_description=stage_data.get("description", ""),
            design_principles=principles,
            alternative_approaches=alternatives,
            selected_approach={"name": "主要方案", "description": stage_data.get("description", "")},
            design_rationale="基于问题分析和设计原则选择最佳方案"
        )
    
    @staticmethod
    def _create_implementation_planning_stage(stage_id: str, stage_data: Dict[str, Any]) -> ImplementationPlanningStage:
        """创建实现规划阶段"""
        content = stage_data.get("content", "")
        
        # 提取实现步骤（假设以数字或"步骤:"开头的行）
        steps = []
        step_pattern = r"^\s*(\d+[\.\)、]|\-|\*|\s*步骤:|\s*Step:)"
        import re
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if re.match(step_pattern, line):
                step_text = re.sub(step_pattern, "", line).strip()
                if step_text:
                    steps.append({
                        "step_number": len(steps) + 1,
                        "description": step_text,
                        "estimated_effort": "medium"
                    })
        
        # 提取潜在风险（假设以"风险:"或"挑战:"开头的行）
        risks = []
        for line in content.split('\n'):
            if line.strip().startswith(("风险:", "挑战:", "Risk:", "Challenge:")):
                risk_text = line.split(':', 1)[1].strip()
                if risk_text:
                    risks.append({"name": risk_text[:50], "description": risk_text, "severity": "medium"})
        
        return ImplementationPlanningStage(
            stage_id=stage_id,
            stage_name=stage_data.get("name", "实现规划"),
            stage_description=stage_data.get("description", ""),
            implementation_steps=steps,
            resource_requirements={},
            timeline={},
            potential_risks=risks
        )
    
    @staticmethod
    def _create_validation_evaluation_stage(stage_id: str, stage_data: Dict[str, Any]) -> ValidationEvaluationStage:
        """创建验证评估阶段"""
        content = stage_data.get("content", "")
        
        # 提取验证标准（假设以"标准:"或"验证标准:"开头的行）
        criteria = []
        for line in content.split('\n'):
            if line.strip().startswith(("标准:", "验证标准:", "Criteria:")):
                criterion_text = line.split(':', 1)[1].strip()
                if criterion_text:
                    criteria.append({"name": criterion_text[:50], "description": criterion_text})
        
        # 提取测试用例（假设以"测试:"或"用例:"开头的行）
        test_cases = []
        for line in content.split('\n'):
            if line.strip().startswith(("测试:", "用例:", "Test:", "Case:")):
                test_text = line.split(':', 1)[1].strip()
                if test_text:
                    test_cases.append({"name": test_text[:50], "description": test_text, "expected_result": ""})
        
        # 提取改进建议（假设以"改进:"或"建议:"开头的行）
        suggestions = []
        for line in content.split('\n'):
            if line.strip().startswith(("改进:", "建议:", "Improvement:", "Suggestion:")):
                suggestion = line.split(':', 1)[1].strip()
                if suggestion:
                    suggestions.append(suggestion)
        
        return ValidationEvaluationStage(
            stage_id=stage_id,
            stage_name=stage_data.get("name", "验证评估"),
            stage_description=stage_data.get("description", ""),
            validation_criteria=criteria,
            test_cases=test_cases,
            evaluation_results={},
            improvement_suggestions=suggestions
        )


if __name__ == "__main__":
    # 示例用法
    raw_thought = """设计一个在线教育平台
    
    问题分析:
    我们需要设计一个功能完善、用户友好的在线教育平台。该平台应支持多种课程类型，包括视频课程、互动测验和讨论区。
    
    约束: 响应时间不超过200ms
    约束: 支持至少10000名并发用户
    挑战: 确保师生实时互动的流畅性
    挑战: 高效管理大量教育内容
    
    方案设计:
    基于微服务架构设计平台，将功能拆分为多个独立服务。
    
    设计原则: 高可用性
    设计原则: 可扩展性
    设计原则: 用户体验优先
    
    方案1: 基于AWS的云原生架构
    方案2: 基于自建数据中心的传统架构
    
    实现规划:
    1. 设计数据库架构
    2. 实现用户认证服务
    3. 开发课程管理系统
    4. 实现视频流处理服务
    5. 开发互动测验模块
    6. 实现实时通讯功能
    
    风险: 视频流处理可能面临性能瓶颈
    风险: 实时通讯在高并发下可能不稳定
    
    验证评估:
    标准: 系统响应时间
    标准: 并发用户支持数量
    标准: 用户满意度
    
    测试: 负载测试以验证并发支持能力
    测试: A/B测试以评估用户界面设计
    
    改进: 考虑引入AI推荐系统
    改进: 增加移动端适配
    """
    
    decomposer = ThoughtDecomposer()
    thought_process = decomposer.decompose_raw_thought(raw_thought)
    
    # 输出结果
    from .schema import ThoughtSchemaManager
    print(ThoughtSchemaManager.to_json(thought_process))
