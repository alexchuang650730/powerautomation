#!/usr/bin/env python3
"""
真实API验证系统优化版本
增加更多公开API端点进行测试，并优化验证逻辑
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
    expected_status: int = 200

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

class EnhancedAPIValidator:
    """增强版真实API验证器"""
    
    def __init__(self):
        self.db_path = "/home/ubuntu/powerautomation/enhanced_api_validation.db"
        self.init_database()
        
        # 配置更多真实的API端点
        self.endpoints = self._configure_enhanced_endpoints()
        
        # 验证结果存储
        self.results: List[ValidationResult] = []
        
    def _configure_enhanced_endpoints(self) -> List[APIEndpoint]:
        """配置增强的API端点列表"""
        
        endpoints = [
            # 基础连接测试
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
            
            # JSONPlaceholder API
            APIEndpoint(
                name="jsonplaceholder_posts",
                url="https://jsonplaceholder.typicode.com/posts/1",
                method="GET",
                headers={"Content-Type": "application/json"},
                auth_required=False
            ),
            
            APIEndpoint(
                name="jsonplaceholder_users",
                url="https://jsonplaceholder.typicode.com/users",
                method="GET",
                headers={"Content-Type": "application/json"},
                auth_required=False
            ),
            
            # GitHub API (公开端点)
            APIEndpoint(
                name="github_user",
                url="https://api.github.com/users/octocat",
                method="GET",
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "PowerAutomation-Validator/1.0"
                },
                auth_required=False
            ),
            
            # REST Countries API
            APIEndpoint(
                name="rest_countries",
                url="https://restcountries.com/v3.1/name/china",
                method="GET",
                headers={"Content-Type": "application/json"},
                auth_required=False
            ),
            
            # Cat Facts API
            APIEndpoint(
                name="cat_facts",
                url="https://catfact.ninja/fact",
                method="GET",
                headers={"Content-Type": "application/json"},
                auth_required=False
            ),
            
            # IP Info API
            APIEndpoint(
                name="ip_info",
                url="https://ipapi.co/json/",
                method="GET",
                headers={"User-Agent": "PowerAutomation-Validator/1.0"},
                auth_required=False
            ),
            
            # Weather API (OpenWeatherMap - 需要API key但有免费层)
            APIEndpoint(
                name="weather_api",
                url="https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo",
                method="GET",
                headers={"Content-Type": "application/json"},
                auth_required=False,
                expected_status=401  # 预期会失败，因为使用demo key
            ),
            
            # Supermemory API (需要有效密钥)
            APIEndpoint(
                name="supermemory_list_memories",
                url="https://api.supermemory.ai/v3/memories",
                method="GET",
                headers={
                    "Authorization": f"Bearer {os.getenv('SUPERMEMORY_API_KEY', 'test-key')}",
                    "Content-Type": "application/json"
                },
                expected_status=401  # 预期会失败，除非有有效密钥
            )
        ]
        
        return endpoints
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_api_results (
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
        logger.info("增强版数据库初始化完成")
    
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
            if endpoint.name == "httpbin_post":
                kwargs['json'] = {
                    "test": "data",
                    "timestamp": datetime.now().isoformat(),
                    "validator": "PowerAutomation"
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
            
            # 判断成功条件 - 考虑预期状态码
            if endpoint.expected_status != 200:
                success = response.status_code == endpoint.expected_status
            else:
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
            
            status_emoji = "✅" if success else "❌"
            logger.info(f"{status_emoji} {endpoint.name}: {response_time:.3f}s (HTTP {response.status_code})")
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
            
            logger.error(f"❌ {endpoint.name}: {error_message}")
            return result
    
    def save_result(self, result: ValidationResult):
        """保存验证结果到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO enhanced_api_results 
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
        logger.info(f"🔍 验证: {endpoint.name}")
        
        result = self.make_api_call(endpoint)
        self.save_result(result)
        self.results.append(result)
        
        return result
    
    def validate_all_endpoints(self, max_workers: int = 5) -> List[ValidationResult]:
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
    
    def run_stress_test(self, endpoint_names: List[str], duration_seconds: int = 30, concurrent_users: int = 3):
        """对指定端点进行压力测试"""
        logger.info(f"🔥 开始压力测试: {len(endpoint_names)}个端点, {concurrent_users}并发, {duration_seconds}秒")
        
        all_results = []
        
        for endpoint_name in endpoint_names:
            endpoint = next((ep for ep in self.endpoints if ep.name == endpoint_name), None)
            if not endpoint:
                logger.warning(f"未找到端点: {endpoint_name}")
                continue
            
            logger.info(f"🎯 压力测试: {endpoint_name}")
            
            start_time = time.time()
            results = []
            
            def worker():
                while time.time() - start_time < duration_seconds:
                    result = self.make_api_call(endpoint)
                    results.append(result)
                    time.sleep(0.2)  # 控制请求频率
            
            threads = []
            for _ in range(concurrent_users):
                thread = threading.Thread(target=worker)
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
            
            # 分析结果
            if results:
                success_count = sum(1 for r in results if r.success)
                total_requests = len(results)
                success_rate = success_count / total_requests * 100
                
                response_times = [r.response_time for r in results if r.success]
                if response_times:
                    avg_response_time = statistics.mean(response_times)
                    min_response_time = min(response_times)
                    max_response_time = max(response_times)
                    
                    logger.info(f"📊 {endpoint_name} 压力测试结果:")
                    logger.info(f"   总请求: {total_requests}, 成功率: {success_rate:.1f}%")
                    logger.info(f"   响应时间: 平均{avg_response_time:.3f}s, 最小{min_response_time:.3f}s, 最大{max_response_time:.3f}s")
                
                all_results.extend(results)
        
        return all_results
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """生成综合验证报告"""
        if not self.results:
            return {"error": "没有验证结果"}
        
        total_endpoints = len(self.results)
        successful_endpoints = sum(1 for r in self.results if r.success)
        success_rate = successful_endpoints / total_endpoints * 100
        
        response_times = [r.response_time for r in self.results if r.success]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        # 按成功/失败分类
        successful_results = [r for r in self.results if r.success]
        failed_results = [r for r in self.results if not r.success]
        
        # 性能分析
        performance_analysis = {}
        if response_times:
            performance_analysis = {
                "fastest_endpoint": min(successful_results, key=lambda x: x.response_time).endpoint_name,
                "slowest_endpoint": max(successful_results, key=lambda x: x.response_time).endpoint_name,
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "median_response_time": statistics.median(response_times)
            }
        
        report = {
            "validation_summary": {
                "total_endpoints": total_endpoints,
                "successful_endpoints": successful_endpoints,
                "failed_endpoints": len(failed_results),
                "success_rate": success_rate,
                "average_response_time": avg_response_time,
                "timestamp": datetime.now().isoformat()
            },
            "performance_analysis": performance_analysis,
            "successful_endpoints": [
                {
                    "name": r.endpoint_name,
                    "response_time": r.response_time,
                    "status_code": r.status_code
                }
                for r in successful_results
            ],
            "failed_endpoints": [
                {
                    "name": r.endpoint_name,
                    "error": r.error_message,
                    "status_code": r.status_code,
                    "response_time": r.response_time
                }
                for r in failed_results
            ],
            "detailed_results": [
                {
                    "name": r.endpoint_name,
                    "success": r.success,
                    "response_time": r.response_time,
                    "status_code": r.status_code,
                    "error_message": r.error_message,
                    "timestamp": r.timestamp.isoformat() if r.timestamp else None
                }
                for r in self.results
            ]
        }
        
        return report

