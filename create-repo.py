#!/usr/bin/env python3
import requests

GITHUB_TOKEN = "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"

print("="*60)
print("🚀 创建 GitHub 私有仓库...")
print("="*60)

url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {
    "name": "arkts-knowledge-graph",
    "description": "ArkTS 代码知识图谱分析系统 - 百万行级，动态更新，基于第一性原理",
    "private": True
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 201:
        print("\n✅ 私有仓库创建成功！")
        print("📦 仓库地址: https://github.com/2358384171/arkts-knowledge-graph")
    elif response.status_code == 422:
        print("\nℹ️  仓库已存在！")
        print("📦 仓库地址: https://github.com/2358384171/arkts-knowledge-graph")
    else:
        print(f"\n⚠️  响应: {response.text}")
        
except Exception as e:
    print(f"\n❌ 请求失败: {e}")

print("\n" + "="*60)
print("📋 下一步:")
print("="*60)
print("1. 如果仓库创建成功，运行:")
print("   cd /workspace && git push -u origin main")
print("\n2. 或手动访问: https://github.com/2358384171/arkts-knowledge-graph")
print("   来确认仓库状态")
