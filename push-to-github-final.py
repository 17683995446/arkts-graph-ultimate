#!/usr/bin/env python3
"""
终极完美版 - 推送代码到 GitHub 私有仓库 (使用 urllib)
"""

import urllib.request
import urllib.error
import subprocess
import json
import sys
from pathlib import Path

GITHUB_API_URL = "https://api.github.com"
TOKEN = "REDACTED_GITHUB_TOKEN"
REPO_NAME = "arkts-graph-ultimate"
REPO_OWNER = "arkts-graph-user"  # 将根据API确定实际用户名

def api_request(url, method="GET", data=None):
    """使用 urllib 发送 API 请求"""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "arkts-graph/1.0"
    }
    
    req_data = None
    if data:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_text = e.read().decode("utf-8")
        return e.code, error_text

def get_user_info():
    """获取用户信息"""
    print("📡 获取 GitHub 用户信息...")
    url = f"{GITHUB_API_URL}/user"
    status, response = api_request(url)
    if status == 200:
        print(f"✅ 用户信息获取成功: {response['login']}")
        return response['login']
    else:
        print(f"❌ 获取用户信息失败: {status}")
        print(f"响应: {response}")
        return None

def create_repo():
    """创建私有仓库"""
    print(f"\n🚀 创建私有仓库: {REPO_NAME}")
    url = f"{GITHUB_API_URL}/user/repos"
    data = {
        "name": REPO_NAME,
        "description": "ArkTS 代码分析与知识图谱系统 - 终极完美版",
        "private": True,
        "auto_init": False
    }
    
    status, response = api_request(url, method="POST", data=data)
    if status in [200, 201]:
        print(f"✅ 私有仓库创建成功: {response['html_url']}")
        return response
    elif status == 422:
        print("ℹ️  仓库已存在，继续...")
        return {"html_url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}"}
    else:
        print(f"❌ 创建仓库失败: {status}")
        print(f"响应: {response}")
        return None

def push_code(username, repo_url):
    """推送代码"""
    print(f"\n📤 推送代码到 GitHub...")
    
    try:
        # 配置远程仓库
        repo_url_with_token = f"https://{TOKEN}@github.com/{username}/{REPO_NAME}.git"
        
        # 检查是否已有 remote
        remotes = subprocess.check_output(["git", "remote"], cwd="/workspace", text=True).strip()
        if "origin" in remotes:
            print("ℹ️  更新现有的 remote origin")
            subprocess.run(["git", "remote", "set-url", "origin", repo_url_with_token], 
                          cwd="/workspace", check=True)
        else:
            print("➕ 添加 remote origin")
            subprocess.run(["git", "remote", "add", "origin", repo_url_with_token], 
                          cwd="/workspace", check=True)
        
        # 强制推送
        print("🚀 执行 git push...")
        result = subprocess.run(
            ["git", "push", "-u", "origin", "main", "--force"],
            cwd="/workspace",
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 代码推送成功!")
            print(f"📦 仓库地址: {repo_url}")
            return True
        else:
            print(f"❌ 推送失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 推送过程出错: {e}")
        return False

def main():
    print("=" * 80)
    print("🚀 终极完美版 - 推送代码到 GitHub 私有仓库")
    print("=" * 80)
    
    # 获取用户信息
    username = get_user_info()
    if not username:
        sys.exit(1)
    
    # 创建仓库
    repo = create_repo()
    if not repo:
        sys.exit(1)
    
    # 推送代码
    success = push_code(username, repo.get('html_url', f"https://github.com/{username}/{REPO_NAME}"))
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 完美成功!")
    else:
        print("⚠️  请检查输出")
    print("=" * 80)

if __name__ == "__main__":
    main()
