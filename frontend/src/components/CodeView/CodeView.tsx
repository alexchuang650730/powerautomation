import React, { useState, useEffect } from 'react';
import { useWorkflowContext } from '../App';
import './CodeView.css';

interface CodeViewProps {
  agentType?: string;
}

const CodeView: React.FC<CodeViewProps> = ({ agentType = 'general' }) => {
  const { selectedNodeId, activeWorkflowType, refreshTrigger } = useWorkflowContext();
  const [activeTab, setActiveTab] = useState<'code' | 'docs'>('code');
  const [codeContent, setCodeContent] = useState<string>('// 选择一个节点查看代码');
  const [docsUrl, setDocsUrl] = useState<string>('');
  const [githubUrl, setGithubUrl] = useState<string>('');

  // 获取代码内容
  useEffect(() => {
    if (!selectedNodeId) {
      setCodeContent('// 选择一个节点查看代码');
      return;
    }

    // 根据工作流类型和节点ID获取相应的代码
    const fetchCode = async () => {
      try {
        let code = '';
        let githubPath = '';

        if (activeWorkflowType === 'automation-test') {
          switch (selectedNodeId) {
            case 'integration-test':
              code = `// 集成测试代码
import { render, screen, fireEvent } from '@testing-library/react';
import { AgentCard } from '../components/agent-cards/AgentCard';
import { WorkflowContent } from '../components/WorkflowContent';

describe('组件交互测试', () => {
  test('AgentCard 与 WorkflowContent 交互', () => {
    // 渲染组件
    render(
      <>
        <AgentCard 
          id="test-agent" 
          name="测试智能体" 
          description="用于测试的智能体"
          status="active" 
        />
        <WorkflowContent agentType="test" />
      </>
    );
    
    // 模拟点击事件
    const agentCard = screen.getByText('测试智能体');
    fireEvent.click(agentCard);
    
    // 验证交互结果
    expect(screen.getByText('测试智能体工作流')).toBeInTheDocument();
  });
  
  test('数据传递正确性', () => {
    // 测试数据
    const testData = { id: 'test-data', value: 'test-value' };
    
    // 渲染组件并传递数据
    render(
      <WorkflowContent 
        agentType="test" 
        testData={testData}
      />
    );
    
    // 验证数据传递
    expect(screen.getByText('test-value')).toBeInTheDocument();
  });
});`;
              githubPath = 'tests/integration/component_interaction.test.js';
              break;
            case 'e2e-test':
              code = `// 端到端测试代码
import { test, expect } from '@playwright/test';

test.describe('端到端测试', () => {
  test('用户登录流程', async ({ page }) => {
    // 访问登录页面
    await page.goto('http://localhost:5178/login');
    
    // 填写登录表单
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    
    // 点击登录按钮
    await page.click('button[type="submit"]');
    
    // 验证登录成功
    await expect(page.locator('.welcome-message')).toContainText('欢迎, testuser');
  });
  
  test('工作流创建测试', async ({ page }) => {
    // 登录
    await page.goto('http://localhost:5178/login');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    
    // 导航到工作流页面
    await page.click('text=工作流');
    
    // 创建新工作流
    await page.click('button:has-text("创建工作流")');
    await page.fill('input[name="workflow-name"]', '测试工作流');
    await page.click('button:has-text("保存")');
    
    // 验证工作流创建成功
    await expect(page.locator('.workflow-list')).toContainText('测试工作流');
  });
});`;
              githubPath = 'tests/e2e/user_workflow.spec.js';
              break;
            case 'visual-test':
              code = `// 视觉自动化测试代码
import { test, expect } from '@playwright/test';

test.describe('视觉自动化测试', () => {
  test('组件视觉测试', async ({ page }) => {
    // 访问组件测试页面
    await page.goto('http://localhost:5178/component-test');
    
    // 等待组件完全加载
    await page.waitForSelector('.test-component', { state: 'visible' });
    
    // 对按钮组件进行截图
    await expect(page.locator('.button-component')).toHaveScreenshot('button.png', {
      maxDiffPixelRatio: 0.1
    });
    
    // 对卡片组件进行截图
    await expect(page.locator('.card-component')).toHaveScreenshot('card.png', {
      maxDiffPixelRatio: 0.1
    });
    
    // 测试响应式布局
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('.responsive-component')).toHaveScreenshot('responsive-mobile.png', {
      maxDiffPixelRatio: 0.1
    });
    
    await page.setViewportSize({ width: 1280, height: 800 });
    await expect(page.locator('.responsive-component')).toHaveScreenshot('responsive-desktop.png', {
      maxDiffPixelRatio: 0.1
    });
  });
  
  test('暗色模式视觉测试', async ({ page }) => {
    // 访问测试页面
    await page.goto('http://localhost:5178/component-test');
    
    // 切换到暗色模式
    await page.click('.theme-toggle');
    
    // 等待主题切换完成
    await page.waitForSelector('body.dark-theme', { state: 'visible' });
    
    // 对暗色模式下的组件进行截图
    await expect(page.locator('.button-component')).toHaveScreenshot('button-dark.png', {
      maxDiffPixelRatio: 0.1
    });
  });
});`;
              githubPath = 'tests/visual/component_visual.spec.js';
              break;
            default:
              code = '// 未找到与所选节点对应的代码';
          }
        } else if (activeWorkflowType === 'agent-design') {
          switch (selectedNodeId) {
            case 'general-agent':
              code = `# 通用智能体代码
import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional

class GeneralAgent:
    """
    通用智能体类
    处理用户输入，作为系统的主要交互入口
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化通用智能体
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config", "general_agent.json")
        self.config = self._load_config()
        self.logger = self._setup_logger()
        self.memory_manager = None  # 将在后续初始化SuperMemory
        
        self.logger.info("通用智能体初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                return {}
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("GeneralAgent")
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        
        return logger
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            处理结果
        """
        self.logger.info(f"接收用户输入: {user_input}")
        
        # 记录用户输入
        self._record_input(user_input)
        
        # 触发SuperMemory记忆检查
        memory_result = self._check_memory(user_input)
        
        # 路由请求到适当的处理组件
        routing_result = self._route_request(user_input, memory_result)
        
        return {
            "status": "success",
            "input": user_input,
            "memory_result": memory_result,
            "routing_result": routing_result,
            "timestamp": self._get_timestamp()
        }
    
    def _record_input(self, user_input: str) -> None:
        """记录用户输入"""
        self.logger.info("记录用户输入")
        # 实际实现会将输入保存到数据库或日志文件
        pass
    
    def _check_memory(self, user_input: str) -> Dict[str, Any]:
        """触发SuperMemory记忆检查"""
        self.logger.info("触发SuperMemory记忆检查")
        # 实际实现会调用SuperMemory组件
        return {
            "has_memory": False,
            "related_memories": []
        }
    
    def _route_request(self, user_input: str, memory_result: Dict[str, Any]) -> Dict[str, Any]:
        """路由请求到适当的处理组件"""
        self.logger.info("路由请求到适当的处理组件")
        # 实际实现会根据输入内容和记忆结果决定路由目标
        return {
            "target_component": "mcp_coordinator",
            "priority": "normal"
        }
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        import datetime
        return datetime.datetime.now().isoformat()`;
              githubPath = 'agents/general_agent/general_agent.py';
              break;
            case 'mcp-coordinator':
              code = `# MCP协调器代码
import os
import sys
import json
import logging
import threading
from typing import Dict, Any, List, Optional

class MCPCoordinator:
    """
    MCP协调器类
    协调多个子系统和组件的工作，确保系统整体协同运行
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化MCP协调器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config", "mcp_coordinator.json")
        self.config = self._load_config()
        self.logger = self._setup_logger()
        self.active_tasks = {}
        self.task_lock = threading.Lock()
        
        self.logger.info("MCP协调器初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                return {}
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("MCPCoordinator")
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        
        return logger
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理请求
        
        Args:
            request: 请求数据
            
        Returns:
            处理结果
        """
        self.logger.info(f"接收请求: {request}")
        
        # 创建任务计划
        task_plan = self._create_task_plan(request)
        
        # 分配任务给各子系统
        allocation_result = self._allocate_tasks(task_plan)
        
        # 监控任务执行状态
        monitoring_result = self._monitor_tasks(allocation_result)
        
        # 汇总执行结果
        summary_result = self._summarize_results(monitoring_result)
        
        return {
            "status": "success",
            "task_plan": task_plan,
            "allocation_result": allocation_result,
            "monitoring_result": monitoring_result,
            "summary_result": summary_result,
            "timestamp": self._get_timestamp()
        }
    
    def _create_task_plan(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """创建任务计划"""
        self.logger.info("创建任务计划")
        # 实际实现会根据请求内容创建详细的任务计划
        return {
            "task_id": f"task_{self._get_timestamp()}",
            "steps": [
                {"id": "step_1", "component": "mcp_planner", "action": "create_execution_plan"},
                {"id": "step_2", "component": "thought_recorder", "action": "record_task_progress"},
                {"id": "step_3", "component": "supermemory", "action": "store_memory"}
            ],
            "priority": request.get("priority", "normal")
        }
    
    def _allocate_tasks(self, task_plan: Dict[str, Any]) -> Dict[str, Any]:
        """分配任务给各子系统"""
        self.logger.info("分配任务给各子系统")
        # 实际实现会将任务分配给相应的组件
        allocation_result = {
            "allocations": [],
            "status": "success"
        }
        
        for step in task_plan.get("steps", []):
            allocation_result["allocations"].append({
                "step_id": step["id"],
                "component": step["component"],
                "status": "allocated"
            })
        
        return allocation_result
    
    def _monitor_tasks(self, allocation_result: Dict[str, Any]) -> Dict[str, Any]:
        """监控任务执行状态"""
        self.logger.info("监控任务执行状态")
        # 实际实现会实时监控各组件的任务执行情况
        monitoring_result = {
            "task_statuses": [],
            "overall_status": "success"
        }
        
        for allocation in allocation_result.get("allocations", []):
            monitoring_result["task_statuses"].append({
                "step_id": allocation["step_id"],
                "component": allocation["component"],
                "status": "completed",
                "completion_time": self._get_timestamp()
            })
        
        return monitoring_result
    
    def _summarize_results(self, monitoring_result: Dict[str, Any]) -> Dict[str, Any]:
        """汇总执行结果"""
        self.logger.info("汇总执行结果")
        # 实际实现会汇总所有任务的执行结果
        return {
            "success_count": len(monitoring_result.get("task_statuses", [])),
            "failed_count": 0,
            "overall_status": "success",
            "completion_time": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        import datetime
        return datetime.datetime.now().isoformat()`;
              githubPath = 'agents/mcp/mcp_coordinator.py';
              break;
            case 'mcp-planner':
              code = `# MCP规划器代码
import os
import sys
import json
import logging
import networkx as nx
from typing import Dict, Any, List, Optional

class MCPPlanner:
    """
    MCP规划器类
    为复杂任务创建详细的执行计划，优化执行顺序和资源分配
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化MCP规划器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config", "mcp_planner.json")
        self.config = self._load_config()
        self.logger = self._setup_logger()
        
        self.logger.info("MCP规划器初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                return {}
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("MCPPlanner")
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        
        return logger
    
    def create_execution_plan(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建执行计划
        
        Args:
            task_data: 任务数据
            
        Returns:
            执行计划
        """
        self.logger.info(f"创建执行计划: {task_data}")
        
        # 分析任务需求
        requirements = self._analyze_requirements(task_data)
        
        # 创建执行步骤
        steps = self._create_steps(requirements)
        
        # 分析任务依赖关系
        dependencies = self._analyze_dependencies(steps)
        
        # 创建执行图
        execution_graph = self._create_execution_graph(steps, dependencies)
        
        # 优化执行顺序
        optimized_order = self._optimize_execution_order(execution_graph)
        
        return {
            "plan_id": f"plan_{self._get_timestamp()}",
            "requirements": requirements,
            "steps": steps,
            "dependencies": dependencies,
            "optimized_order": optimized_order,
            "status": "success",
            "timestamp": self._get_timestamp()
        }
    
    def _analyze_requirements(self, task_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析任务需求"""
        self.logger.info("分析任务需求")
        # 实际实现会分析任务数据，提取关键需求
        return [
            {"id": "req_1", "type": "data", "description": "需要用户历史数据"},
            {"id": "req_2", "type": "processing", "description": "需要数据处理能力"},
            {"id": "req_3", "type": "output", "description": "需要生成响应"}
        ]
    
    def _create_steps(self, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """创建执行步骤"""
        self.logger.info("创建执行步骤")
        # 实际实现会根据需求创建具体的执行步骤
        return [
            {"id": "step_1", "name": "获取用户数据", "component": "data_service", "requirement_id": "req_1"},
            {"id": "step_2", "name": "处理数据", "component": "processing_service", "requirement_id": "req_2"},
            {"id": "step_3", "name": "生成响应", "component": "response_generator", "requirement_id": "req_3"}
        ]
    
    def _analyze_dependencies(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析任务依赖关系"""
        self.logger.info("分析任务依赖关系")
        # 实际实现会分析步骤间的依赖关系
        return [
            {"from": "step_1", "to": "step_2", "type": "data_dependency"},
            {"from": "step_2", "to": "step_3", "type": "data_dependency"}
        ]
    
    def _create_execution_graph(self, steps: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> nx.DiGraph:
        """创建执行图"""
        self.logger.info("创建执行图")
        # 使用NetworkX创建有向图
        graph = nx.DiGraph()
        
        # 添加节点
        for step in steps:
            graph.add_node(step["id"], **step)
        
        # 添加边
        for dep in dependencies:
            graph.add_edge(dep["from"], dep["to"], type=dep["type"])
        
        return graph
    
    def _optimize_execution_order(self, execution_graph: nx.DiGraph) -> List[str]:
        """优化执行顺序"""
        self.logger.info("优化执行顺序")
        # 使用拓扑排序获取优化的执行顺序
        try:
            return list(nx.topological_sort(execution_graph))
        except nx.NetworkXUnfeasible:
            self.logger.error("执行图中存在循环依赖，无法进行拓扑排序")
            # 返回节点列表作为备选
            return list(execution_graph.nodes())
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        import datetime
        return datetime.datetime.now().isoformat()`;
              githubPath = 'agents/mcp/mcp_planner.py';
              break;
            case 'thought-recorder':
              code = `# 思维行为记录器代码
import os
import sys
import json
import logging
import datetime
from typing import Dict, Any, List, Optional

class ThoughtRecorder:
    """
    思维行为记录器类
    记录智能体的思考过程和行为模式，用于后续分析和优化
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化思维行为记录器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config", "thought_recorder.json")
        self.config = self._load_config()
        self.logger = self._setup_logger()
        self.records_dir = os.path.join(os.path.dirname(__file__), "records")
        
        # 确保记录目录存在
        os.makedirs(self.records_dir, exist_ok=True)
        
        self.logger.info("思维行为记录器初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                return {}
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("ThoughtRecorder")
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        
        return logger
    
    def record_task_progress(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        记录任务进度
        
        Args:
            task_data: 任务数据
            
        Returns:
            记录结果
        """
        self.logger.info(f"记录任务进度: {task_data}")
        
        # 创建记录
        record = {
            "record_id": f"record_{self._get_timestamp()}",
            "task_id": task_data.get("task_id", "unknown"),
            "timestamp": self._get_timestamp(),
            "progress": task_data.get("progress", 0),
            "current_step": task_data.get("current_step", ""),
            "thoughts": task_data.get("thoughts", []),
            "decisions": task_data.get("decisions", [])
        }
        
        # 保存记录
        self._save_record(record)
        
        # 分析用户历史回复
        user_history_analysis = self._analyze_user_history(task_data)
        
        # 识别行为模式
        behavior_patterns = self._identify_behavior_patterns(record, user_history_analysis)
        
        # 生成思维记录报告
        report = self._generate_report(record, user_history_analysis, behavior_patterns)
        
        return {
            "status": "success",
            "record_id": record["record_id"],
            "user_history_analysis": user_history_analysis,
            "behavior_patterns": behavior_patterns,
            "report": report
        }
    
    def _save_record(self, record: Dict[str, Any]) -> None:
        """保存记录"""
        record_path = os.path.join(self.records_dir, f"{record['record_id']}.json")
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"记录已保存: {record_path}")
    
    def _analyze_user_history(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析用户历史回复"""
        self.logger.info("分析用户历史回复")
        # 实际实现会分析用户的历史交互数据
        return {
            "interaction_count": task_data.get("user_interaction_count", 0),
            "common_patterns": ["pattern_1", "pattern_2"],
            "sentiment": "positive",
            "engagement_level": "high"
        }
    
    def _identify_behavior_patterns(self, record: Dict[str, Any], user_history_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """识别行为模式"""
        self.logger.info("识别行为模式")
        # 实际实现会基于记录和用户历史分析识别行为模式
        return [
            {
                "pattern_id": "pattern_1",
                "name": "深度思考",
                "confidence": 0.85,
                "description": "在决策前进行多步骤推理"
            },
            {
                "pattern_id": "pattern_2",
                "name": "用户关注",
                "confidence": 0.92,
                "description": "优先考虑用户明确表达的需求"
            }
        ]
    
    def _generate_report(self, record: Dict[str, Any], user_history_analysis: Dict[str, Any], behavior_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成思维记录报告"""
        self.logger.info("生成思维记录报告")
        # 实际实现会生成详细的思维记录报告
        return {
            "report_id": f"report_{self._get_timestamp()}",
            "task_id": record["task_id"],
            "timestamp": self._get_timestamp(),
            "summary": "智能体展现了深度思考和用户关注的行为模式",
            "key_insights": [
                "决策过程中考虑了多个因素",
                "优先处理了用户明确表达的需求",
                "在不确定情况下寻求更多信息"
            ],
            "recommendations": [
                "可以进一步优化决策速度",
                "增强对隐含需求的识别能力"
            ]
        }
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.datetime.now().isoformat()`;
              githubPath = 'agents/thought_recorder/thought_recorder.py';
              break;
            case 'release-manager':
              code = `# 发布管理器代码
import os
import sys
import json
import logging
import requests
import subprocess
from typing import Dict, Any, List, Optional

class ReleaseManager:
    """
    发布管理器类
    管理系统版本发布和更新，确保代码部署的稳定性
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化发布管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config", "release_manager.json")
        self.config = self._load_config()
        self.logger = self._setup_logger()
        
        # 设置GitHub相关参数
        self.github_repo = self.config.get("github_repo", "")
        self.github_token = self.config.get("github_token", "")
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}"
        
        self.logger.info("发布管理器初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                return {}
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("ReleaseManager")
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        
        return logger
    
    def check_for_updates(self) -> Dict[str, Any]:
        """
        检查是否有更新
        
        Returns:
            更新检查结果
        """
        self.logger.info("检查是否有更新")
        
        try:
            # 检查GitHub上是否有新的release
            latest_release = self._check_github_releases()
            
            # 检查本地版本
            local_version = self._check_local_version()
            
            # 比较版本
            comparison_result = self._compare_versions(local_version, latest_release)
            
            return {
                "status": "success",
                "local_version": local_version,
                "latest_release": latest_release,
                "needs_update": comparison_result["needs_update"],
                "comparison_details": comparison_result
            }
        except Exception as e:
            self.logger.error(f"检查更新失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def _check_github_releases(self) -> Dict[str, Any]:
        """检查GitHub上是否有新的release"""
        self.logger.info("检查GitHub上是否有新的release")
        
        if not self.github_repo:
            self.logger.warning("未配置GitHub仓库信息")
            return {"version": "unknown", "tag_name": "unknown", "published_at": "unknown"}
        
        try:
            # 设置请求头
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            # 发送请求获取最新release
            response = requests.get(f"{self.github_api_url}/releases/latest", headers=headers)
            
            if response.status_code == 200:
                release_data = response.json()
                return {
                    "version": release_data.get("tag_name", "").lstrip("v"),
                    "tag_name": release_data.get("tag_name", ""),
                    "published_at": release_data.get("published_at", ""),
                    "body": release_data.get("body", ""),
                    "html_url": release_data.get("html_url", "")
                }
            else:
                self.logger.warning(f"获取GitHub release失败: {response.status_code} - {response.text}")
                return {"version": "unknown", "tag_name": "unknown", "published_at": "unknown"}
        except Exception as e:
            self.logger.error(f"检查GitHub releases异常: {str(e)}")
            return {"version": "unknown", "tag_name": "unknown", "published_at": "unknown"}
    
    def _check_local_version(self) -> Dict[str, Any]:
        """检查本地版本"""
        self.logger.info("检查本地版本")
        
        version_file = os.path.join(os.path.dirname(self.config_path), "..", "version.json")
        
        if os.path.exists(version_file):
            try:
                with open(version_file, "r", encoding="utf-8") as f:
                    version_data = json.load(f)
                    return {
                        "version": version_data.get("version", "0.0.0"),
                        "build_date": version_data.get("build_date", ""),
                        "commit_hash": version_data.get("commit_hash", "")
                    }
            except Exception as e:
                self.logger.error(f"读取本地版本文件失败: {str(e)}")
        
        # 如果版本文件不存在或读取失败，尝试从git获取信息
        try:
            # 获取当前commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=os.path.dirname(self.config_path),
                capture_output=True,
                text=True,
                check=True
            )
            commit_hash = result.stdout.strip()
            
            # 获取最新tag
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                cwd=os.path.dirname(self.config_path),
                capture_output=True,
                text=True
            )
            tag = result.stdout.strip() if result.returncode == 0 else "v0.0.0"
            
            return {
                "version": tag.lstrip("v"),
                "build_date": "",
                "commit_hash": commit_hash
            }
        except Exception as e:
            self.logger.error(f"从git获取版本信息失败: {str(e)}")
            return {
                "version": "0.0.0",
                "build_date": "",
                "commit_hash": ""
            }
    
    def _compare_versions(self, local_version: Dict[str, Any], latest_release: Dict[str, Any]) -> Dict[str, Any]:
        """比较版本"""
        self.logger.info("比较版本")
        
        local_ver = local_version.get("version", "0.0.0")
        remote_ver = latest_release.get("version", "0.0.0")
        
        # 解析版本号
        local_parts = self._parse_version(local_ver)
        remote_parts = self._parse_version(remote_ver)
        
        # 比较主版本号
        if remote_parts[0] > local_parts[0]:
            return {
                "needs_update": True,
                "update_type": "major",
                "message": f"有主要版本更新: {local_ver} -> {remote_ver}"
            }
        
        # 比较次版本号
        if remote_parts[0] == local_parts[0] and remote_parts[1] > local_parts[1]:
            return {
                "needs_update": True,
                "update_type": "minor",
                "message": f"有次要版本更新: {local_ver} -> {remote_ver}"
            }
        
        # 比较修订版本号
        if remote_parts[0] == local_parts[0] and remote_parts[1] == local_parts[1] and remote_parts[2] > local_parts[2]:
            return {
                "needs_update": True,
                "update_type": "patch",
                "message": f"有补丁版本更新: {local_ver} -> {remote_ver}"
            }
        
        return {
            "needs_update": False,
            "update_type": "none",
            "message": f"当前版本已是最新: {local_ver}"
        }
    
    def _parse_version(self, version: str) -> List[int]:
        """解析版本号"""
        parts = version.split(".")
        result = []
        
        for part in parts:
            try:
                result.append(int(part))
            except ValueError:
                result.append(0)
        
        # 确保至少有三个部分
        while len(result) < 3:
            result.append(0)
        
        return result
    
    def update_system(self, version: str = None) -> Dict[str, Any]:
        """
        更新系统
        
        Args:
            version: 目标版本，如果为None则更新到最新版本
            
        Returns:
            更新结果
        """
        self.logger.info(f"更新系统到版本: {version or '最新'}")
        
        try:
            # 检查权限
            if not self._check_permissions():
                return {
                    "status": "error",
                    "error_message": "权限不足，无法执行更新操作"
                }
            
            # 执行更新操作
            update_result = self._execute_update(version)
            
            # 验证更新结果
            verification_result = self._verify_update(update_result)
            
            return {
                "status": "success" if verification_result["success"] else "error",
                "update_result": update_result,
                "verification_result": verification_result
            }
        except Exception as e:
            self.logger.error(f"更新系统失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def _check_permissions(self) -> bool:
        """检查权限"""
        self.logger.info("检查权限")
        # 实际实现会检查当前用户是否有足够的权限执行更新操作
        
        # 模拟权限检查
        try:
            # 尝试写入临时文件
            test_file = os.path.join(os.path.dirname(self.config_path), ".permission_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            
            # 尝试执行git命令
            result = subprocess.run(
                ["git", "status"],
                cwd=os.path.dirname(self.config_path),
                capture_output=True,
                text=True,
                check=True
            )
            
            return True
        except Exception as e:
            self.logger.error(f"权限检查失败: {str(e)}")
            return False
    
    def _execute_update(self, version: str = None) -> Dict[str, Any]:
        """执行更新操作"""
        self.logger.info(f"执行更新操作: {version or '最新'}")
        # 实际实现会执行git pull或其他更新操作
        
        # 模拟更新操作
        try:
            if version:
                # 更新到指定版本
                result = subprocess.run(
                    ["git", "checkout", f"tags/{version}"],
                    cwd=os.path.dirname(self.config_path),
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                # 更新到最新版本
                result = subprocess.run(
                    ["git", "pull", "origin", "main"],
                    cwd=os.path.dirname(self.config_path),
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            return {
                "success": True,
                "message": "更新成功",
                "details": result.stdout
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"执行更新命令失败: {e.stderr}")
            return {
                "success": False,
                "message": "更新失败",
                "details": e.stderr
            }
        except Exception as e:
            self.logger.error(f"执行更新操作异常: {str(e)}")
            return {
                "success": False,
                "message": "更新异常",
                "details": str(e)
            }
    
    def _verify_update(self, update_result: Dict[str, Any]) -> Dict[str, Any]:
        """验证更新结果"""
        self.logger.info("验证更新结果")
        # 实际实现会验证更新是否成功
        
        if not update_result.get("success", False):
            return {
                "success": False,
                "message": "更新失败，无需验证"
            }
        
        # 检查版本文件
        try:
            local_version = self._check_local_version()
            return {
                "success": True,
                "message": "更新验证成功",
                "current_version": local_version
            }
        except Exception as e:
            self.logger.error(f"验证更新结果失败: {str(e)}")
            return {
                "success": False,
                "message": "更新验证失败",
                "error": str(e)
            }`;
              githubPath = 'agents/release_manager/release_manager.py';
              break;
            case 'supermemory':
              code = `# SuperMemory代码
import os
import sys
import json
import logging
import datetime
import sqlite3
from typing import Dict, Any, List, Optional, Union

class SuperMemory:
    """
    SuperMemory类
    管理智能体的记忆系统，提供长期记忆存储和检索功能
    """
    
    def __init__(self, config_path: str = None, db_path: str = None):
        """
        初始化SuperMemory
        
        Args:
            config_path: 配置文件路径
            db_path: 数据库文件路径
        """
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "config", "supermemory.json")
        self.config = self._load_config()
        self.logger = self._setup_logger()
        
        # 设置数据库路径
        self.db_path = db_path or self.config.get("db_path", os.path.join(os.path.dirname(__file__), "data", "memory.db"))
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        self.logger.info("SuperMemory初始化完成")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                return {}
        return {}
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("SuperMemory")
        logger.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(console_handler)
        
        return logger
    
    def _init_database(self) -> None:
        """初始化数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建记忆表
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                type TEXT NOT NULL,
                importance REAL NOT NULL,
                created_at TEXT NOT NULL,
                last_accessed TEXT,
                access_count INTEGER DEFAULT 0,
                metadata TEXT
            )
            ''')
            
            # 创建标签表
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                memory_id TEXT,
                tag TEXT,
                PRIMARY KEY (memory_id, tag),
                FOREIGN KEY (memory_id) REFERENCES memories (id) ON DELETE CASCADE
            )
            ''')
            
            # 创建关联表
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS associations (
                source_id TEXT,
                target_id TEXT,
                strength REAL NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (source_id, target_id),
                FOREIGN KEY (source_id) REFERENCES memories (id) ON DELETE CASCADE,
                FOREIGN KEY (target_id) REFERENCES memories (id) ON DELETE CASCADE
            )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("数据库初始化完成")
        except Exception as e:
            self.logger.error(f"初始化数据库失败: {str(e)}")
            raise
    
    def store_memory(self, content: str, memory_type: str, importance: float = 0.5, tags: List[str] = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        存储记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性（0-1）
            tags: 标签列表
            metadata: 元数据
            
        Returns:
            存储结果
        """
        self.logger.info(f"存储记忆: {memory_type} - {content[:50]}...")
        
        try:
            # 生成记忆ID
            memory_id = f"mem_{self._get_timestamp_str()}_{hash(content) % 10000:04d}"
            
            # 准备记忆数据
            now = self._get_timestamp()
            memory_data = {
                "id": memory_id,
                "content": content,
                "type": memory_type,
                "importance": importance,
                "created_at": now,
                "last_accessed": None,
                "access_count": 0,
                "metadata": json.dumps(metadata or {})
            }
            
            # 存储到数据库
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 插入记忆
            cursor.execute('''
            INSERT INTO memories (id, content, type, importance, created_at, last_accessed, access_count, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory_data["id"],
                memory_data["content"],
                memory_data["type"],
                memory_data["importance"],
                memory_data["created_at"],
                memory_data["last_accessed"],
                memory_data["access_count"],
                memory_data["metadata"]
            ))
            
            # 插入标签
            if tags:
                for tag in tags:
                    cursor.execute('''
                    INSERT INTO tags (memory_id, tag)
                    VALUES (?, ?)
                    ''', (memory_id, tag))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "memory_id": memory_id,
                "message": "记忆存储成功"
            }
        except Exception as e:
            self.logger.error(f"存储记忆失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def retrieve_memory(self, query: str, memory_type: str = None, tags: List[str] = None, limit: int = 10) -> Dict[str, Any]:
        """
        检索记忆
        
        Args:
            query: 查询内容
            memory_type: 记忆类型过滤
            tags: 标签过滤
            limit: 返回结果数量限制
            
        Returns:
            检索结果
        """
        self.logger.info(f"检索记忆: {query[:50]}...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 构建查询条件
            conditions = ["1=1"]  # 始终为真的条件，方便后续添加AND条件
            params = []
            
            # 添加内容匹配条件
            if query:
                conditions.append("content LIKE ?")
                params.append(f"%{query}%")
            
            # 添加类型过滤条件
            if memory_type:
                conditions.append("type = ?")
                params.append(memory_type)
            
            # 构建基本查询
            base_query = f'''
            SELECT id, content, type, importance, created_at, last_accessed, access_count, metadata
            FROM memories
            WHERE {" AND ".join(conditions)}
            '''
            
            # 如果有标签过滤，需要连接tags表
            if tags:
                tag_conditions = []
                for tag in tags:
                    tag_conditions.append("t.tag = ?")
                    params.append(tag)
                
                base_query = f'''
                SELECT DISTINCT m.id, m.content, m.type, m.importance, m.created_at, m.last_accessed, m.access_count, m.metadata
                FROM memories m
                JOIN tags t ON m.id = t.memory_id
                WHERE {" AND ".join(conditions)} AND ({" OR ".join(tag_conditions)})
                '''
            
            # 添加排序和限制
            final_query = f'''
            {base_query}
            ORDER BY importance DESC, last_accessed DESC, created_at DESC
            LIMIT ?
            '''
            params.append(limit)
            
            # 执行查询
            cursor.execute(final_query, params)
            rows = cursor.fetchall()
            
            # 处理结果
            memories = []
            for row in rows:
                memory = dict(row)
                
                # 更新访问时间和计数
                now = self._get_timestamp()
                cursor.execute('''
                UPDATE memories
                SET last_accessed = ?, access_count = access_count + 1
                WHERE id = ?
                ''', (now, memory["id"]))
                
                # 获取标签
                cursor.execute('''
                SELECT tag FROM tags WHERE memory_id = ?
                ''', (memory["id"],))
                memory_tags = [t[0] for t in cursor.fetchall()]
                
                # 解析元数据
                try:
                    memory["metadata"] = json.loads(memory["metadata"])
                except:
                    memory["metadata"] = {}
                
                # 添加标签到结果
                memory["tags"] = memory_tags
                memories.append(memory)
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "query": query,
                "memory_type": memory_type,
                "tags": tags,
                "count": len(memories),
                "memories": memories
            }
        except Exception as e:
            self.logger.error(f"检索记忆失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def create_association(self, source_id: str, target_id: str, strength: float = 0.5) -> Dict[str, Any]:
        """
        创建记忆关联
        
        Args:
            source_id: 源记忆ID
            target_id: 目标记忆ID
            strength: 关联强度（0-1）
            
        Returns:
            创建结果
        """
        self.logger.info(f"创建记忆关联: {source_id} -> {target_id}, 强度: {strength}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查记忆是否存在
            cursor.execute("SELECT id FROM memories WHERE id IN (?, ?)", (source_id, target_id))
            existing_ids = [row[0] for row in cursor.fetchall()]
            
            if len(existing_ids) < 2:
                missing_ids = set([source_id, target_id]) - set(existing_ids)
                return {
                    "status": "error",
                    "error_message": f"记忆不存在: {', '.join(missing_ids)}"
                }
            
            # 创建关联
            now = self._get_timestamp()
            cursor.execute('''
            INSERT OR REPLACE INTO associations (source_id, target_id, strength, created_at)
            VALUES (?, ?, ?, ?)
            ''', (source_id, target_id, strength, now))
            
            conn.commit()
            conn.close()
            
            return {
                "status": "success",
                "source_id": source_id,
                "target_id": target_id,
                "strength": strength,
                "message": "记忆关联创建成功"
            }
        except Exception as e:
            self.logger.error(f"创建记忆关联失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def get_associated_memories(self, memory_id: str, min_strength: float = 0.0, limit: int = 10) -> Dict[str, Any]:
        """
        获取关联记忆
        
        Args:
            memory_id: 记忆ID
            min_strength: 最小关联强度
            limit: 返回结果数量限制
            
        Returns:
            关联记忆列表
        """
        self.logger.info(f"获取关联记忆: {memory_id}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 查询关联记忆
            cursor.execute('''
            SELECT a.target_id, a.strength, a.created_at,
                   m.content, m.type, m.importance, m.created_at as memory_created_at
            FROM associations a
            JOIN memories m ON a.target_id = m.id
            WHERE a.source_id = ? AND a.strength >= ?
            ORDER BY a.strength DESC
            LIMIT ?
            ''', (memory_id, min_strength, limit))
            
            target_rows = cursor.fetchall()
            
            # 查询反向关联
            cursor.execute('''
            SELECT a.source_id as target_id, a.strength, a.created_at,
                   m.content, m.type, m.importance, m.created_at as memory_created_at
            FROM associations a
            JOIN memories m ON a.source_id = m.id
            WHERE a.target_id = ? AND a.strength >= ?
            ORDER BY a.strength DESC
            LIMIT ?
            ''', (memory_id, min_strength, limit))
            
            source_rows = cursor.fetchall()
            
            # 合并结果
            associated_memories = []
            
            for row in target_rows:
                memory = dict(row)
                memory["direction"] = "outgoing"
                associated_memories.append(memory)
            
            for row in source_rows:
                memory = dict(row)
                memory["direction"] = "incoming"
                associated_memories.append(memory)
            
            # 按强度排序
            associated_memories.sort(key=lambda x: x["strength"], reverse=True)
            
            # 如果结果超过限制，截取前limit个
            if len(associated_memories) > limit:
                associated_memories = associated_memories[:limit]
            
            conn.close()
            
            return {
                "status": "success",
                "memory_id": memory_id,
                "count": len(associated_memories),
                "associated_memories": associated_memories
            }
        except Exception as e:
            self.logger.error(f"获取关联记忆失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def optimize_memory_storage(self) -> Dict[str, Any]:
        """
        优化记忆存储
        
        Returns:
            优化结果
        """
        self.logger.info("优化记忆存储")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 执行数据库优化
            cursor.execute("VACUUM")
            
            # 获取统计信息
            cursor.execute("SELECT COUNT(*) FROM memories")
            memory_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM tags")
            tag_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM associations")
            association_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "status": "success",
                "message": "记忆存储优化成功",
                "statistics": {
                    "memory_count": memory_count,
                    "tag_count": tag_count,
                    "association_count": association_count
                }
            }
        except Exception as e:
            self.logger.error(f"优化记忆存储失败: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e)
            }
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.datetime.now().isoformat()
    
    def _get_timestamp_str(self) -> str:
        """获取格式化的时间戳字符串"""
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")`;
              githubPath = 'agents/supermemory/supermemory.py';
              break;
            default:
              code = '// 未找到与所选节点对应的代码';
          }
        }

        // 设置GitHub URL
        if (githubPath) {
          setGithubUrl(`https://github.com/yourusername/powerautomation/blob/main/${githubPath}`);
        } else {
          setGithubUrl('');
        }

        // 设置文档URL
        if (activeWorkflowType === 'automation-test') {
          setDocsUrl('https://github.com/yourusername/powerautomation/blob/main/frontend/src/docs/automation_test_workflow.md');
        } else if (activeWorkflowType === 'agent-design') {
          setDocsUrl('https://github.com/yourusername/powerautomation/blob/main/frontend/src/docs/agent_design_workflow.md');
        }

        setCodeContent(code);
      } catch (error) {
        console.error('获取代码失败:', error);
        setCodeContent('// 加载代码时发生错误');
      }
    };

    fetchCode();
  }, [selectedNodeId, activeWorkflowType, refreshTrigger]);

  return (
    <div className="code-view">
      <h2 className="section-title">代码视图</h2>
      
      {selectedNodeId && (
        <div className="selected-node-info">
          <span className="selected-node-label">当前选中节点:</span>
          <span className="selected-node-id">{selectedNodeId}</span>
        </div>
      )}
      
      <div className="code-tabs">
        <button 
          className={`code-tab ${activeTab === 'code' ? 'active' : ''}`}
          onClick={() => setActiveTab('code')}
        >
          代码
        </button>
        <button 
          className={`code-tab ${activeTab === 'docs' ? 'active' : ''}`}
          onClick={() => setActiveTab('docs')}
        >
          文档
        </button>
      </div>
      
      <div className="code-content">
        {activeTab === 'code' ? (
          <>
            <div className="code-actions">
              <button 
                className="copy-btn"
                onClick={() => {
                  navigator.clipboard.writeText(codeContent);
                  alert('代码已复制到剪贴板');
                }}
              >
                复制代码
              </button>
              {githubUrl && (
                <a 
                  href={githubUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="github-link"
                >
                  在GitHub上查看
                </a>
              )}
            </div>
            <pre className="code-display">
              <code>{codeContent}</code>
            </pre>
          </>
        ) : (
          <div className="docs-content">
            <div className="docs-actions">
              {docsUrl && (
                <a 
                  href={docsUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="docs-link"
                >
                  在GitHub上查看完整文档
                </a>
              )}
            </div>
            <div className="docs-frame">
              <iframe 
                src={activeWorkflowType === 'automation-test' 
                  ? '/src/docs/automation_test_workflow.md'
                  : '/src/docs/agent_design_workflow.md'} 
                title="文档"
                className="docs-iframe"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CodeView;
