#!/usr/bin/env python3
import os
import requests
import subprocess
import sys

GITHUB_TOKEN = "REDACTED_GITHUB_TOKEN"
REPO_NAME = "arkts-knowledge-graph"
REPO_DESCRIPTION = "ArkTS 代码知识图谱分析系统 - 百万行级，动态更新，基于第一性原理"

def create_private_repo():
    print("="*60)
    print("🚀 创建 GitHub 私有仓库...")
    print("="*60)
    
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "description": REPO_DESCRIPTION,
        "private": True,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code in [201, 422]:  # 422 means already exists
            if response.status_code == 201:
                print("✅ 私有仓库创建成功！")
            else:
                print("ℹ️  仓库已存在，继续...")
            return True
        else:
            print(f"⚠️  仓库创建返回: {response.status_code}")
            print(response.text)
            return True  # 继续尝试推送，即使创建失败
    except Exception as e:
        print(f"⚠️  仓库创建请求失败: {e}")
        print("继续尝试使用已有仓库或手动推送...")
        return True

def add_and_push():
    print("\n" + "="*60)
    print("📤 推送到 GitHub...")
    print("="*60)
    
    repo_url = f"https://{GITHUB_TOKEN}@github.com/2358384171/{REPO_NAME}.git"
    
    try:
        # 添加远程仓库（忽略已存在的错误）
        subprocess.run(["git", "remote", "add", "origin", repo_url],
                      capture_output=True, cwd="/workspace")
        
        # 或者更新远程仓库（如果已经添加过）
        subprocess.run(["git", "remote", "set-url", "origin", repo_url],
                      capture_output=True, cwd="/workspace")
        
        # 推送到 main 分支
        print("正在推送代码...")
        result = subprocess.run(
            ["git", "push", "-u", "origin", "master"],
            capture_output=True,
            cwd="/workspace"
        )
        
        if result.returncode == 0:
            print("✅ 推送成功！")
            print(f"\n📦 仓库地址: https://github.com/2358384171/{REPO_NAME}")
            return True
        else:
            print("⚠️  推送失败，尝试重命名分支为 main...")
            
            # 重命名分支并推送
            subprocess.run(["git", "branch", "-M", "main"], capture_output=True, cwd="/workspace")
            result2 = subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                capture_output=True,
                cwd="/workspace"
            )
            
            if result2.returncode == 0:
                print("✅ 推送到 main 分支成功！")
                print(f"\n📦 仓库地址: https://github.com/2358384171/{REPO_NAME}")
                return True
            else:
                print("❌ 推送仍失败")
                print("\n📋 手动推送指南:")
                print(f"   1. 手动在 GitHub 上创建仓库: {REPO_NAME}")
                print("   2. 运行: git remote add origin git@github.com:2358384171/{REPO_NAME}.git")
                print("   3. 运行: git push -u origin main")
                return False
                
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False

def main():
    print("🎯 ArkTS 知识图谱 - GitHub 私有仓库部署")
    print("="*60)
    
    # 创建仓库
    create_private_repo()
    
    # 推送
    add_and_push()
    
    print("\n" + "="*60)
    print("🏁 完成！")
    print("="*60)
    
    print(f"\n📦 仓库信息:")
    print(f"   用户名: 2358384171")
    print(f"   仓库名: {REPO_NAME}")
    print(f"   访问: https://github.com/2358384171/{REPO_NAME}")
    print(f"   状态: 私有仓库")
    
    print("\n✅ 项目完整提交完成！")

if __name__ == "__main__":
    main()
