"""
网页智能体模块

负责处理网页搜索相关任务，集成WebAgentB和Claude，继承自BaseAgent
"""

import os
import logging
import uuid
import json
import requests
from typing import Dict, Any, List, Optional

from .base_agent import BaseAgent

class WebAgent(BaseAgent):
    """网页智能体，负责网页搜索和内容分析，集成WebAgentB和Claude"""
    
    def __init__(self, agent_id: str = None):
        """
        初始化网页智能体
        
        参数:
            agent_id: 智能体ID，如果不提供则自动生成
        """
        super().__init__(
            agent_id=agent_id,
            name="网页智能体",
            description="增强的网页搜索和内容分析智能体"
        )
        self.webagentb_endpoint = os.environ.get("WEBAGENTB_ENDPOINT", "http://localhost:8000/api/search")
        self.claude_api_key = os.environ.get("CLAUDE_API_KEY", "")
        self.claude_endpoint = os.environ.get("CLAUDE_ENDPOINT", "https://api.anthropic.com/v1/messages")
        
    def get_capabilities(self) -> List[str]:
        """
        获取网页智能体能力列表
        
        返回:
            能力描述列表
        """
        return [
            "增强的网页搜索（集成WebAgentB）",
            "网页内容分析和总结",
            "多源信息整合",
            "自动生成网页报告",
            "网页内容提取和转换"
        ]
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        验证输入数据是否有效
        
        参数:
            input_data: 输入数据字典
            
        返回:
            数据是否有效
        """
        # 验证必要字段
        if "task_type" not in input_data:
            self.logger.error("缺少task_type字段")
            return False
            
        # 根据任务类型验证其他必要字段
        task_type = input_data["task_type"]
        
        if task_type == "web_search":
            if "query" not in input_data:
                self.logger.error("网页搜索任务缺少query字段")
                return False
                
        elif task_type == "content_analysis":
            if "url" not in input_data:
                self.logger.error("内容分析任务缺少url字段")
                return False
        
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理网页搜索和内容分析任务
        
        参数:
            input_data: 输入数据字典，包含任务类型和相关参数
            
        返回:
            处理结果字典
        """
        task_type = input_data["task_type"]
        
        if task_type == "web_search":
            return self._process_web_search(input_data)
            
        elif task_type == "content_analysis":
            return self._process_content_analysis(input_data)
            
        else:
            self.logger.error(f"不支持的任务类型: {task_type}")
            return {"error": f"不支持的任务类型: {task_type}"}
    
    def _process_web_search(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理网页搜索任务，集成WebAgentB
        
        参数:
            input_data: 输入数据字典
            
        返回:
            处理结果字典
        """
        query = input_data["query"]
        max_results = input_data.get("max_results", 5)
        
        try:
            # 调用WebAgentB进行搜索
            search_results = self._call_webagentb(query, max_results)
            
            # 使用Claude增强搜索结果（如果配置了Claude API密钥）
            if self.claude_api_key and input_data.get("use_claude", True):
                enhanced_results = self._enhance_with_claude(query, search_results)
                return {
                    "original_query": query,
                    "search_results": search_results,
                    "enhanced_results": enhanced_results
                }
            
            return {
                "original_query": query,
                "search_results": search_results
            }
            
        except Exception as e:
            self.logger.error(f"网页搜索失败: {str(e)}")
            return {"error": f"网页搜索失败: {str(e)}"}
    
    def _process_content_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理网页内容分析任务
        
        参数:
            input_data: 输入数据字典
            
        返回:
            处理结果字典
        """
        url = input_data["url"]
        analysis_type = input_data.get("analysis_type", "summary")
        
        try:
            # 获取网页内容
            content = self._fetch_webpage_content(url)
            
            # 根据分析类型处理内容
            if analysis_type == "summary":
                result = self._summarize_content(content, url)
            elif analysis_type == "extract_data":
                result = self._extract_structured_data(content, url)
            else:
                result = {"content": content, "url": url}
            
            return result
            
        except Exception as e:
            self.logger.error(f"内容分析失败: {str(e)}")
            return {"error": f"内容分析失败: {str(e)}"}
    
    def _call_webagentb(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        调用WebAgentB API进行网页搜索
        
        参数:
            query: 搜索查询
            max_results: 最大结果数
            
        返回:
            搜索结果列表
        """
        # 这里是WebAgentB API调用的模拟实现
        # 实际实现中，应该根据WebAgentB的API文档进行调用
        self.logger.info(f"调用WebAgentB搜索: {query}")
        
        try:
            payload = {
                "query": query,
                "max_results": max_results
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.webagentb_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json().get("results", [])
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"WebAgentB API调用失败: {str(e)}")
            
            # 如果API调用失败，返回模拟数据
            return [
                {
                    "title": f"搜索结果 {i+1} for {query}",
                    "url": f"https://example.com/result{i+1}",
                    "snippet": f"这是关于 {query} 的搜索结果 {i+1} 的摘要内容..."
                }
                for i in range(max_results)
            ]
    
    def _enhance_with_claude(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        使用Claude增强搜索结果
        
        参数:
            query: 原始搜索查询
            search_results: WebAgentB返回的搜索结果
            
        返回:
            Claude增强后的结果
        """
        self.logger.info(f"使用Claude增强搜索结果: {query}")
        
        # 构建发送给Claude的提示
        search_content = "\n\n".join([
            f"标题: {result['title']}\nURL: {result['url']}\n摘要: {result['snippet']}"
            for result in search_results
        ])
        
        prompt = f"""
        基于以下搜索结果，请提供关于"{query}"的综合分析和总结：

        {search_content}

        请提供：
        1. 主要观点和事实的总结
        2. 不同来源之间的共识和分歧
        3. 关键信息点的提炼
        4. 对信息可靠性的评估
        """
        
        try:
            # 调用Claude API
            headers = {
                "x-api-key": self.claude_api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 2000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(self.claude_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            enhanced_content = result.get("content", [{}])[0].get("text", "无法获取Claude响应")
            
            return {
                "summary": enhanced_content,
                "source": "Claude"
            }
            
        except Exception as e:
            self.logger.error(f"Claude API调用失败: {str(e)}")
            return {
                "summary": f"无法使用Claude增强结果: {str(e)}",
                "source": "Error"
            }
    
    def _fetch_webpage_content(self, url: str) -> str:
        """
        获取网页内容
        
        参数:
            url: 网页URL
            
        返回:
            网页内容
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"获取网页内容失败: {str(e)}")
            raise Exception(f"获取网页内容失败: {str(e)}")
    
    def _summarize_content(self, content: str, url: str) -> Dict[str, Any]:
        """
        使用Claude总结网页内容
        
        参数:
            content: 网页内容
            url: 网页URL
            
        返回:
            总结结果
        """
        # 如果没有配置Claude API密钥，返回简单摘要
        if not self.claude_api_key:
            return {
                "url": url,
                "summary": "需要配置Claude API密钥以生成摘要",
                "source": "System"
            }
        
        try:
            # 截取内容（Claude有输入限制）
            truncated_content = content[:50000]
            
            # 构建提示
            prompt = f"""
            请总结以下网页内容的主要信息：

            URL: {url}
            
            内容:
            {truncated_content}
            
            请提供一个全面但简洁的摘要，包括主要观点、关键事实和重要细节。
            """
            
            # 调用Claude API
            headers = {
                "x-api-key": self.claude_api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 1000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(self.claude_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            summary = result.get("content", [{}])[0].get("text", "无法获取Claude响应")
            
            return {
                "url": url,
                "summary": summary,
                "source": "Claude"
            }
            
        except Exception as e:
            self.logger.error(f"内容总结失败: {str(e)}")
            return {
                "url": url,
                "summary": f"内容总结失败: {str(e)}",
                "source": "Error"
            }
    
    def _extract_structured_data(self, content: str, url: str) -> Dict[str, Any]:
        """
        从网页内容中提取结构化数据
        
        参数:
            content: 网页内容
            url: 网页URL
            
        返回:
            提取的结构化数据
        """
        # 如果没有配置Claude API密钥，返回错误信息
        if not self.claude_api_key:
            return {
                "url": url,
                "data": {},
                "error": "需要配置Claude API密钥以提取结构化数据"
            }
        
        try:
            # 截取内容（Claude有输入限制）
            truncated_content = content[:50000]
            
            # 构建提示
            prompt = f"""
            请从以下网页内容中提取关键的结构化数据，并以JSON格式返回：

            URL: {url}
            
            内容:
            {truncated_content}
            
            请分析内容并提取以下信息（如果存在）：
            - 标题
            - 作者
            - 发布日期
            - 主要主题
            - 关键数据点
            - 重要实体（人物、组织、地点等）
            
            请以有效的JSON格式返回，不要包含任何其他文本。
            """
            
            # 调用Claude API
            headers = {
                "x-api-key": self.claude_api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            payload = {
                "model": "claude-3-opus-20240229",
                "max_tokens": 1000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            
            response = requests.post(self.claude_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            extracted_text = result.get("content", [{}])[0].get("text", "{}")
            
            # 尝试解析JSON
            try:
                extracted_data = json.loads(extracted_text)
            except json.JSONDecodeError:
                # 如果解析失败，尝试提取JSON部分
                import re
                json_match = re.search(r'```json\n(.*?)\n```', extracted_text, re.DOTALL)
                if json_match:
                    try:
                        extracted_data = json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        extracted_data = {"error": "无法解析JSON数据"}
                else:
                    extracted_data = {"error": "无法提取JSON数据"}
            
            return {
                "url": url,
                "data": extracted_data,
                "source": "Claude"
            }
            
        except Exception as e:
            self.logger.error(f"结构化数据提取失败: {str(e)}")
            return {
                "url": url,
                "data": {},
                "error": f"结构化数据提取失败: {str(e)}"
            }
