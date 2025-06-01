"""
GitHub Actions与Release Manager集成适配器
"""
import os
import json
import requests
from typing import Dict, List, Any, Optional, Union, Tuple
import subprocess
import time


class GitHubActionsAdapter:
    """GitHub Actions适配器，用于与GitHub Actions进行交互"""
    
    def __init__(self, owner=None, repo=None, repo_owner=None, repo_name=None, token=None):
        """
        初始化GitHub Actions适配器
        
        Args:
            owner: 仓库所有者（兼容旧接口）
            repo: 仓库名称（兼容旧接口）
            repo_owner: 仓库所有者
            repo_name: 仓库名称
            token: GitHub访问令牌（可选）
        """
        # 兼容两种不同的参数命名方式
        self.repo_owner = repo_owner or owner or "default-owner"
        self.repo_name = repo_name or repo or "default-repo"
        self.token = token
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        self.headers = {}
        
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        列出所有工作流
        
        Returns:
            工作流列表
        """
        url = f"{self.base_url}/actions/workflows"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get("workflows", [])
        else:
            print(f"Failed to list workflows: {response.status_code} - {response.text}")
            return []
    
    def get_workflow(self, workflow_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        获取工作流信息
        
        Args:
            workflow_id: 工作流ID或文件名
            
        Returns:
            工作流信息
        """
        url = f"{self.base_url}/actions/workflows/{workflow_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get workflow: {response.status_code} - {response.text}")
            return None
    
    def list_workflow_runs(self, workflow_id: Union[int, str]) -> List[Dict[str, Any]]:
        """
        列出工作流运行记录
        
        Args:
            workflow_id: 工作流ID或文件名
            
        Returns:
            运行记录列表
        """
        url = f"{self.base_url}/actions/workflows/{workflow_id}/runs"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get("workflow_runs", [])
        else:
            print(f"Failed to list workflow runs: {response.status_code} - {response.text}")
            return []
    
    def get_workflow_run(self, run_id: int) -> Optional[Dict[str, Any]]:
        """
        获取工作流运行记录
        
        Args:
            run_id: 运行ID
            
        Returns:
            运行记录
        """
        url = f"{self.base_url}/actions/runs/{run_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get workflow run: {response.status_code} - {response.text}")
            return None
    
    def trigger_workflow(self, workflow_id: Union[int, str], ref: str = "main", 
                        inputs: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        触发工作流
        
        Args:
            workflow_id: 工作流ID或文件名
            ref: 分支或标签
            inputs: 工作流输入参数
            
        Returns:
            触发结果
        """
        url = f"{self.base_url}/actions/workflows/{workflow_id}/dispatches"
        payload = {"ref": ref}
        
        if inputs:
            payload["inputs"] = inputs
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 204:
            return {"status": "success"}
        else:
            print(f"Failed to trigger workflow: {response.status_code} - {response.text}")
            return None
    
    def cancel_workflow_run(self, run_id: int) -> bool:
        """
        取消工作流运行
        
        Args:
            run_id: 运行ID
            
        Returns:
            是否成功取消
        """
        url = f"{self.base_url}/actions/runs/{run_id}/cancel"
        response = requests.post(url, headers=self.headers)
        
        return response.status_code == 202
    
    def get_workflow_run_logs(self, run_id: int) -> Optional[bytes]:
        """
        获取工作流运行日志
        
        Args:
            run_id: 运行ID
            
        Returns:
            日志内容
        """
        url = f"{self.base_url}/actions/runs/{run_id}/logs"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to get workflow run logs: {response.status_code} - {response.text}")
            return None
    
    def wait_for_workflow_completion(self, run_id: int, timeout: int = 600, 
                                   check_interval: int = 10) -> Optional[Dict[str, Any]]:
        """
        等待工作流完成
        
        Args:
            run_id: 运行ID
            timeout: 超时时间（秒）
            check_interval: 检查间隔（秒）
            
        Returns:
            完成的运行记录
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            run = self.get_workflow_run(run_id)
            
            if not run:
                return None
            
            status = run.get("status")
            conclusion = run.get("conclusion")
            
            if status == "completed":
                return run
            
            time.sleep(check_interval)
        
        print(f"Workflow run {run_id} did not complete within {timeout} seconds")
        return None


class ReleaseManagerAdapter:
    """Release Manager适配器，用于与Release Manager进行交互"""
    
    def __init__(self, base_dir: str = None):
        """
        初始化Release Manager适配器
        
        Args:
            base_dir: 基础目录
        """
        self.base_dir = base_dir or os.getcwd()
        self.release_config_path = os.path.join(self.base_dir, "release_config.json")
        self.release_history_path = os.path.join(self.base_dir, "release_history.json")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.release_config_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.release_history_path), exist_ok=True)
        
        # 加载配置和历史
        self.config = self._load_json(self.release_config_path, {})
        self.history = self._load_json(self.release_history_path, {"releases": []})
    
    def _load_json(self, path: str, default: Any) -> Any:
        """
        加载JSON文件
        
        Args:
            path: 文件路径
            default: 默认值
            
        Returns:
            加载的数据
        """
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load {path}: {e}")
        
        return default
    
    def _save_json(self, path: str, data: Any) -> bool:
        """
        保存JSON文件
        
        Args:
            path: 文件路径
            data: 数据
            
        Returns:
            是否成功保存
        """
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save {path}: {e}")
            return False
    
    def get_release_config(self) -> Dict[str, Any]:
        """
        获取发布配置
        
        Returns:
            发布配置
        """
        return self.config
    
    def update_release_config(self, config: Dict[str, Any]) -> bool:
        """
        更新发布配置
        
        Args:
            config: 新的配置
            
        Returns:
            是否成功更新
        """
        self.config = config
        return self._save_json(self.release_config_path, config)
    
    def get_release_history(self) -> List[Dict[str, Any]]:
        """
        获取发布历史
        
        Returns:
            发布历史
        """
        return self.history.get("releases", [])
    
    def add_release(self, release: Dict[str, Any]) -> bool:
        """
        添加发布记录
        
        Args:
            release: 发布记录
            
        Returns:
            是否成功添加
        """
        releases = self.history.get("releases", [])
        releases.append(release)
        self.history["releases"] = releases
        
        return self._save_json(self.release_history_path, self.history)
    
    def check_release_rules(self, version: str, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        检查发布规则
        
        Args:
            version: 版本号
            changes: 变更列表
            
        Returns:
            检查结果
        """
        rules = self.config.get("rules", [])
        results = []
        
        for rule in rules:
            rule_name = rule.get("name", "")
            rule_type = rule.get("type", "")
            rule_condition = rule.get("condition", {})
            
            # 检查版本号规则
            if rule_type == "version":
                import re
                pattern = rule_condition.get("pattern", "")
                if pattern and not re.match(pattern, version):
                    results.append({
                        "rule": rule_name,
                        "status": "failed",
                        "message": f"Version {version} does not match pattern {pattern}"
                    })
                else:
                    results.append({
                        "rule": rule_name,
                        "status": "passed"
                    })
            
            # 检查变更规则
            elif rule_type == "changes":
                min_changes = rule_condition.get("min_changes", 0)
                if len(changes) < min_changes:
                    results.append({
                        "rule": rule_name,
                        "status": "failed",
                        "message": f"Number of changes ({len(changes)}) is less than minimum required ({min_changes})"
                    })
                else:
                    results.append({
                        "rule": rule_name,
                        "status": "passed"
                    })
        
        # 汇总结果
        passed = all(result.get("status") == "passed" for result in results)
        
        return {
            "passed": passed,
            "results": results
        }
    
    def trigger_release(self, version: str, changes: List[Dict[str, Any]], 
                       github_actions: GitHubActionsAdapter = None) -> Dict[str, Any]:
        """
        触发发布
        
        Args:
            version: 版本号
            changes: 变更列表
            github_actions: GitHub Actions适配器（可选）
            
        Returns:
            触发结果
        """
        # 检查发布规则
        check_result = self.check_release_rules(version, changes)
        
        if not check_result.get("passed", False):
            return {
                "status": "failed",
                "message": "Release rules check failed",
                "details": check_result
            }
        
        # 创建发布记录
        release = {
            "version": version,
            "changes": changes,
            "timestamp": int(time.time()),
            "status": "pending"
        }
        
        # 添加发布记录
        if not self.add_release(release):
            return {
                "status": "failed",
                "message": "Failed to add release record"
            }
        
        # 触发GitHub Actions工作流
        if github_actions:
            workflow_id = self.config.get("github_actions", {}).get("workflow_id")
            
            if workflow_id:
                trigger_result = github_actions.trigger_workflow(
                    workflow_id=workflow_id,
                    ref=self.config.get("github_actions", {}).get("ref", "main"),
                    inputs={
                        "version": version,
                        "changes": json.dumps(changes)
                    }
                )
                
                if trigger_result:
                    return {
                        "status": "success",
                        "message": "Release triggered successfully",
                        "github_actions": trigger_result
                    }
                else:
                    return {
                        "status": "failed",
                        "message": "Failed to trigger GitHub Actions workflow"
                    }
            else:
                return {
                    "status": "failed",
                    "message": "GitHub Actions workflow ID not configured"
                }
        
        return {
            "status": "success",
            "message": "Release record added successfully"
        }
    
    def update_release_status(self, version: str, status: str, details: Dict[str, Any] = None) -> bool:
        """
        更新发布状态
        
        Args:
            version: 版本号
            status: 状态
            details: 详细信息
            
        Returns:
            是否成功更新
        """
        releases = self.history.get("releases", [])
        
        for release in releases:
            if release.get("version") == version:
                release["status"] = status
                
                if details:
                    release["details"] = details
                
                return self._save_json(self.release_history_path, self.history)
        
        return False


class GitHubReleaseManagerIntegration:
    """GitHub Actions与Release Manager集成"""
    
    def __init__(self, repo_owner: str, repo_name: str, token: str = None, base_dir: str = None):
        """
        初始化GitHub Actions与Release Manager集成
        
        Args:
            repo_owner: 仓库所有者
            repo_name: 仓库名称
            token: GitHub访问令牌（可选）
            base_dir: 基础目录
        """
        self.github_actions = GitHubActionsAdapter(repo_owner=repo_owner, repo_name=repo_name, token=token)
        self.release_manager = ReleaseManagerAdapter(base_dir)
    
    def setup_integration(self, workflow_id: str, ref: str = "main") -> bool:
        """
        设置集成
        
        Args:
            workflow_id: 工作流ID或文件名
            ref: 分支或标签
            
        Returns:
            是否成功设置
        """
        config = self.release_manager.get_release_config()
        
        if "github_actions" not in config:
            config["github_actions"] = {}
        
        config["github_actions"]["workflow_id"] = workflow_id
        config["github_actions"]["ref"] = ref
        
        return self.release_manager.update_release_config(config)
    
    def trigger_release(self, version: str, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        触发发布
        
        Args:
            version: 版本号
            changes: 变更列表
            
        Returns:
            触发结果
        """
        return self.release_manager.trigger_release(version, changes, self.github_actions)
    
    def monitor_release(self, version: str, run_id: int, timeout: int = 600) -> Dict[str, Any]:
        """
        监控发布
        
        Args:
            version: 版本号
            run_id: 运行ID
            timeout: 超时时间（秒）
            
        Returns:
            监控结果
        """
        # 等待工作流完成
        run = self.github_actions.wait_for_workflow_completion(run_id, timeout)
        
        if not run:
            self.release_manager.update_release_status(version, "failed", {
                "message": "Workflow did not complete within timeout"
            })
            
            return {
                "status": "failed",
                "message": "Workflow did not complete within timeout"
            }
        
        # 更新发布状态
        status = "success" if run.get("conclusion") == "success" else "failed"
        
        self.release_manager.update_release_status(version, status, {
            "conclusion": run.get("conclusion"),
            "html_url": run.get("html_url")
        })
        
        return {
            "status": status,
            "message": f"Release {version} {status}",
            "details": run
        }
