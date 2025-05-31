"""
监督学习模块，基于历史数据的监督学习
"""
import os
import json
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from rl_factory.core.thought.schema import ThoughtProcess
from rl_factory.core.thought.serializer import ThoughtSerializer


class ThoughtDataset(Dataset):
    """思考过程数据集"""
    
    def __init__(self, thought_processes: List[ThoughtProcess], tokenizer, max_length: int = 512):
        """
        初始化思考过程数据集
        
        Args:
            thought_processes: 思考过程列表
            tokenizer: 分词器
            max_length: 最大序列长度
        """
        self.thought_processes = thought_processes
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.thought_processes)
    
    def __getitem__(self, idx):
        thought = self.thought_processes[idx]
        
        # 将思考过程序列化为文本
        text = ThoughtSerializer.to_markdown(thought)
        
        # 分词
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 提取特征和标签
        input_ids = encoding["input_ids"].squeeze()
        attention_mask = encoding["attention_mask"].squeeze()
        
        # 使用整体质量评分作为标签
        label = torch.tensor(thought.overall_quality, dtype=torch.float)
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": label
        }


class ThoughtEncoder(nn.Module):
    """思考过程编码器"""
    
    def __init__(self, base_model_name: str, hidden_size: int = 768):
        """
        初始化思考过程编码器
        
        Args:
            base_model_name: 基础模型名称
            hidden_size: 隐藏层大小
        """
        super(ThoughtEncoder, self).__init__()
        
        # 加载预训练模型
        from transformers import AutoModel
        self.encoder = AutoModel.from_pretrained(base_model_name)
        
        # 输出层
        self.output_layer = nn.Linear(hidden_size, 1)
        
    def forward(self, input_ids, attention_mask):
        """前向传播"""
        # 编码输入
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        
        # 获取[CLS]标记的表示
        cls_output = outputs.last_hidden_state[:, 0, :]
        
        # 输出质量评分
        quality_score = self.output_layer(cls_output)
        
        return quality_score


class SupervisedLearner:
    """基于监督学习的思考过程学习器"""
    
    def __init__(self, model_name: str = "bert-base-uncased", device: str = None):
        """
        初始化监督学习器
        
        Args:
            model_name: 模型名称
            device: 设备（CPU或GPU）
        """
        # 设置设备
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # 加载分词器
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # 创建模型
        self.model = ThoughtEncoder(model_name)
        self.model.to(self.device)
        
        # 设置优化器和损失函数
        self.optimizer = optim.Adam(self.model.parameters(), lr=2e-5)
        self.criterion = nn.MSELoss()
        
    def train(self, thought_processes: List[ThoughtProcess], batch_size: int = 8, epochs: int = 3):
        """
        训练模型
        
        Args:
            thought_processes: 思考过程列表
            batch_size: 批次大小
            epochs: 训练轮数
        """
        # 创建数据集和数据加载器
        dataset = ThoughtDataset(thought_processes, self.tokenizer)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # 训练模型
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            
            for batch in dataloader:
                # 将数据移动到设备
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                labels = batch["labels"].to(self.device)
                
                # 前向传播
                self.optimizer.zero_grad()
                outputs = self.model(input_ids, attention_mask)
                
                # 计算损失
                loss = self.criterion(outputs.squeeze(), labels)
                
                # 反向传播
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
            
            # 打印训练信息
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
    
    def evaluate(self, thought_processes: List[ThoughtProcess], batch_size: int = 8):
        """
        评估模型
        
        Args:
            thought_processes: 思考过程列表
            batch_size: 批次大小
            
        Returns:
            评估结果
        """
        # 创建数据集和数据加载器
        dataset = ThoughtDataset(thought_processes, self.tokenizer)
        dataloader = DataLoader(dataset, batch_size=batch_size)
        
        # 评估模型
        self.model.eval()
        total_loss = 0
        predictions = []
        actuals = []
        
        with torch.no_grad():
            for batch in dataloader:
                # 将数据移动到设备
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                labels = batch["labels"].to(self.device)
                
                # 前向传播
                outputs = self.model(input_ids, attention_mask)
                
                # 计算损失
                loss = self.criterion(outputs.squeeze(), labels)
                total_loss += loss.item()
                
                # 收集预测和实际值
                predictions.extend(outputs.squeeze().cpu().numpy())
                actuals.extend(labels.cpu().numpy())
        
        # 计算评估指标
        mse = np.mean((np.array(predictions) - np.array(actuals)) ** 2)
        mae = np.mean(np.abs(np.array(predictions) - np.array(actuals)))
        
        return {
            "loss": total_loss / len(dataloader),
            "mse": mse,
            "mae": mae
        }
    
    def predict(self, thought_process: ThoughtProcess) -> float:
        """
        预测思考过程的质量
        
        Args:
            thought_process: 思考过程
            
        Returns:
            质量评分
        """
        # 将思考过程序列化为文本
        text = ThoughtSerializer.to_markdown(thought_process)
        
        # 分词
        encoding = self.tokenizer(
            text,
            max_length=512,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 将数据移动到设备
        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)
        
        # 预测
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_ids, attention_mask)
        
        return output.item()
    
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
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict()
        }, path)
    
    def load(self, path: str):
        """
        加载模型
        
        Args:
            path: 加载路径
        """
        # 加载模型
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])


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
    thought_process.overall_quality = 0.85  # 设置质量评分
    
    # 创建监督学习器
    learner = SupervisedLearner(model_name="bert-base-uncased")
    
    # 训练模型（实际应用中需要更多数据）
    learner.train([thought_process], batch_size=1, epochs=1)
    
    # 评估模型
    eval_result = learner.evaluate([thought_process])
    print(f"Evaluation result: {eval_result}")
    
    # 预测质量
    quality = learner.predict(thought_process)
    print(f"Predicted quality: {quality:.4f}")
