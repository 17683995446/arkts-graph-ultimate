#!/usr/bin/env python3
"""
全面基线测试 - 深入了解系统当前状态
"""
import time
import os
import gc
import tracemalloc
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration
import subprocess

def get_memory_mb():
    """获取当前内存使用（MB）"""
    if tracemalloc.is_tracing():
        current, peak = tracemalloc.get_traced_memory()
        return current / 1024 / 1024
    return 0

def test_baseline():
    """基线性能测试"""
    print("="*70)
    print("ArkTS 知识图谱系统 - 全面基线测试")
    print("="*70)
    
    project_path = Path("/workspace/complex_test_project")
    db_path = Path("/workspace/baseline_test.db")
    json_path = Path("/workspace/baseline_analysis.json")
    
    if db_path.exists():
        db_path.unlink()
    
    # 测试1: 内存基线
    gc.collect()
    tracemalloc.start()
    mem_start = get_memory_mb()
    print(f"\n1. 内存基线: {mem_start:.2f} MB")
    
    # 测试2: 初始化性能
    print("\n2. 数据库初始化测试...")
    times = []
    for i in range(5):
        start = time.time()
        db = Database(db_path)
        elapsed = time.time() - start
        times.append(elapsed * 1000)
        db.close()
    
    print(f"   平均: {sum(times)/len(times):.2f}ms")
    print(f"   最小: {min(times):.2f}ms")
    print(f"   最大: {max(times):.2f}ms")
    
    # 测试3: ArkAnalyzer性能
    print("\n3. ArkAnalyzer性能测试...")
    analyzer_path = Path("/workspace/arkanalyzer-wrapper/src/ark-analyzer-final.js")
    cmd = ['node', str(analyzer_path), str(project_path), str(json_path)]
    
    times = []
    for i in range(3):
        start = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"   第{i+1}次: {elapsed:.3f}s")
    
    print(f"   平均: {sum(times)/len(times):.3f}s")
    
    # 测试4: 完整导入流程
    print("\n4. 完整导入流程测试...")
    gc.collect()
    mem_before = get_memory_mb()
    
    db = Database(db_path)
    integration = ArkAnalyzerIntegration(db)
    
    start = time.time()
    result = integration.load_from_json(json_path)
    import_time = time.time() - start
    
    mem_after = get_memory_mb()
    mem_growth = mem_after - mem_before
    
    print(f"   导入耗时: {import_time:.3f}s")
    print(f"   内存增长: {mem_growth:.2f} MB")
    print(f"   文件数: {result['files']}")
    print(f"   类数: {result['classes']}")
    print(f"   方法数: {result['methods']}")
    print(f"   调用关系: {result['calls']}")
    
    # 测试5: 数据库查询性能
    print("\n5. 查询性能详细测试...")
    queries = [
        ("SELECT COUNT(*) FROM files", "SELECT COUNT(*) FROM files"),
        ("SELECT COUNT(*) FROM classes", "SELECT COUNT(*) FROM classes"),
        ("SELECT COUNT(*) FROM methods", "SELECT COUNT(*) FROM methods"),
        ("SELECT COUNT(*) FROM calls", "SELECT COUNT(*) FROM calls"),
        ("SELECT * FROM methods LIMIT 100", "SELECT * FROM methods LIMIT 100"),
    ]
    
    for name, query in queries:
        times = []
        for _ in range(20):
            start = time.time()
            try:
                cursor = db._get_connection().execute(query)
                list(cursor.fetchall())
            except Exception as e:
                print(f"   {name}: ❌ {e}")
                break
            elapsed = time.time() - start
            times.append(elapsed * 1000)
        else:
            print(f"   {name}:")
            print(f"     平均: {sum(times)/len(times):.2f}ms, 最小: {min(times):.2f}ms, 最大: {max(times):.2f}ms")
    
    # 测试6: 数据库大小
    print("\n6. 数据库存储效率...")
    db_size = db_path.stat().st_size
    print(f"   数据库大小: {db_size / 1024:.2f} KB")
    
    stats = db.get_stats()
    total_records = sum(stats.values())
    print(f"   总记录数: {total_records}")
    if db_size > 0:
        print(f"   每KB存储记录数: {total_records / (db_size/1024):.2f}")
    
    db.close()
    
    # 测试7: 内存泄漏检测
    print("\n7. 内存泄漏检测（1000次查询）...")
    gc.collect()
    mem_before = get_memory_mb()
    
    db = Database(db_path)
    for i in range(1000):
        _ = db.get_stats()
        _ = db.get_classes()
        _ = db.get_methods()
        if i % 100 == 0:
            gc.collect()
            mem_current = get_memory_mb()
            print(f"   第{i}次后: {mem_current:.2f} MB (增长: {mem_current - mem_before:.2f} MB)")
    
    mem_after = get_memory_mb()
    mem_growth = mem_after - mem_before
    mem_rate = (mem_growth / max(mem_before, 1)) * 100
    
    print(f"   最终增长: {mem_growth:.2f} MB ({mem_rate:.2f}%)")
    if mem_rate < 1:
        print("   ✅ 无内存泄漏")
    else:
        print("   ⚠️ 可能有内存泄漏")
    
    db.close()
    
    # 测试8: 并发安全
    print("\n8. 并发安全测试...")
    import threading
    
    errors = []
    results = [0]
    lock = threading.Lock()
    
    def concurrent_query(iteration):
        try:
            db = Database(db_path)
            for _ in range(10):
                _ = db.get_stats()
                _ = db.get_classes()
            db.close()
            with lock:
                results[0] += 1
        except Exception as e:
            with lock:
                errors.append(str(e))
    
    threads = []
    for i in range(20):
        t = threading.Thread(target=concurrent_query, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"   成功: {results[0]}/20")
    print(f"   错误: {len(errors)}")
    if errors:
        print(f"   错误类型: {type(errors[0]).__name__}")
    
    # 测试9: 错误处理
    print("\n9. 错误处理测试...")
    test_cases = [
        ("空JSON", Path("/tmp/empty.json")),
        ("损坏的JSON", Path("/tmp/corrupt.json")),
        ("不存在的文件", Path("/tmp/nonexistent.json")),
    ]
    
    # 创建测试文件
    Path("/tmp/empty.json").write_text("{}")
    Path("/tmp/corrupt.json").write_text("{ invalid json")
    
    for name, path in test_cases:
        try:
            db = Database(Path("/tmp/test.db"))
            integration = ArkAnalyzerIntegration(db)
            result = integration.load_from_json(path)
            print(f"   {name}: ✅ 通过")
            db.close()
        except Exception as e:
            print(f"   {name}: ⚠️ {type(e).__name__}: {str(e)[:50]}")
    
    tracemalloc.stop()
    print("\n" + "="*70)
    print("基线测试完成")
    print("="*70)

if __name__ == '__main__':
    test_baseline()
