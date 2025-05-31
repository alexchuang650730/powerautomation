"""
混合学习架构，结合监督学习、强化学习和对比学习
"""
import os
import json
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
import torch
import torch.nn as nn
import torch.optim as optim

from powerautomation_integration.rl_core.core.learning.supervised import SupervisedLearner
from powerautomation_integration.rl_core.core.learning.reinforcement import ReinforcementLearner
from powerautomation_integration.rl_core.core.learning.contrastive import ContrastiveLearner


class HybridLearningArchitecture:
    """混合学习架构类"""
    
    def __init__(self, model_name: str = "bert-base-uncased", device: str = None):
        """
        初始化混合学习架构
        
        Args:
            model_name: 模型名称
            device: 设备（CPU或GPU）
        """
        # 设置设备
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # 创建学习器
        self.supervised_learner = SupervisedLearner(model_name, device=self.device)
        self.reinforcement_learner = ReinforcementLearner(model_name, device=self.device)
        self.contrastive_learner = ContrastiveLearner(model_name, device=self.device)
    
    def train(self, training_data: List[Dict[str, Any]], epochs: int = 3) -> Dict[str, Any]:
        """
        训练模型
        
        Args:
            training_data: 训练数据
            epochs: 训练轮数
            
        Returns:
            训练结果
        """
        # 提取思考过程
        thought_processes = []
        for item in training_data:
            input_data = item["input"]
            output_data = item["output"]
            
            # 如果输入是字典，提取思考过程
            if isinstance(input_data, dict):
                thought_process = input_data
            else:
                # 否则，创建简单的思考过程
                thought_process = {
                    "task": input_data,
                    "thinking": "思考过程",
                    "steps": ["步骤1", "步骤2", "步骤3"]
                }
            
            # 添加质量评分
            thought_process["overall_quality"] = 0.8
            
            thought_processes.append(thought_process)
        
        # 监督学习
        supervised_result = self.supervised_learner.train(thought_processes, epochs=epochs)
        
        # 强化学习
        reinforcement_result = self.reinforcement_learner.train(thought_processes, epochs=epochs)
        
        # 对比学习
        contrastive_result = self.contrastive_learner.train(thought_processes, epochs=epochs)
        
        return {
            "supervised_result": supervised_result,
            "reinforcement_result": reinforcement_result,
            "contrastive_result": contrastive_result
        }
    
    def predict(self, thought_process: Dict[str, Any]) -> Dict[str, Any]:
        """
        预测思考过程的质量
        
        Args:
            thought_process: 思考过程
            
        Returns:
            预测结果
        """
        # 监督学习预测
        supervised_quality = self.supervised_learner.predict(thought_process)
        
        # 强化学习预测
        reinforcement_quality = self.reinforcement_learner.predict(thought_process)
        
        # 对比学习预测
        contrastive_quality = self.contrastive_learner.predict(thought_process)
        
        # 综合评分
        overall_quality = (supervised_quality + reinforcement_quality + contrastive_quality) / 3
        
        return {
            "supervised_quality": supervised_quality,
            "reinforcement_quality": reinforcement_quality,
            "contrastive_quality": contrastive_quality,
            "overall_quality": overall_quality
        }
    
    def save(self, path: str):
        """
        保存模型
        
        Args:
            path: 保存路径
        """
        # 创建目录
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 保存各个学习器
        supervised_path = f"{path}_supervised"
        reinforcement_path = f"{path}_reinforcement"
        contrastive_path = f"{path}_contrastive"
        
        self.supervised_learner.save(supervised_path)
        self.reinforcement_learner.save(reinforcement_path)
        self.contrastive_learner.save(contrastive_path)
    
    def load(self, path: str):
        """
        加载模型
        
        Args:
            path: 加载路径
        """
        # 加载各个学习器
        supervised_path = f"{path}_supervised"
        reinforcement_path = f"{path}_reinforcement"
        contrastive_path = f"{path}_contrastive"
        
        self.supervised_learner.load(supervised_path)
        self.reinforcement_learner.load(reinforcement_path)
        self.contrastive_learner.load(contrastive_path)
