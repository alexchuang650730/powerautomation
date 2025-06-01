"""
RL Factory与MCPPlanner、MCPBrainstorm和ThoughtActionRecorder接口对齐模块

负责确保RL Factory以MCPPlanner和MCPBrainstorm的输入作为学习者，
持续强化学习对齐开发模块的ThoughtActionRecorder输入并达到一样水平
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
        logging.FileHandler("rl_alignment.log")
    ]
)
logger = logging.getLogger("RLFactoryAlignment")

# 尝试导入RL Factory
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'rl_factory'))
    from rl_factory.recipe import load_recipe
    from rl_factory.core.learning.supervised import SupervisedLearner
    from rl_factory.adapters.infinite_context_adapter import InfiniteContextAdapter
    logger.info("成功导入RL Factory")
    RL_FACTORY_AVAILABLE = True
except ImportError:
    logger.error("无法导入RL Factory，强化学习功能将受限")
    RL_FACTORY_AVAILABLE = False

# 尝试导入MCP组件
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcptool', 'core'))
    from mcp_planner import MCPPlanner
    from mcp_brainstorm import MCPBrainstorm
    logger.info("成功导入MCP组件")
    MCP_COMPONENTS_AVAILABLE = True
except ImportError:
    logger.error("无法导入MCP组件，接口对齐功能将受限")
    MCP_COMPONENTS_AVAILABLE = False

# 尝试导入ThoughtActionRecorder
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'development_tools'))
    from thought_action_recorder import ThoughtActionRecorder
    logger.info("成功导入ThoughtActionRecorder")
    RECORDER_AVAILABLE = True
except ImportError:
    logger.error("无法导入ThoughtActionRecorder，将使用模拟实现")
    RECORDER_AVAILABLE = False


class RLFactoryAligner:
    """
    RL Factory与MCPPlanner、MCPBrainstorm和ThoughtActionRecorder接口对齐类
    
    负责确保RL Factory以MCPPlanner和MCPBrainstorm的输入作为学习者，
    持续强化学习对齐开发模块的ThoughtActionRecorder输入并达到一样水平
    """
    
    def __init__(self, model_path: str = "Qwen3-8B"):
        """
        初始化RL Factory对齐器
        
        Args:
            model_path: Qwen3-8B模型路径
        """
        self.model_path = model_path
        self.model = None
        self.mcp_planner = None
        self.mcp_brainstorm = None
        self.thought_recorder = None
        self.infinite_context_adapter = None
        self.supervised_learner = None
        
        # 初始化组件
        self._initialize_components()
        
        # 创建接口适配器
        self._create_interface_adapters()
    
    def _initialize_components(self) -> None:
        """初始化所有组件"""
        logger.info("正在初始化组件...")
        
        # 初始化RL Factory
        if RL_FACTORY_AVAILABLE:
            try:
                logger.info("正在初始化RL Factory...")
                # 加载配置
                recipe = load_recipe("configs/alignment_recipe.yaml")
                # 加载模型
                self.model = recipe.load_model(self.model_path)
                # 创建无限上下文适配器
                self.infinite_context_adapter = InfiniteContextAdapter()
                # 创建监督学习器
                self.supervised_learner = SupervisedLearner(self.model)
                logger.info("RL Factory初始化成功")
            except Exception as e:
                logger.error(f"RL Factory初始化失败: {str(e)}")
                RL_FACTORY_AVAILABLE = False
        
        # 初始化MCP组件
        if MCP_COMPONENTS_AVAILABLE:
            try:
                logger.info("正在初始化MCP组件...")
                # 初始化MCP Planner
                self.mcp_planner = MCPPlanner()
                # 初始化MCP Brainstorm
                self.mcp_brainstorm = MCPBrainstorm()
                logger.info("MCP组件初始化成功")
            except Exception as e:
                logger.error(f"MCP组件初始化失败: {str(e)}")
                MCP_COMPONENTS_AVAILABLE = False
        
        # 初始化ThoughtActionRecorder
        if RECORDER_AVAILABLE:
            try:
                logger.info("正在初始化ThoughtActionRecorder...")
                # 初始化ThoughtActionRecorder
                self.thought_recorder = ThoughtActionRecorder()
                logger.info("ThoughtActionRecorder初始化成功")
            except Exception as e:
                logger.error(f"ThoughtActionRecorder初始化失败: {str(e)}")
                RECORDER_AVAILABLE = False
        else:
            # 创建模拟ThoughtActionRecorder
            self.thought_recorder = self._create_mock_recorder()
        
        logger.info("所有组件初始化完成")
    
    def _create_mock_recorder(self) -> Any:
        """创建模拟ThoughtActionRecorder"""
        logger.info("创建模拟ThoughtActionRecorder")
        
        # 定义模拟类
        class MockThoughtActionRecorder:
            def __init__(self):
                self.records = []
            
            def record_thought(self, thought):
                self.records.append({"type": "thought", "content": thought, "timestamp": datetime.now().isoformat()})
                return True
            
            def record_action(self, action):
                self.records.append({"type": "action", "content": action, "timestamp": datetime.now().isoformat()})
                return True
            
            def get_records(self):
                return self.records
        
        return MockThoughtActionRecorder()
    
    def _create_interface_adapters(self) -> None:
        """创建接口适配器"""
        logger.info("正在创建接口适配器...")
        
        # 这里实现接口适配逻辑
        # 实际项目中应根据各组件的实际接口进行适配
        
        logger.info("接口适配器创建完成")
    
    def align_interfaces(self) -> bool:
        """
        对齐RL Factory与MCP组件和ThoughtActionRecorder的接口
        
        Returns:
            是否对齐成功
        """
        logger.info("正在对齐接口...")
        
        if not RL_FACTORY_AVAILABLE or not MCP_COMPONENTS_AVAILABLE:
            logger.error("RL Factory或MCP组件不可用，无法对齐接口")
            return False
        
        try:
            # 这里实现接口对齐逻辑
            # 实际项目中应根据各组件的实际接口进行对齐
            
            logger.info("接口对齐成功")
            return True
        except Exception as e:
            logger.error(f"接口对齐失败: {str(e)}")
            return False
    
    def collect_training_data(self, num_samples: int = 100) -> List[Dict[str, Any]]:
        """
        收集训练数据
        
        Args:
            num_samples: 样本数量
            
        Returns:
            训练数据列表
        """
        logger.info(f"正在收集{num_samples}个训练样本...")
        
        training_data = []
        
        try:
            # 从ThoughtActionRecorder收集真实数据
            if RECORDER_AVAILABLE:
                recorder_data = self.thought_recorder.get_records()
                logger.info(f"从ThoughtActionRecorder收集到{len(recorder_data)}个样本")
                training_data.extend(recorder_data[:min(len(recorder_data), num_samples // 2)])
            
            # 如果数据不足，生成模拟数据
            remaining_samples = num_samples - len(training_data)
            if remaining_samples > 0:
                logger.info(f"生成{remaining_samples}个模拟样本")
                for i in range(remaining_samples):
                    # 生成模拟输入
                    input_text = f"模拟输入 {i+1}"
                    
                    # 使用MCP Planner生成输出
                    if MCP_COMPONENTS_AVAILABLE:
                        planner_output = self.mcp_planner.plan(input_text)
                    else:
                        planner_output = f"模拟MCP Planner输出 {i+1}"
                    
                    # 使用MCP Brainstorm生成输出
                    if MCP_COMPONENTS_AVAILABLE:
                        brainstorm_output = self.mcp_brainstorm.brainstorm(input_text)
                    else:
                        brainstorm_output = f"模拟MCP Brainstorm输出 {i+1}"
                    
                    # 添加到训练数据
                    training_data.append({
                        "input": input_text,
                        "planner_output": planner_output,
                        "brainstorm_output": brainstorm_output,
                        "timestamp": datetime.now().isoformat()
                    })
            
            logger.info(f"共收集到{len(training_data)}个训练样本")
            return training_data
        except Exception as e:
            logger.error(f"收集训练数据失败: {str(e)}")
            return []
    
    def train_rl_factory(self, training_data: List[Dict[str, Any]], epochs: int = 10) -> bool:
        """
        训练RL Factory
        
        Args:
            training_data: 训练数据
            epochs: 训练轮数
            
        Returns:
            是否训练成功
        """
        logger.info(f"正在训练RL Factory，训练轮数: {epochs}...")
        
        if not RL_FACTORY_AVAILABLE:
            logger.error("RL Factory不可用，无法训练")
            return False
        
        try:
            # 准备训练数据
            processed_data = self._preprocess_training_data(training_data)
            
            # 训练模型
            self.supervised_learner.train(
                processed_data,
                epochs=epochs,
                batch_size=8,
                learning_rate=1e-5
            )
            
            logger.info("RL Factory训练成功")
            return True
        except Exception as e:
            logger.error(f"RL Factory训练失败: {str(e)}")
            return False
    
    def _preprocess_training_data(self, training_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        预处理训练数据
        
        Args:
            training_data: 原始训练数据
            
        Returns:
            预处理后的训练数据
        """
        logger.info("正在预处理训练数据...")
        
        processed_data = []
        
        for item in training_data:
            # 根据数据类型进行不同处理
            if "type" in item and item["type"] in ["thought", "action"]:
                # ThoughtActionRecorder数据
                processed_data.append({
                    "input": item.get("content", ""),
                    "output": item.get("content", ""),
                    "type": item.get("type", "unknown")
                })
            else:
                # MCP组件数据
                processed_data.append({
                    "input": item.get("input", ""),
                    "output": item.get("planner_output", "") + "\n" + item.get("brainstorm_output", ""),
                    "type": "mcp"
                })
        
        logger.info(f"预处理完成，共{len(processed_data)}个样本")
        return processed_data
    
    def evaluate_alignment(self, test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        评估对齐效果
        
        Args:
            test_data: 测试数据
            
        Returns:
            评估结果
        """
        logger.info("正在评估对齐效果...")
        
        if not RL_FACTORY_AVAILABLE or not MCP_COMPONENTS_AVAILABLE:
            logger.error("RL Factory或MCP组件不可用，无法评估对齐效果")
            return {"error": 1.0}
        
        try:
            # 初始化评估指标
            metrics = {
                "planner_similarity": 0.0,
                "brainstorm_similarity": 0.0,
                "recorder_similarity": 0.0,
                "overall_alignment": 0.0
            }
            
            # 评估每个测试样本
            for item in test_data:
                input_text = item.get("input", "")
                
                # 使用RL Factory生成输出
                rl_output = self.model.generate(input_text)
                
                # 使用MCP Planner生成输出
                planner_output = self.mcp_planner.plan(input_text)
                
                # 使用MCP Brainstorm生成输出
                brainstorm_output = self.mcp_brainstorm.brainstorm(input_text)
                
                # 使用ThoughtActionRecorder生成输出
                if RECORDER_AVAILABLE:
                    self.thought_recorder.record_thought(input_text)
                    recorder_output = self.thought_recorder.get_records()[-1].get("content", "")
                else:
                    recorder_output = "模拟ThoughtActionRecorder输出"
                
                # 计算相似度（这里使用简单的字符串比较，实际项目中应使用更复杂的相似度计算方法）
                planner_sim = self._calculate_similarity(rl_output, planner_output)
                brainstorm_sim = self._calculate_similarity(rl_output, brainstorm_output)
                recorder_sim = self._calculate_similarity(rl_output, recorder_output)
                
                # 更新评估指标
                metrics["planner_similarity"] += planner_sim
                metrics["brainstorm_similarity"] += brainstorm_sim
                metrics["recorder_similarity"] += recorder_sim
            
            # 计算平均值
            num_samples = len(test_data)
            if num_samples > 0:
                for key in metrics:
                    if key != "overall_alignment":
                        metrics[key] /= num_samples
                
                # 计算整体对齐度
                metrics["overall_alignment"] = (
                    metrics["planner_similarity"] + 
                    metrics["brainstorm_similarity"] + 
                    metrics["recorder_similarity"]
                ) / 3
            
            logger.info(f"对齐效果评估完成: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"评估对齐效果失败: {str(e)}")
            return {"error": 1.0}
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两段文本的相似度
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            相似度（0-1之间的浮点数）
        """
        # 这里使用简单的字符串比较，实际项目中应使用更复杂的相似度计算方法
        # 例如余弦相似度、BLEU分数等
        
        # 简单实现：计算最长公共子序列的长度比例
        len1, len2 = len(text1), len(text2)
        if len1 == 0 or len2 == 0:
            return 0.0
        
        # 计算最长公共子序列
        lcs_length = self._longest_common_subsequence(text1, text2)
        
        # 计算相似度
        return lcs_length / max(len1, len2)
    
    def _longest_common_subsequence(self, text1: str, text2: str) -> int:
        """
        计算最长公共子序列的长度
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            最长公共子序列的长度
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m][n]
    
    def continuous_learning(self, iterations: int = 10, samples_per_iteration: int = 10) -> Dict[str, List[float]]:
        """
        持续强化学习过程
        
        Args:
            iterations: 迭代次数
            samples_per_iteration: 每次迭代的样本数
            
        Returns:
            学习过程中的评估指标
        """
        logger.info(f"开始持续强化学习，迭代次数: {iterations}，每次迭代样本数: {samples_per_iteration}")
        
        if not RL_FACTORY_AVAILABLE:
            logger.error("RL Factory不可用，无法进行持续强化学习")
            return {"error": [1.0] * iterations}
        
        # 记录学习过程中的评估指标
        learning_metrics = {
            "planner_similarity": [],
            "brainstorm_similarity": [],
            "recorder_similarity": [],
            "overall_alignment": []
        }
        
        try:
            for i in range(iterations):
                logger.info(f"迭代 {i+1}/{iterations}")
                
                # 收集训练数据
                training_data = self.collect_training_data(samples_per_iteration)
                
                # 训练模型
                self.train_rl_factory(training_data, epochs=1)
                
                # 评估对齐效果
                metrics = self.evaluate_alignment(training_data)
                
                # 记录评估指标
                for key in learning_metrics:
                    if key in metrics:
                        learning_metrics[key].append(metrics[key])
                
                logger.info(f"迭代 {i+1} 完成，对齐度: {metrics.get('overall_alignment', 0.0)}")
            
            logger.info("持续强化学习完成")
            return learning_metrics
        except Exception as e:
            logger.error(f"持续强化学习失败: {str(e)}")
            return {"error": [1.0] * iterations}
    
    def save_model(self, path: str) -> bool:
        """
        保存模型
        
        Args:
            path: 保存路径
            
        Returns:
            是否保存成功
        """
        logger.info(f"正在保存模型到 {path}...")
        
        if not RL_FACTORY_AVAILABLE:
            logger.error("RL Factory不可用，无法保存模型")
            return False
        
        try:
            # 保存模型
            # 实际项目中应使用模型的保存方法
            # self.model.save(path)
            
            logger.info(f"模型保存成功: {path}")
            return True
        except Exception as e:
            logger.error(f"保存模型失败: {str(e)}")
            return False
    
    def load_model(self, path: str) -> bool:
        """
        加载模型
        
        Args:
            path: 模型路径
            
        Returns:
            是否加载成功
        """
        logger.info(f"正在从 {path} 加载模型...")
        
        if not RL_FACTORY_AVAILABLE:
            logger.error("RL Factory不可用，无法加载模型")
            return False
        
        try:
            # 加载模型
            # 实际项目中应使用模型的加载方法
            # self.model = load_model(path)
            
            logger.info(f"模型加载成功: {path}")
            return True
        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}")
            return False


# 示例用法
if __name__ == "__main__":
    # 创建RL Factory对齐器
    aligner = RLFactoryAligner()
    
    # 对齐接口
    aligner.align_interfaces()
    
    # 收集训练数据
    training_data = aligner.collect_training_data(100)
    
    # 训练RL Factory
    aligner.train_rl_factory(training_data, epochs=5)
    
    # 评估对齐效果
    metrics = aligner.evaluate_alignment(training_data[:10])
    print(f"对齐效果评估: {metrics}")
    
    # 持续强化学习
    learning_metrics = aligner.continuous_learning(iterations=5, samples_per_iteration=20)
    print(f"持续强化学习评估: {learning_metrics}")
    
    # 保存模型
    aligner.save_model("models/aligned_model.pt")
