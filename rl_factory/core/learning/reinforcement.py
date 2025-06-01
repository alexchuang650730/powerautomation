"""
强化学习模块，基于奖励信号的强化学习
"""
import os
import json
import numpy as np
import random
from typing import Dict, List, Any, Optional, Union, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

from rl_factory.core.thought.schema import ThoughtProcess
from rl_factory.core.thought.serializer import ThoughtSerializer


class ThoughtPolicyNetwork(nn.Module):
    """思考过程策略网络"""
    
    def __init__(self, input_size: int, hidden_size: int = 128, output_size: int = 4):
        """
        初始化思考过程策略网络
        
        Args:
            input_size: 输入特征维度
            hidden_size: 隐藏层大小
            output_size: 输出动作空间大小（对应思考阶段数量）
        """
        super(ThoughtPolicyNetwork, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
            nn.Softmax(dim=-1)
        )
    
    def forward(self, x):
        """前向传播"""
        return self.network(x)


class ThoughtValueNetwork(nn.Module):
    """思考过程价值网络"""
    
    def __init__(self, input_size: int, hidden_size: int = 128):
        """
        初始化思考过程价值网络
        
        Args:
            input_size: 输入特征维度
            hidden_size: 隐藏层大小
        """
        super(ThoughtValueNetwork, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, x):
        """前向传播"""
        return self.network(x)


class ThoughtFeatureExtractor:
    """思考过程特征提取器"""
    
    def __init__(self, tokenizer, max_length: int = 512):
        """
        初始化特征提取器
        
        Args:
            tokenizer: 分词器
            max_length: 最大序列长度
        """
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def extract_features(self, thought_process: ThoughtProcess) -> torch.Tensor:
        """
        提取思考过程特征
        
        Args:
            thought_process: 思考过程
            
        Returns:
            特征向量
        """
        # 将思考过程序列化为文本
        text = ThoughtSerializer.to_markdown(thought_process)
        
        # 分词
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 使用预训练模型提取特征
        from transformers import AutoModel
        model = AutoModel.from_pretrained(self.tokenizer.name_or_path)
        with torch.no_grad():
            outputs = model(**encoding)
            
        # 使用[CLS]标记的表示作为特征
        features = outputs.last_hidden_state[:, 0, :]
        
        return features.squeeze()


