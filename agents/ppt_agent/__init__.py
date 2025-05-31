"""
PPT智能体入口模块

提供PPT智能体的主要功能和参数化调用接口
"""

import os
import logging
import json
from typing import Dict, Any, List, Optional

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PPTAgentInterface:
    """PPT智能体接口类，提供参数化调用方法"""
    
    def __init__(self, config_path: str = None):
        """
        初始化PPT智能体接口
        
        参数:
            config_path: 配置文件路径，如果不提供则使用默认配置
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = self._load_config(config_path)
        
        # 导入核心实现
        from .core.ppt_agent import PPTAgent
        self.agent = PPTAgent()
        
        self.logger.info("PPT智能体接口初始化完成")
    
    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """
        加载配置文件
        
        参数:
            config_path: 配置文件路径
            
        返回:
            配置字典
        """
        default_config = {
            "template_dir": os.path.join(os.path.dirname(__file__), "templates"),
            "output_dir": os.path.join(os.path.dirname(__file__), "output"),
            "default_template": "专业简历.pptx"
        }
        
        if not config_path:
            return default_config
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # 合并配置
                default_config.update(user_config)
                return default_config
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {str(e)}")
            return default_config
    
    def process(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理PPT生成请求
        
        参数:
            params: 参数字典，包含任务类型和相关参数
            
        返回:
            处理结果字典
        """
        self.logger.info(f"处理PPT生成请求: {params.get('task_type', 'unknown')}")
        
        # 验证必要参数
        if "task_type" not in params:
            return {"status": "error", "message": "缺少task_type参数"}
        
        # 添加配置信息
        if "template_name" not in params:
            params["template_name"] = self.config["default_template"]
            
        # 调用智能体处理
        try:
            result = self.agent.execute(params)
            return result
        except Exception as e:
            self.logger.error(f"处理请求失败: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_capabilities(self) -> List[str]:
        """
        获取PPT智能体能力列表
        
        返回:
            能力描述列表
        """
        return self.agent.get_capabilities()
    
    def get_templates(self) -> List[Dict[str, Any]]:
        """
        获取可用的PPT模板列表
        
        返回:
            模板信息列表
        """
        templates = []
        template_dir = self.config["template_dir"]
        
        try:
            for filename in os.listdir(template_dir):
                if filename.endswith('.pptx'):
                    template_path = os.path.join(template_dir, filename)
                    template_info = {
                        "name": filename,
                        "path": template_path,
                        "size": os.path.getsize(template_path)
                    }
                    templates.append(template_info)
        except Exception as e:
            self.logger.error(f"获取模板列表失败: {str(e)}")
        
        return templates
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取PPT智能体信息
        
        返回:
            智能体信息字典
        """
        return {
            "name": "PPT智能体",
            "description": "省时高效的专家级PPT智能体",
            "version": "2.0.0",
            "capabilities": self.get_capabilities(),
            "templates": len(self.get_templates())
        }


# 提供便捷的函数接口
def create_ppt_from_text(title: str, content: str, template_name: str = None, config_path: str = None) -> Dict[str, Any]:
    """
    从文本内容创建PPT
    
    参数:
        title: PPT标题
        content: 文本内容
        template_name: 模板名称
        config_path: 配置文件路径
        
    返回:
        处理结果字典
    """
    agent = PPTAgentInterface(config_path)
    
    params = {
        "task_type": "text_to_ppt",
        "title": title,
        "content": content
    }
    
    if template_name:
        params["template_name"] = template_name
        
    return agent.process(params)

def create_ppt_from_mindmap(title: str, mindmap_data: Dict[str, Any], template_name: str = None, config_path: str = None) -> Dict[str, Any]:
    """
    从思维导图创建PPT
    
    参数:
        title: PPT标题
        mindmap_data: 思维导图数据
        template_name: 模板名称
        config_path: 配置文件路径
        
    返回:
        处理结果字典
    """
    agent = PPTAgentInterface(config_path)
    
    params = {
        "task_type": "mindmap_to_ppt",
        "title": title,
        "mindmap_data": mindmap_data
    }
    
    if template_name:
        params["template_name"] = template_name
        
    return agent.process(params)

# 命令行入口
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="PPT智能体命令行工具")
    parser.add_argument("--task", choices=["text", "mindmap"], required=True, help="任务类型")
    parser.add_argument("--title", required=True, help="PPT标题")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--template", help="模板名称")
    parser.add_argument("--config", help="配置文件路径")
    
    args = parser.parse_args()
    
    try:
        if args.task == "text":
            with open(args.input, 'r', encoding='utf-8') as f:
                content = f.read()
            result = create_ppt_from_text(args.title, content, args.template, args.config)
        elif args.task == "mindmap":
            with open(args.input, 'r', encoding='utf-8') as f:
                mindmap_data = json.load(f)
            result = create_ppt_from_mindmap(args.title, mindmap_data, args.template, args.config)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result.get("status") != "error" else 1)
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)
