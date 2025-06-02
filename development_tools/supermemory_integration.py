"""
SuperMemory.ai集成模块 - 使用SuperMemory API实现任务进度和历史数据的分类存储
版本: 1.0.0
更新日期: 2025-06-02
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("supermemory_integration.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("SuperMemoryIntegration")

class SuperMemoryIntegration:
    """
    SuperMemory.ai集成类
    负责任务进度和历史数据的分类存储
    """
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.supermemory.ai"):
        """
        初始化SuperMemory.ai集成
        
        Args:
            api_key: SuperMemory API密钥
            base_url: SuperMemory API基础URL
        """
        self.api_key = api_key or os.environ.get("SUPERMEMORY_API_KEY")
        if not self.api_key:
            logger.warning("未提供SuperMemory API密钥，将使用模拟模式")
        
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 六大特性定义
        self.six_features = [
            "platform",  # 平台特性
            "ui_layout",  # UI布局特性
            "prompt",     # 提示词特性
            "thinking",   # 思维特性
            "content",    # 内容特性
            "memory"      # 记忆特性
        ]
        
        # 数据类型定义
        self.data_types = [
            "task_progress",      # 任务进度
            "user_history",       # 用户历史回复及分析
            "action_record",      # 创建及更新/取代/消除动作
            "work_completion"     # 更新及完成的工作
        ]
        
        logger.info(f"SuperMemoryIntegration初始化完成，API基础URL: {base_url}")
    
    def _make_api_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """
        发送API请求
        
        Args:
            method: 请求方法（GET, POST, PUT, DELETE）
            endpoint: API端点
            data: 请求数据
            
        Returns:
            API响应
        """
        if not self.api_key:
            logger.info(f"模拟API请求: {method} {endpoint}")
            return {"success": True, "data": {"id": f"mock_{int(time.time())}"}}
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}")
            return {"error": str(e), "status": "failed"}
    
    def create_memory(self, content: str, metadata: Dict = None, tags: List[str] = None) -> Dict:
        """
        创建记忆
        
        Args:
            content: 记忆内容
            metadata: 元数据
            tags: 标签
            
        Returns:
            创建结果
        """
        logger.info(f"创建记忆: {content[:50]}...")
        
        data = {
            "content": content,
            "metadata": metadata or {},
            "tags": tags or []
        }
        
        return self._make_api_request("POST", "/v1/memories", data)
    
    def get_memory(self, memory_id: str) -> Dict:
        """
        获取记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            记忆信息
        """
        logger.info(f"获取记忆: {memory_id}")
        
        return self._make_api_request("GET", f"/v1/memories/{memory_id}")
    
    def update_memory(self, memory_id: str, content: str = None, metadata: Dict = None, tags: List[str] = None) -> Dict:
        """
        更新记忆
        
        Args:
            memory_id: 记忆ID
            content: 记忆内容
            metadata: 元数据
            tags: 标签
            
        Returns:
            更新结果
        """
        logger.info(f"更新记忆: {memory_id}")
        
        data = {}
        if content is not None:
            data["content"] = content
        if metadata is not None:
            data["metadata"] = metadata
        if tags is not None:
            data["tags"] = tags
        
        return self._make_api_request("PUT", f"/v1/memories/{memory_id}", data)
    
    def delete_memory(self, memory_id: str) -> Dict:
        """
        删除记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            删除结果
        """
        logger.info(f"删除记忆: {memory_id}")
        
        return self._make_api_request("DELETE", f"/v1/memories/{memory_id}")
    
    def list_memories(self, query: str = None, tags: List[str] = None, limit: int = 10) -> Dict:
        """
        列出记忆
        
        Args:
            query: 查询字符串
            tags: 标签过滤
            limit: 返回数量限制
            
        Returns:
            记忆列表
        """
        logger.info(f"列出记忆: query={query}, tags={tags}, limit={limit}")
        
        params = {
            "limit": limit
        }
        if query:
            params["query"] = query
        if tags:
            params["tags"] = ",".join(tags)
        
        endpoint = "/v1/memories"
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            endpoint = f"{endpoint}?{query_string}"
        
        return self._make_api_request("GET", endpoint)
    
    def classify_text(self, text: str) -> Dict[str, str]:
        """
        对文本进行分类
        
        Args:
            text: 待分类文本
            
        Returns:
            分类结果
        """
        logger.info(f"对文本进行分类: {text[:50]}...")
        
        # 关键词映射
        keywords = {
            "task_progress": ["进度", "完成", "状态", "百分比", "阶段", "里程碑", "进展"],
            "user_history": ["用户", "回复", "问题", "反馈", "询问", "请求", "历史"],
            "action_record": ["创建", "更新", "修改", "删除", "替换", "添加", "移除"],
            "work_completion": ["完成", "结果", "输出", "成果", "交付", "验证", "测试"]
        }
        
        # 计算每个类别的匹配度
        scores = {data_type: 0 for data_type in self.data_types}
        
        for data_type, words in keywords.items():
            for word in words:
                if word in text:
                    scores[data_type] += 1
        
        # 找出得分最高的类别
        max_score = 0
        best_type = "task_progress"  # 默认类别
        
        for data_type, score in scores.items():
            if score > max_score:
                max_score = score
                best_type = data_type
        
        return best_type
    
    def store_task_data(self, task_id: str, text: str, feature: str = None, data_type: str = None) -> Dict:
        """
        存储任务数据
        
        Args:
            task_id: 任务ID
            text: 文本内容
            feature: 特性类别（可选，如果为None则自动判断）
            data_type: 数据类型（可选，如果为None则自动分类）
            
        Returns:
            存储结果
        """
        logger.info(f"存储任务数据: task_id={task_id}, feature={feature}, data_type={data_type}")
        
        # 如果未指定特性，尝试自动判断
        if not feature:
            feature = self._determine_feature(text)
        
        # 如果未指定数据类型，进行自动分类
        if not data_type:
            data_type = self.classify_text(text)
        
        # 构建元数据
        metadata = {
            "task_id": task_id,
            "feature": feature,
            "data_type": data_type,
            "timestamp": datetime.now().isoformat()
        }
        
        # 构建标签
        tags = [
            f"task:{task_id}",
            f"feature:{feature}",
            f"type:{data_type}"
        ]
        
        # 创建记忆
        result = self.create_memory(text, metadata, tags)
        
        if "error" in result:
            logger.error(f"存储任务数据失败: {result['error']}")
        else:
            logger.info(f"存储任务数据成功: memory_id={result.get('data', {}).get('id')}")
        
        return result
    
    def _determine_feature(self, text: str) -> str:
        """
        根据文本内容判断所属特性
        
        Args:
            text: 文本内容
            
        Returns:
            特性类别
        """
        # 特性关键词映射
        feature_keywords = {
            "platform": ["平台", "系统", "功能", "能力", "接口", "服务", "集成"],
            "ui_layout": ["界面", "布局", "UI", "设计", "视觉", "交互", "组件"],
            "prompt": ["提示", "指令", "命令", "输入", "请求", "查询", "问题"],
            "thinking": ["思考", "分析", "推理", "判断", "决策", "规划", "评估"],
            "content": ["内容", "文本", "图像", "视频", "音频", "数据", "信息"],
            "memory": ["记忆", "历史", "上下文", "存储", "检索", "回忆", "记录"]
        }
        
        # 计算每个特性的匹配度
        scores = {feature: 0 for feature in self.six_features}
        
        for feature, words in feature_keywords.items():
            for word in words:
                if word in text:
                    scores[feature] += 1
        
        # 找出得分最高的特性
        max_score = 0
        best_feature = "platform"  # 默认特性
        
        for feature, score in scores.items():
            if score > max_score:
                max_score = score
                best_feature = feature
        
        return best_feature
    
    def get_task_data(self, task_id: str, data_type: str = None, feature: str = None, limit: int = 10) -> List[Dict]:
        """
        获取任务数据
        
        Args:
            task_id: 任务ID
            data_type: 数据类型（可选）
            feature: 特性类别（可选）
            limit: 返回数量限制
            
        Returns:
            任务数据列表
        """
        logger.info(f"获取任务数据: task_id={task_id}, data_type={data_type}, feature={feature}")
        
        # 构建标签
        tags = [f"task:{task_id}"]
        if data_type:
            tags.append(f"type:{data_type}")
        if feature:
            tags.append(f"feature:{feature}")
        
        # 查询记忆
        result = self.list_memories(tags=tags, limit=limit)
        
        if "error" in result:
            logger.error(f"获取任务数据失败: {result['error']}")
            return []
        
        return result.get("data", [])
    
    def get_task_progress(self, task_id: str, feature: str = None) -> List[Dict]:
        """
        获取任务进度
        
        Args:
            task_id: 任务ID
            feature: 特性类别（可选）
            
        Returns:
            任务进度数据
        """
        return self.get_task_data(task_id, "task_progress", feature)
    
    def get_user_history(self, task_id: str, feature: str = None) -> List[Dict]:
        """
        获取用户历史
        
        Args:
            task_id: 任务ID
            feature: 特性类别（可选）
            
        Returns:
            用户历史数据
        """
        return self.get_task_data(task_id, "user_history", feature)
    
    def get_action_records(self, task_id: str, feature: str = None) -> List[Dict]:
        """
        获取动作记录
        
        Args:
            task_id: 任务ID
            feature: 特性类别（可选）
            
        Returns:
            动作记录数据
        """
        return self.get_task_data(task_id, "action_record", feature)
    
    def get_work_completions(self, task_id: str, feature: str = None) -> List[Dict]:
        """
        获取工作完成记录
        
        Args:
            task_id: 任务ID
            feature: 特性类别（可选）
            
        Returns:
            工作完成数据
        """
        return self.get_task_data(task_id, "work_completion", feature)
    
    def process_manus_output(self, task_id: str, text: str) -> Dict:
        """
        处理Manus输出文本，自动分类并存储
        
        Args:
            task_id: 任务ID
            text: Manus输出文本
            
        Returns:
            处理结果
        """
        logger.info(f"处理Manus输出: task_id={task_id}, text={text[:50]}...")
        
        # 自动分类
        data_type = self.classify_text(text)
        
        # 自动判断特性
        feature = self._determine_feature(text)
        
        # 存储数据
        result = self.store_task_data(task_id, text, feature, data_type)
        
        return {
            "task_id": task_id,
            "data_type": data_type,
            "feature": feature,
            "result": result
        }

# 示例用法
def main():
    # 创建SuperMemory集成实例
    api_key = os.environ.get("SUPERMEMORY_API_KEY", "your_api_key_here")
    supermemory = SuperMemoryIntegration(api_key)
    
    # 示例任务ID
    task_id = "task_123456"
    
    # 示例文本
    texts = [
        "任务已完成50%，正在进行第三阶段的开发工作",
        "用户反馈界面响应速度较慢，需要优化",
        "创建了新的组件，替换了旧的实现方式",
        "完成了所有测试用例，输出结果符合预期"
    ]
    
    # 处理文本
    for text in texts:
        result = supermemory.process_manus_output(task_id, text)
        print(f"分类结果: {result['data_type']}, 特性: {result['feature']}")
    
    # 获取任务进度
    progress_data = supermemory.get_task_progress(task_id)
    print(f"任务进度数据: {len(progress_data)}条")

if __name__ == "__main__":
    main()
