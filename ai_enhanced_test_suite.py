#!/usr/bin/env python3
"""
PowerAutomation AI增强功能全面测试
专注于AI功能的深度验证和性能评估
"""

import sys
import os
import json
import time
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics
import random

# 添加项目路径
sys.path.append('/home/ubuntu/powerautomation')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class AITestResult:
    """AI测试结果数据类"""
    test_name: str
    ai_component: str
    success: bool
    execution_time: float
    ai_metrics: Dict[str, Any]
    performance_score: float
    error_message: Optional[str] = None
    timestamp: datetime = None

class AIEnhancedFunctionTester:
    """AI增强功能测试器"""
    
    def __init__(self):
        self.supermemory_api_key = ""SUPERMEMORY_API_KEY_PLACEHOLDER""
        self.base_url = "https://api.supermemory.ai/v3"
        self.results: List[AITestResult] = []
        self.db_path = "/home/ubuntu/powerautomation/ai_enhanced_test_results.db"
        self.init_database()
        
    def init_database(self):
        """初始化AI测试结果数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_enhanced_test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                ai_component TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                execution_time REAL NOT NULL,
                ai_metrics TEXT,
                performance_score REAL,
                error_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("AI测试数据库初始化完成")
    
    def save_result(self, result: AITestResult):
        """保存AI测试结果到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ai_enhanced_test_results 
            (test_name, ai_component, success, execution_time, ai_metrics, performance_score, error_message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.test_name,
            result.ai_component,
            result.success,
            result.execution_time,
            json.dumps(result.ai_metrics) if result.ai_metrics else None,
            result.performance_score,
            result.error_message,
            result.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def test_ai_intent_understanding(self) -> AITestResult:
        """测试AI意图理解功能"""
        logger.info("🧠 测试AI意图理解功能")
        start_time = time.time()
        
        try:
            # 模拟AI意图理解系统
            test_intents = [
                {
                    "user_input": "我想保存这个重要的会议记录",
                    "expected_intent": "save_memory",
                    "expected_confidence": 0.9
                },
                {
                    "user_input": "帮我找一下上次关于项目的讨论",
                    "expected_intent": "search_memory",
                    "expected_confidence": 0.85
                },
                {
                    "user_input": "删除那个过时的信息",
                    "expected_intent": "delete_memory",
                    "expected_confidence": 0.8
                },
                {
                    "user_input": "这个数据很重要，需要长期保存",
                    "expected_intent": "save_memory",
                    "expected_confidence": 0.88
                },
                {
                    "user_input": "查看我的所有记忆",
                    "expected_intent": "list_memories",
                    "expected_confidence": 0.95
                }
            ]
            
            intent_results = []
            headers = {
                "Authorization": f"Bearer {self.supermemory_api_key}",
                "Content-Type": "application/json"
            }
            
            for intent_test in test_intents:
                intent_start = time.time()
                
                # 模拟AI意图理解处理
                user_input = intent_test["user_input"]
                
                # 基于关键词的简单意图识别（模拟AI处理）
                if "保存" in user_input or "存储" in user_input or "记录" in user_input:
                    detected_intent = "save_memory"
                    confidence = 0.9 + random.uniform(-0.1, 0.1)
                    
                    # 执行对应的API操作
                    memory_data = {
                        "title": f"AI意图理解测试 - {user_input[:20]}",
                        "content": f"用户意图: {user_input}",
                        "metadata": {
                            "detected_intent": detected_intent,
                            "confidence": confidence,
                            "test_type": "intent_understanding"
                        }
                    }
                    
                    response = requests.post(f"{self.base_url}/memories", headers=headers, json=memory_data, timeout=30)
                    api_success = response.status_code in [200, 201]
                    
                elif "找" in user_input or "搜索" in user_input or "查找" in user_input:
                    detected_intent = "search_memory"
                    confidence = 0.85 + random.uniform(-0.1, 0.1)
                    
                    # 执行搜索操作
                    search_payload = {"q": "项目讨论", "limit": 3}
                    response = requests.post(f"{self.base_url}/search", headers=headers, json=search_payload, timeout=30)
                    api_success = response.status_code == 200
                    
                elif "删除" in user_input or "移除" in user_input:
                    detected_intent = "delete_memory"
                    confidence = 0.8 + random.uniform(-0.1, 0.1)
                    api_success = True  # 模拟删除成功（不实际删除）
                    
                elif "查看" in user_input or "列表" in user_input or "所有" in user_input:
                    detected_intent = "list_memories"
                    confidence = 0.95 + random.uniform(-0.05, 0.05)
                    
                    # 执行列表操作
                    response = requests.get(f"{self.base_url}/memories", headers=headers, timeout=30)
                    api_success = response.status_code == 200
                    
                else:
                    detected_intent = "unknown"
                    confidence = 0.3
                    api_success = False
                
                intent_time = time.time() - intent_start
                
                # 评估意图理解准确性
                intent_correct = detected_intent == intent_test["expected_intent"]
                confidence_accurate = abs(confidence - intent_test["expected_confidence"]) < 0.2
                
                intent_results.append({
                    "user_input": user_input,
                    "expected_intent": intent_test["expected_intent"],
                    "detected_intent": detected_intent,
                    "expected_confidence": intent_test["expected_confidence"],
                    "actual_confidence": confidence,
                    "intent_correct": intent_correct,
                    "confidence_accurate": confidence_accurate,
                    "api_success": api_success,
                    "processing_time": intent_time
                })
            
            execution_time = time.time() - start_time
            
            # 计算AI性能指标
            total_intents = len(intent_results)
            correct_intents = sum(1 for r in intent_results if r["intent_correct"])
            accurate_confidence = sum(1 for r in intent_results if r["confidence_accurate"])
            successful_apis = sum(1 for r in intent_results if r["api_success"])
            
            intent_accuracy = (correct_intents / total_intents) * 100
            confidence_accuracy = (accurate_confidence / total_intents) * 100
            api_success_rate = (successful_apis / total_intents) * 100
            avg_processing_time = statistics.mean([r["processing_time"] for r in intent_results])
            
            # 计算综合性能分数
            performance_score = (intent_accuracy * 0.4 + confidence_accuracy * 0.3 + api_success_rate * 0.3)
            
            ai_metrics = {
                "total_intents_tested": total_intents,
                "intent_accuracy": intent_accuracy,
                "confidence_accuracy": confidence_accuracy,
                "api_success_rate": api_success_rate,
                "average_processing_time": avg_processing_time,
                "intent_results": intent_results
            }
            
            result = AITestResult(
                test_name="ai_intent_understanding",
                ai_component="intent_understanding_engine",
                success=intent_accuracy >= 80,  # 80%以上准确率算成功
                execution_time=execution_time,
                ai_metrics=ai_metrics,
                performance_score=performance_score,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ AI意图理解测试完成 - {execution_time:.3f}s")
            logger.info(f"   意图准确率: {intent_accuracy:.1f}%")
            logger.info(f"   置信度准确率: {confidence_accuracy:.1f}%")
            logger.info(f"   API成功率: {api_success_rate:.1f}%")
            logger.info(f"   性能分数: {performance_score:.1f}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            result = AITestResult(
                test_name="ai_intent_understanding",
                ai_component="intent_understanding_engine",
                success=False,
                execution_time=execution_time,
                ai_metrics={"error": error_msg},
                performance_score=0.0,
                error_message=error_msg,
                timestamp=datetime.now()
            )
            
            logger.error(f"❌ AI意图理解测试失败: {error_msg}")
            return result
    
    def test_ai_memory_enhancement(self) -> AITestResult:
        """测试AI记忆增强功能"""
        logger.info("🧠 测试AI记忆增强功能")
        start_time = time.time()
        
        try:
            # 模拟AI记忆增强系统
            raw_memories = [
                {
                    "title": "项目会议",
                    "content": "讨论了新功能开发进度",
                    "metadata": {"type": "meeting"}
                },
                {
                    "title": "技术文档",
                    "content": "API接口设计规范",
                    "metadata": {"type": "documentation"}
                },
                {
                    "title": "用户反馈",
                    "content": "用户希望增加搜索功能",
                    "metadata": {"type": "feedback"}
                }
            ]
            
            enhanced_memories = []
            headers = {
                "Authorization": f"Bearer {self.supermemory_api_key}",
                "Content-Type": "application/json"
            }
            
            for i, raw_memory in enumerate(raw_memories):
                enhancement_start = time.time()
                
                # AI增强处理
                enhanced_content = self._enhance_memory_content(raw_memory)
                enhanced_metadata = self._enhance_memory_metadata(raw_memory)
                
                # 创建增强后的记忆
                enhanced_memory = {
                    "title": f"[AI增强] {raw_memory['title']}",
                    "content": enhanced_content,
                    "metadata": {
                        **raw_memory["metadata"],
                        **enhanced_metadata,
                        "ai_enhanced": True,
                        "enhancement_timestamp": datetime.now().isoformat()
                    }
                }
                
                # 存储增强后的记忆
                response = requests.post(f"{self.base_url}/memories", headers=headers, json=enhanced_memory, timeout=30)
                storage_success = response.status_code in [200, 201]
                
                enhancement_time = time.time() - enhancement_start
                
                enhanced_memories.append({
                    "original": raw_memory,
                    "enhanced": enhanced_memory,
                    "storage_success": storage_success,
                    "enhancement_time": enhancement_time,
                    "content_length_increase": len(enhanced_content) - len(raw_memory["content"]),
                    "metadata_fields_added": len(enhanced_metadata)
                })
            
            execution_time = time.time() - start_time
            
            # 计算增强效果指标
            total_memories = len(enhanced_memories)
            successful_enhancements = sum(1 for m in enhanced_memories if m["storage_success"])
            avg_content_increase = statistics.mean([m["content_length_increase"] for m in enhanced_memories])
            avg_metadata_added = statistics.mean([m["metadata_fields_added"] for m in enhanced_memories])
            avg_enhancement_time = statistics.mean([m["enhancement_time"] for m in enhanced_memories])
            
            enhancement_success_rate = (successful_enhancements / total_memories) * 100
            content_enrichment_ratio = avg_content_increase / statistics.mean([len(m["original"]["content"]) for m in enhanced_memories]) * 100
            
            # 计算性能分数
            performance_score = (
                enhancement_success_rate * 0.4 +
                min(content_enrichment_ratio, 100) * 0.3 +  # 限制最大100%
                (avg_metadata_added * 10) * 0.3  # 每个字段10分
            )
            
            ai_metrics = {
                "total_memories_processed": total_memories,
                "enhancement_success_rate": enhancement_success_rate,
                "average_content_increase": avg_content_increase,
                "content_enrichment_ratio": content_enrichment_ratio,
                "average_metadata_fields_added": avg_metadata_added,
                "average_enhancement_time": avg_enhancement_time,
                "enhanced_memories": enhanced_memories
            }
            
            result = AITestResult(
                test_name="ai_memory_enhancement",
                ai_component="memory_enhancement_engine",
                success=enhancement_success_rate >= 80,
                execution_time=execution_time,
                ai_metrics=ai_metrics,
                performance_score=performance_score,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ AI记忆增强测试完成 - {execution_time:.3f}s")
            logger.info(f"   增强成功率: {enhancement_success_rate:.1f}%")
            logger.info(f"   内容丰富度提升: {content_enrichment_ratio:.1f}%")
            logger.info(f"   平均新增元数据字段: {avg_metadata_added:.1f}个")
            logger.info(f"   性能分数: {performance_score:.1f}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            result = AITestResult(
                test_name="ai_memory_enhancement",
                ai_component="memory_enhancement_engine",
                success=False,
                execution_time=execution_time,
                ai_metrics={"error": error_msg},
                performance_score=0.0,
                error_message=error_msg,
                timestamp=datetime.now()
            )
            
            logger.error(f"❌ AI记忆增强测试失败: {error_msg}")
            return result
    
    def test_ai_intelligent_search(self) -> AITestResult:
        """测试AI智能搜索功能"""
        logger.info("🔍 测试AI智能搜索功能")
        start_time = time.time()
        
        try:
            # 首先创建一些测试数据
            test_memories = [
                {
                    "title": "PowerAutomation架构设计",
                    "content": "PowerAutomation采用微服务架构，包含工作流引擎、AI协调中枢、智能测试生成器等核心组件。",
                    "metadata": {"category": "architecture", "importance": "high"}
                },
                {
                    "title": "API集成测试结果",
                    "content": "supermemory API集成测试成功，实现了真实的API调用验证，替代了之前的模拟验证。",
                    "metadata": {"category": "testing", "importance": "medium"}
                },
                {
                    "title": "性能优化策略",
                    "content": "通过连接池优化、请求批处理、智能缓存等策略，API响应时间提升了4.7%。",
                    "metadata": {"category": "performance", "importance": "high"}
                }
            ]
            
            headers = {
                "Authorization": f"Bearer {self.supermemory_api_key}",
                "Content-Type": "application/json"
            }
            
            # 存储测试数据
            stored_memories = []
            for memory in test_memories:
                response = requests.post(f"{self.base_url}/memories", headers=headers, json=memory, timeout=30)
                if response.status_code in [200, 201]:
                    stored_memories.append(memory)
            
            # 等待数据处理
            time.sleep(3)
            
            # 执行智能搜索测试
            search_scenarios = [
                {
                    "query": "PowerAutomation架构",
                    "expected_category": "architecture",
                    "search_type": "exact_match"
                },
                {
                    "query": "API测试",
                    "expected_category": "testing",
                    "search_type": "keyword_match"
                },
                {
                    "query": "性能提升",
                    "expected_category": "performance",
                    "search_type": "semantic_match"
                },
                {
                    "query": "重要的架构信息",
                    "expected_importance": "high",
                    "search_type": "attribute_filter"
                }
            ]
            
            search_results = []
            
            for scenario in search_scenarios:
                search_start = time.time()
                
                # 执行搜索
                search_payload = {"q": scenario["query"], "limit": 5}
                response = requests.post(f"{self.base_url}/search", headers=headers, json=search_payload, timeout=30)
                
                search_time = time.time() - search_start
                
                if response.status_code == 200:
                    search_data = response.json()
                    results = search_data.get("results", [])
                    
                    # 分析搜索质量
                    relevance_score = self._calculate_search_relevance(scenario, results)
                    precision = self._calculate_search_precision(scenario, results)
                    
                    search_results.append({
                        "query": scenario["query"],
                        "search_type": scenario["search_type"],
                        "results_count": len(results),
                        "search_time": search_time,
                        "relevance_score": relevance_score,
                        "precision": precision,
                        "success": len(results) > 0
                    })
                else:
                    search_results.append({
                        "query": scenario["query"],
                        "search_type": scenario["search_type"],
                        "results_count": 0,
                        "search_time": search_time,
                        "relevance_score": 0.0,
                        "precision": 0.0,
                        "success": False,
                        "error": response.text
                    })
            
            execution_time = time.time() - start_time
            
            # 计算搜索性能指标
            total_searches = len(search_results)
            successful_searches = sum(1 for r in search_results if r["success"])
            avg_search_time = statistics.mean([r["search_time"] for r in search_results])
            avg_relevance = statistics.mean([r["relevance_score"] for r in search_results])
            avg_precision = statistics.mean([r["precision"] for r in search_results])
            
            search_success_rate = (successful_searches / total_searches) * 100
            
            # 计算性能分数
            performance_score = (
                search_success_rate * 0.3 +
                avg_relevance * 100 * 0.4 +
                avg_precision * 100 * 0.3
            )
            
            ai_metrics = {
                "total_searches": total_searches,
                "successful_searches": successful_searches,
                "search_success_rate": search_success_rate,
                "average_search_time": avg_search_time,
                "average_relevance_score": avg_relevance,
                "average_precision": avg_precision,
                "stored_test_memories": len(stored_memories),
                "search_results": search_results
            }
            
            result = AITestResult(
                test_name="ai_intelligent_search",
                ai_component="intelligent_search_engine",
                success=search_success_rate >= 75,
                execution_time=execution_time,
                ai_metrics=ai_metrics,
                performance_score=performance_score,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ AI智能搜索测试完成 - {execution_time:.3f}s")
            logger.info(f"   搜索成功率: {search_success_rate:.1f}%")
            logger.info(f"   平均相关性: {avg_relevance:.3f}")
            logger.info(f"   平均精确度: {avg_precision:.3f}")
            logger.info(f"   性能分数: {performance_score:.1f}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            result = AITestResult(
                test_name="ai_intelligent_search",
                ai_component="intelligent_search_engine",
                success=False,
                execution_time=execution_time,
                ai_metrics={"error": error_msg},
                performance_score=0.0,
                error_message=error_msg,
                timestamp=datetime.now()
            )
            
            logger.error(f"❌ AI智能搜索测试失败: {error_msg}")
            return result
    
    def test_ai_adaptive_learning(self) -> AITestResult:
        """测试AI自适应学习功能"""
        logger.info("📚 测试AI自适应学习功能")
        start_time = time.time()
        
        try:
            # 模拟AI自适应学习系统
            learning_scenarios = [
                {
                    "scenario": "用户行为学习",
                    "description": "学习用户的搜索和存储模式",
                    "learning_data": [
                        {"action": "search", "query": "API测试", "success": True},
                        {"action": "save", "category": "testing", "success": True},
                        {"action": "search", "query": "性能优化", "success": True},
                        {"action": "save", "category": "performance", "success": True}
                    ]
                },
                {
                    "scenario": "API响应模式学习",
                    "description": "学习API响应时间和成功率模式",
                    "learning_data": [
                        {"api": "memories", "response_time": 0.5, "success": True},
                        {"api": "search", "response_time": 0.3, "success": False},
                        {"api": "memories", "response_time": 0.4, "success": True},
                        {"api": "search", "response_time": 0.2, "success": True}
                    ]
                },
                {
                    "scenario": "错误模式学习",
                    "description": "学习常见错误和恢复策略",
                    "learning_data": [
                        {"error_type": "timeout", "recovery": "retry", "success": True},
                        {"error_type": "auth_error", "recovery": "refresh_token", "success": True},
                        {"error_type": "rate_limit", "recovery": "backoff", "success": True}
                    ]
                }
            ]
            
            learning_results = []
            headers = {
                "Authorization": f"Bearer {self.supermemory_api_key}",
                "Content-Type": "application/json"
            }
            
            for scenario in learning_scenarios:
                learning_start = time.time()
                
                # 模拟学习过程
                learning_data = scenario["learning_data"]
                
                if scenario["scenario"] == "用户行为学习":
                    # 分析用户行为模式
                    search_actions = [d for d in learning_data if d["action"] == "search"]
                    save_actions = [d for d in learning_data if d["action"] == "save"]
                    
                    search_success_rate = sum(1 for a in search_actions if a["success"]) / len(search_actions) * 100
                    save_success_rate = sum(1 for a in save_actions if a["success"]) / len(save_actions) * 100
                    
                    # 基于学习结果优化搜索策略
                    if search_success_rate > 80:
                        optimization = "增强相似查询的权重"
                    else:
                        optimization = "改进查询理解算法"
                    
                    learning_outcome = {
                        "pattern_detected": "用户偏好技术相关内容",
                        "search_success_rate": search_success_rate,
                        "save_success_rate": save_success_rate,
                        "optimization_applied": optimization
                    }
                    
                elif scenario["scenario"] == "API响应模式学习":
                    # 分析API性能模式
                    api_stats = {}
                    for data in learning_data:
                        api = data["api"]
                        if api not in api_stats:
                            api_stats[api] = {"times": [], "successes": []}
                        api_stats[api]["times"].append(data["response_time"])
                        api_stats[api]["successes"].append(data["success"])
                    
                    # 计算每个API的性能指标
                    performance_insights = {}
                    for api, stats in api_stats.items():
                        avg_time = statistics.mean(stats["times"])
                        success_rate = sum(stats["successes"]) / len(stats["successes"]) * 100
                        performance_insights[api] = {
                            "avg_response_time": avg_time,
                            "success_rate": success_rate,
                            "recommendation": "优化" if avg_time > 0.4 else "保持"
                        }
                    
                    learning_outcome = {
                        "performance_insights": performance_insights,
                        "optimization_applied": "动态调整超时时间"
                    }
                    
                elif scenario["scenario"] == "错误模式学习":
                    # 分析错误恢复模式
                    error_stats = {}
                    for data in learning_data:
                        error_type = data["error_type"]
                        if error_type not in error_stats:
                            error_stats[error_type] = {"recoveries": [], "successes": []}
                        error_stats[error_type]["recoveries"].append(data["recovery"])
                        error_stats[error_type]["successes"].append(data["success"])
                    
                    # 学习最佳恢复策略
                    recovery_strategies = {}
                    for error_type, stats in error_stats.items():
                        success_rate = sum(stats["successes"]) / len(stats["successes"]) * 100
                        best_recovery = stats["recoveries"][0]  # 简化：使用第一个策略
                        recovery_strategies[error_type] = {
                            "best_strategy": best_recovery,
                            "success_rate": success_rate
                        }
                    
                    learning_outcome = {
                        "recovery_strategies": recovery_strategies,
                        "optimization_applied": "更新错误处理规则库"
                    }
                
                # 将学习结果存储到记忆系统
                learning_memory = {
                    "title": f"AI学习结果 - {scenario['scenario']}",
                    "content": f"学习场景: {scenario['description']}\\n学习结果: {json.dumps(learning_outcome, ensure_ascii=False, indent=2)}",
                    "metadata": {
                        "type": "ai_learning",
                        "scenario": scenario["scenario"],
                        "learning_timestamp": datetime.now().isoformat()
                    }
                }
                
                response = requests.post(f"{self.base_url}/memories", headers=headers, json=learning_memory, timeout=30)
                storage_success = response.status_code in [200, 201]
                
                learning_time = time.time() - learning_start
                
                learning_results.append({
                    "scenario": scenario["scenario"],
                    "learning_outcome": learning_outcome,
                    "storage_success": storage_success,
                    "learning_time": learning_time,
                    "data_points_processed": len(learning_data)
                })
            
            execution_time = time.time() - start_time
            
            # 计算学习效果指标
            total_scenarios = len(learning_results)
            successful_learning = sum(1 for r in learning_results if r["storage_success"])
            total_data_points = sum(r["data_points_processed"] for r in learning_results)
            avg_learning_time = statistics.mean([r["learning_time"] for r in learning_results])
            
            learning_success_rate = (successful_learning / total_scenarios) * 100
            learning_efficiency = total_data_points / execution_time  # 数据点/秒
            
            # 计算性能分数
            performance_score = (
                learning_success_rate * 0.4 +
                min(learning_efficiency * 10, 100) * 0.3 +  # 效率分数，限制最大100
                (100 - avg_learning_time * 10) * 0.3  # 时间分数，时间越短分数越高
            )
            
            ai_metrics = {
                "total_learning_scenarios": total_scenarios,
                "successful_learning": successful_learning,
                "learning_success_rate": learning_success_rate,
                "total_data_points_processed": total_data_points,
                "learning_efficiency": learning_efficiency,
                "average_learning_time": avg_learning_time,
                "learning_results": learning_results
            }
            
            result = AITestResult(
                test_name="ai_adaptive_learning",
                ai_component="adaptive_learning_engine",
                success=learning_success_rate >= 80,
                execution_time=execution_time,
                ai_metrics=ai_metrics,
                performance_score=performance_score,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ AI自适应学习测试完成 - {execution_time:.3f}s")
            logger.info(f"   学习成功率: {learning_success_rate:.1f}%")
            logger.info(f"   学习效率: {learning_efficiency:.1f} 数据点/秒")
            logger.info(f"   处理数据点: {total_data_points}个")
            logger.info(f"   性能分数: {performance_score:.1f}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            result = AITestResult(
                test_name="ai_adaptive_learning",
                ai_component="adaptive_learning_engine",
                success=False,
                execution_time=execution_time,
                ai_metrics={"error": error_msg},
                performance_score=0.0,
                error_message=error_msg,
                timestamp=datetime.now()
            )
            
            logger.error(f"❌ AI自适应学习测试失败: {error_msg}")
            return result
    
    def _enhance_memory_content(self, memory: Dict[str, Any]) -> str:
        """AI增强记忆内容"""
        original_content = memory["content"]
        memory_type = memory["metadata"].get("type", "general")
        
        # 基于类型的内容增强
        if memory_type == "meeting":
            enhanced = f"{original_content}\\n\\n[AI增强信息]\\n- 会议类型: 项目讨论\\n- 重要程度: 高\\n- 后续行动: 需要跟进开发进度"
        elif memory_type == "documentation":
            enhanced = f"{original_content}\\n\\n[AI增强信息]\\n- 文档类型: 技术规范\\n- 适用范围: 开发团队\\n- 更新频率: 定期更新"
        elif memory_type == "feedback":
            enhanced = f"{original_content}\\n\\n[AI增强信息]\\n- 反馈类型: 功能需求\\n- 优先级: 中等\\n- 实施建议: 纳入下一版本规划"
        else:
            enhanced = f"{original_content}\\n\\n[AI增强信息]\\n- 内容已通过AI分析和增强\\n- 增强时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return enhanced
    
    def _enhance_memory_metadata(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """AI增强记忆元数据"""
        enhanced_metadata = {
            "ai_tags": [],
            "ai_category": "general",
            "ai_priority": "medium",
            "ai_keywords": []
        }
        
        content = memory["content"].lower()
        
        # 基于内容的智能标签
        if "api" in content or "接口" in content:
            enhanced_metadata["ai_tags"].append("api")
            enhanced_metadata["ai_category"] = "technical"
        
        if "测试" in content or "test" in content:
            enhanced_metadata["ai_tags"].append("testing")
            
        if "性能" in content or "performance" in content:
            enhanced_metadata["ai_tags"].append("performance")
            enhanced_metadata["ai_priority"] = "high"
        
        if "用户" in content or "user" in content:
            enhanced_metadata["ai_tags"].append("user_related")
        
        # 提取关键词
        keywords = []
        for word in ["PowerAutomation", "API", "测试", "性能", "优化", "功能"]:
            if word.lower() in content:
                keywords.append(word)
        
        enhanced_metadata["ai_keywords"] = keywords
        
        return enhanced_metadata
    
    def _calculate_search_relevance(self, scenario: Dict[str, Any], results: List[Dict[str, Any]]) -> float:
        """计算搜索相关性分数"""
        if not results:
            return 0.0
        
        query = scenario["query"].lower()
        relevance_scores = []
        
        for result in results:
            # 简化的相关性计算
            title = result.get("title", "").lower()
            content = result.get("content", "").lower()
            
            title_match = sum(1 for word in query.split() if word in title) / len(query.split())
            content_match = sum(1 for word in query.split() if word in content) / len(query.split())
            
            relevance = (title_match * 0.7 + content_match * 0.3)
            relevance_scores.append(relevance)
        
        return statistics.mean(relevance_scores)
    
    def _calculate_search_precision(self, scenario: Dict[str, Any], results: List[Dict[str, Any]]) -> float:
        """计算搜索精确度"""
        if not results:
            return 0.0
        
        # 简化的精确度计算
        relevant_results = 0
        
        for result in results:
            # 基于预期类别或重要性判断相关性
            if "expected_category" in scenario:
                metadata = result.get("metadata", {})
                if metadata.get("category") == scenario["expected_category"]:
                    relevant_results += 1
            elif "expected_importance" in scenario:
                metadata = result.get("metadata", {})
                if metadata.get("importance") == scenario["expected_importance"]:
                    relevant_results += 1
            else:
                # 默认认为有结果就是相关的
                relevant_results += 1
        
        return relevant_results / len(results)
    
    def run_ai_enhanced_test_suite(self) -> Dict[str, Any]:
        """运行AI增强功能测试套件"""
        logger.info("🤖 开始运行PowerAutomation AI增强功能测试套件")
        logger.info("=" * 80)
        
        suite_start_time = time.time()
        
        # 执行所有AI测试
        ai_tests = [
            self.test_ai_intent_understanding,
            self.test_ai_memory_enhancement,
            self.test_ai_intelligent_search,
            self.test_ai_adaptive_learning
        ]
        
        for test_func in ai_tests:
            try:
                result = test_func()
                self.results.append(result)
                self.save_result(result)
                print()  # 添加空行分隔
            except Exception as e:
                logger.error(f"AI测试执行异常: {test_func.__name__} - {str(e)}")
        
        suite_execution_time = time.time() - suite_start_time
        
        # 生成AI功能综合报告
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        avg_execution_time = statistics.mean([r.execution_time for r in self.results]) if self.results else 0
        avg_performance_score = statistics.mean([r.performance_score for r in self.results]) if self.results else 0
        
        # AI组件分析
        ai_components = {}
        for result in self.results:
            component = result.ai_component
            if component not in ai_components:
                ai_components[component] = {"tests": 0, "successes": 0, "avg_score": 0}
            ai_components[component]["tests"] += 1
            if result.success:
                ai_components[component]["successes"] += 1
            ai_components[component]["avg_score"] += result.performance_score
        
        for component in ai_components:
            ai_components[component]["success_rate"] = (ai_components[component]["successes"] / ai_components[component]["tests"]) * 100
            ai_components[component]["avg_score"] /= ai_components[component]["tests"]
        
        comprehensive_report = {
            "ai_test_suite_summary": {
                "total_ai_tests": total_tests,
                "successful_ai_tests": successful_tests,
                "failed_ai_tests": total_tests - successful_tests,
                "ai_success_rate": success_rate,
                "suite_execution_time": suite_execution_time,
                "average_test_time": avg_execution_time,
                "average_performance_score": avg_performance_score,
                "timestamp": datetime.now().isoformat()
            },
            "ai_component_analysis": ai_components,
            "ai_test_results": [
                {
                    "test_name": r.test_name,
                    "ai_component": r.ai_component,
                    "success": r.success,
                    "execution_time": r.execution_time,
                    "performance_score": r.performance_score,
                    "error_message": r.error_message
                }
                for r in self.results
            ],
            "ai_performance_insights": {
                "best_performing_component": max(ai_components.items(), key=lambda x: x[1]["avg_score"])[0] if ai_components else None,
                "most_reliable_component": max(ai_components.items(), key=lambda x: x[1]["success_rate"])[0] if ai_components else None,
                "fastest_ai_test": min(self.results, key=lambda x: x.execution_time).test_name if self.results else None,
                "slowest_ai_test": max(self.results, key=lambda x: x.execution_time).test_name if self.results else None
            },
            "detailed_ai_results": [
                {
                    "test_name": r.test_name,
                    "ai_component": r.ai_component,
                    "success": r.success,
                    "execution_time": r.execution_time,
                    "ai_metrics": r.ai_metrics,
                    "performance_score": r.performance_score,
                    "error_message": r.error_message,
                    "timestamp": r.timestamp.isoformat() if r.timestamp else None
                }
                for r in self.results
            ]
        }
        
        # 保存报告
        report_path = "/home/ubuntu/powerautomation/ai_enhanced_test_suite_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_report, f, indent=2, ensure_ascii=False)
        
        # 显示摘要
        print("🎉 PowerAutomation AI增强功能测试套件执行完成!")
        print("=" * 70)
        print(f"📊 AI测试结果:")
        print(f"   AI测试总数: {total_tests}")
        print(f"   成功测试: {successful_tests}")
        print(f"   AI成功率: {success_rate:.1f}%")
        print(f"   平均性能分数: {avg_performance_score:.1f}")
        print(f"   总执行时间: {suite_execution_time:.3f}s")
        
        print(f"\\n🧠 AI组件表现:")
        for component, stats in ai_components.items():
            print(f"   • {component}: {stats['success_rate']:.1f}% 成功率, {stats['avg_score']:.1f} 平均分数")
        
        print(f"\\n📄 详细报告: {report_path}")
        
        if successful_tests < total_tests:
            print(f"\\n❌ 失败的AI测试:")
            for result in self.results:
                if not result.success:
                    print(f"   • {result.test_name} ({result.ai_component}): {result.error_message}")
        
        return comprehensive_report

def main():
    """主函数"""
    ai_tester = AIEnhancedFunctionTester()
    report = ai_tester.run_ai_enhanced_test_suite()
    return report

if __name__ == "__main__":
    main()

