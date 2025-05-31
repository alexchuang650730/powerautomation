"""
思考过程序列化工具，负责序列化和反序列化思考过程数据
"""
import json
from typing import Dict, List, Any, Optional, Union
from .schema import (
    ThoughtProcess, ThoughtStage, 
    ProblemAnalysisStage, SolutionDesignStage,
    ImplementationPlanningStage, ValidationEvaluationStage
)


class ThoughtSerializer:
    """思考过程序列化工具"""
    
    @staticmethod
    def to_json(thought_process: ThoughtProcess) -> str:
        """
        将ThoughtProcess对象序列化为JSON字符串
        
        Args:
            thought_process: ThoughtProcess对象
            
        Returns:
            JSON字符串
        """
        return thought_process.model_dump_json(indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> ThoughtProcess:
        """
        从JSON字符串反序列化为ThoughtProcess对象
        
        Args:
            json_str: JSON字符串
            
        Returns:
            ThoughtProcess对象
        """
        data = json.loads(json_str)
        
        # 处理stages字段中的不同阶段类型
        if "stages" in data:
            stages_data = data["stages"]
            stages = {}
            
            for stage_id, stage_data in stages_data.items():
                if "problem_statement" in stage_data:
                    stages[stage_id] = ProblemAnalysisStage(**stage_data)
                elif "design_principles" in stage_data:
                    stages[stage_id] = SolutionDesignStage(**stage_data)
                elif "implementation_steps" in stage_data:
                    stages[stage_id] = ImplementationPlanningStage(**stage_data)
                elif "validation_criteria" in stage_data:
                    stages[stage_id] = ValidationEvaluationStage(**stage_data)
                else:
                    stages[stage_id] = ThoughtStage(**stage_data)
            
            data["stages"] = stages
        
        return ThoughtProcess(**data)
    
    @staticmethod
    def to_file(thought_process: ThoughtProcess, file_path: str) -> None:
        """
        将ThoughtProcess对象保存到文件
        
        Args:
            thought_process: ThoughtProcess对象
            file_path: 文件路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(ThoughtSerializer.to_json(thought_process))
    
    @staticmethod
    def from_file(file_path: str) -> ThoughtProcess:
        """
        从文件加载ThoughtProcess对象
        
        Args:
            file_path: 文件路径
            
        Returns:
            ThoughtProcess对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return ThoughtSerializer.from_json(f.read())
    
    @staticmethod
    def to_dict(thought_process: ThoughtProcess) -> Dict[str, Any]:
        """
        将ThoughtProcess对象转换为字典
        
        Args:
            thought_process: ThoughtProcess对象
            
        Returns:
            字典表示
        """
        return json.loads(ThoughtSerializer.to_json(thought_process))
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> ThoughtProcess:
        """
        从字典创建ThoughtProcess对象
        
        Args:
            data: 字典数据
            
        Returns:
            ThoughtProcess对象
        """
        return ThoughtSerializer.from_json(json.dumps(data))
    
    @staticmethod
    def to_markdown(thought_process: ThoughtProcess) -> str:
        """
        将ThoughtProcess对象转换为Markdown格式
        
        Args:
            thought_process: ThoughtProcess对象
            
        Returns:
            Markdown字符串
        """
        md = [f"# {thought_process.task_description}", ""]
        
        md.append(f"**Process ID**: {thought_process.process_id}")
        md.append(f"**Created**: {thought_process.created_at}")
        md.append(f"**Updated**: {thought_process.updated_at}")
        md.append(f"**Author**: {thought_process.author}")
        md.append("")
        
        if thought_process.tags:
            md.append("**Tags**: " + ", ".join(thought_process.tags))
            md.append("")
        
        # 按阶段类型排序
        stage_order = {
            "problem_analysis": 1,
            "solution_design": 2,
            "implementation_planning": 3,
            "validation_evaluation": 4
        }
        
        sorted_stages = sorted(
            thought_process.stages.items(),
            key=lambda x: stage_order.get(x[0].split('_')[0], 99)
        )
        
        for stage_id, stage in sorted_stages:
            md.append(f"## {stage.stage_name}")
            md.append("")
            md.append(stage.stage_description)
            md.append("")
            
            if isinstance(stage, ProblemAnalysisStage):
                md.append("### 问题陈述")
                md.append("")
                md.append(stage.problem_statement)
                md.append("")
                
                if stage.key_constraints:
                    md.append("### 关键约束")
                    md.append("")
                    for constraint in stage.key_constraints:
                        md.append(f"- {constraint}")
                    md.append("")
                
                if stage.identified_challenges:
                    md.append("### 识别的挑战")
                    md.append("")
                    for challenge in stage.identified_challenges:
                        md.append(f"- **{challenge['name']}**: {challenge.get('description', '')}")
                    md.append("")
            
            elif isinstance(stage, SolutionDesignStage):
                if stage.design_principles:
                    md.append("### 设计原则")
                    md.append("")
                    for principle in stage.design_principles:
                        md.append(f"- {principle}")
                    md.append("")
                
                if stage.alternative_approaches:
                    md.append("### 备选方案")
                    md.append("")
                    for i, approach in enumerate(stage.alternative_approaches, 1):
                        md.append(f"#### 方案 {i}: {approach['name']}")
                        md.append("")
                        md.append(approach.get('description', ''))
                        md.append("")
                
                md.append("### 选定方案")
                md.append("")
                md.append(f"**{stage.selected_approach['name']}**")
                md.append("")
                md.append(stage.selected_approach.get('description', ''))
                md.append("")
                
                md.append("### 设计理由")
                md.append("")
                md.append(stage.design_rationale)
                md.append("")
            
            elif isinstance(stage, ImplementationPlanningStage):
                if stage.implementation_steps:
                    md.append("### 实现步骤")
                    md.append("")
                    for step in stage.implementation_steps:
                        md.append(f"{step['step_number']}. {step['description']}")
                    md.append("")
                
                if stage.potential_risks:
                    md.append("### 潜在风险")
                    md.append("")
                    for risk in stage.potential_risks:
                        md.append(f"- **{risk['name']}**: {risk.get('description', '')}")
                    md.append("")
            
            elif isinstance(stage, ValidationEvaluationStage):
                if stage.validation_criteria:
                    md.append("### 验证标准")
                    md.append("")
                    for criterion in stage.validation_criteria:
                        md.append(f"- **{criterion['name']}**: {criterion.get('description', '')}")
                    md.append("")
                
                if stage.test_cases:
                    md.append("### 测试用例")
                    md.append("")
                    for i, test in enumerate(stage.test_cases, 1):
                        md.append(f"#### 测试 {i}: {test['name']}")
                        md.append("")
                        md.append(test.get('description', ''))
                        md.append("")
                
                if stage.improvement_suggestions:
                    md.append("### 改进建议")
                    md.append("")
                    for suggestion in stage.improvement_suggestions:
                        md.append(f"- {suggestion}")
                    md.append("")
        
        if thought_process.references:
            md.append("## 参考资料")
            md.append("")
            for ref in thought_process.references:
                md.append(f"- [{ref.get('title', 'Reference')}]({ref.get('url', '#')})")
            md.append("")
        
        return "\n".join(md)


if __name__ == "__main__":
    # 示例用法
    from .decomposer import ThoughtDecomposer
    
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
    
    # 分解思考过程
    decomposer = ThoughtDecomposer()
    thought_process = decomposer.decompose_raw_thought(raw_thought)
    
    # 序列化为JSON
    serializer = ThoughtSerializer()
    json_str = serializer.to_json(thought_process)
    print("JSON序列化结果:")
    print(json_str)
    print("\n")
    
    # 反序列化
    recovered = serializer.from_json(json_str)
    print("反序列化后的对象与原对象相同:", recovered == thought_process)
    
    # 转换为Markdown
    markdown = serializer.to_markdown(thought_process)
    print("\nMarkdown格式:")
    print(markdown)
