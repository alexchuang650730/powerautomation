"""
PPT智能体API接口模块

提供PPT智能体的RESTful API接口
"""

from flask import Blueprint, request, jsonify
import logging
import os
import json
from typing import Dict, Any

from ..agents.ppt_agent.ppt_agent import PPTAgent

# 创建蓝图
ppt_agent_bp = Blueprint('ppt_agent', __name__, url_prefix='/api/agents/ppt')

# 初始化PPT智能体
ppt_agent = PPTAgent()

# 配置日志
logger = logging.getLogger(__name__)

@ppt_agent_bp.route('/info', methods=['GET'])
def get_agent_info():
    """获取PPT智能体信息"""
    try:
        # 获取所有MCP模块信息
        mcps = ppt_agent.get_all_mcps()
        
        return jsonify({
            "status": "success",
            "agent": {
                "name": "PPT智能体",
                "description": "省时高效的专家级PPT智能体",
                "version": "2.0.0",
                "mcps": mcps
            }
        })
    except Exception as e:
        logger.error(f"获取智能体信息异常: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"获取智能体信息异常: {str(e)}"
        }), 500

@ppt_agent_bp.route('/process', methods=['POST'])
def process_request():
    """处理PPT智能体请求"""
    try:
        # 获取请求数据
        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求数据为空"
            }), 400
        
        # 处理请求
        result = ppt_agent.process(data)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"处理请求异常: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"处理请求异常: {str(e)}"
        }), 500

@ppt_agent_bp.route('/generate', methods=['POST'])
def generate_ppt():
    """生成PPT"""
    try:
        # 获取请求数据
        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求数据为空"
            }), 400
        
        # 检查必要参数
        if not data.get("title"):
            return jsonify({
                "status": "error",
                "message": "缺少title参数"
            }), 400
        
        if not data.get("content") and not data.get("topic"):
            return jsonify({
                "status": "error",
                "message": "缺少content或topic参数"
            }), 400
        
        # 设置输出路径
        if not data.get("output_path"):
            # 生成默认输出路径
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
            data["output_path"] = os.path.join(output_dir, f"{data.get('title', 'presentation')}.pptx")
        
        # 生成PPT
        result = ppt_agent.generate_ppt(data)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"生成PPT异常: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"生成PPT异常: {str(e)}"
        }), 500

@ppt_agent_bp.route('/templates', methods=['GET'])
def list_templates():
    """列出可用的PPT模板"""
    try:
        # 获取查询参数
        template_type = request.args.get('type')
        industry = request.args.get('industry')
        
        # 构建请求数据
        data = {
            "mcp_type": "content_template",
            "template_action": "list_templates"
        }
        
        if template_type:
            data["template_type"] = template_type
        
        if industry:
            data["industry"] = industry
        
        # 获取模板列表
        result = ppt_agent.process(data)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"列出模板异常: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"列出模板异常: {str(e)}"
        }), 500

@ppt_agent_bp.route('/memory', methods=['POST'])
def manage_memory():
    """管理项目记忆"""
    try:
        # 获取请求数据
        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求数据为空"
            }), 400
        
        # 添加MCP类型
        data["mcp_type"] = "project_memory"
        
        # 处理记忆请求
        result = ppt_agent.process(data)
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"管理记忆异常: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"管理记忆异常: {str(e)}"
        }), 500