class RewardCalculator:
    """奖励计算器"""
    
    def __init__(self):
        """初始化奖励计算器"""
        pass
    
    def calculate_local_reward(self, thought_stage: Dict[str, Any]) -> float:
        """
        计算单个思考阶段的局部奖励
        
        Args:
            thought_stage: 思考阶段
            
        Returns:
            局部奖励值
        """
        reward = 0.0
        
        # 根据阶段类型计算奖励
        stage_type = thought_stage.get("stage_type", "")
        
        if stage_type == "problem_analysis":
            # 问题分析阶段奖励
            if "problem_statement" in thought_stage and len(thought_stage["problem_statement"]) > 50:
                reward += 0.5
            
            if "key_constraints" in thought_stage:
                reward += min(0.1 * len(thought_stage["key_constraints"]), 0.5)
                
            if "identified_challenges" in thought_stage:
                reward += min(0.1 * len(thought_stage["identified_challenges"]), 0.5)
        
        elif stage_type == "solution_design":
            # 方案设计阶段奖励
            if "design_principles" in thought_stage:
                reward += min(0.1 * len(thought_stage["design_principles"]), 0.3)
                
            if "alternative_approaches" in thought_stage:
                reward += min(0.1 * len(thought_stage["alternative_approaches"]), 0.3)
                
            if "selected_approach" in thought_stage and "rationale" in thought_stage["selected_approach"]:
                reward += 0.4
                
            if "design_rationale" in thought_stage and len(thought_stage["design_rationale"]) > 100:
                reward += 0.5
        
        elif stage_type == "implementation_planning":
            # 实现规划阶段奖励
            if "implementation_steps" in thought_stage:
                steps = thought_stage["implementation_steps"]
                reward += min(0.1 * len(steps), 0.5)
                
                # 检查步骤是否有序且详细
                ordered = all(i+1 == step.get("step_number", 0) for i, step in enumerate(steps))
                detailed = all(len(step.get("description", "")) > 20 for step in steps)
                
                if ordered:
                    reward += 0.3
                if detailed:
                    reward += 0.3
                
            if "potential_risks" in thought_stage:
                reward += min(0.1 * len(thought_stage["potential_risks"]), 0.4)
        
        elif stage_type == "validation_evaluation":
            # 验证评估阶段奖励
            if "validation_criteria" in thought_stage:
                reward += min(0.1 * len(thought_stage["validation_criteria"]), 0.4)
                
            if "test_cases" in thought_stage:
                reward += min(0.1 * len(thought_stage["test_cases"]), 0.4)
                
            if "improvement_suggestions" in thought_stage:
                reward += min(0.1 * len(thought_stage["improvement_suggestions"]), 0.3)
        
        # 通用质量奖励
        description_length = len(thought_stage.get("stage_description", ""))
        if description_length > 200:
            reward += 0.3
        elif description_length > 100:
            reward += 0.2
        elif description_length > 50:
            reward += 0.1
        
        return reward
    
    def calculate_global_reward(self, thought_process: ThoughtProcess) -> float:
        """
        计算整体思考过程的全局奖励
        
        Args:
            thought_process: 思考过程
            
        Returns:
            全局奖励值
        """
        reward = 0.0
        
        # 阶段完整性奖励
        stage_types = set(stage.stage_type for stage in thought_process.stages.values())
        expected_types = {"problem_analysis", "solution_design", "implementation_planning", "validation_evaluation"}
        
        completeness = len(stage_types.intersection(expected_types)) / len(expected_types)
        reward += completeness * 2.0
        
        # 阶段顺序奖励
        ordered_stages = sorted(thought_process.stages.values(), key=lambda s: s.stage_order)
        correct_order = all(ordered_stages[i].stage_order < ordered_stages[i+1].stage_order 
                           for i in range(len(ordered_stages)-1))
        
        if correct_order:
            reward += 1.0
        
        # 引用和参考奖励
        if thought_process.references:
            reward += min(0.1 * len(thought_process.references), 0.5)
        
        # 标签奖励
        if thought_process.tags:
            reward += min(0.05 * len(thought_process.tags), 0.3)
        
        return reward
    
    def calculate_delayed_reward(self, execution_result: Dict[str, Any]) -> float:
        """
        计算基于执行结果的延迟奖励
        
        Args:
            execution_result: 执行结果
            
        Returns:
            延迟奖励值
        """
        reward = 0.0
        
        # 执行成功奖励
        if execution_result.get("success", False):
            reward += 2.0
        
        # 执行效率奖励
        efficiency = execution_result.get("efficiency", 0.0)
        reward += efficiency * 1.5
        
        # 用户满意度奖励
        satisfaction = execution_result.get("user_satisfaction", 0.0)
        reward += satisfaction * 2.0
        
        return reward


