#!/usr/bin/env python3
"""
确认仓库设置为 private
"""
import urllib.request
import urllib.error
import json

def main():
    github_token = "REDACTED_GITHUB_TOKEN"
    repo_owner = "17683995446"
    repo_name = "arkts-graph-ultimate"
    
    print("=" * 80)
    print("✅ 检查 GitHub 仓库状态")
    print("=" * 80)
    
    # 检查仓库信息
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "arkts-graph/1.0"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            print(f"\n✅ 仓库信息:")
            print(f"   - 名称: {data['name']}")
            print(f"   - 所有者: {data['owner']['login']}")
            print(f"   - 私有状态: {'✅ 私有' if data['private'] else '❌ 公开'}")
            print(f"   - 仓库地址: {data['html_url']}")
            print(f"   - 默认分支: {data['default_branch']}")
            print(f"   - 最后更新: {data['updated_at']}")
            
            if data['private']:
                print("\n🎉 仓库已成功设置为私有！")
                print("=" * 80)
                return True
            else:
                print("\n⚠️ 仓库是公开的，正在设置为私有...")
                
                # 更新仓库设置为 private
                update_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
                update_data = json.dumps({"private": True}).encode('utf-8')
                
                update_req = urllib.request.Request(
                    update_url,
                    data=update_data,
                    headers=headers,
                    method="PATCH"
                )
                
                with urllib.request.urlopen(update_req) as update_response:
                    updated_data = json.loads(update_response.read().decode('utf-8'))
                    print("\n✅ 仓库已成功设置为私有！")
                    print("=" * 80)
                    
    except urllib.error.HTTPError as e:
        print(f"\n❌ API 请求失败: {e.code}")
        print(f"错误信息: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        return False

if __name__ == "__main__":
    main()
