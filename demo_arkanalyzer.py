#!/usr/bin/env python3
"""
ArkTS 知识图谱系统 - 功能演示（使用 Arkanalyzer）
"""
import time
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration


def demo_with_arkanalyzer():
    print("=" * 60)
    print("ArkTS 知识图谱系统 - ArkAnalyzer 集成演示")
    print("=" * 60)

    # 初始化
    sample_project = Path("/workspace/sample_project")
    db_path = Path("/workspace/arkanalyzer_graph.db")
    json_output = Path("/workspace/arkanalyzer_output.json")

    if db_path.exists():
        db_path.unlink()

    print("\n1. 初始化数据库...")
    db = Database(db_path)

    print("\n2. 运行 ArkAnalyzer 进行代码分析...")
    integration = ArkAnalyzerIntegration(db)
    result = integration.run_arkanalyzer(sample_project, json_output)
    
    print(f"   已处理 {result['files']} 个文件")
    print(f"   提取了 {result['classes']} 个类")
    print(f"   提取了 {result['methods']} 个方法")
    print(f"   提取了 {result['calls']} 个调用关系")
    print(f"   提取了 {result['components']} 个组件")
    print(f"   导入耗时 {result['elapsed']:.4f} 秒")

    print("\n3. 获取统计信息...")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n4. 获取类列表...")
    classes = db.get_classes()
    if classes:
        for cls in classes:
            print(f"   - {cls.name}")

    print("\n5. 获取方法列表...")
    methods = db.get_methods()
    if methods:
        for method in methods[:10]:  # 只显示前10个
            print(f"   - {method.name}")

    print("\n" + "=" * 60)
    print("功能演示完成！")
    print("\n启动可视化服务命令:")
    print("  python -m arkts_graph.main --project /workspace/sample_project")
    print("\nArkAnalyzer JSON 输出:")
    print(f"  {json_output}")
    print("数据库文件位置:")
    print(f"  {db_path}")
    print("=" * 60)

    db.close()


if __name__ == "__main__":
    demo_with_arkanalyzer()
