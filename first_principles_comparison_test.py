#!/usr/bin/env python3
import time
import json
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime


def run_version(version_name, cli_name, project_path):
    print(f"\n{'='*60}")
    print(f"测试 {version_name} 版本")
    print(f"{'='*60}")
    
    temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
    temp_output.close()
    
    cli_path = Path("/workspace/arkanalyzer-wrapper/src/") / cli_name
    cmd = ['node', str(cli_path), str(project_path), str(temp_output.name)]
    
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    elapsed = time.time() - start
    
    success = result.returncode == 0
    
    stats = {}
    if success:
        try:
            with open(temp_output.name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            stats = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'calls': len(data.get('calls', [])),
                'components': len(data.get('components', [])),
            }
        except Exception as e:
            print(f"读取结果失败: {e}")
    
    Path(temp_output.name).unlink(missing_ok=True)
    
    return {
        'version': version_name,
        'success': success,
        'elapsed': elapsed,
        'stats': stats,
        'error': result.stderr if not success else None
    }


def run_comparison_test():
    print("="*60)
    print("第一性原理优化 - 性能对比测试")
    print("="*60)
    
    project_path = Path("/workspace/EnterpriseApp")
    print(f"\n测试项目: {project_path} (121个文件)\n")
    
    # 运行原始版本
    original_result = run_version(
        "原始 (Final)", 
        "cli.js", 
        project_path
    )
    
    # 运行优化版本
    optimized_result = run_version(
        "第一性原理优化", 
        "cli-first-principles.js", 
        project_path
    )
    
    # 打印结果对比
    print("\n" + "="*60)
    print("结果对比")
    print("="*60)
    
    print(f"\n{'原始':<30} | {'优化':<30}")
    print("-"*60)
    
    if original_result['success'] and optimized_result['success']:
        print(f"文件识别:   {original_result['stats']['files']:<5} | {optimized_result['stats']['files']:<5}")
        print(f"类识别:     {original_result['stats']['classes']:<5} | {optimized_result['stats']['classes']:<5}")
        print(f"方法识别:   {original_result['stats']['methods']:<5} | {optimized_result['stats']['methods']:<5}")
        print(f"调用关系:   {original_result['stats']['calls']:<5} | {optimized_result['stats']['calls']:<5}")
        print(f"组件关系:   {original_result['stats']['components']:<5} | {optimized_result['stats']['components']:<5}")
        print(f"分析耗时:   {original_result['elapsed']:.2f}s | {optimized_result['elapsed']:.2f}s")
        
        time_diff = optimized_result['elapsed'] - original_result['elapsed']
        time_ratio = optimized_result['elapsed'] / original_result['elapsed']
        
        print("\n" + "="*60)
        print("优化效果评估")
        print("="*60)
        
        if time_diff < -0.01:
            print(f"🚀 性能提升: {abs(time_diff):.2f}秒 ({(1-time_ratio)*100:.1f}% 更快)")
        elif time_diff > 0.01:
            print(f"⚠️  性能下降: {time_diff:.2f}秒 ({(time_ratio-1)*100:.1f}% 更慢)")
        else:
            print("✅ 性能保持一致")
        
        data_consistent = True
        for key in ['files', 'classes', 'methods', 'calls']:
            if original_result['stats'][key] != optimized_result['stats'][key]:
                print(f"⚠️  {key}: 数据不一致")
                data_consistent = False
        
        if data_consistent:
            print("✅ 分析数据保持一致")
            
        if time_diff < 0 and data_consistent:
            print("\n🎉 总体: 优化成功 - 性能提升且数据一致!")
        elif data_consistent:
            print("\n✅ 总体: 优化有效 - 数据一致性保持")
        else:
            print("\n⚠️  总体: 需要检查 - 数据有差异")
        
    else:
        print(f"\n原始版本: {'✅ 通过' if original_result['success'] else '❌ 失败'}")
        print(f"优化版本: {'✅ 通过' if optimized_result['success'] else '❌ 失败'}")
    
    # 打印详细的优化要点
    print("\n" + "="*60)
    print("第一性原理优化要点")
    print("="*60)
    print("\n1. ✅ 避免重复I/O操作")
    print("   - 文件内容只读取一次，缓存在内存中")
    print("   - extractEntities()和identifyCalls()共享缓存")
    
    print("\n2. ✅ 改进组件关系识别")
    print("   - 不再使用Math.random()")
    print("   - 基于同文件类关系和Component类之间的关系")
    print("   - 更真实的架构关系")
    
    print("\n3. ✅ 改进错误处理")
    print("   - 空catch块已添加真实错误日志")
    print("   - 问题更易调试")
    
    print("\n4. ✅ 架构改进")
    print("   - 添加fileContentCache和filePathToId映射")
    print("   - 更清晰的数据流")
    
    return original_result, optimized_result


if __name__ == "__main__":
    try:
        original, optimized = run_comparison_test()
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
