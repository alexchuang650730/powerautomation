"""
后端API路由模块 - PPT智能体

提供PPT智能体相关的API端点，将请求转发给MCP规划器进行处理。
"""

from flask import Blueprint, request, jsonify, send_file
import json
import os
from ...agents.ppt_agent.ppt_agent import PPTAgent

ppt_agent_bp = Blueprint('ppt_agent', __name__)
ppt_agent = PPTAgent()

@ppt_agent_bp.route('/generate_ppt', methods=['POST'])
def generate_ppt():
    """
    生成PPT演示文稿
    """
    data = request.json
    topic = data.get('topic', '')
    content = data.get('content')
    style = data.get('style')
    template = data.get('template')
    
    file_path = ppt_agent.generate_ppt(topic, content, style, template)
    
    # 返回文件路径，前端可以通过另一个接口下载
    return jsonify({
        "status": "success",
        "file_path": file_path
    })

@ppt_agent_bp.route('/mindmap_to_ppt', methods=['POST'])
def mindmap_to_ppt():
    """
    将思维导图转换为PPT
    """
    data = request.json
    mindmap_data = data.get('mindmap_data', {})
    style = data.get('style')
    template = data.get('template')
    
    file_path = ppt_agent.mindmap_to_ppt(mindmap_data, style, template)
    
    # 返回文件路径，前端可以通过另一个接口下载
    return jsonify({
        "status": "success",
        "file_path": file_path
    })

@ppt_agent_bp.route('/generate_mindmap', methods=['POST'])
def generate_mindmap():
    """
    生成思维导图
    """
    data = request.json
    topic = data.get('topic', '')
    content = data.get('content')
    
    mindmap_data = ppt_agent.generate_mindmap(topic, content)
    return jsonify(mindmap_data)

@ppt_agent_bp.route('/edit_mindmap', methods=['POST'])
def edit_mindmap():
    """
    编辑思维导图
    """
    data = request.json
    mindmap_data = data.get('mindmap_data', {})
    changes = data.get('changes', {})
    
    updated_mindmap = ppt_agent.edit_mindmap(mindmap_data, changes)
    return jsonify(updated_mindmap)

@ppt_agent_bp.route('/download_ppt/<path:filename>', methods=['GET'])
def download_ppt(filename):
    """
    下载生成的PPT文件
    """
    directory = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    return send_file(filename, as_attachment=True, download_name=file_name)
