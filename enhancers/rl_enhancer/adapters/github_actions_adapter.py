"""
GitHub Actions与Release Manager集成适配器
"""
import os
import json
import requests
import time
from typing import Dict, List, Any, Optional, Union, Tuple

class GitHubActionsAdapter:
    """GitHub Actions适配器，用于与GitHub Actions API交互"""
    
    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        """
        初始化GitHub Actions适配器
        
        Args:
            owner: GitHub仓库所有者
            repo: GitHub仓库名称
            token: GitHub API令牌（可选，如果不提供则尝试从环境变量获取）
        """
        self.owner = owner
        self.repo = repo
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def trigger_workflow(self, workflow_id: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        触发GitHub Actions工作流
        
        Args:
            workflow_id: 工作流ID或文件名
            inputs: 工作流输入参数
        
        Returns:
            工作流运行信息
        """
        url = f"{self.base_url}/actions/workflows/{workflow_id}/dispatches"
        data = {
            "ref": "main"  # 默认使用main分支
        }
        if inputs:
            data["inputs"] = inputs
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            # GitHub API在触发工作流时不返回工作流运行ID
            # 需要额外查询最近的工作流运行
            time.sleep(2)  # 等待工作流创建
            runs = self.list_workflow_runs(workflow_id, limit=1)
            if runs and len(runs) > 0:
                return runs[0]
            return {"status": "queued", "message": "Workflow triggered successfully"}
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def list_workflow_runs(self, workflow_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取工作流运行列表
        
        Args:
            workflow_id: 工作流ID或文件名
            limit: 返回结果数量限制
        
        Returns:
            工作流运行列表
        """
        url = f"{self.base_url}/actions/workflows/{workflow_id}/runs"
        params = {"per_page": limit}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("workflow_runs", [])
        except requests.RequestException:
            return []
    
    def get_workflow_run(self, run_id: int) -> Dict[str, Any]:
        """
        获取工作流运行详情
        
        Args:
            run_id: 工作流运行ID
        
        Returns:
            工作流运行详情
        """
        url = f"{self.base_url}/actions/runs/{run_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def cancel_workflow_run(self, run_id: int) -> bool:
        """
        取消工作流运行
        
        Args:
            run_id: 工作流运行ID
        
        Returns:
            是否成功取消
        """
        url = f"{self.base_url}/actions/runs/{run_id}/cancel"
        
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False
    
    def get_workflow_run_logs(self, run_id: int) -> bytes:
        """
        获取工作流运行日志
        
        Args:
            run_id: 工作流运行ID
        
        Returns:
            日志内容（ZIP文件二进制数据）
        """
        url = f"{self.base_url}/actions/runs/{run_id}/logs"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.content
        except requests.RequestException:
            return b""


class ReleaseManagerAdapter:
    """Release Manager适配器，用于与Release Manager交互"""
    
    def __init__(self, base_dir: str):
        """
        初始化Release Manager适配器
        
        Args:
            base_dir: 基础目录，用于存储发布信息
        """
        self.base_dir = base_dir
        self.releases_file = os.path.join(base_dir, "releases.json")
        self._ensure_releases_file()
    
    def _ensure_releases_file(self):
        """确保releases.json文件存在"""
        os.makedirs(os.path.dirname(self.releases_file), exist_ok=True)
        if not os.path.exists(self.releases_file):
            with open(self.releases_file, "w") as f:
                json.dump({"releases": []}, f)
    
    def _load_releases(self) -> Dict[str, List[Dict[str, Any]]]:
        """加载发布信息"""
        with open(self.releases_file, "r") as f:
            return json.load(f)
    
    def _save_releases(self, data: Dict[str, List[Dict[str, Any]]]):
        """保存发布信息"""
        with open(self.releases_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def list_releases(self) -> List[Dict[str, Any]]:
        """
        获取所有发布信息
        
        Returns:
            发布信息列表
        """
        data = self._load_releases()
        return data.get("releases", [])
    
    def get_release(self, version: str) -> Optional[Dict[str, Any]]:
        """
        获取指定版本的发布信息
        
        Args:
            version: 版本号
        
        Returns:
            发布信息，如果不存在则返回None
        """
        releases = self.list_releases()
        for release in releases:
            if release.get("version") == version:
                return release
        return None
    
    def add_release(self, version: str, description: str, assets: List[str] = None) -> bool:
        """
        添加新的发布
        
        Args:
            version: 版本号
            description: 发布描述
            assets: 资源文件列表
        
        Returns:
            是否成功添加
        """
        if self.get_release(version):
            return False  # 版本已存在
        
        data = self._load_releases()
        release = {
            "version": version,
            "description": description,
            "assets": assets or [],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        }
        data["releases"].append(release)
        self._save_releases(data)
        return True
    
    def update_release_status(self, version: str, status: str) -> bool:
        """
        更新发布状态
        
        Args:
            version: 版本号
            status: 新状态（pending, success, failed）
        
        Returns:
            是否成功更新
        """
        data = self._load_releases()
        for release in data["releases"]:
            if release.get("version") == version:
                release["status"] = status
                release["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                self._save_releases(data)
                return True
        return False
    
    def delete_release(self, version: str) -> bool:
        """
        删除发布
        
        Args:
            version: 版本号
        
        Returns:
            是否成功删除
        """
        data = self._load_releases()
        initial_count = len(data["releases"])
        data["releases"] = [r for r in data["releases"] if r.get("version") != version]
        if len(data["releases"]) < initial_count:
            self._save_releases(data)
            return True
        return False
    
    def trigger_github_actions(self, github_adapter: GitHubActionsAdapter, 
                              version: str, workflow_id: str) -> Dict[str, Any]:
        """
        触发GitHub Actions工作流
        
        Args:
            github_adapter: GitHub Actions适配器
            version: 版本号
            workflow_id: 工作流ID或文件名
        
        Returns:
            工作流运行信息
        """
        release = self.get_release(version)
        if not release:
            return {"status": "error", "message": f"Release {version} not found"}
        
        inputs = {
            "version": version,
            "description": release.get("description", ""),
            "assets": ",".join(release.get("assets", []))
        }
        
        result = github_adapter.trigger_workflow(workflow_id, inputs)
        
        if result.get("status") != "error":
            self.update_release_status(version, "building")
        
        return result
    
    def check_github_actions_status(self, github_adapter: GitHubActionsAdapter,
                                   version: str, run_id: int) -> Dict[str, Any]:
        """
        检查GitHub Actions工作流状态
        
        Args:
            github_adapter: GitHub Actions适配器
            version: 版本号
            run_id: 工作流运行ID
        
        Returns:
            状态信息
        """
        run_info = github_adapter.get_workflow_run(run_id)
        
        if run_info.get("status") == "completed":
            if run_info.get("conclusion") == "success":
                self.update_release_status(version, "success")
            else:
                self.update_release_status(version, "failed")
        
        return run_info