class ReinforcementLearner:
    """基于强化学习的思考过程学习器"""
    
    def __init__(self, model_name: str = "bert-base-uncased", device: str = None):
        """
        初始化强化学习器
        
        Args:
            model_name: 模型名称
            device: 设备（CPU或GPU）
        """
        # 设置设备
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # 加载分词器
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # 特征提取器
        self.feature_extractor = ThoughtFeatureExtractor(self.tokenizer)
        
        # 特征维度
        self.feature_dim = 768  # BERT base hidden size
        
        # 创建策略网络和价值网络
        self.policy_net = ThoughtPolicyNetwork(self.feature_dim)
        self.value_net = ThoughtValueNetwork(self.feature_dim)
        
        self.policy_net.to(self.device)
        self.value_net.to(self.device)
        
        # 设置优化器
        self.policy_optimizer = optim.Adam(self.policy_net.parameters(), lr=1e-4)
        self.value_optimizer = optim.Adam(self.value_net.parameters(), lr=1e-4)
        
        # 奖励计算器
        self.reward_calculator = RewardCalculator()
        
        # 经验回放缓冲区
        self.replay_buffer = []
        
        # 折扣因子
        self.gamma = 0.99
        
    def select_action(self, state: torch.Tensor) -> int:
        """
        根据状态选择动作
        
        Args:
            state: 状态特征
            
        Returns:
            选择的动作
        """
        state = state.to(self.device)
        probs = self.policy_net(state)
        m = Categorical(probs)
        action = m.sample()
        
        return action.item(), m.log_prob(action)
    
    def update_policy(self, rewards, log_probs, values):
        """
        更新策略网络
        
        Args:
            rewards: 奖励列表
            log_probs: 动作对数概率列表
            values: 状态价值列表
        """
        # 计算优势函数
        advantages = []
        returns = []
        R = 0
        
        for r in reversed(rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        
        returns = torch.tensor(returns, device=self.device)
        values = torch.cat(values)
        
        advantages = returns - values.detach()
        
        # 策略损失
        policy_loss = []
        for log_prob, advantage in zip(log_probs, advantages):
            policy_loss.append(-log_prob * advantage)
        
        policy_loss = torch.cat(policy_loss).sum()
        
        # 价值损失
        value_loss = nn.MSELoss()(values, returns)
        
        # 更新策略网络
        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        self.policy_optimizer.step()
        
        # 更新价值网络
        self.value_optimizer.zero_grad()
        value_loss.backward()
        self.value_optimizer.step()
    
    def train_episode(self, thought_process: ThoughtProcess, execution_result: Dict[str, Any] = None):
        """
        训练一个回合
        
        Args:
            thought_process: 思考过程
            execution_result: 执行结果（可选）
        """
        # 提取特征
        state = self.feature_extractor.extract_features(thought_process)
        state = state.to(self.device)
        
        # 计算每个阶段的局部奖励
        local_rewards = []
        for stage in thought_process.stages.values():
            reward = self.reward_calculator.calculate_local_reward(stage.dict())
            local_rewards.append(reward)
        
        # 计算全局奖励
        global_reward = self.reward_calculator.calculate_global_reward(thought_process)
        
        # 计算延迟奖励（如果有执行结果）
        delayed_reward = 0.0
        if execution_result:
            delayed_reward = self.reward_calculator.calculate_delayed_reward(execution_result)
        
        # 组合奖励
        rewards = local_rewards
        rewards[-1] += global_reward + delayed_reward
        
        # 记录动作、奖励和状态值
        log_probs = []
        values = []
        
        # 模拟动作选择（实际应用中应该是真实的动作选择）
        for i in range(len(thought_process.stages)):
            action, log_prob = self.select_action(state)
            value = self.value_net(state)
            
            log_probs.append(log_prob)
            values.append(value)
        
        # 更新策略
        self.update_policy(rewards, log_probs, values)
    
    def train(self, thought_processes: List[Tuple[ThoughtProcess, Dict[str, Any]]], epochs: int = 5):
        """
        训练模型
        
        Args:
            thought_processes: 思考过程和执行结果的元组列表
            epochs: 训练轮数
        """
        for epoch in range(epochs):
            total_reward = 0
            
            for thought_process, execution_result in thought_processes:
                # 训练一个回合
                self.train_episode(thought_process, execution_result)
                
                # 计算总奖励
                local_rewards = [self.reward_calculator.calculate_local_reward(stage.dict()) 
                                for stage in thought_process.stages.values()]
                global_reward = self.reward_calculator.calculate_global_reward(thought_process)
                delayed_reward = 0.0
                if execution_result:
                    delayed_reward = self.reward_calculator.calculate_delayed_reward(execution_result)
                
                episode_reward = sum(local_rewards) + global_reward + delayed_reward
                total_reward += episode_reward
            
            # 打印训练信息
            print(f"Epoch {epoch+1}/{epochs}, Average Reward: {total_reward/len(thought_processes):.4f}")
    
    def save(self, path: str):
        """
        保存模型
        
        Args:
            path: 保存路径
        """
        # 创建目录
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 保存模型
        torch.save({
            "policy_state_dict": self.policy_net.state_dict(),
            "value_state_dict": self.value_net.state_dict(),
            "policy_optimizer_state_dict": self.policy_optimizer.state_dict(),
            "value_optimizer_state_dict": self.value_optimizer.state_dict()
        }, path)
    
    def load(self, path: str):
        """
        加载模型
        
        Args:
            path: 加载路径
        """
        # 加载模型
        checkpoint = torch.load(path, map_location=self.device)
        self.policy_net.load_state_dict(checkpoint["policy_state_dict"])
        self.value_net.load_state_dict(checkpoint["value_state_dict"])
        self.policy_optimizer.load_state_dict(checkpoint["policy_optimizer_state_dict"])
        self.value_optimizer.load_state_dict(checkpoint["value_optimizer_state_dict"])


if __name__ == "__main__":
    # 示例用法
    from rl_factory.core.thought.decomposer import ThoughtDecomposer
    
    # 创建示例思考过程
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
    
    # 模拟执行结果
    execution_result = {
        "success": True,
        "efficiency": 0.85,
        "user_satisfaction": 0.9
    }
    
    # 创建强化学习器
    learner = ReinforcementLearner(model_name="bert-base-uncased")
    
    # 训练模型（实际应用中需要更多数据）
    learner.train([(thought_process, execution_result)], epochs=2)
    
    # 保存模型
    learner.save("models/rl_model.pt")
