"""
前后端职责分离重构脚本

此脚本用于创建前后端分离的目录结构，并调整相关导入路径。
"""

import os
import shutil
import re

def create_directory_structure():
    """创建新的目录结构"""
    # 前端目录结构
    frontend_dirs = [
        "frontend/components",
        "frontend/pages",
        "frontend/services",
        "frontend/utils",
        "frontend/styles",
        "frontend/public"
    ]
    
    # 后端目录结构
    backend_dirs = [
        "backend/api",
        "backend/services",
        "backend/utils",
        "backend/config"
    ]
    
    # 创建目录
    base_dir = "/home/ubuntu/powerautomation_integration"
    for dir_path in frontend_dirs + backend_dirs:
        full_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"创建目录: {full_path}")

def create_frontend_service_stubs():
    """创建前端服务存根，用于与后端API交互"""
    base_dir = "/home/ubuntu/powerautomation_integration"
    
    # 创建agent服务存根
    agent_service_content = """/**
 * 智能体服务
 * 
 * 提供与各种智能体交互的前端服务
 */

import axios from 'axios';

const API_BASE_URL = '/api';

/**
 * 智能体服务类
 */
export class AgentService {
  /**
   * 调用通用智能体
   * @param {Object} data - 请求数据
   * @returns {Promise<Object>} - 响应结果
   */
  static async callGeneralAgent(data) {
    return axios.post(`${API_BASE_URL}/agents/general`, data);
  }
  
  /**
   * 调用PPT智能体
   * @param {Object} data - 请求数据
   * @returns {Promise<Object>} - 响应结果
   */
  static async callPPTAgent(data) {
    return axios.post(`${API_BASE_URL}/agents/ppt`, data);
  }
  
  /**
   * 调用Web智能体
   * @param {Object} data - 请求数据
   * @returns {Promise<Object>} - 响应结果
   */
  static async callWebAgent(data) {
    return axios.post(`${API_BASE_URL}/agents/web`, data);
  }
  
  /**
   * 获取所有可用智能体
   * @returns {Promise<Array>} - 智能体列表
   */
  static async getAvailableAgents() {
    return axios.get(`${API_BASE_URL}/agents`);
  }
}
"""
    
    agent_service_path = os.path.join(base_dir, "frontend/services/agent-service.js")
    with open(agent_service_path, "w") as f:
        f.write(agent_service_content)
    print(f"创建前端服务存根: {agent_service_path}")

def create_backend_api_stubs():
    """创建后端API路由存根"""
    base_dir = "/home/ubuntu/powerautomation_integration"
    
    # 创建agent API路由存根
    agent_api_content = """
from flask import Blueprint, request, jsonify
from powerautomation_integration.agents.general.general_agent import GeneralAgent
from powerautomation_integration.agents.ppt.ppt_agent import PPTAgent
from powerautomation_integration.agents.web.web_agent import WebAgent

# 创建蓝图
agent_bp = Blueprint('agent', __name__, url_prefix='/api/agents')

# 智能体实例
general_agent = GeneralAgent()
ppt_agent = PPTAgent()
web_agent = WebAgent()

@agent_bp.route('', methods=['GET'])
def get_available_agents():
    """获取所有可用智能体"""
    agents = [
        {
            "id": "general",
            "name": general_agent.name,
            "description": general_agent.description,
            "capabilities": general_agent.get_capabilities()
        },
        {
            "id": "ppt",
            "name": ppt_agent.name,
            "description": ppt_agent.description,
            "capabilities": ppt_agent.get_capabilities()
        },
        {
            "id": "web",
            "name": web_agent.name,
            "description": web_agent.description,
            "capabilities": web_agent.get_capabilities()
        }
    ]
    return jsonify(agents)

@agent_bp.route('/general', methods=['POST'])
def call_general_agent():
    """调用通用智能体"""
    data = request.json
    result = general_agent.process(data)
    return jsonify(result)

@agent_bp.route('/ppt', methods=['POST'])
def call_ppt_agent():
    """调用PPT智能体"""
    data = request.json
    result = ppt_agent.process(data)
    return jsonify(result)

@agent_bp.route('/web', methods=['POST'])
def call_web_agent():
    """调用Web智能体"""
    data = request.json
    result = web_agent.process(data)
    return jsonify(result)
"""
    
    agent_api_path = os.path.join(base_dir, "backend/api/agent_routes.py")
    with open(agent_api_path, "w") as f:
        f.write(agent_api_content)
    print(f"创建后端API路由存根: {agent_api_path}")
    
    # 创建API初始化文件
    api_init_content = """
from flask import Flask
from .agent_routes import agent_bp

def init_app(app):
    """初始化所有API路由"""
    app.register_blueprint(agent_bp)
"""
    
    api_init_path = os.path.join(base_dir, "backend/api/__init__.py")
    with open(api_init_path, "w") as f:
        f.write(api_init_content)
    print(f"创建API初始化文件: {api_init_path}")

