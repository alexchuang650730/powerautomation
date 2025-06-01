"""
无限上下文适配器，用于处理大规模上下文数据
"""
import os
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import torch
from transformers import AutoTokenizer, AutoModel

from rl_factory.core.thought.schema import ThoughtProcess
from rl_factory.core.thought.serializer import ThoughtSerializer


class InfiniteContextAdapter:
    """无限上下文适配器，用于处理大规模上下文数据"""
    
    def __init__(self, model_name: str = "bert-base-uncased", max_chunk_size: int = 512, 
                 overlap_size: int = 128, device: str = None):
        """
        初始化无限上下文适配器
        
        Args:
            model_name: 模型名称
            max_chunk_size: 最大块大小
            overlap_size: 重叠大小
            device: 设备（CPU或GPU）
        """
        # 设置设备
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # 加载分词器和模型
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        
        # 设置参数
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        
        # 上下文缓存
        self.context_cache = {}
    
    def _split_text_into_chunks(self, text: str) -> List[str]:
        """
        将文本分割为多个块
        
        Args:
            text: 输入文本
            
        Returns:
            文本块列表
        """
        # 分词
        tokens = self.tokenizer.tokenize(text)
        
        # 分块
        chunks = []
        for i in range(0, len(tokens), self.max_chunk_size - self.overlap_size):
            chunk_tokens = tokens[i:i + self.max_chunk_size]
            chunk_text = self.tokenizer.convert_tokens_to_string(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks
    
    def _encode_chunks(self, chunks: List[str]) -> List[torch.Tensor]:
        """
        编码文本块
        
        Args:
            chunks: 文本块列表
            
        Returns:
            编码向量列表
        """
        encodings = []
        
        for chunk in chunks:
            # 分词
            inputs = self.tokenizer(
                chunk,
                max_length=self.max_chunk_size,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )
            
            # 将数据移动到设备
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 编码
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # 获取[CLS]标记的表示
            encoding = outputs.last_hidden_state[:, 0, :]
            encodings.append(encoding)
        
        return encodings
    
    def _merge_encodings(self, encodings: List[torch.Tensor]) -> torch.Tensor:
        """
        合并编码向量
        
        Args:
            encodings: 编码向量列表
            
        Returns:
            合并后的编码向量
        """
        # 简单平均
        if encodings:
            merged = torch.mean(torch.cat(encodings, dim=0), dim=0, keepdim=True)
        else:
            # 如果没有编码，返回零向量
            merged = torch.zeros((1, self.model.config.hidden_size), device=self.device)
        
        return merged
    
    def process_context(self, context_id: str, text: str) -> torch.Tensor:
        """
        处理上下文
        
        Args:
            context_id: 上下文ID
            text: 上下文文本
            
        Returns:
            上下文编码向量
        """
        # 分割文本
        chunks = self._split_text_into_chunks(text)
        
        # 编码块
        encodings = self._encode_chunks(chunks)
        
        # 合并编码
        merged = self._merge_encodings(encodings)
        
        # 缓存编码
        self.context_cache[context_id] = merged
        
        return merged
    
    def update_context(self, context_id: str, text: str) -> torch.Tensor:
        """
        更新上下文
        
        Args:
            context_id: 上下文ID
            text: 新的上下文文本
            
        Returns:
            更新后的上下文编码向量
        """
        # 如果上下文不存在，直接处理
        if context_id not in self.context_cache:
            return self.process_context(context_id, text)
        
        # 分割文本
        chunks = self._split_text_into_chunks(text)
        
        # 编码块
        encodings = self._encode_chunks(chunks)
        
        # 合并编码
        new_merged = self._merge_encodings(encodings)
        
        # 获取旧编码
        old_merged = self.context_cache[context_id]
        
        # 加权平均（新旧各占一半）
        updated = (old_merged + new_merged) / 2
        
        # 更新缓存
        self.context_cache[context_id] = updated
        
        return updated
    
    def get_context(self, context_id: str) -> Optional[torch.Tensor]:
        """
        获取上下文
        
        Args:
            context_id: 上下文ID
            
        Returns:
            上下文编码向量，如果不存在则返回None
        """
        return self.context_cache.get(context_id)
    
    def clear_context(self, context_id: str) -> bool:
        """
        清除上下文
        
        Args:
            context_id: 上下文ID
            
        Returns:
            是否成功清除
        """
        if context_id in self.context_cache:
            del self.context_cache[context_id]
            return True
        return False
    
    def process_thought(self, thought_process: ThoughtProcess) -> torch.Tensor:
        """
        处理思考过程
        
        Args:
            thought_process: 思考过程
            
        Returns:
            思考过程编码向量
        """
        # 将思考过程序列化为文本
        text = ThoughtSerializer.to_markdown(thought_process)
        
        # 生成上下文ID
        context_id = f"thought_{thought_process.id}"
        
        # 处理上下文
        return self.process_context(context_id, text)
    
    def save_contexts(self, path: str):
        """
        保存上下文缓存
        
        Args:
            path: 保存路径
        """
        # 创建目录
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 将张量转换为列表
        serializable_cache = {
            k: v.cpu().numpy().tolist() for k, v in self.context_cache.items()
        }
        
        # 保存为JSON
        with open(path, "w") as f:
            json.dump(serializable_cache, f)
    
    def load_contexts(self, path: str):
        """
        加载上下文缓存
        
        Args:
            path: 加载路径
        """
        # 加载JSON
        with open(path, "r") as f:
            serializable_cache = json.load(f)
        
        # 将列表转换为张量
        self.context_cache = {
            k: torch.tensor(v, device=self.device) for k, v in serializable_cache.items()
        }


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
    
    # 创建无限上下文适配器
    adapter = InfiniteContextAdapter(model_name="bert-base-uncased")
    
    # 处理思考过程
    encoding = adapter.process_thought(thought_process)
    
    print(f"Thought process encoding shape: {encoding.shape}")
    
    # 更新上下文
    context_id = f"thought_{thought_process.id}"
    updated = adapter.update_context(context_id, "新的上下文信息")
    
    print(f"Updated context encoding shape: {updated.shape}")
    
    # 保存上下文
    adapter.save_contexts("contexts.json")
