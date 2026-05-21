#!/usr/bin/env python3
"""
ArkTS 知识图谱系统 - 功能演示
"""
import time
from pathlib import Path
from arkts_graph.core.database import Database
from arkts_graph.core.parser import ArkTSParser
from arkts_graph.core.engine import UpdateEngine


def demo_basic_functionality():
    print("=" * 60)
    print("ArkTS 知识图谱系统 - 功能演示")
    print("=" * 60)

    # 初始化
    sample_project = Path("/workspace/sample_project")
    db_path = Path("/workspace/sample_graph.db")

    if db_path.exists():
        db_path.unlink()

    print("\n1. 初始化数据库...")
    db = Database(db_path)

    print("\n2. 执行全量同步...")
    engine = UpdateEngine(sample_project, db)
    count, elapsed = engine.full_sync()
    print(f"   已处理 {count} 个文件，耗时 {elapsed:.2f} 秒")

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
        for method in methods[:5]:  # 只显示前5个
            print(f"   - {method.name}")

    print("\n" + "=" * 60)
    print("功能演示完成！")
    print("\n启动可视化服务命令:")
    print("  python -m arkts_graph.main --project /workspace/sample_project")
    print("\n数据库文件位置:")
    print(f"  {db_path}")
    print("=" * 60)

    db.close()


if __name__ == "__main__":
    demo_basic_functionality()
