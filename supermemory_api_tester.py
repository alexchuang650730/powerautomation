#!/usr/bin/env python3
"""
Supermemory API 真实验证测试
使用提供的真实API密钥测试supermemory API
"""

import requests
import json
import time
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupermemoryAPITester:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.supermemory.ai/v3"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def test_list_memories(self):
        """测试获取记忆列表"""
        url = f"{self.base_url}/memories"
        
        try:
            start_time = time.time()
            response = requests.get(url, headers=self.headers, timeout=30)
            response_time = time.time() - start_time
            
            logger.info(f"📋 List Memories API:")
            logger.info(f"   状态码: {response.status_code}")
            logger.info(f"   响应时间: {response_time:.3f}s")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"   ✅ 成功! 返回 {len(data.get('memories', []))} 条记忆")
                return True, data
            else:
                logger.error(f"   ❌ 失败: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"   ❌ 异常: {str(e)}")
            return False, str(e)
    
    def test_add_memory(self):
        """测试添加记忆"""
        url = f"{self.base_url}/memories"
        
        payload = {
            "title": "PowerAutomation API测试",
            "content": "这是一个来自PowerAutomation真实API验证系统的测试记忆。",
            "metadata": {
                "source": "PowerAutomation",
                "category": "API测试",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        try:
            start_time = time.time()
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response_time = time.time() - start_time
            
            logger.info(f"➕ Add Memory API:")
            logger.info(f"   状态码: {response.status_code}")
            logger.info(f"   响应时间: {response_time:.3f}s")
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"   ✅ 成功! 记忆ID: {data.get('id', 'N/A')}")
                return True, data
            else:
                logger.error(f"   ❌ 失败: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"   ❌ 异常: {str(e)}")
            return False, str(e)
    
    def test_search_memories(self):
        """测试搜索记忆"""
        url = f"{self.base_url}/search"
        
        payload = {
            "query": "PowerAutomation",
            "limit": 5
        }
        
        try:
            start_time = time.time()
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response_time = time.time() - start_time
            
            logger.info(f"🔍 Search Memories API:")
            logger.info(f"   状态码: {response.status_code}")
            logger.info(f"   响应时间: {response_time:.3f}s")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                logger.info(f"   ✅ 成功! 找到 {len(results)} 条相关记忆")
                return True, data
            else:
                logger.error(f"   ❌ 失败: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"   ❌ 异常: {str(e)}")
            return False, str(e)
    
    def test_model_enhancement(self):
        """测试模型增强功能 (OpenAI代理)"""
        url = f"{self.base_url}/https://api.openai.com/v1/chat/completions"
        
        # 注意：这需要OpenAI API密钥
        headers = {
            "Authorization": "Bearer sk-test-key",  # 使用测试密钥
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Hello, this is a test from PowerAutomation API validator."}
            ],
            "max_tokens": 50
        }
        
        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response_time = time.time() - start_time
            
            logger.info(f"🤖 Model Enhancement API:")
            logger.info(f"   状态码: {response.status_code}")
            logger.info(f"   响应时间: {response_time:.3f}s")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"   ✅ 成功! 模型增强功能正常")
                return True, data
            else:
                logger.error(f"   ❌ 失败: {response.text}")
                return False, response.text
                
        except Exception as e:
            logger.error(f"   ❌ 异常: {str(e)}")
            return False, str(e)
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        logger.info("🌐 开始Supermemory API综合测试")
        logger.info("=" * 60)
        
        results = {}
        
        # 测试1: 获取记忆列表
        success, data = self.test_list_memories()
        results['list_memories'] = {'success': success, 'data': data}
        
        print()
        
        # 测试2: 添加记忆
        success, data = self.test_add_memory()
        results['add_memory'] = {'success': success, 'data': data}
        
        print()
        
        # 测试3: 搜索记忆
        success, data = self.test_search_memories()
        results['search_memories'] = {'success': success, 'data': data}
        
        print()
        
        # 测试4: 模型增强 (预期会失败，因为没有有效的OpenAI密钥)
        success, data = self.test_model_enhancement()
        results['model_enhancement'] = {'success': success, 'data': data}
        
        # 生成测试报告
        print("\n📊 测试结果摘要:")
        print("=" * 40)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results.values() if r['success'])
        success_rate = successful_tests / total_tests * 100
        
        print(f"总测试数: {total_tests}")
        print(f"成功测试: {successful_tests}")
        print(f"成功率: {success_rate:.1f}%")
        
        print("\n详细结果:")
        for test_name, result in results.items():
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {test_name}")
        
        # 保存详细报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "api_key_used": f"{self.api_key[:10]}...{self.api_key[-10:]}",
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": success_rate
            },
            "detailed_results": results
        }
        
        report_path = "/home/ubuntu/powerautomation/supermemory_api_test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 详细报告已保存: {report_path}")
        
        return results

def main():
    # 使用提供的API密钥
    api_key = ""SUPERMEMORY_API_KEY_PLACEHOLDER""
    
    tester = SupermemoryAPITester(api_key)
    results = tester.run_comprehensive_test()
    
    return results

if __name__ == "__main__":
    main()