def create_backend_service_stubs():
    """创建后端服务存根"""
    base_dir = "/home/ubuntu/powerautomation_integration"
    
    # 创建agent服务存根
    agent_service_content = """
from powerautomation_integration.agents.general.general_agent import GeneralAgent
from powerautomation_integration.agents.ppt.ppt_agent import PPTAgent
from powerautomation_integration.agents.web.web_agent import WebAgent

class AgentService:
    """智能体服务，提供智能体管理和调用功能"""
    
    def __init__(self):
        """初始化智能体服务"""
        self.agents = {
            "general": GeneralAgent(),
            "ppt": PPTAgent(),
            "web": WebAgent()
        }
    
    def get_agent(self, agent_id):
        """获取指定ID的智能体"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self):
        """获取所有智能体信息"""
        return {
            agent_id: {
                "id": agent_id,
                "name": agent.name,
                "description": agent.description,
                "capabilities": agent.get_capabilities()
            }
            for agent_id, agent in self.agents.items()
        }
    
    def process_request(self, agent_id, data):
        """处理智能体请求"""
        agent = self.get_agent(agent_id)
        if not agent:
            return {"error": f"未找到智能体: {agent_id}"}
        
        return agent.process(data)
"""
    
    agent_service_path = os.path.join(base_dir, "backend/services/agent_service.py")
    with open(agent_service_path, "w") as f:
        f.write(agent_service_content)
    print(f"创建后端服务存根: {agent_service_path}")
    
    # 创建服务初始化文件
    service_init_content = """
from .agent_service import AgentService

# 导出服务类
__all__ = ['AgentService']
"""
    
    service_init_path = os.path.join(base_dir, "backend/services/__init__.py")
    with open(service_init_path, "w") as f:
        f.write(service_init_content)
    print(f"创建服务初始化文件: {service_init_path}")

def create_init_files():
    """创建必要的__init__.py文件"""
    base_dir = "/home/ubuntu/powerautomation_integration"
    
    # 前端目录初始化文件
    frontend_init_dirs = [
        "frontend",
        "frontend/components",
        "frontend/pages",
        "frontend/services",
        "frontend/utils"
    ]
    
    # 后端目录初始化文件
    backend_init_dirs = [
        "backend",
        "backend/api",
        "backend/services",
        "backend/utils",
        "backend/config"
    ]
    
    # 创建初始化文件
    for dir_path in frontend_init_dirs + backend_init_dirs:
        init_file = os.path.join(base_dir, dir_path, "__init__.py")
        with open(init_file, "w") as f:
            f.write("# 自动生成的初始化文件\n")
        print(f"创建初始化文件: {init_file}")

def create_agents_init_files():
    """为agents目录创建__init__.py文件"""
    base_dir = "/home/ubuntu/powerautomation_integration"
    
    # agents目录初始化文件
    agents_init_dirs = [
        "agents",
        "agents/base",
        "agents/general",
        "agents/ppt",
        "agents/web"
    ]
    
    # 创建初始化文件
    for dir_path in agents_init_dirs:
        init_file = os.path.join(base_dir, dir_path, "__init__.py")
        with open(init_file, "w") as f:
            f.write("# 自动生成的初始化文件\n")
        print(f"创建初始化文件: {init_file}")

def main():
    """主函数"""
    print("开始前后端职责分离重构...")
    
    # 创建目录结构
    create_directory_structure()
    
    # 创建前端服务存根
    create_frontend_service_stubs()
    
    # 创建后端API路由存根
    create_backend_api_stubs()
    
    # 创建后端服务存根
    create_backend_service_stubs()
    
    # 创建初始化文件
    create_init_files()
    
    # 创建agents初始化文件
    create_agents_init_files()
    
    print("前后端职责分离重构完成！")

if __name__ == "__main__":
    main()