def main():
    """主函数"""
    print("🌐 PowerAutomation 增强版真实API验证系统")
    print("=" * 70)
    
    validator = EnhancedAPIValidator()
    
    # 第一阶段: 基础验证
    print("🔍 第一阶段: 基础API连通性验证")
    results = validator.validate_all_endpoints()
    
    # 第二阶段: 压力测试
    print("\n🔥 第二阶段: 压力测试")
    successful_endpoints = [r.endpoint_name for r in results if r.success]
    
    if successful_endpoints:
        # 选择前3个成功的端点进行压力测试
        test_endpoints = successful_endpoints[:3]
        stress_results = validator.run_stress_test(test_endpoints, duration_seconds=20, concurrent_users=2)
    
    # 第三阶段: 生成报告
    print("\n📊 第三阶段: 生成综合报告")
    report = validator.generate_comprehensive_report()
    
    # 保存报告
    report_path = "/home/ubuntu/powerautomation/enhanced_api_validation_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # 显示摘要
    summary = report["validation_summary"]
    print(f"\n✅ 验证完成!")
    print(f"📈 成功率: {summary['success_rate']:.1f}% ({summary['successful_endpoints']}/{summary['total_endpoints']})")
    print(f"⏱️  平均响应时间: {summary['average_response_time']:.3f}s")
    
    if "performance_analysis" in report and report["performance_analysis"]:
        perf = report["performance_analysis"]
        print(f"🚀 最快端点: {perf.get('fastest_endpoint', 'N/A')}")
        print(f"🐌 最慢端点: {perf.get('slowest_endpoint', 'N/A')}")
    
    print(f"📄 详细报告: {report_path}")
    
    if report["failed_endpoints"]:
        print(f"\n❌ 失败的端点 ({len(report['failed_endpoints'])}个):")
        for failed in report["failed_endpoints"]:
            print(f"   • {failed['name']}: {failed['error'][:100]}...")

if __name__ == "__main__":
    main()

