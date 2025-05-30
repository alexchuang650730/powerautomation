"""
Web Agent API路由模块

提供Web Agent相关的API端点，包括网页抓取、内容分析、数据提取和自动化操作。
"""

from flask import Blueprint, request, jsonify
from ..agents.web_agent import WebAgent
from ..services.web_service import WebService

web_agent_bp = Blueprint('web_agent', __name__, url_prefix='/api/web-agent')
web_agent = WebAgent()
web_service = WebService()

@web_agent_bp.route('/extract', methods=['POST'])
def extract_data():
    """
    从指定网页提取数据
    
    请求体:
    {
        "url": "网页URL",
        "extraction_query": "提取指令"
    }
    """
    data = request.json
    url = data.get('url')
    extraction_query = data.get('extraction_query')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        result = web_agent.extract_data(url, extraction_query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@web_agent_bp.route('/automate', methods=['POST'])
def automate_task():
    """
    在指定网页执行自动化任务
    
    请求体:
    {
        "url": "网页URL",
        "task": "自动化任务描述"
    }
    """
    data = request.json
    url = data.get('url')
    task = data.get('task')
    
    if not url or not task:
        return jsonify({"error": "URL and task are required"}), 400
    
    try:
        result = web_agent.automate_task(url, task)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@web_agent_bp.route('/analyze', methods=['POST'])
def analyze_content():
    """
    分析指定网页的内容
    
    请求体:
    {
        "url": "网页URL",
        "analysis_type": "分析类型",
        "analysis_query": "分析要求"
    }
    """
    data = request.json
    url = data.get('url')
    analysis_type = data.get('analysis_type', 'general')
    analysis_query = data.get('analysis_query', '')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        result = web_agent.analyze_content(url, analysis_type, analysis_query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@web_agent_bp.route('/screenshot', methods=['POST'])
def take_screenshot():
    """
    获取指定网页的截图
    
    请求体:
    {
        "url": "网页URL",
        "full_page": true/false
    }
    """
    data = request.json
    url = data.get('url')
    full_page = data.get('full_page', False)
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        screenshot_path = web_service.take_screenshot(url, full_page)
        return jsonify({"screenshot_path": screenshot_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@web_agent_bp.route('/status', methods=['GET'])
def get_status():
    """获取Web Agent状态"""
    return jsonify({
        "status": "active",
        "version": "1.0.0",
        "capabilities": [
            "网页抓取",
            "内容分析",
            "数据提取",
            "自动化操作"
        ]
    })
