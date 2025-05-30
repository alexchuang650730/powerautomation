"""
主应用入口模块

Flask应用入口，提供API接口
"""

import os
import sys
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 确保可以导入项目模块
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.services.ppt_service import PPTTaskService
from backend.agents.web_agent import WebAgent

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__, static_folder='../frontend/build')
CORS(app)  # 启用跨域支持

# 初始化服务
ppt_service = PPTTaskService()
web_agent = WebAgent()

# 静态文件路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# PPT相关API
@app.route('/api/ppt/create', methods=['POST'])
def create_ppt():
    """创建PPT的API接口"""
    try:
        data = request.json
        task_type = data.get('task_type')
        title = data.get('title', '未命名演示文稿')
        template_name = data.get('template_name', '专业简历.pptx')
        
        if task_type == 'text':
            content = data.get('content', '')
            result = ppt_service.create_ppt_from_text(title, content, template_name)
        elif task_type == 'mindmap':
            mindmap_data = data.get('mindmap_data', {})
            result = ppt_service.create_ppt_from_mindmap(title, mindmap_data, template_name)
        else:
            return jsonify({'status': 'error', 'message': f'不支持的任务类型: {task_type}'}), 400
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"创建PPT失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/ppt/templates', methods=['GET'])
def get_templates():
    """获取可用PPT模板的API接口"""
    try:
        templates = ppt_service.get_available_templates()
        return jsonify({'status': 'success', 'templates': templates})
    except Exception as e:
        logger.error(f"获取模板列表失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/ppt/recent', methods=['GET'])
def get_recent_ppts():
    """获取最近生成的PPT列表的API接口"""
    try:
        limit = request.args.get('limit', 10, type=int)
        ppts = ppt_service.get_recent_ppts(limit)
        return jsonify({'status': 'success', 'ppts': ppts})
    except Exception as e:
        logger.error(f"获取最近PPT列表失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 网页搜索相关API
@app.route('/api/web/search', methods=['POST'])
def web_search():
    """网页搜索的API接口"""
    try:
        data = request.json
        query = data.get('query', '')
        max_results = data.get('max_results', 5)
        use_claude = data.get('use_claude', True)
        
        if not query:
            return jsonify({'status': 'error', 'message': '搜索查询不能为空'}), 400
        
        input_data = {
            'task_type': 'web_search',
            'query': query,
            'max_results': max_results,
            'use_claude': use_claude
        }
        
        result = web_agent.execute(input_data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"网页搜索失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/web/analyze', methods=['POST'])
def analyze_webpage():
    """网页内容分析的API接口"""
    try:
        data = request.json
        url = data.get('url', '')
        analysis_type = data.get('analysis_type', 'summary')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL不能为空'}), 400
        
        input_data = {
            'task_type': 'content_analysis',
            'url': url,
            'analysis_type': analysis_type
        }
        
        result = web_agent.execute(input_data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"网页内容分析失败: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 健康检查API
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查API接口"""
    return jsonify({'status': 'ok', 'message': 'Service is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
