"""
思考过程结构化表示的JSON Schema定义
"""
import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class ThoughtStage(BaseModel):
    """思考阶段基础模型"""
    stage_id: str = Field(..., description="阶段唯一标识符")
    stage_name: str = Field(..., description="阶段名称")
    stage_description: str = Field(..., description="阶段描述")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="阶段输入数据")
    outputs: Dict[str, Any] = Field(default_factory=dict, description="阶段输出数据")
    quality_metrics: Dict[str, float] = Field(default_factory=dict, description="质量评估指标")


class ProblemAnalysisStage(ThoughtStage):
    """问题分析阶段"""
    problem_statement: str = Field(..., description="问题陈述")
    key_constraints: List[str] = Field(default_factory=list, description="关键约束条件")
    identified_challenges: List[Dict[str, Any]] = Field(default_factory=list, description="识别的挑战")
    background_knowledge: Dict[str, Any] = Field(default_factory=dict, description="背景知识")


class SolutionDesignStage(ThoughtStage):
    """方案设计阶段"""
    design_principles: List[str] = Field(default_factory=list, description="设计原则")
    alternative_approaches: List[Dict[str, Any]] = Field(default_factory=list, description="备选方案")
    selected_approach: Dict[str, Any] = Field(..., description="选定方案")
    design_rationale: str = Field(..., description="设计理由")


class ImplementationPlanningStage(ThoughtStage):
    """实现规划阶段"""
    implementation_steps: List[Dict[str, Any]] = Field(default_factory=list, description="实现步骤")
    resource_requirements: Dict[str, Any] = Field(default_factory=dict, description="资源需求")
    timeline: Dict[str, Any] = Field(default_factory=dict, description="时间线")
    potential_risks: List[Dict[str, Any]] = Field(default_factory=list, description="潜在风险")


class ValidationEvaluationStage(ThoughtStage):
    """验证评估阶段"""
    validation_criteria: List[Dict[str, Any]] = Field(default_factory=list, description="验证标准")
    test_cases: List[Dict[str, Any]] = Field(default_factory=list, description="测试用例")
    evaluation_results: Dict[str, Any] = Field(default_factory=dict, description="评估结果")
    improvement_suggestions: List[str] = Field(default_factory=list, description="改进建议")


class ThoughtProcess(BaseModel):
    """完整思考过程模型"""
    process_id: str = Field(..., description="思考过程唯一标识符")
    task_description: str = Field(..., description="任务描述")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")
    author: str = Field(..., description="作者")
    stages: Dict[str, ThoughtStage] = Field(default_factory=dict, description="思考阶段")
    overall_quality: float = Field(0.0, description="整体质量评分")
    tags: List[str] = Field(default_factory=list, description="标签")
    references: List[Dict[str, str]] = Field(default_factory=list, description="参考资料")


class ThoughtSchemaManager:
    """思考过程Schema管理器"""
    
    @staticmethod
    def get_schema() -> Dict[str, Any]:
        """获取完整的思考过程JSON Schema"""
        return ThoughtProcess.schema()
    
    @staticmethod
    def validate_thought_process(thought_data: Dict[str, Any]) -> bool:
        """验证思考过程数据是否符合Schema"""
        try:
            ThoughtProcess(**thought_data)
            return True
        except Exception:
            return False
    
    @staticmethod
    def create_empty_thought_process(process_id: str, task_description: str, author: str) -> ThoughtProcess:
        """创建空的思考过程模板"""
        import datetime
        now = datetime.datetime.now().isoformat()
        
        return ThoughtProcess(
            process_id=process_id,
            task_description=task_description,
            created_at=now,
            updated_at=now,
            author=author,
            stages={},
            overall_quality=0.0,
            tags=[],
            references=[]
        )
    
    @staticmethod
    def add_stage(thought_process: ThoughtProcess, stage: ThoughtStage) -> ThoughtProcess:
        """向思考过程添加阶段"""
        thought_process.stages[stage.stage_id] = stage
        import datetime
        thought_process.updated_at = datetime.datetime.now().isoformat()
        return thought_process
    
    @staticmethod
    def to_json(thought_process: ThoughtProcess) -> str:
        """将思考过程转换为JSON字符串"""
        return thought_process.json(indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> ThoughtProcess:
        """从JSON字符串加载思考过程"""
        data = json.loads(json_str)
        return ThoughtProcess(**data)


if __name__ == "__main__":
    # 示例用法
    manager = ThoughtSchemaManager()
    
    # 创建空的思考过程
    thought = manager.create_empty_thought_process(
        process_id="TP-001",
        task_description="设计一个在线教育平台",
        author="Manus"
    )
    
    # 添加问题分析阶段
    problem_analysis = ProblemAnalysisStage(
        stage_id="PA-001",
        stage_name="问题分析",
        stage_description="分析在线教育平台的需求和挑战",
        problem_statement="设计一个功能完善、用户友好的在线教育平台",
        key_constraints=["响应时间不超过200ms", "支持至少10000名并发用户"],
        identified_challenges=[
            {"name": "实时互动", "description": "确保师生实时互动的流畅性"},
            {"name": "内容管理", "description": "高效管理大量教育内容"}
        ],
        background_knowledge={
            "existing_platforms": ["Coursera", "Udemy", "edX"],
            "key_features": ["视频课程", "互动测验", "讨论区", "进度跟踪"]
        }
    )
    
    thought = manager.add_stage(thought, problem_analysis)
    
    # 输出JSON
    print(manager.to_json(thought))
