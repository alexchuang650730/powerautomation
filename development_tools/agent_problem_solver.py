"""
Agent问题解决驱动器（AgentProblemSolver）

具备自动回滚和问题提交能力的智能体问题解决组件
"""

import os
import sys
import json
import logging
import datetime
import subprocess
import hashlib
from typing import Dict, List, Any, Optional, Union, Tuple

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("agent_problem_solver.log")
    ]
)
logger = logging.getLogger("AgentProblemSolver")

# 尝试导入MCP组件
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcptool', 'core'))
    from mcp_planner import MCPPlanner
    logger.info("成功导入MCP Planner")
    MCP_PLANNER_AVAILABLE = True
except ImportError:
    logger.error("无法导入MCP Planner，将使用模拟实现")
    MCP_PLANNER_AVAILABLE = False

# 尝试导入RL Factory
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rl_factory'))
    from rl_factory.recipe import load_recipe
    logger.info("成功导入RL Factory")
    RL_FACTORY_AVAILABLE = True
except ImportError:
    logger.error("无法导入RL Factory，将使用模拟实现")
    RL_FACTORY_AVAILABLE = False


class AgentProblemSolver:
    """
    Agent问题解决驱动器
    
    具备以下能力：
    1. 版本回滚管理：支持每个版本的回滚，在持续出错时回滚至保存点
    2. 自动回滚：当测试方案持续出错超过5次时自动回滚到前一个保存点
    3. 问题提交能力：透过mcpplanner把问题分解后提交给manus.im，并跟RL Factory输出的结果持续比对
    4. 保存点管理：创建和管理代码版本保存点
    5. 错误计数与监控：监控错误次数并触发自动回滚
    """
    
    def __init__(self, project_dir: str, max_errors: int = 5):
        """
        初始化Agent问题解决驱动器
        
        Args:
            project_dir: 项目目录
            max_errors: 触发自动回滚的最大错误次数
        """
        self.project_dir = os.path.abspath(project_dir)
        self.max_errors = max_errors
        self.error_count = 0
        self.savepoints = []
        self.current_savepoint_index = -1
        
        # 初始化MCP Planner
        self.mcp_planner = self._initialize_mcp_planner()
        
        # 初始化RL Factory
        self.rl_factory = self._initialize_rl_factory()
        
        # 创建保存点目录
        self.savepoints_dir = os.path.join(self.project_dir, '.savepoints')
        os.makedirs(self.savepoints_dir, exist_ok=True)
        
        # 加载现有保存点
        self._load_savepoints()
        
        logger.info(f"Agent问题解决驱动器初始化完成，项目目录: {self.project_dir}")
    
    def _initialize_mcp_planner(self) -> Any:
        """初始化MCP Planner"""
        if MCP_PLANNER_AVAILABLE:
            try:
                return MCPPlanner()
            except Exception as e:
                logger.error(f"MCP Planner初始化失败: {str(e)}")
        
        # 返回模拟MCP Planner
        return self._create_mock_mcp_planner()
    
    def _create_mock_mcp_planner(self) -> Any:
        """创建模拟MCP Planner"""
        class MockMCPPlanner:
            def plan(self, problem):
                return {
                    "steps": [
                        {"description": "分析问题", "details": f"分析问题: {problem}"},
                        {"description": "提出解决方案", "details": "提出可能的解决方案"},
                        {"description": "实施解决方案", "details": "实施选定的解决方案"}
                    ],
                    "summary": f"问题 '{problem}' 的解决方案"
                }
        
        return MockMCPPlanner()
    
    def _initialize_rl_factory(self) -> Any:
        """初始化RL Factory"""
        if RL_FACTORY_AVAILABLE:
            try:
                recipe = load_recipe("configs/problem_solver_recipe.yaml")
                return recipe.load_model("Qwen3-8B")
            except Exception as e:
                logger.error(f"RL Factory初始化失败: {str(e)}")
        
        # 返回模拟RL Factory
        return self._create_mock_rl_factory()
    
    def _create_mock_rl_factory(self) -> Any:
        """创建模拟RL Factory"""
        class MockRLFactory:
            def generate(self, prompt):
                return f"RL Factory生成的解决方案: {prompt}"
            
            def compare(self, solution1, solution2):
                return {
                    "similarity": 0.8,
                    "differences": ["解决方案1更详细", "解决方案2更简洁"],
                    "recommendation": "建议采用解决方案1"
                }
        
        return MockRLFactory()
    
    def _load_savepoints(self) -> None:
        """加载现有保存点"""
        savepoints_file = os.path.join(self.savepoints_dir, 'savepoints.json')
        if os.path.exists(savepoints_file):
            try:
                with open(savepoints_file, 'r') as f:
                    data = json.load(f)
                    self.savepoints = data.get('savepoints', [])
                    self.current_savepoint_index = data.get('current_index', -1)
                logger.info(f"加载了 {len(self.savepoints)} 个保存点")
            except Exception as e:
                logger.error(f"加载保存点失败: {str(e)}")
                self.savepoints = []
                self.current_savepoint_index = -1
    
    def _save_savepoints(self) -> None:
        """保存保存点信息"""
        savepoints_file = os.path.join(self.savepoints_dir, 'savepoints.json')
        try:
            with open(savepoints_file, 'w') as f:
                json.dump({
                    'savepoints': self.savepoints,
                    'current_index': self.current_savepoint_index
                }, f, indent=2)
            logger.info(f"保存了 {len(self.savepoints)} 个保存点信息")
        except Exception as e:
            logger.error(f"保存保存点信息失败: {str(e)}")
    
    def create_savepoint(self, description: str = "") -> Dict[str, Any]:
        """
        创建代码版本保存点
        
        Args:
            description: 保存点描述
            
        Returns:
            保存点信息
        """
        logger.info(f"创建保存点: {description}")
        
        try:
            # 生成保存点ID
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            savepoint_id = f"sp_{timestamp}"
            
            # 创建保存点目录
            savepoint_dir = os.path.join(self.savepoints_dir, savepoint_id)
            os.makedirs(savepoint_dir, exist_ok=True)
            
            # 复制项目文件到保存点目录
            self._copy_project_files(savepoint_dir)
            
            # 计算项目文件哈希值
            project_hash = self._calculate_project_hash()
            
            # 创建保存点信息
            savepoint = {
                'id': savepoint_id,
                'timestamp': timestamp,
                'description': description,
                'project_hash': project_hash,
                'path': savepoint_dir
            }
            
            # 添加到保存点列表
            self.savepoints.append(savepoint)
            self.current_savepoint_index = len(self.savepoints) - 1
            
            # 保存保存点信息
            self._save_savepoints()
            
            logger.info(f"保存点创建成功: {savepoint_id}")
            return savepoint
        except Exception as e:
            logger.error(f"创建保存点失败: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _copy_project_files(self, target_dir: str) -> None:
        """
        复制项目文件到目标目录
        
        Args:
            target_dir: 目标目录
        """
        # 排除的目录和文件
        exclude_patterns = [
            '.git', '.savepoints', '__pycache__', '*.pyc', '*.pyo',
            'node_modules', 'venv', '.env', '.venv'
        ]
        
        # 构建rsync命令
        exclude_args = ' '.join([f'--exclude="{pattern}"' for pattern in exclude_patterns])
        cmd = f'rsync -a {exclude_args} {self.project_dir}/ {target_dir}/'
        
        # 执行命令
        subprocess.run(cmd, shell=True, check=True)
    
    def _calculate_project_hash(self) -> str:
        """
        计算项目文件哈希值
        
        Returns:
            项目哈希值
        """
        hash_md5 = hashlib.md5()
        
        # 排除的目录和文件
        exclude_patterns = [
            '.git', '.savepoints', '__pycache__', '*.pyc', '*.pyo',
            'node_modules', 'venv', '.env', '.venv'
        ]
        
        # 遍历项目文件
        for root, dirs, files in os.walk(self.project_dir):
            # 排除目录
            dirs[:] = [d for d in dirs if not any(
                d == pattern or 
                (pattern.startswith('*') and d.endswith(pattern[1:])) or
                (pattern.endswith('*') and d.startswith(pattern[:-1]))
                for pattern in exclude_patterns
            )]
            
            # 处理文件
            for file in files:
                # 排除文件
                if any(
                    file == pattern or 
                    (pattern.startswith('*') and file.endswith(pattern[1:])) or
                    (pattern.endswith('*') and file.startswith(pattern[:-1]))
                    for pattern in exclude_patterns
                ):
                    continue
                
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                except Exception as e:
                    logger.warning(f"计算文件哈希值失败: {file_path}, {str(e)}")
        
        return hash_md5.hexdigest()
    
    def list_savepoints(self) -> List[Dict[str, Any]]:
        """
        列出所有保存点
        
        Returns:
            保存点列表
        """
        return self.savepoints
    
    def get_current_savepoint(self) -> Optional[Dict[str, Any]]:
        """
        获取当前保存点
        
        Returns:
            当前保存点信息
        """
        if self.current_savepoint_index >= 0 and self.current_savepoint_index < len(self.savepoints):
            return self.savepoints[self.current_savepoint_index]
        return None
    
    def rollback_to_savepoint(self, savepoint_id: str = None) -> Dict[str, Any]:
        """
        回滚到指定保存点
        
        Args:
            savepoint_id: 保存点ID，如果为None则回滚到上一个保存点
            
        Returns:
            回滚结果
        """
        # 如果未指定保存点ID，回滚到上一个保存点
        if savepoint_id is None:
            if self.current_savepoint_index > 0:
                self.current_savepoint_index -= 1
                savepoint = self.savepoints[self.current_savepoint_index]
                savepoint_id = savepoint['id']
            else:
                return {
                    'error': '没有上一个保存点可回滚',
                    'status': 'failed'
                }
        
        # 查找保存点
        savepoint = None
        new_index = -1
        for i, sp in enumerate(self.savepoints):
            if sp['id'] == savepoint_id:
                savepoint = sp
                new_index = i
                break
        
        if savepoint is None:
            return {
                'error': f'未找到保存点: {savepoint_id}',
                'status': 'failed'
            }
        
        logger.info(f"回滚到保存点: {savepoint_id}")
        
        try:
            # 复制保存点文件到项目目录
            self._copy_savepoint_files(savepoint['path'])
            
            # 更新当前保存点索引
            self.current_savepoint_index = new_index
            
            # 保存保存点信息
            self._save_savepoints()
            
            # 重置错误计数
            self.error_count = 0
            
            logger.info(f"回滚成功: {savepoint_id}")
            return {
                'status': 'success',
                'savepoint': savepoint
            }
        except Exception as e:
            logger.error(f"回滚失败: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def _copy_savepoint_files(self, savepoint_dir: str) -> None:
        """
        复制保存点文件到项目目录
        
        Args:
            savepoint_dir: 保存点目录
        """
        # 排除的目录和文件
        exclude_patterns = [
            '.git', '.savepoints', '__pycache__', '*.pyc', '*.pyo',
            'node_modules', 'venv', '.env', '.venv'
        ]
        
        # 构建rsync命令
        exclude_args = ' '.join([f'--exclude="{pattern}"' for pattern in exclude_patterns])
        cmd = f'rsync -a --delete {exclude_args} {savepoint_dir}/ {self.project_dir}/'
        
        # 执行命令
        subprocess.run(cmd, shell=True, check=True)
    
    def report_error(self, error_message: str, error_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        报告错误
        
        Args:
            error_message: 错误信息
            error_context: 错误上下文
            
        Returns:
            处理结果
        """
        logger.info(f"报告错误: {error_message}")
        
        # 增加错误计数
        self.error_count += 1
        
        # 记录错误
        error_record = {
            'timestamp': datetime.datetime.now().isoformat(),
            'message': error_message,
            'context': error_context or {},
            'count': self.error_count
        }
        
        # 检查是否需要自动回滚
        if self.error_count >= self.max_errors:
            logger.warning(f"错误次数达到阈值 ({self.error_count}/{self.max_errors})，触发自动回滚")
            rollback_result = self.rollback_to_savepoint()
            
            return {
                'status': 'auto_rollback',
                'error': error_record,
                'rollback_result': rollback_result
            }
        
        return {
            'status': 'recorded',
            'error': error_record
        }
    
    def reset_error_count(self) -> None:
        """重置错误计数"""
        self.error_count = 0
        logger.info("错误计数已重置")
    
    def submit_problem(self, problem: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        提交问题
        
        Args:
            problem: 问题描述
            context: 问题上下文
            
        Returns:
            处理结果
        """
        logger.info(f"提交问题: {problem}")
        
        try:
            # 使用MCP Planner分解问题
            plan = self.mcp_planner.plan(problem)
            
            # 使用RL Factory生成解决方案
            rl_solution = self.rl_factory.generate(problem)
            
            # 准备提交到manus.im的数据
            submission_data = {
                'problem': problem,
                'context': context or {},
                'plan': plan,
                'rl_solution': rl_solution,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # 提交到manus.im（模拟）
            manus_solution = self._submit_to_manus(submission_data)
            
            # 比较RL Factory和manus.im的解决方案
            comparison = self.rl_factory.compare(rl_solution, manus_solution)
            
            return {
                'status': 'success',
                'plan': plan,
                'rl_solution': rl_solution,
                'manus_solution': manus_solution,
                'comparison': comparison
            }
        except Exception as e:
            logger.error(f"提交问题失败: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _submit_to_manus(self, data: Dict[str, Any]) -> str:
        """
        提交数据到manus.im（模拟）
        
        Args:
            data: 提交数据
            
        Returns:
            manus.im的解决方案
        """
        # 这里是模拟代码，实际项目中应与manus.im API交互
        logger.info("提交数据到manus.im（模拟）")
        
        # 模拟manus.im的解决方案
        return f"Manus.im生成的解决方案: {data['problem']}\n\n" + \
               f"1. 分析问题根源\n" + \
               f"2. 提出解决方案\n" + \
               f"3. 实施解决步骤\n" + \
               f"4. 验证解决效果"
    
    def monitor_project(self) -> Dict[str, Any]:
        """
        监控项目状态
        
        Returns:
            项目状态
        """
        logger.info("监控项目状态")
        
        try:
            # 计算当前项目哈希值
            current_hash = self._calculate_project_hash()
            
            # 获取当前保存点
            current_savepoint = self.get_current_savepoint()
            
            # 检查项目是否有变化
            has_changes = False
            if current_savepoint:
                has_changes = current_hash != current_savepoint['project_hash']
            
            return {
                'status': 'success',
                'current_hash': current_hash,
                'current_savepoint': current_savepoint,
                'has_changes': has_changes,
                'error_count': self.error_count,
                'timestamp': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"监控项目状态失败: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }


# 示例用法
if __name__ == "__main__":
    # 创建Agent问题解决驱动器
    solver = AgentProblemSolver("/path/to/project")
    
    # 创建保存点
    savepoint = solver.create_savepoint("初始版本")
    print(f"创建保存点: {savepoint}")
    
    # 报告错误
    for i in range(6):
        result = solver.report_error(f"测试错误 {i+1}")
        print(f"报告错误结果: {result}")
        
        # 如果触发了自动回滚，退出循环
        if result['status'] == 'auto_rollback':
            print("触发自动回滚")
            break
    
    # 提交问题
    problem_result = solver.submit_problem("如何优化代码性能？")
    print(f"提交问题结果: {problem_result}")
    
    # 监控项目状态
    status = solver.monitor_project()
    print(f"项目状态: {status}")
