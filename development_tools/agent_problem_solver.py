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
    6. 回滚历史记录：记录所有回滚操作的历史和结果
    7. 工作节点展示：为web端提供工作节点数据，支持可视化展示
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
        
        # 初始化回滚历史记录
        self.rollback_history = []
        self._load_rollback_history()
        
        # 初始化回滚统计数据
        self.rollback_stats = {
            'total_rollbacks': 0,
            'successful_rollbacks': 0,
            'failed_rollbacks': 0,
            'auto_rollbacks': 0,
            'manual_rollbacks': 0
        }
        self._load_rollback_stats()
        
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
    
    def _load_rollback_history(self) -> None:
        """加载回滚历史记录"""
        history_file = os.path.join(self.savepoints_dir, 'rollback_history.json')
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.rollback_history = json.load(f)
                logger.info(f"加载了 {len(self.rollback_history)} 条回滚历史记录")
            except Exception as e:
                logger.error(f"加载回滚历史记录失败: {str(e)}")
                self.rollback_history = []
        else:
            self.rollback_history = []
    
    def _save_rollback_history(self) -> None:
        """保存回滚历史记录"""
        history_file = os.path.join(self.savepoints_dir, 'rollback_history.json')
        try:
            with open(history_file, 'w') as f:
                json.dump(self.rollback_history, f, indent=2)
            logger.info(f"保存了 {len(self.rollback_history)} 条回滚历史记录")
        except Exception as e:
            logger.error(f"保存回滚历史记录失败: {str(e)}")
    
    def _load_rollback_stats(self) -> None:
        """加载回滚统计数据"""
        stats_file = os.path.join(self.savepoints_dir, 'rollback_stats.json')
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    self.rollback_stats = json.load(f)
                logger.info(f"加载了回滚统计数据")
            except Exception as e:
                logger.error(f"加载回滚统计数据失败: {str(e)}")
        else:
            # 初始化默认统计数据
            self.rollback_stats = {
                'total_rollbacks': 0,
                'successful_rollbacks': 0,
                'failed_rollbacks': 0,
                'auto_rollbacks': 0,
                'manual_rollbacks': 0
            }
    
    def _save_rollback_stats(self) -> None:
        """保存回滚统计数据"""
        stats_file = os.path.join(self.savepoints_dir, 'rollback_stats.json')
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.rollback_stats, f, indent=2)
            logger.info(f"保存了回滚统计数据")
        except Exception as e:
            logger.error(f"保存回滚统计数据失败: {str(e)}")
    
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
                'path': savepoint_dir,
                'test_status': 'pending',  # 新增：测试状态
                'deployment_status': 'pending',  # 新增：部署状态
                'created_at': datetime.datetime.now().isoformat(),
                'tags': []  # 新增：标签，用于分类和筛选
            }
            
            # 添加到保存点列表
            self.savepoints.append(savepoint)
            self.current_savepoint_index = len(self.savepoints) - 1
            
            # 保存保存点信息
            self._save_savepoints()
            
            # 创建工作节点记录
            self._create_work_node(savepoint_id, "创建保存点", description)
            
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
    
    def rollback_to_savepoint(self, savepoint_id: str = None, is_auto: bool = False) -> Dict[str, Any]:
        """
        回滚到指定保存点
        
        Args:
            savepoint_id: 保存点ID，如果为None则回滚到上一个保存点
            is_auto: 是否为自动回滚
            
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
            # 保存回滚前的项目哈希值，用于前后对比
            pre_rollback_hash = self._calculate_project_hash()
            
            # 复制保存点文件到项目目录
            self._copy_savepoint_files(savepoint['path'])
            
            # 计算回滚后的项目哈希值
            post_rollback_hash = self._calculate_project_hash()
            
            # 更新当前保存点索引
            self.current_savepoint_index = new_index
            
            # 保存保存点信息
            self._save_savepoints()
            
            # 重置错误计数
            self.error_count = 0
            
            # 更新回滚统计数据
            self.rollback_stats['total_rollbacks'] += 1
            self.rollback_stats['successful_rollbacks'] += 1
            if is_auto:
                self.rollback_stats['auto_rollbacks'] += 1
            else:
                self.rollback_stats['manual_rollbacks'] += 1
            self._save_rollback_stats()
            
            # 记录回滚历史
            rollback_record = {
                'id': f"rb_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'savepoint_id': savepoint_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'is_auto': is_auto,
                'status': 'success',
                'pre_rollback_hash': pre_rollback_hash,
                'post_rollback_hash': post_rollback_hash,
                'hash_diff': pre_rollback_hash != post_rollback_hash,
                'description': f"回滚到保存点: {savepoint.get('description', savepoint_id)}"
            }
            self.rollback_history.append(rollback_record)
            self._save_rollback_history()
            
            # 创建工作节点记录
            self._create_work_node(
                savepoint_id, 
                "回滚操作", 
                f"{'自动' if is_auto else '手动'}回滚到保存点: {savepoint.get('description', '')}"
            )
            
            logger.info(f"回滚成功: {savepoint_id}")
            return {
                'status': 'success',
                'savepoint': savepoint,
                'rollback_record': rollback_record
            }
        except Exception as e:
            logger.error(f"回滚失败: {str(e)}")
            
            # 更新回滚统计数据
            self.rollback_stats['total_rollbacks'] += 1
            self.rollback_stats['failed_rollbacks'] += 1
            self._save_rollback_stats()
            
            # 记录回滚历史
            rollback_record = {
                'id': f"rb_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'savepoint_id': savepoint_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'is_auto': is_auto,
                'status': 'failed',
                'error': str(e),
                'description': f"回滚到保存点失败: {savepoint.get('description', savepoint_id)}"
            }
            self.rollback_history.append(rollback_record)
            self._save_rollback_history()
            
            # 创建工作节点记录
            self._create_work_node(
                savepoint_id, 
                "回滚失败", 
                f"{'自动' if is_auto else '手动'}回滚失败: {str(e)}"
            )
            
            return {
                'error': str(e),
                'status': 'failed',
                'rollback_record': rollback_record
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
        
        # 获取当前保存点
        current_savepoint = self.get_current_savepoint()
        if current_savepoint:
            # 创建工作节点记录
            self._create_work_node(
                current_savepoint['id'], 
                "错误报告", 
                f"错误 ({self.error_count}/{self.max_errors}): {error_message}"
            )
        
        # 检查是否需要自动回滚
        if self.error_count >= self.max_errors:
            logger.warning(f"错误次数达到阈值 ({self.error_count}/{self.max_errors})，触发自动回滚")
            rollback_result = self.rollback_to_savepoint(is_auto=True)
            
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
            
            # 获取当前保存点
            current_savepoint = self.get_current_savepoint()
            if current_savepoint:
                # 创建工作节点记录
                self._create_work_node(
                    current_savepoint['id'], 
                    "问题提交", 
                    f"问题: {problem}"
                )
            
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
                'has_changes': has_changes
            }
        except Exception as e:
            logger.error(f"监控项目状态失败: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_rollback_history(self) -> List[Dict[str, Any]]:
        """
        获取回滚历史记录
        
        Returns:
            回滚历史记录列表
        """
        return self.rollback_history
    
    def get_rollback_stats(self) -> Dict[str, Any]:
        """
        获取回滚统计数据
        
        Returns:
            回滚统计数据
        """
        return self.rollback_stats
    
    def update_savepoint_status(self, savepoint_id: str, test_status: str = None, deployment_status: str = None) -> Dict[str, Any]:
        """
        更新保存点状态
        
        Args:
            savepoint_id: 保存点ID
            test_status: 测试状态
            deployment_status: 部署状态
            
        Returns:
            更新结果
        """
        # 查找保存点
        savepoint = None
        index = -1
        for i, sp in enumerate(self.savepoints):
            if sp['id'] == savepoint_id:
                savepoint = sp
                index = i
                break
        
        if savepoint is None:
            return {
                'error': f'未找到保存点: {savepoint_id}',
                'status': 'failed'
            }
        
        # 更新状态
        if test_status is not None:
            savepoint['test_status'] = test_status
        
        if deployment_status is not None:
            savepoint['deployment_status'] = deployment_status
        
        # 更新保存点列表
        self.savepoints[index] = savepoint
        
        # 保存保存点信息
        self._save_savepoints()
        
        # 创建工作节点记录
        status_updates = []
        if test_status is not None:
            status_updates.append(f"测试状态: {test_status}")
        if deployment_status is not None:
            status_updates.append(f"部署状态: {deployment_status}")
        
        if status_updates:
            self._create_work_node(
                savepoint_id, 
                "状态更新", 
                ", ".join(status_updates)
            )
        
        return {
            'status': 'success',
            'savepoint': savepoint
        }
    
    def _create_work_node(self, savepoint_id: str, node_type: str, description: str) -> Dict[str, Any]:
        """
        创建工作节点记录
        
        Args:
            savepoint_id: 保存点ID
            node_type: 节点类型
            description: 节点描述
            
        Returns:
            工作节点信息
        """
        # 创建工作节点目录
        work_nodes_dir = os.path.join(self.savepoints_dir, 'work_nodes')
        os.makedirs(work_nodes_dir, exist_ok=True)
        
        # 生成节点ID
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        node_id = f"node_{timestamp}"
        
        # 创建节点信息
        node = {
            'id': node_id,
            'savepoint_id': savepoint_id,
            'type': node_type,
            'description': description,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'active'
        }
        
        # 保存节点信息
        nodes_file = os.path.join(work_nodes_dir, 'nodes.json')
        nodes = []
        
        if os.path.exists(nodes_file):
            try:
                with open(nodes_file, 'r') as f:
                    nodes = json.load(f)
            except Exception as e:
                logger.error(f"加载工作节点记录失败: {str(e)}")
                nodes = []
        
        nodes.append(node)
        
        try:
            with open(nodes_file, 'w') as f:
                json.dump(nodes, f, indent=2)
            logger.info(f"保存了工作节点记录: {node_id}")
        except Exception as e:
            logger.error(f"保存工作节点记录失败: {str(e)}")
        
        return node
    
    def get_work_nodes(self, savepoint_id: str = None) -> List[Dict[str, Any]]:
        """
        获取工作节点记录
        
        Args:
            savepoint_id: 保存点ID，如果为None则获取所有节点
            
        Returns:
            工作节点记录列表
        """
        # 加载工作节点记录
        work_nodes_dir = os.path.join(self.savepoints_dir, 'work_nodes')
        nodes_file = os.path.join(work_nodes_dir, 'nodes.json')
        nodes = []
        
        if os.path.exists(nodes_file):
            try:
                with open(nodes_file, 'r') as f:
                    nodes = json.load(f)
            except Exception as e:
                logger.error(f"加载工作节点记录失败: {str(e)}")
                return []
        
        # 如果指定了保存点ID，筛选节点
        if savepoint_id is not None:
            nodes = [node for node in nodes if node['savepoint_id'] == savepoint_id]
        
        return nodes
    
    def get_web_display_data(self) -> Dict[str, Any]:
        """
        获取用于Web端显示的数据
        
        Returns:
            Web端显示数据
        """
        # 获取保存点列表
        savepoints = self.list_savepoints()
        
        # 获取所有工作节点
        work_nodes = self.get_work_nodes()
        
        # 获取回滚历史
        rollback_history = self.get_rollback_history()
        
        # 获取回滚统计数据
        rollback_stats = self.get_rollback_stats()
        
        # 获取当前保存点
        current_savepoint = self.get_current_savepoint()
        
        # 构建Web显示数据
        web_data = {
            'savepoints': savepoints,
            'work_nodes': work_nodes,
            'rollback_history': rollback_history,
            'rollback_stats': rollback_stats,
            'current_savepoint': current_savepoint,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return web_data
    
    def compare_savepoints(self, savepoint_id1: str, savepoint_id2: str) -> Dict[str, Any]:
        """
        比较两个保存点的差异
        
        Args:
            savepoint_id1: 第一个保存点ID
            savepoint_id2: 第二个保存点ID
            
        Returns:
            比较结果
        """
        # 查找保存点
        savepoint1 = None
        savepoint2 = None
        
        for sp in self.savepoints:
            if sp['id'] == savepoint_id1:
                savepoint1 = sp
            if sp['id'] == savepoint_id2:
                savepoint2 = sp
        
        if savepoint1 is None:
            return {
                'error': f'未找到保存点: {savepoint_id1}',
                'status': 'failed'
            }
        
        if savepoint2 is None:
            return {
                'error': f'未找到保存点: {savepoint_id2}',
                'status': 'failed'
            }
        
        # 比较保存点
        try:
            # 使用diff命令比较目录
            diff_cmd = f"diff -r --brief {savepoint1['path']} {savepoint2['path']}"
            diff_result = subprocess.run(diff_cmd, shell=True, capture_output=True, text=True)
            
            # 解析diff结果
            diff_lines = diff_result.stdout.strip().split('\n')
            diff_files = [line for line in diff_lines if line]
            
            return {
                'status': 'success',
                'savepoint1': savepoint1,
                'savepoint2': savepoint2,
                'diff_count': len(diff_files),
                'diff_files': diff_files,
                'is_identical': len(diff_files) == 0
            }
        except Exception as e:
            logger.error(f"比较保存点失败: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }


# 使用示例
if __name__ == "__main__":
    # 创建Agent问题解决驱动器
    solver = AgentProblemSolver("/path/to/project")
    
    # 创建保存点
    savepoint = solver.create_savepoint("初始版本")
    print(f"创建保存点: {savepoint['id']}")
    
    # 报告错误
    error_result = solver.report_error("测试失败")
    print(f"报告错误: {error_result['status']}")
    
    # 回滚到保存点
    rollback_result = solver.rollback_to_savepoint(savepoint['id'])
    print(f"回滚结果: {rollback_result['status']}")
    
    # 获取Web显示数据
    web_data = solver.get_web_display_data()
    print(f"Web数据: {len(web_data['savepoints'])} 个保存点, {len(web_data['work_nodes'])} 个工作节点")
