"""
后端主模块 - 集成所有API路由

将所有智能体的API路由集成到Flask应用中，并确保通过MCP规划器进行统一调度。
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

from .routes.general_agent_routes import general_agent_bp
from .routes.web_agent_routes import web_agent_bp
from .routes.ppt_agent_routes import ppt_agent_bp
from .routes.code_agent_routes import code_agent_bp

app = Flask(__name__)
CORS(app)

# 注册蓝图
app.register_blueprint(general_agent_bp, url_prefix='/api/general_agent')
app.register_blueprint(web_agent_bp, url_prefix='/api/web_agent')
app.register_blueprint(ppt_agent_bp, url_prefix='/api/ppt_agent')
app.register_blueprint(code_agent_bp, url_prefix='/api/code_agent')

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "PowerAutomation API服务正在运行",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
