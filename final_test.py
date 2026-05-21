#!/usr/bin/env python3
"""
最终集成测试 - 使用增强版 ArkAnalyzer
"""
import time
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration

def test_enhanced_arkanalyzer():
    print("="*60)
    print("ArkTS 知识图谱系统 - 最终集成测试")
    print("="*60)
    
    project_path = Path("/workspace/complex_test_project")
    db_path = Path("/workspace/enhanced_graph.db")
    json_output = Path("/workspace/enhanced_analysis.json")
    
    if db_path.exists():
        db_path.unlink()
    
    print("\n1. 初始化数据库...")
    db = Database(db_path)
    
    print("\n2. 运行增强版 ArkAnalyzer...")
    integration = ArkAnalyzerIntegration(db)
    
    # 修改为使用增强版
    import subprocess
    wrapper_path = Path(__file__).parent / 'arkanalyzer-wrapper' / 'src' / 'ark-analyzer-enhanced.js'
    cmd = ['node', str(wrapper_path), str(project_path), str(json_output)]
    
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return
    
    print(result.stdout)
    
    print("\n3. 导入数据库...")
    result = integration.load_from_json(json_output)
    
    print(f"   导入耗时: {result['elapsed']:.3f}s")
    print(f"   文件数: {result['files']}")
    print(f"   类数: {result['classes']}")
    print(f"   方法数: {result['methods']}")
    print(f"   调用关系: {result['calls']}")
    print(f"   组件关系: {result['components']}")
    
    print("\n4. 获取统计信息...")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)
    
    db.close()

if __name__ == '__main__':
    test_enhanced_arkanalyzer()
