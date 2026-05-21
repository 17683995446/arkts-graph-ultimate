#!/usr/bin/env python3
"""
超大规模压力测试 - 500文件
"""
import time
import gc
import tracemalloc
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration
import subprocess

def get_memory_mb():
    if tracemalloc.is_tracing():
        current, _ = tracemalloc.get_traced_memory()
        return current / 1024 / 1024
    return 0

def test_massive():
    print("="*70)
    print("超大规模压力测试 - 500文件")
    print("="*70)
    
    project_path = Path("/workspace/massive_test_project")
    db_path = Path("/workspace/massive_test.db")
    json_path = Path("/workspace/massive_analysis.json")
    
    if db_path.exists():
        db_path.unlink()
    
    # 测试1: ArkAnalyzer分析大规模项目
    print("\n1. ArkAnalyzer分析性能...")
    analyzer_path = Path("/workspace/arkanalyzer-wrapper/src/ark-analyzer-final.js")
    cmd = ['node', str(analyzer_path), str(project_path), str(json_path)]
    
    gc.collect()
    tracemalloc.start()
    mem_start = get_memory_mb()
    
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    analyze_time = time.time() - start
    
    mem_after = get_memory_mb()
    
    print(f"   分析耗时: {analyze_time:.3f}s")
    print(f"   内存使用: {mem_after:.2f} MB")
    print(f"   文件数: {result.stdout.count('文件:')}")
    
    # 解析输出
    for line in result.stdout.split('\n'):
        if '文件:' in line or '类:' in line or '方法:' in line or '调用:' in line:
            print(f"   {line.strip()}")
    
    # 测试2: 数据库导入性能
    print("\n2. 数据库导入性能...")
    gc.collect()
    mem_before = get_memory_mb()
    
    db = Database(db_path)
    integration = ArkAnalyzerIntegration(db)
    
    start = time.time()
    result = integration.load_from_json(json_path)
    import_time = time.time() - start
    
    mem_after_import = get_memory_mb()
    
    print(f"   导入耗时: {import_time:.3f}s")
    print(f"   内存增长: {mem_after_import - mem_before:.2f} MB")
    print(f"   文件数: {result['files']}")
    print(f"   类数: {result['classes']}")
    print(f"   方法数: {result['methods']}")
    print(f"   调用关系: {result['calls']}")
    
    # 测试3: 查询性能
    print("\n3. 大规模查询性能...")
    queries = [
        ("统计信息", lambda: db.get_stats()),
        ("获取所有类", lambda: db.get_classes()),
        ("获取所有方法", lambda: db.get_methods()),
        ("获取调用图", lambda: db.get_call_graph()),
        ("获取组件图", lambda: db.get_component_graph()),
    ]
    
    for name, query in queries:
        times = []
        for _ in range(10):
            start = time.time()
            _ = query()
            elapsed = time.time() - start
            times.append(elapsed * 1000)
        
        print(f"   {name}: {sum(times)/len(times):.2f}ms (平均)")
    
    # 测试4: 数据库大小
    print("\n4. 存储效率...")
    db_size = db_path.stat().st_size
    stats = db.get_stats()
    total = sum(stats.values())
    
    print(f"   数据库大小: {db_size / 1024 / 1024:.2f} MB")
    print(f"   总记录数: {total}")
    print(f"   每MB存储记录数: {total / (db_size/1024/1024):.0f}")
    
    db.close()
    
    # 测试5: 增量更新性能
    print("\n5. 增量更新性能...")
    db = Database(db_path)
    
    # 修改一个文件
    test_file = project_path / "models" / "model_000.ets"
    if test_file.exists():
        original = test_file.read_text()
        test_file.write_text(original + "\n// Test comment\n")
        
        start = time.time()
        db.delete_file_data(test_file)
        delete_time = time.time() - start
        
        print(f"   删除旧数据: {delete_time*1000:.2f}ms")
        
        test_file.write_text(original)  # 恢复
    
    db.close()
    
    # 测试6: 内存峰值
    print("\n6. 内存管理测试...")
    gc.collect()
    tracemalloc.reset_peak()
    
    db = Database(db_path)
    for _ in range(500):
        _ = db.get_stats()
        _ = db.get_classes()
        _ = db.get_methods()
    
    _, peak = tracemalloc.get_traced_memory()
    print(f"   峰值内存: {peak / 1024 / 1024:.2f} MB")
    
    db.close()
    tracemalloc.stop()
    
    print("\n" + "="*70)
    print("超大规模测试完成")
    print("="*70)

if __name__ == '__main__':
    test_massive()
