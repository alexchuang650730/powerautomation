"""
通用智能体路由模块

提供通用智能体相关的API端点，包括对话、任务执行和项目管理。
"""

from flask import Blueprint, request, jsonify
from ..agents.general_agent import GeneralAgent
from ..services.general_service import GeneralService

general_agent_bp = Blueprint('general_agent', __name__, url_prefix='/api/general-agent')
general_agent = GeneralAgent()
general_service = GeneralService()

@general_agent_bp.route('/chat', methods=['POST'])
def chat():
    """
    与通用智能体进行对话
    
    请求体:
    {
        "query": "用户问题",
        "session_id": "会话ID（可选）",
        "context": "上下文信息（可选）"
    }
    """
    data = request.json
    query = data.get('query')
    session_id = data.get('session_id')
    context = data.get('context', {})
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        result = general_agent.chat(query, session_id, context)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general_agent_bp.route('/execute_task', methods=['POST'])
def execute_task():
    """
    执行指定任务
    
    请求体:
    {
        "task": "任务描述",
        "session_id": "会话ID（可选）",
        "parameters": "任务参数（可选）"
    }
    """
    data = request.json
    task = data.get('task')
    session_id = data.get('session_id')
    parameters = data.get('parameters', {})
    
    if not task:
        return jsonify({"error": "Task is required"}), 400
    
    try:
        result = general_agent.execute_task(task, session_id, parameters)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general_agent_bp.route('/create_project', methods=['POST'])
def create_project():
    """
    创建项目
    
    请求体:
    {
        "project_name": "项目名称",
        "project_description": "项目描述",
        "session_id": "会话ID（可选）",
        "parameters": "项目参数（可选）"
    }
    """
    data = request.json
    project_name = data.get('project_name')
    project_description = data.get('project_description')
    session_id = data.get('session_id')
    parameters = data.get('parameters', {})
    
    if not project_name or not project_description:
        return jsonify({"error": "Project name and description are required"}), 400
    
    try:
        result = general_agent.create_project(project_name, project_description, session_id, parameters)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general_agent_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """获取所有会话"""
    try:
        sessions = general_service.get_sessions()
        return jsonify(sessions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general_agent_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """获取指定会话的详细信息"""
    try:
        session = general_service.get_session(session_id)
        return jsonify(session)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@general_agent_bp.route('/status', methods=['GET'])
def get_status():
    """获取通用智能体状态"""
    return jsonify({
        "status": "active",
        "version": "1.0.0",
        "capabilities": [
            "对话",
            "任务执行",
            "项目管理"
        ]
    })
