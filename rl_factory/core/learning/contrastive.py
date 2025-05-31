"""
对比学习模块，基于对比学习的思考过程学习
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


class ContrastiveThoughtDataset(Dataset):
    """对比学习思考过程数据集"""
    
    def __init__(self, positive_pairs: List[Tuple[ThoughtProcess, ThoughtProcess]], 
                 negative_pairs: List[Tuple[ThoughtProcess, ThoughtProcess]],
                 tokenizer, max_length: int = 512):
        """
        初始化对比学习数据集
        
        Args:
            positive_pairs: 正样本对列表（高质量思考过程对）
            negative_pairs: 负样本对列表（高质量与低质量思考过程对）
            tokenizer: 分词器
            max_length: 最大序列长度
        """
        self.positive_pairs = positive_pairs
        self.negative_pairs = negative_pairs
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # 合并所有样本对
        self.pairs = []
        self.labels = []
        
        for pos_pair in positive_pairs:
            self.pairs.append(pos_pair)
            self.labels.append(1)  # 正样本标签为1
            
        for neg_pair in negative_pairs:
            self.pairs.append(neg_pair)
            self.labels.append(0)  # 负样本标签为0
    
    def __len__(self):
        return len(self.pairs)
    
    def __getitem__(self, idx):
        thought1, thought2 = self.pairs[idx]
        label = self.labels[idx]
        
        # 将思考过程序列化为文本
        text1 = ThoughtSerializer.to_markdown(thought1)
        text2 = ThoughtSerializer.to_markdown(thought2)
        
        # 分词
        encoding1 = self.tokenizer(
            text1,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        encoding2 = self.tokenizer(
            text2,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        # 提取特征
        input_ids1 = encoding1["input_ids"].squeeze()
        attention_mask1 = encoding1["attention_mask"].squeeze()
        
        input_ids2 = encoding2["input_ids"].squeeze()
        attention_mask2 = encoding2["attention_mask"].squeeze()
        
        return {
            "input_ids1": input_ids1,
            "attention_mask1": attention_mask1,
            "input_ids2": input_ids2,
            "attention_mask2": attention_mask2,
            "label": torch.tensor(label, dtype=torch.float)
        }


class ThoughtEncoder(nn.Module):
    """思考过程编码器"""
    
    def __init__(self, base_model_name: str, hidden_size: int = 768, projection_size: int = 128):
        """
        初始化思考过程编码器
        
        Args:
            base_model_name: 基础模型名称
            hidden_size: 隐藏层大小
            projection_size: 投影层大小
        """
        super(ThoughtEncoder, self).__init__()
        
        # 加载预训练模型
        from transformers import AutoModel
        self.encoder = AutoModel.from_pretrained(base_model_name)
        
        # 投影层
        self.projection = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, projection_size)
        )
        
    def forward(self, input_ids, attention_mask):
        """前向传播"""
        # 编码输入
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        
        # 获取[CLS]标记的表示
        cls_output = outputs.last_hidden_state[:, 0, :]
        
        # 投影到低维空间
        projection = self.projection(cls_output)
        
        # 归一化
        projection = nn.functional.normalize(projection, p=2, dim=1)
        
        return projection


class ContrastiveLoss(nn.Module):
    """对比损失函数"""
    
    def __init__(self, temperature: float = 0.5):
        """
        初始化对比损失函数
        
        Args:
            temperature: 温度参数
        """
        super(ContrastiveLoss, self).__init__()
        self.temperature = temperature
        self.similarity = nn.CosineSimilarity(dim=-1)
        self.criterion = nn.BCEWithLogitsLoss()
        
    def forward(self, z1, z2, labels):
        """
        计算对比损失
        
        Args:
            z1: 第一个样本的表示
            z2: 第二个样本的表示
            labels: 标签（1表示正样本对，0表示负样本对）
            
        Returns:
            损失值
        """
        # 计算余弦相似度
        sim = self.similarity(z1, z2) / self.temperature
        
        # 计算损失
        loss = self.criterion(sim, labels)
        
        return loss


class ContrastiveLearner:
    """基于对比学习的思考过程学习器"""
    
    def __init__(self, model_name: str = "bert-base-uncased", device: str = None):
        """
        初始化对比学习器
        
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
        
        # 设置损失函数和优化器
        self.criterion = ContrastiveLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=2e-5)
        
    def train(self, positive_pairs: List[Tuple[ThoughtProcess, ThoughtProcess]], 
              negative_pairs: List[Tuple[ThoughtProcess, ThoughtProcess]],
              batch_size: int = 8, epochs: int = 3):
        """
        训练模型
        
        Args:
            positive_pairs: 正样本对列表（高质量思考过程对）
            negative_pairs: 负样本对列表（高质量与低质量思考过程对）
            batch_size: 批次大小
            epochs: 训练轮数
        """
        # 创建数据集和数据加载器
        dataset = ContrastiveThoughtDataset(positive_pairs, negative_pairs, self.tokenizer)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # 训练模型
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            
            for batch in dataloader:
                # 将数据移动到设备
                input_ids1 = batch["input_ids1"].to(self.device)
                attention_mask1 = batch["attention_mask1"].to(self.device)
                input_ids2 = batch["input_ids2"].to(self.device)
                attention_mask2 = batch["attention_mask2"].to(self.device)
                labels = batch["label"].to(self.device)
                
                # 前向传播
                self.optimizer.zero_grad()
                z1 = self.model(input_ids1, attention_mask1)
                z2 = self.model(input_ids2, attention_mask2)
                
                # 计算损失
                loss = self.criterion(z1, z2, labels)
                
                # 反向传播
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
            
            # 打印训练信息
            print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
    
    def encode(self, thought_process: ThoughtProcess) -> torch.Tensor:
        """
        编码思考过程
        
        Args:
            thought_process: 思考过程
            
        Returns:
            编码向量
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
        
        # 编码
        self.model.eval()
        with torch.no_grad():
            encoding = self.model(input_ids, attention_mask)
        
        return encoding.cpu()
    
    def similarity(self, thought1: ThoughtProcess, thought2: ThoughtProcess) -> float:
        """
        计算两个思考过程的相似度
        
        Args:
            thought1: 第一个思考过程
            thought2: 第二个思考过程
            
        Returns:
            相似度值
        """
        # 编码思考过程
        z1 = self.encode(thought1)
        z2 = self.encode(thought2)
        
        # 计算余弦相似度
        similarity = nn.functional.cosine_similarity(z1, z2).item()
        
        return similarity
    
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
    raw_thought_high_quality = """设计一个在线教育平台
    
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
    
    raw_thought_low_quality = """设计在线教育平台
    
    问题:
    需要一个在线教育平台。
    
    方案:
    使用微服务架构。
    
    实现:
    1. 设计数据库
    2. 开发前端
    3. 开发后端
    
    测试:
    进行测试。
    """
    
    # 分解思考过程
    decomposer = ThoughtDecomposer()
    thought_high_quality1 = decomposer.decompose_raw_thought(raw_thought_high_quality)
    thought_high_quality2 = decomposer.decompose_raw_thought(raw_thought_high_quality)  # 另一个高质量样本
    thought_low_quality = decomposer.decompose_raw_thought(raw_thought_low_quality)
    
    # 创建正样本对和负样本对
    positive_pairs = [(thought_high_quality1, thought_high_quality2)]
    negative_pairs = [(thought_high_quality1, thought_low_quality)]
    
    # 创建对比学习器
    learner = ContrastiveLearner(model_name="bert-base-uncased")
    
    # 训练模型（实际应用中需要更多数据）
    learner.train(positive_pairs, negative_pairs, batch_size=1, epochs=2)
    
    # 计算相似度
    pos_similarity = learner.similarity(thought_high_quality1, thought_high_quality2)
    neg_similarity = learner.similarity(thought_high_quality1, thought_low_quality)
    
    print(f"Positive pair similarity: {pos_similarity:.4f}")
    print(f"Negative pair similarity: {neg_similarity:.4f}")
    
    # 保存模型
    learner.save("models/contrastive_model.pt")
