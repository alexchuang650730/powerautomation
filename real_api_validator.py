#!/usr/bin/env python3
"""
真实API验证系统 - 集成supermemory API
支持真实的API调用和验证
"""

import requests
import json
import time
import logging
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class APIEndpoint:
    """API端点配置"""
    name: str
    url: str
    method: str
    headers: Dict[str, str]
    auth_required: bool = True
    timeout: int = 30

@dataclass
class ValidationResult:
    """验证结果"""
    endpoint_name: str
    success: bool
    response_time: float
    status_code: int
    error_message: Optional[str] = None
    response_data: Optional[Dict] = None
    timestamp: datetime = None

class RealAPIValidator:
    """真实API验证器"""
    
    def __init__(self):
        self.db_path = "/home/ubuntu/powerautomation/real_api_validation.db"
        self.init_database()
        
        # 配置真实的API端点
        self.endpoints = self._configure_endpoints()
        
        # 验证结果存储
        self.results: List[ValidationResult] = []
        
    def _configure_endpoints(self) -> List[APIEndpoint]:
        """配置真实的API端点"""
        
        # 从环境变量获取API密钥
        supermemory_api_key = os.getenv('SUPERMEMORY_API_KEY', 'test-key')
        openai_api_key = os.getenv('OPENAI_API_KEY', 'test-key')
        
        endpoints = [
            # Supermemory Memory API
            APIEndpoint(
                name="supermemory_list_memories",
                url="https://api.supermemory.ai/v3/memories",
                method="GET",
                headers={
                    "Authorization": f"Bearer {supermemory_api_key}",
                    "Content-Type": "application/json"
                }
            ),
            
            # Supermemory Model Enhancement (OpenAI proxy)
            APIEndpoint(
                name="supermemory_openai_chat",
                url="https://api.supermemory.ai/v3/https://api.openai.com/v1/chat/completions",
                method="POST",
                headers={
                    "Authorization": f"Bearer {openai_api_key}",
                    "x-api-key": supermemory_api_key,
                    "Content-Type": "application/json"
                }
            ),
            
            # Supermemory Search API
            APIEndpoint(
                name="supermemory_search",
                url="https://api.supermemory.ai/v3/search",
                method="POST",
                headers={
                    "Authorization": f"Bearer {supermemory_api_key}",
                    "Content-Type": "application/json"
                }
            ),
            
            # 公开API端点用于基础连接测试
            APIEndpoint(
                name="httpbin_get",
                url="https://httpbin.org/get",
                method="GET",
                headers={"User-Agent": "PowerAutomation-Validator/1.0"},
                auth_required=False
            ),
            
            APIEndpoint(
                name="httpbin_post",
                url="https://httpbin.org/post",
                method="POST",
                headers={
                    "User-Agent": "PowerAutomation-Validator/1.0",
                    "Content-Type": "application/json"
                },
                auth_required=False
            ),
            
            # JSONPlaceholder API for testing
            APIEndpoint(
                name="jsonplaceholder_posts",
                url="https://jsonplaceholder.typicode.com/posts/1",
                method="GET",
                headers={"Content-Type": "application/json"},
                auth_required=False
            )
        ]
        
        return endpoints
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_validation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint_name TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                response_time REAL NOT NULL,
                status_code INTEGER,
                error_message TEXT,
                response_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("数据库初始化完成")
    
    def make_api_call(self, endpoint: APIEndpoint, payload: Optional[Dict] = None) -> ValidationResult:
        """执行真实的API调用"""
        start_time = time.time()
        
        try:
            # 准备请求参数
            kwargs = {
                'url': endpoint.url,
                'headers': endpoint.headers,
                'timeout': endpoint.timeout
            }
            
            # 根据端点准备特定的payload
            if endpoint.name == "supermemory_openai_chat":
                kwargs['json'] = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "user", "content": "Hello, this is a test message for API validation."}
                    ],
                    "max_tokens": 50
                }
            elif endpoint.name == "supermemory_search":
                kwargs['json'] = {
                    "query": "test search query",
                    "limit": 5
                }
            elif endpoint.name == "httpbin_post":
                kwargs['json'] = {
                    "test": "data",
                    "timestamp": datetime.now().isoformat()
                }
            elif payload:
                kwargs['json'] = payload
            
            # 执行HTTP请求
            if endpoint.method.upper() == "GET":
                response = requests.get(**{k: v for k, v in kwargs.items() if k != 'json'})
            elif endpoint.method.upper() == "POST":
                response = requests.post(**kwargs)
            elif endpoint.method.upper() == "PUT":
                response = requests.put(**kwargs)
            elif endpoint.method.upper() == "DELETE":
                response = requests.delete(**{k: v for k, v in kwargs.items() if k != 'json'})
            else:
                raise ValueError(f"不支持的HTTP方法: {endpoint.method}")
            
            response_time = time.time() - start_time
            
            # 解析响应
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text[:500]}
            
            # 判断成功条件
            success = response.status_code < 400
            error_message = None if success else f"HTTP {response.status_code}: {response.text[:200]}"
            
            result = ValidationResult(
                endpoint_name=endpoint.name,
                success=success,
                response_time=response_time,
                status_code=response.status_code,
                error_message=error_message,
                response_data=response_data,
                timestamp=datetime.now()
            )
            
            logger.info(f"API调用完成: {endpoint.name} - 成功: {success} - 响应时间: {response_time:.3f}s")
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            error_message = str(e)
            
            result = ValidationResult(
                endpoint_name=endpoint.name,
                success=False,
                response_time=response_time,
                status_code=0,
                error_message=error_message,
                timestamp=datetime.now()
            )
            
            logger.error(f"API调用失败: {endpoint.name} - 错误: {error_message}")
            return result
    
    def save_result(self, result: ValidationResult):
        """保存验证结果到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_validation_results 
            (endpoint_name, success, response_time, status_code, error_message, response_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.endpoint_name,
            result.success,
            result.response_time,
            result.status_code,
            result.error_message,
            json.dumps(result.response_data) if result.response_data else None,
            result.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def validate_single_endpoint(self, endpoint: APIEndpoint) -> ValidationResult:
        """验证单个API端点"""
        logger.info(f"🔍 开始验证API端点: {endpoint.name}")
        
        result = self.make_api_call(endpoint)
        self.save_result(result)
        self.results.append(result)
        
        status = "✅" if result.success else "❌"
        logger.info(f"{status} {endpoint.name}: {result.response_time:.3f}s")
        
        return result
    
    def validate_all_endpoints(self, max_workers: int = 3) -> List[ValidationResult]:
        """并发验证所有API端点"""
        logger.info(f"🚀 开始验证 {len(self.endpoints)} 个API端点")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_endpoint = {
                executor.submit(self.validate_single_endpoint, endpoint): endpoint 
                for endpoint in self.endpoints
            }
            
            for future in future_to_endpoint:
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    endpoint = future_to_endpoint[future]
                    logger.error(f"验证端点 {endpoint.name} 时发生异常: {e}")
        
        return results
    
    def run_load_test(self, endpoint_name: str, duration_seconds: int = 60, concurrent_users: int = 5):
        """对指定端点进行负载测试"""
        endpoint = next((ep for ep in self.endpoints if ep.name == endpoint_name), None)
        if not endpoint:
            logger.error(f"未找到端点: {endpoint_name}")
            return
        
        logger.info(f"🔥 开始负载测试: {endpoint_name} - {concurrent_users}并发用户, {duration_seconds}秒")
        
        start_time = time.time()
        results = []
        
        def worker():
            while time.time() - start_time < duration_seconds:
                result = self.make_api_call(endpoint)
                results.append(result)
                time.sleep(0.1)  # 避免过于频繁的请求
        
        threads = []
        for _ in range(concurrent_users):
            thread = threading.Thread(target=worker)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        # 分析负载测试结果
        if results:
            success_count = sum(1 for r in results if r.success)
            total_requests = len(results)
            success_rate = success_count / total_requests * 100
            
            response_times = [r.response_time for r in results if r.success]
            if response_times:
                avg_response_time = statistics.mean(response_times)
                p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
                
                logger.info(f"📊 负载测试结果:")
                logger.info(f"   总请求数: {total_requests}")
                logger.info(f"   成功率: {success_rate:.1f}%")
                logger.info(f"   平均响应时间: {avg_response_time:.3f}s")
                logger.info(f"   P95响应时间: {p95_response_time:.3f}s")
        
        return results
    
    def generate_report(self) -> Dict[str, Any]:
        """生成验证报告"""
        if not self.results:
            return {"error": "没有验证结果"}
        
        total_endpoints = len(self.results)
        successful_endpoints = sum(1 for r in self.results if r.success)
        success_rate = successful_endpoints / total_endpoints * 100
        
        response_times = [r.response_time for r in self.results if r.success]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        failed_endpoints = [r for r in self.results if not r.success]
        
        report = {
            "validation_summary": {
                "total_endpoints": total_endpoints,
                "successful_endpoints": successful_endpoints,
                "success_rate": success_rate,
                "average_response_time": avg_response_time,
                "timestamp": datetime.now().isoformat()
            },
            "endpoint_results": [
                {
                    "name": r.endpoint_name,
                    "success": r.success,
                    "response_time": r.response_time,
                    "status_code": r.status_code,
                    "error_message": r.error_message
                }
                for r in self.results
            ],
            "failed_endpoints": [
                {
                    "name": r.endpoint_name,
                    "error": r.error_message,
                    "status_code": r.status_code
                }
                for r in failed_endpoints
            ]
        }
        
        return report

def main():
    """主函数"""
    print("🌐 PowerAutomation 真实API验证系统")
    print("=" * 60)
    
    validator = RealAPIValidator()
    
    # 1. 验证所有端点
    print("🔍 第一阶段: 基础API连通性验证")
    results = validator.validate_all_endpoints()
    
    # 2. 对成功的端点进行负载测试
    print("\n🔥 第二阶段: 负载测试")
    successful_endpoints = [r.endpoint_name for r in results if r.success]
    
    for endpoint_name in successful_endpoints[:2]:  # 只测试前2个成功的端点
        validator.run_load_test(endpoint_name, duration_seconds=30, concurrent_users=3)
    
    # 3. 生成报告
    print("\n📊 第三阶段: 生成验证报告")
    report = validator.generate_report()
    
    # 保存报告
    report_path = "/home/ubuntu/powerautomation/real_api_validation_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 显示摘要
    summary = report["validation_summary"]
    print(f"\n✅ 验证完成!")
    print(f"📈 成功率: {summary['success_rate']:.1f}% ({summary['successful_endpoints']}/{summary['total_endpoints']})")
    print(f"⏱️  平均响应时间: {summary['average_response_time']:.3f}s")
    print(f"📄 详细报告: {report_path}")
    
    if report["failed_endpoints"]:
        print(f"\n❌ 失败的端点:")
        for failed in report["failed_endpoints"]:
            print(f"   • {failed['name']}: {failed['error']}")

if __name__ == "__main__":
    main()

