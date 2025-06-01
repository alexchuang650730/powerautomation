"""
ReleaseManager - 自动化GitHub Release监控与部署工具

负责监控GitHub Release事件，自动下载代码，支持SSH密钥认证，
处理代码上传和推送，并在端侧完成部署。
"""

import os
import sys
import json
import time
import logging
import requests
import subprocess
import datetime
import hashlib
import shutil
from typing import Dict, List, Any, Optional, Union, Tuple

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("release_manager.log")
    ]
)
logger = logging.getLogger("ReleaseManager")

# 尝试导入AgentProblemSolver
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'development_tools'))
    from agent_problem_solver import AgentProblemSolver
    logger.info("成功导入AgentProblemSolver")
    AGENT_PROBLEM_SOLVER_AVAILABLE = True
except ImportError:
    logger.error("无法导入AgentProblemSolver，将使用模拟实现")
    AGENT_PROBLEM_SOLVER_AVAILABLE = False


class ReleaseManager:
    """
    ReleaseManager - 自动化GitHub Release监控与部署工具
    
    具备以下能力：
    1. GitHub Release监控：自动检测GitHub上的新版本发布
    2. 代码自动下载：将新版本代码下载到指定本地路径
    3. SSH密钥认证：支持使用SSH密钥进行GitHub认证
    4. 代码上传功能：自动处理代码提交和推送
    5. 端侧自动部署：完成代码部署并更新状态
    6. 与AgentProblemSolver集成：创建部署保存点并记录工作节点
    """
    
    def __init__(self, 
                 project_dir: str, 
                 github_repo: str, 
                 local_path: str,
                 ssh_key_path: Optional[str] = None,
                 auto_check_interval: int = 3600,
                 github_token: Optional[str] = None):
        """
        初始化ReleaseManager
        
        Args:
            project_dir: 项目目录
            github_repo: GitHub仓库地址 (格式: 'owner/repo')
            local_path: 本地代码路径
            ssh_key_path: SSH密钥路径 (可选)
            auto_check_interval: 自动检查间隔 (秒)
            github_token: GitHub API令牌 (可选)
        """
        self.project_dir = os.path.abspath(project_dir)
        self.github_repo = github_repo
        self.local_path = os.path.abspath(local_path)
        self.ssh_key_path = ssh_key_path
        self.auto_check_interval = auto_check_interval
        self.github_token = github_token
        
        # 初始化AgentProblemSolver
        if AGENT_PROBLEM_SOLVER_AVAILABLE:
            self.problem_solver = AgentProblemSolver(self.project_dir)
        else:
            self.problem_solver = None
        
        # 创建本地路径
        os.makedirs(self.local_path, exist_ok=True)
        
        # 初始化release记录
        self.releases_dir = os.path.join(self.project_dir, '.releases')
        os.makedirs(self.releases_dir, exist_ok=True)
        
        # 加载现有release记录
        self.releases = []
        self.current_release = None
        self._load_releases()
        
        # 初始化部署记录
        self.deployments = []
        self._load_deployments()
        
        logger.info(f"ReleaseManager初始化完成，项目目录: {self.project_dir}, GitHub仓库: {self.github_repo}")
    
    def _load_releases(self) -> None:
        """加载现有release记录"""
        releases_file = os.path.join(self.releases_dir, 'releases.json')
        if os.path.exists(releases_file):
            try:
                with open(releases_file, 'r') as f:
                    data = json.load(f)
                    self.releases = data.get('releases', [])
                    self.current_release = data.get('current_release')
                logger.info(f"加载了 {len(self.releases)} 个release记录")
            except Exception as e:
                logger.error(f"加载release记录失败: {str(e)}")
                self.releases = []
                self.current_release = None
    
    def _save_releases(self) -> None:
        """保存release记录"""
        releases_file = os.path.join(self.releases_dir, 'releases.json')
        try:
            with open(releases_file, 'w') as f:
                json.dump({
                    'releases': self.releases,
                    'current_release': self.current_release
                }, f, indent=2)
            logger.info(f"保存了 {len(self.releases)} 个release记录")
        except Exception as e:
            logger.error(f"保存release记录失败: {str(e)}")
    
    def _load_deployments(self) -> None:
        """加载部署记录"""
        deployments_file = os.path.join(self.releases_dir, 'deployments.json')
        if os.path.exists(deployments_file):
            try:
                with open(deployments_file, 'r') as f:
                    self.deployments = json.load(f)
                logger.info(f"加载了 {len(self.deployments)} 个部署记录")
            except Exception as e:
                logger.error(f"加载部署记录失败: {str(e)}")
                self.deployments = []
        else:
            self.deployments = []
    
    def _save_deployments(self) -> None:
        """保存部署记录"""
        deployments_file = os.path.join(self.releases_dir, 'deployments.json')
        try:
            with open(deployments_file, 'w') as f:
                json.dump(self.deployments, f, indent=2)
            logger.info(f"保存了 {len(self.deployments)} 个部署记录")
        except Exception as e:
            logger.error(f"保存部署记录失败: {str(e)}")
    
    def check_github_releases(self) -> List[Dict[str, Any]]:
        """
        检查GitHub上的releases
        
        Returns:
            新的releases列表
        """
        logger.info(f"检查GitHub仓库 {self.github_repo} 的releases")
        
        try:
            # 构建GitHub API URL
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases"
            
            # 设置请求头
            headers = {}
            if self.github_token:
                headers['Authorization'] = f"token {self.github_token}"
            
            # 发送请求
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            
            # 解析响应
            github_releases = response.json()
            
            # 过滤出新的releases
            existing_release_ids = [r['id'] for r in self.releases]
            new_releases = []
            
            for release in github_releases:
                if release['id'] not in existing_release_ids:
                    new_release = {
                        'id': release['id'],
                        'tag_name': release['tag_name'],
                        'name': release['name'],
                        'published_at': release['published_at'],
                        'html_url': release['html_url'],
                        'assets': [
                            {
                                'name': asset['name'],
                                'download_url': asset['browser_download_url'],
                                'size': asset['size']
                            }
                            for asset in release['assets']
                        ],
                        'tarball_url': release['tarball_url'],
                        'zipball_url': release['zipball_url'],
                        'body': release['body']
                    }
                    new_releases.append(new_release)
            
            if new_releases:
                logger.info(f"发现 {len(new_releases)} 个新的release")
                # 更新releases列表
                self.releases.extend(new_releases)
                self._save_releases()
            else:
                logger.info("没有发现新的release")
            
            return new_releases
        except Exception as e:
            logger.error(f"检查GitHub releases失败: {str(e)}")
            return []
    
    def download_release(self, release_id: Union[str, int]) -> Dict[str, Any]:
        """
        下载指定的release
        
        Args:
            release_id: Release ID
            
        Returns:
            下载结果
        """
        # 查找release
        release = None
        for r in self.releases:
            if str(r['id']) == str(release_id):
                release = r
                break
        
        if release is None:
            logger.error(f"未找到release: {release_id}")
            return {
                'status': 'error',
                'message': f"未找到release: {release_id}"
            }
        
        logger.info(f"下载release: {release['tag_name']}")
        
        try:
            # 创建release目录
            release_dir = os.path.join(self.local_path, release['tag_name'])
            os.makedirs(release_dir, exist_ok=True)
            
            # 下载ZIP文件
            zip_url = release['zipball_url']
            zip_path = os.path.join(release_dir, f"{release['tag_name']}.zip")
            
            # 设置请求头
            headers = {}
            if self.github_token:
                headers['Authorization'] = f"token {self.github_token}"
            
            # 下载文件
            response = requests.get(zip_url, headers=headers, stream=True)
            response.raise_for_status()
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 解压文件
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(release_dir)
            
            # 查找解压后的目录
            extracted_dirs = [d for d in os.listdir(release_dir) if os.path.isdir(os.path.join(release_dir, d))]
            if not extracted_dirs:
                raise Exception("解压后未找到目录")
            
            # 假设第一个目录是我们需要的
            extracted_dir = os.path.join(release_dir, extracted_dirs[0])
            
            # 更新release信息
            release['downloaded'] = True
            release['download_time'] = datetime.datetime.now().isoformat()
            release['local_path'] = release_dir
            release['extracted_path'] = extracted_dir
            self._save_releases()
            
            # 更新当前release
            self.current_release = release
            self._save_releases()
            
            # 创建下载记录
            download_record = {
                'release_id': release['id'],
                'tag_name': release['tag_name'],
                'download_time': release['download_time'],
                'local_path': release['local_path'],
                'status': 'success'
            }
            
            # 如果有AgentProblemSolver，创建工作节点
            if self.problem_solver:
                # 创建保存点
                savepoint = self.problem_solver.create_savepoint(f"下载release: {release['tag_name']}")
                
                # 更新下载记录
                download_record['savepoint_id'] = savepoint['id']
            
            logger.info(f"下载release成功: {release['tag_name']}")
            return {
                'status': 'success',
                'release': release,
                'download_record': download_record
            }
        except Exception as e:
            logger.error(f"下载release失败: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def deploy_release(self, release_id: Union[str, int], target_path: str) -> Dict[str, Any]:
        """
        部署指定的release
        
        Args:
            release_id: Release ID
            target_path: 目标路径
            
        Returns:
            部署结果
        """
        # 查找release
        release = None
        for r in self.releases:
            if str(r['id']) == str(release_id):
                release = r
                break
        
        if release is None:
            logger.error(f"未找到release: {release_id}")
            return {
                'status': 'error',
                'message': f"未找到release: {release_id}"
            }
        
        # 检查release是否已下载
        if not release.get('downloaded'):
            logger.error(f"Release未下载: {release['tag_name']}")
            return {
                'status': 'error',
                'message': f"Release未下载: {release['tag_name']}"
            }
        
        logger.info(f"部署release: {release['tag_name']} 到 {target_path}")
        
        try:
            # 创建目标路径
            os.makedirs(target_path, exist_ok=True)
            
            # 复制文件
            extracted_path = release['extracted_path']
            
            # 使用rsync复制文件
            cmd = f"rsync -a {extracted_path}/ {target_path}/"
            subprocess.run(cmd, shell=True, check=True)
            
            # 创建部署记录
            deployment = {
                'id': f"deploy_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'release_id': release['id'],
                'tag_name': release['tag_name'],
                'target_path': target_path,
                'deploy_time': datetime.datetime.now().isoformat(),
                'status': 'success'
            }
            
            # 添加到部署记录
            self.deployments.append(deployment)
            self._save_deployments()
            
            # 如果有AgentProblemSolver，创建工作节点
            if self.problem_solver:
                # 创建保存点
                savepoint = self.problem_solver.create_savepoint(f"部署release: {release['tag_name']}")
                
                # 更新部署状态
                self.problem_solver.update_savepoint_status(
                    savepoint['id'],
                    deployment_status='success'
                )
                
                # 更新部署记录
                deployment['savepoint_id'] = savepoint['id']
                self._save_deployments()
            
            logger.info(f"部署release成功: {release['tag_name']}")
            return {
                'status': 'success',
                'release': release,
                'deployment': deployment
            }
        except Exception as e:
            logger.error(f"部署release失败: {str(e)}")
            
            # 创建失败的部署记录
            deployment = {
                'id': f"deploy_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'release_id': release['id'],
                'tag_name': release['tag_name'],
                'target_path': target_path,
                'deploy_time': datetime.datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            }
            
            # 添加到部署记录
            self.deployments.append(deployment)
            self._save_deployments()
            
            # 如果有AgentProblemSolver，创建工作节点
            if self.problem_solver:
                # 创建保存点
                savepoint = self.problem_solver.create_savepoint(f"部署release失败: {release['tag_name']}")
                
                # 更新部署状态
                self.problem_solver.update_savepoint_status(
                    savepoint['id'],
                    deployment_status='failed'
                )
                
                # 更新部署记录
                deployment['savepoint_id'] = savepoint['id']
                self._save_deployments()
            
            return {
                'status': 'error',
                'message': str(e),
                'deployment': deployment
            }
    
    def setup_ssh_key(self, ssh_key_path: str) -> Dict[str, Any]:
        """
        设置SSH密钥
        
        Args:
            ssh_key_path: SSH密钥路径
            
        Returns:
            设置结果
        """
        logger.info(f"设置SSH密钥: {ssh_key_path}")
        
        try:
            # 检查SSH密钥是否存在
            if not os.path.exists(ssh_key_path):
                return {
                    'status': 'error',
                    'message': f"SSH密钥不存在: {ssh_key_path}"
                }
            
            # 设置SSH密钥路径
            self.ssh_key_path = ssh_key_path
            
            # 测试SSH连接
            cmd = f"ssh -T -i {self.ssh_key_path} git@github.com"
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # GitHub会返回"You've successfully authenticated"，但退出码是1
            if "successfully authenticated" in process.stderr:
                logger.info("SSH密钥认证成功")
                return {
                    'status': 'success',
                    'message': "SSH密钥认证成功"
                }
            else:
                logger.error(f"SSH密钥认证失败: {process.stderr}")
                return {
                    'status': 'error',
                    'message': f"SSH密钥认证失败: {process.stderr}"
                }
        except Exception as e:
            logger.error(f"设置SSH密钥失败: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def upload_code(self, source_path: str, remote_repo: str, branch: str = "main", commit_message: str = None) -> Dict[str, Any]:
        """
        上传代码到GitHub
        
        Args:
            source_path: 源代码路径
            remote_repo: 远程仓库地址
            branch: 分支名称
            commit_message: 提交信息
            
        Returns:
            上传结果
        """
        logger.info(f"上传代码: {source_path} -> {remote_repo}:{branch}")
        
        try:
            # 检查源代码路径是否存在
            if not os.path.exists(source_path):
                return {
                    'status': 'error',
                    'message': f"源代码路径不存在: {source_path}"
                }
            
            # 检查是否设置了SSH密钥
            if not self.ssh_key_path:
                return {
                    'status': 'error',
                    'message': "未设置SSH密钥"
                }
            
            # 创建临时目录
            temp_dir = os.path.join(self.project_dir, '.temp_git')
            os.makedirs(temp_dir, exist_ok=True)
            
            # 克隆仓库
            cmd = f"GIT_SSH_COMMAND='ssh -i {self.ssh_key_path}' git clone {remote_repo} {temp_dir}"
            subprocess.run(cmd, shell=True, check=True)
            
            # 切换到指定分支
            cmd = f"cd {temp_dir} && git checkout {branch}"
            subprocess.run(cmd, shell=True, check=True)
            
            # 复制源代码
            cmd = f"rsync -a --delete {source_path}/ {temp_dir}/"
            subprocess.run(cmd, shell=True, check=True)
            
            # 添加所有文件
            cmd = f"cd {temp_dir} && git add ."
            subprocess.run(cmd, shell=True, check=True)
            
            # 提交更改
            if not commit_message:
                commit_message = f"Update code at {datetime.datetime.now().isoformat()}"
            
            cmd = f"cd {temp_dir} && git commit -m '{commit_message}'"
            subprocess.run(cmd, shell=True, check=True)
            
            # 推送更改
            cmd = f"cd {temp_dir} && GIT_SSH_COMMAND='ssh -i {self.ssh_key_path}' git push origin {branch}"
            subprocess.run(cmd, shell=True, check=True)
            
            # 清理临时目录
            shutil.rmtree(temp_dir)
            
            # 创建上传记录
            upload_record = {
                'id': f"upload_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'source_path': source_path,
                'remote_repo': remote_repo,
                'branch': branch,
                'commit_message': commit_message,
                'upload_time': datetime.datetime.now().isoformat(),
                'status': 'success'
            }
            
            # 如果有AgentProblemSolver，创建工作节点
            if self.problem_solver:
                # 创建保存点
                savepoint = self.problem_solver.create_savepoint(f"上传代码: {commit_message}")
                
                # 更新上传记录
                upload_record['savepoint_id'] = savepoint['id']
            
            logger.info(f"上传代码成功: {remote_repo}:{branch}")
            return {
                'status': 'success',
                'upload_record': upload_record
            }
        except Exception as e:
            logger.error(f"上传代码失败: {str(e)}")
            
            # 创建失败的上传记录
            upload_record = {
                'id': f"upload_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'source_path': source_path,
                'remote_repo': remote_repo,
                'branch': branch,
                'commit_message': commit_message,
                'upload_time': datetime.datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            }
            
            # 如果有AgentProblemSolver，创建工作节点
            if self.problem_solver:
                # 创建保存点
                savepoint = self.problem_solver.create_savepoint(f"上传代码失败: {commit_message}")
                
                # 更新上传记录
                upload_record['savepoint_id'] = savepoint['id']
            
            return {
                'status': 'error',
                'message': str(e),
                'upload_record': upload_record
            }
    
    def start_auto_check(self, callback=None) -> None:
        """
        启动自动检查
        
        Args:
            callback: 回调函数，当发现新release时调用
        """
        logger.info(f"启动自动检查，间隔: {self.auto_check_interval}秒")
        
        try:
            while True:
                # 检查GitHub releases
                new_releases = self.check_github_releases()
                
                # 如果有新release并且设置了回调函数，调用回调函数
                if new_releases and callback:
                    for release in new_releases:
                        callback(release)
                
                # 等待下一次检查
                time.sleep(self.auto_check_interval)
        except KeyboardInterrupt:
            logger.info("自动检查已停止")
        except Exception as e:
            logger.error(f"自动检查失败: {str(e)}")
    
    def get_releases(self) -> List[Dict[str, Any]]:
        """
        获取所有releases
        
        Returns:
            releases列表
        """
        return self.releases
    
    def get_current_release(self) -> Optional[Dict[str, Any]]:
        """
        获取当前release
        
        Returns:
            当前release
        """
        return self.current_release
    
    def get_deployments(self) -> List[Dict[str, Any]]:
        """
        获取所有部署记录
        
        Returns:
            部署记录列表
        """
        return self.deployments
    
    def get_web_display_data(self) -> Dict[str, Any]:
        """
        获取用于Web端显示的数据
        
        Returns:
            Web端显示数据
        """
        # 获取releases列表
        releases = self.get_releases()
        
        # 获取部署记录
        deployments = self.get_deployments()
        
        # 获取当前release
        current_release = self.get_current_release()
        
        # 如果有AgentProblemSolver，获取工作节点数据
        work_nodes = []
        if self.problem_solver:
            work_nodes = self.problem_solver.get_work_nodes()
        
        # 构建Web显示数据
        web_data = {
            'releases': releases,
            'deployments': deployments,
            'current_release': current_release,
            'work_nodes': work_nodes,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return web_data


# 使用示例
if __name__ == "__main__":
    # 创建ReleaseManager
    manager = ReleaseManager(
        project_dir="/path/to/project",
        github_repo="owner/repo",
        local_path="/path/to/local",
        ssh_key_path="/path/to/ssh_key"
    )
    
    # 检查GitHub releases
    new_releases = manager.check_github_releases()
    
    if new_releases:
        # 下载第一个新release
        result = manager.download_release(new_releases[0]['id'])
        
        if result['status'] == 'success':
            # 部署release
            deploy_result = manager.deploy_release(
                new_releases[0]['id'],
                "/path/to/deploy"
            )
            
            print(f"部署结果: {deploy_result['status']}")
    
    # 获取Web显示数据
    web_data = manager.get_web_display_data()
    print(f"Web数据: {len(web_data['releases'])} 个releases, {len(web_data['deployments'])} 个部署记录")
