#!/usr/bin/env python3
"""
大规模压力测试脚本
测试系统在大规模代码库下的性能和稳定性
"""
import time
import psutil
import os
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration

def get_memory_usage():
    """获取当前进程内存使用（MB）"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def test_full_sync():
    """测试全量同步性能"""
    print("\n" + "="*60)
    print("测试 1: 全量同步性能测试")
    print("="*60)
    
    project_path = Path("/workspace/complex_test_project")
    db_path = Path("/workspace/complex_test.db")
    
    if db_path.exists():
        db_path.unlink()
    
    # 记录初始内存
    mem_start = get_memory_usage()
    print(f"初始内存: {mem_start:.2f} MB")
    
    # 初始化
    print("\n1.1 初始化数据库...")
    start = time.time()
    db = Database(db_path)
    init_time = time.time() - start
    print(f"   初始化耗时: {init_time:.3f}s")
    
    # 运行 ArkAnalyzer
    print("\n1.2 运行 ArkAnalyzer 分析...")
    integration = ArkAnalyzerIntegration(db)
    json_output = Path("/workspace/complex_analysis.json")
    
    start = time.time()
    result = integration.run_arkanalyzer(project_path, json_output)
    analyze_time = time.time() - start
    print(f"   分析耗时: {analyze_time:.3f}s")
    print(f"   文件数: {result['files']}")
    print(f"   类数: {result['classes']}")
    print(f"   方法数: {result['methods']}")
    print(f"   调用关系: {result['calls']}")
    print(f"   组件数: {result['components']}")
    
    # 获取统计
    print("\n1.3 获取数据库统计...")
    start = time.time()
    stats = db.get_stats()
    query_time = time.time() - start
    print(f"   查询耗时: {query_time:.3f}s")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 记录最终内存
    mem_end = get_memory_usage()
    mem_used = mem_end - mem_start
    print(f"\n1.4 内存使用:")
    print(f"   最终内存: {mem_end:.2f} MB")
    print(f"   内存增长: {mem_used:.2f} MB")
    
    # 性能指标
    print("\n1.5 性能指标:")
    total_time = init_time + analyze_time + query_time
    files_per_sec = result['files'] / analyze_time if analyze_time > 0 else 0
    classes_per_sec = result['classes'] / analyze_time if analyze_time > 0 else 0
    print(f"   总耗时: {total_time:.3f}s")
    print(f"   文件/秒: {files_per_sec:.1f}")
    print(f"   类/秒: {classes_per_sec:.1f}")
    
    db.close()
    
    return {
        'total_time': total_time,
        'files': result['files'],
        'classes': result['classes'],
        'memory_used': mem_used,
        'success': True
    }

def test_query_performance():
    """测试查询性能"""
    print("\n" + "="*60)
    print("测试 2: 查询性能测试")
    print("="*60)
    
    db_path = Path("/workspace/complex_test.db")
    if not db_path.exists():
        print("数据库不存在，跳过查询测试")
        return None
    
    db = Database(db_path)
    
    # 测试各类查询
    queries = [
        ("获取所有类", lambda: db.get_classes()),
        ("获取所有方法", lambda: db.get_methods()),
        ("获取调用图", lambda: db.get_call_graph()),
        ("获取组件图", lambda: db.get_component_graph()),
        ("获取统计信息", lambda: db.get_stats()),
    ]
    
    results = []
    for name, query_func in queries:
        times = []
        for _ in range(10):
            start = time.time()
            query_func()
            elapsed = time.time() - start
            times.append(elapsed * 1000)  # 转换为毫秒
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n{name}:")
        print(f"  平均: {avg_time:.2f}ms")
        print(f"  最小: {min_time:.2f}ms")
        print(f"  最大: {max_time:.2f}ms")
        
        results.append({
            'name': name,
            'avg': avg_time,
            'min': min_time,
            'max': max_time
        })
    
    db.close()
    return results

def test_memory_leak():
    """测试内存泄漏"""
    print("\n" + "="*60)
    print("测试 3: 内存泄漏测试（100次查询）")
    print("="*60)
    
    db_path = Path("/workspace/complex_test.db")
    if not db_path.exists():
        print("数据库不存在，跳过内存测试")
        return None
    
    mem_start = get_memory_usage()
    print(f"初始内存: {mem_start:.2f} MB")
    
    db = Database(db_path)
    
    for i in range(100):
        _ = db.get_classes()
        _ = db.get_methods()
        _ = db.get_stats()
        
        if i % 20 == 0:
            mem_current = get_memory_usage()
            print(f"  第{i}次查询后: {mem_current:.2f} MB (增长: {mem_current - mem_start:.2f} MB)")
    
    mem_end = get_memory_usage()
    mem_growth = mem_end - mem_start
    
    print(f"\n最终内存: {mem_end:.2f} MB")
    print(f"内存增长: {mem_growth:.2f} MB")
    print(f"增长率: {(mem_growth / mem_start * 100):.2f}%")
    
    db.close()
    
    return {
        'mem_start': mem_start,
        'mem_end': mem_end,
        'mem_growth': mem_growth,
        'growth_rate': (mem_growth / mem_start * 100)
    }

def test_concurrent_updates():
    """测试并发更新"""
    print("\n" + "="*60)
    print("测试 4: 并发更新测试")
    print("="*60)
    
    db_path = Path("/workspace/complex_test.db")
    if not db_path.exists():
        print("数据库不存在，跳过并发测试")
        return None
    
    import threading
    
    errors = []
    success_count = [0]
    lock = threading.Lock()
    
    def update_worker(file_path):
        try:
            db = Database(db_path)
            db.delete_file_data(file_path)
            db.close()
            with lock:
                success_count[0] += 1
        except Exception as e:
            with lock:
                errors.append(str(e))
    
    print("启动 10 个并发更新线程...")
    threads = []
    for i in range(10):
        t = threading.Thread(target=update_worker, args=(Path(f"/test/file{i}.ets"),))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"成功更新: {success_count[0]}/10")
    if errors:
        print(f"错误数: {len(errors)}")
        for err in errors[:3]:
            print(f"  - {err}")
    
    return {
        'success': success_count[0],
        'errors': len(errors)
    }

def test_edge_cases():
    """测试边界情况"""
    print("\n" + "="*60)
    print("测试 5: 边界情况测试")
    print("="*60)
    
    test_cases = [
        ("空文件", ""),
        ("仅有注释", "// just a comment\n/* multi\nline */"),
        ("仅有装饰器", "@Entry\n@Component"),
        ("嵌套大文件", "class A {\n" + "\n".join([f"    method{i}() {{}}" for i in range(1000)]) + "\n}"),
        ("特殊字符", "class 我的类 { method() { console.log('Hello 世界'); } }"),
    ]
    
    results = []
    for name, content in test_cases:
        print(f"\n测试: {name}")
        test_file = Path("/tmp/edge_test.ets")
        try:
            test_file.write_text(content, encoding='utf-8')
            
            db_path = Path("/tmp/edge_test.db")
            if db_path.exists():
                db_path.unlink()
            
            db = Database(db_path)
            integration = ArkAnalyzerIntegration(db)
            
            start = time.time()
            result = integration.run_arkanalyzer(Path("/tmp"), test_file.parent / "edge_analysis.json")
            elapsed = time.time() - start
            
            print(f"  结果: 成功")
            print(f"  耗时: {elapsed:.3f}s")
            results.append({'name': name, 'success': True, 'time': elapsed})
            
            db.close()
        except Exception as e:
            print(f"  结果: 失败")
            print(f"  错误: {str(e)}")
            results.append({'name': name, 'success': False, 'error': str(e)})
    
    return results

def main():
    print("="*60)
    print("ArkTS 知识图谱系统 - 大规模压力测试")
    print("="*60)
    print(f"测试项目: /workspace/complex_test_project")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. 全量同步测试
    results['full_sync'] = test_full_sync()
    
    # 2. 查询性能测试
    results['query'] = test_query_performance()
    
    # 3. 内存泄漏测试
    results['memory'] = test_memory_leak()
    
    # 4. 并发更新测试
    results['concurrent'] = test_concurrent_updates()
    
    # 5. 边界情况测试
    results['edge_cases'] = test_edge_cases()
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    if results['full_sync']:
        print(f"\n✓ 全量同步: {results['full_sync']['files']} 文件, "
              f"{results['full_sync']['classes']} 类, "
              f"{results['full_sync']['total_time']:.2f}s")
    
    if results['memory']:
        print(f"✓ 内存使用: 增长 {results['memory']['mem_growth']:.2f} MB "
              f"({results['memory']['growth_rate']:.2f}%)")
    
    if results['concurrent']:
        print(f"✓ 并发测试: {results['concurrent']['success']}/10 成功")
    
    success_cases = sum(1 for r in results['edge_cases'] if r['success'])
    total_cases = len(results['edge_cases'])
    print(f"✓ 边界测试: {success_cases}/{total_cases} 成功")
    
    print("\n测试完成！")

if __name__ == '__main__':
    main()
