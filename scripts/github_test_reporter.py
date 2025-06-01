import requests
import json
import os
from datetime import datetime

def send_test_results_to_github(repo_owner, repo_name, test_results, token):
    """将测试结果发送到GitHub，创建或更新issue"""
    
    # GitHub API URL
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    
    # 准备认证头
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 准备issue内容
    issue_title = "PowerAutomation UI测试结果报告"
    issue_body = f"""
# PowerAutomation UI测试结果

## 测试概况
- 总测试数: {test_results['total']}
- 通过: {test_results['passed']}
- 失败: {test_results['failed']}
- 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 测试详情
"""
    
    # 添加每个测试的详细信息
    for test in test_results['tests']:
        status_emoji = "✅" if test['status'] == "passed" else "❌"
        issue_body += f"### {status_emoji} {test['name']}\n"
        issue_body += f"- 状态: {test['status']}\n"
        issue_body += f"- 消息: {test['message']}\n\n"
    
    # 添加环境信息
    issue_body += f"""
## 环境信息
- 分支: {os.environ.get('GITHUB_REF', 'main')}
- 提交: {os.environ.get('GITHUB_SHA', '最新提交')}
- 运行ID: {os.environ.get('GITHUB_RUN_ID', '本地测试')}
"""
    
    # 检查是否已存在相关issue
    try:
        existing_issues = requests.get(
            f"{api_url}?labels=test-results",
            headers=headers
        ).json()
        
        existing_issue_number = None
        for issue in existing_issues:
            if issue['title'] == issue_title:
                existing_issue_number = issue['number']
                break
        
        if existing_issue_number:
            # 更新现有issue
            update_url = f"{api_url}/{existing_issue_number}"
            response = requests.patch(
                update_url,
                headers=headers,
                json={"body": issue_body}
            )
        else:
            # 创建新issue
            response = requests.post(
                api_url,
                headers=headers,
                json={
                    "title": issue_title,
                    "body": issue_body,
                    "labels": ["test-results", "ui", "automated"]
                }
            )
        
        return {
            "success": True,
            "url": response.json().get('html_url', ''),
            "message": "测试结果已成功发送到GitHub"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "发送测试结果到GitHub失败"
        }

def parse_test_report(report_file):
    """解析测试报告文件，提取结构化数据"""
    try:
        with open(report_file, "r") as f:
            content = f.read()
        
        # 解析总体结果
        import re
        total_match = re.search(r'总测试数: (\d+)', content)
        passed_match = re.search(r'通过: (\d+)', content)
        failed_match = re.search(r'失败: (\d+)', content)
        
        total = int(total_match.group(1)) if total_match else 0
        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0
        
        # 解析测试详情
        tests = []
        test_sections = re.findall(r'测试: (.*?)\n状态: (.*?)\n消息: (.*?)\n-{40}', content, re.DOTALL)
        
        for name, status, message in test_sections:
            tests.append({
                "name": name.strip(),
                "status": status.strip(),
                "message": message.strip()
            })
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "tests": tests
        }
    
    except Exception as e:
        print(f"解析测试报告失败: {str(e)}")
        return None

if __name__ == "__main__":
    # 从环境变量获取GitHub token
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("错误: 未设置GITHUB_TOKEN环境变量")
        exit(1)
    
    # 解析测试报告
    report_file = "reports/test_report.txt"
    if not os.path.exists(report_file):
        print(f"错误: 测试报告文件不存在: {report_file}")
        exit(1)
    
    test_results = parse_test_report(report_file)
    if not test_results:
        print("错误: 无法解析测试报告")
        exit(1)
    
    # 发送结果到GitHub
    repo_owner = "alexchuang650730"
    repo_name = "powerautomation"
    
    result = send_test_results_to_github(
        repo_owner,
        repo_name,
        test_results,
        token
    )
    
    if result["success"]:
        print(f"测试结果已成功发送到GitHub: {result['url']}")
    else:
        print(f"发送测试结果失败: {result['error']}")
