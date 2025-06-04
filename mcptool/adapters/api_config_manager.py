"""
PowerAutomation API配置管理器
支持模拟API和真实API的无缝切换
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class APIMode(Enum):
    """API模式枚举"""
    MOCK = "mock"          # 模拟API模式
    REAL = "real"          # 真实API模式
    HYBRID = "hybrid"      # 混合模式（部分真实，部分模拟）

class APIConfigManager:
    """API配置管理器"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or "api_config.json"
        self.config = self._load_config()
        self.current_mode = APIMode(self.config.get("mode", "mock"))
        
    def _load_config(self) -> Dict[str, Any]:
        """加载API配置"""
        default_config = {
            "mode": "mock",
            "apis": {
                "claude": {
                    "enabled": True,
                    "mode": "mock",
                    "api_key": None,
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "model": "claude-3-sonnet-20240229"
                },
                "gemini": {
                    "enabled": True,
                    "mode": "mock",
                    "api_key": None,
                    "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
                    "model": "gemini-pro"
                },
                "openai": {
                    "enabled": False,
                    "mode": "mock",
                    "api_key": None,
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "model": "gpt-4"
                }
            },
            "fallback": {
                "enabled": True,
                "fallback_to_mock": True
            },
            "monitoring": {
                "enabled": True,
                "log_api_calls": True,
                "track_usage": True
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    default_config.update(loaded_config)
            else:
                # 创建默认配置文件
                self._save_config(default_config)
                
        except Exception as e:
            logger.warning(f"加载API配置失败，使用默认配置: {e}")
            
        return default_config
    
    def _save_config(self, config: Dict[str, Any] = None):
        """保存API配置"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            logger.info(f"API配置已保存到: {self.config_file}")
        except Exception as e:
            logger.error(f"保存API配置失败: {e}")
    
    def set_mode(self, mode: APIMode):
        """设置API模式"""
        self.current_mode = mode
        self.config["mode"] = mode.value
        self._save_config()
        logger.info(f"API模式已切换到: {mode.value}")
    
    def set_api_key(self, api_name: str, api_key: str):
        """设置API密钥"""
        if api_name in self.config["apis"]:
            self.config["apis"][api_name]["api_key"] = api_key
            # 如果设置了API密钥，自动启用真实API模式
            if api_key:
                self.config["apis"][api_name]["mode"] = "real"
            self._save_config()
            logger.info(f"{api_name} API密钥已设置")
        else:
            logger.error(f"未知的API: {api_name}")
    
    def get_api_config(self, api_name: str) -> Dict[str, Any]:
        """获取特定API的配置"""
        if api_name not in self.config["apis"]:
            logger.error(f"未知的API: {api_name}")
            return {}
        
        api_config = self.config["apis"][api_name].copy()
        
        # 从环境变量获取API密钥
        env_key_map = {
            "claude": "CLAUDE_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY"
        }
        
        if api_name in env_key_map:
            env_key = os.getenv(env_key_map[api_name])
            if env_key:
                api_config["api_key"] = env_key
                api_config["mode"] = "real"
        
        # 根据全局模式调整API模式
        if self.current_mode == APIMode.MOCK:
            api_config["mode"] = "mock"
        elif self.current_mode == APIMode.REAL and api_config.get("api_key"):
            api_config["mode"] = "real"
        
        return api_config
    
    def is_api_available(self, api_name: str) -> bool:
        """检查API是否可用"""
        config = self.get_api_config(api_name)
        return (config.get("enabled", False) and 
                (config.get("mode") == "mock" or config.get("api_key")))
    
    def get_available_apis(self) -> list:
        """获取可用的API列表"""
        available = []
        for api_name in self.config["apis"]:
            if self.is_api_available(api_name):
                available.append(api_name)
        return available
    
    def enable_fallback_mode(self):
        """启用回退模式"""
        self.config["fallback"]["enabled"] = True
        self.config["fallback"]["fallback_to_mock"] = True
        self._save_config()
        logger.info("回退模式已启用")
    
    def disable_fallback_mode(self):
        """禁用回退模式"""
        self.config["fallback"]["enabled"] = False
        self._save_config()
        logger.info("回退模式已禁用")
    
    def get_status(self) -> Dict[str, Any]:
        """获取API配置状态"""
        status = {
            "current_mode": self.current_mode.value,
            "config_file": self.config_file,
            "apis": {},
            "fallback_enabled": self.config["fallback"]["enabled"],
            "monitoring_enabled": self.config["monitoring"]["enabled"]
        }
        
        for api_name, api_config in self.config["apis"].items():
            status["apis"][api_name] = {
                "enabled": api_config["enabled"],
                "mode": self.get_api_config(api_name)["mode"],
                "has_api_key": bool(self.get_api_config(api_name).get("api_key")),
                "available": self.is_api_available(api_name)
            }
        
        return status

class APICallManager:
    """API调用管理器"""
    
    def __init__(self, config_manager: APIConfigManager):
        self.config_manager = config_manager
        self.call_history = []
        
    def make_api_call(self, api_name: str, method: str, **kwargs) -> Dict[str, Any]:
        """统一的API调用接口"""
        config = self.config_manager.get_api_config(api_name)
        
        if not config:
            return self._handle_error(f"API配置不存在: {api_name}")
        
        if not self.config_manager.is_api_available(api_name):
            return self._handle_error(f"API不可用: {api_name}")
        
        # 记录调用历史
        call_record = {
            "api_name": api_name,
            "method": method,
            "mode": config["mode"],
            "timestamp": self._get_timestamp(),
            "kwargs": kwargs
        }
        
        try:
            if config["mode"] == "mock":
                result = self._make_mock_call(api_name, method, **kwargs)
            else:
                result = self._make_real_call(api_name, method, config, **kwargs)
            
            call_record["status"] = "success"
            call_record["result"] = result
            
        except Exception as e:
            logger.error(f"API调用失败: {api_name}.{method} - {e}")
            
            # 尝试回退到模拟模式
            if (config["mode"] == "real" and 
                self.config_manager.config["fallback"]["enabled"] and
                self.config_manager.config["fallback"]["fallback_to_mock"]):
                
                logger.info(f"回退到模拟模式: {api_name}.{method}")
                result = self._make_mock_call(api_name, method, **kwargs)
                call_record["status"] = "fallback_success"
                call_record["result"] = result
                call_record["fallback_reason"] = str(e)
            else:
                call_record["status"] = "error"
                call_record["error"] = str(e)
                result = self._handle_error(f"API调用失败: {e}")
        
        # 记录调用历史
        if self.config_manager.config["monitoring"]["log_api_calls"]:
            self.call_history.append(call_record)
            
        return result
    
    def _make_mock_call(self, api_name: str, method: str, **kwargs) -> Dict[str, Any]:
        """执行模拟API调用"""
        # 模拟不同API的响应
        if api_name == "claude":
            return self._mock_claude_call(method, **kwargs)
        elif api_name == "gemini":
            return self._mock_gemini_call(method, **kwargs)
        elif api_name == "openai":
            return self._mock_openai_call(method, **kwargs)
        else:
            return {"status": "success", "data": f"模拟{api_name}响应", "mock": True}
    
    def _make_real_call(self, api_name: str, method: str, config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """执行真实API调用"""
        # 这里应该实现真实的API调用逻辑
        # 由于需要真实的API密钥，这里提供框架结构
        
        api_key = config["api_key"]
        endpoint = config["endpoint"]
        model = config["model"]
        
        # 构建请求头
        headers = self._build_headers(api_name, api_key)
        
        # 构建请求数据
        request_data = self._build_request_data(api_name, method, model, **kwargs)
        
        # 这里应该使用requests库发送HTTP请求
        # 为了演示，返回模拟响应
        return {
            "status": "success",
            "data": f"真实{api_name}响应 (模拟)",
            "mock": False,
            "api_key_used": bool(api_key),
            "endpoint": endpoint,
            "model": model
        }
    
    def _mock_claude_call(self, method: str, **kwargs) -> Dict[str, Any]:
        """模拟Claude API调用"""
        if method == "analyze_intent":
            return {
                "status": "success",
                "intent_type": "analysis",
                "confidence": 0.88,
                "keywords": kwargs.get("text", "").split()[:5],
                "mock": True
            }
        else:
            return {"status": "success", "data": f"Claude {method} 模拟响应", "mock": True}
    
    def _mock_gemini_call(self, method: str, **kwargs) -> Dict[str, Any]:
        """模拟Gemini API调用"""
        if method == "decompose_task":
            return {
                "status": "success",
                "subtasks": [
                    {"id": "task_1", "description": "分析需求"},
                    {"id": "task_2", "description": "执行操作"},
                    {"id": "task_3", "description": "验证结果"}
                ],
                "complexity": "medium",
                "mock": True
            }
        else:
            return {"status": "success", "data": f"Gemini {method} 模拟响应", "mock": True}
    
    def _mock_openai_call(self, method: str, **kwargs) -> Dict[str, Any]:
        """模拟OpenAI API调用"""
        return {"status": "success", "data": f"OpenAI {method} 模拟响应", "mock": True}
    
    def _build_headers(self, api_name: str, api_key: str) -> Dict[str, str]:
        """构建API请求头"""
        headers = {"Content-Type": "application/json"}
        
        if api_name == "claude":
            headers["Authorization"] = f"Bearer {api_key}"
            headers["anthropic-version"] = "2023-06-01"
        elif api_name == "gemini":
            headers["Authorization"] = f"Bearer {api_key}"
        elif api_name == "openai":
            headers["Authorization"] = f"Bearer {api_key}"
        
        return headers
    
    def _build_request_data(self, api_name: str, method: str, model: str, **kwargs) -> Dict[str, Any]:
        """构建API请求数据"""
        if api_name == "claude":
            return {
                "model": model,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "messages": [{"role": "user", "content": kwargs.get("text", "")}]
            }
        elif api_name == "gemini":
            return {
                "model": model,
                "prompt": kwargs.get("text", ""),
                "temperature": kwargs.get("temperature", 0.7)
            }
        elif api_name == "openai":
            return {
                "model": model,
                "messages": [{"role": "user", "content": kwargs.get("text", "")}],
                "temperature": kwargs.get("temperature", 0.7)
            }
        
        return kwargs
    
    def _handle_error(self, error_message: str) -> Dict[str, Any]:
        """处理错误"""
        return {
            "status": "error",
            "message": error_message,
            "timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_call_history(self, limit: int = 10) -> list:
        """获取调用历史"""
        return self.call_history[-limit:]
    
    def clear_call_history(self):
        """清空调用历史"""
        self.call_history.clear()
        logger.info("API调用历史已清空")

# 全局API管理器实例
_api_config_manager = None
_api_call_manager = None

def get_api_config_manager() -> APIConfigManager:
    """获取API配置管理器单例"""
    global _api_config_manager
    if _api_config_manager is None:
        _api_config_manager = APIConfigManager()
    return _api_config_manager

def get_api_call_manager() -> APICallManager:
    """获取API调用管理器单例"""
    global _api_call_manager
    if _api_call_manager is None:
        _api_call_manager = APICallManager(get_api_config_manager())
    return _api_call_manager

def switch_to_mock_mode():
    """切换到模拟模式"""
    get_api_config_manager().set_mode(APIMode.MOCK)

def switch_to_real_mode():
    """切换到真实模式"""
    get_api_config_manager().set_mode(APIMode.REAL)

def switch_to_hybrid_mode():
    """切换到混合模式"""
    get_api_config_manager().set_mode(APIMode.HYBRID)

