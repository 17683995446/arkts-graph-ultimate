#!/usr/bin/env python3
import sys
from pathlib import Path

# 测试2: 验证 Python 集成流程
sys.path.insert(0, '/workspace')
from arkts_graph.core.database import Database
from arkts_graph.core.ark_analyzer_integration import ArkAnalyzerIntegration

print('='.repeat(60))
print('🔍 测试2: 验证集成流程')
print('='.repeat(60))

db = Database(Path('/workspace/test_integration.db'))
integration = ArkAnalyzerIntegration(db)

# 1. 测试 load_from_json
test_json = Path('/workspace/test_output_structure.json')

print('\n📄 加载 JSON 结果...')
try:
    result = integration.load_from_json(test_json)
    print(f'✅ 加载结果: {result}')
    
    print('\n📊 数据库统计:')
    stats = db.get_stats()
    print(f'  - 文件: {stats["files"]}')
    print(f'  - 类: {stats["classes"]}')
    print(f'  - 方法: {stats["methods"]}')
    print(f'  - 调用: {stats["calls"]}')
    print(f'  - 组件: {stats["components"]}')
    
    # 问题发现！类数量为 0！这证实了 bug！
    if stats["classes"] == 0:
        print('\n⚠️  发现关键问题: 类数量为0！')
    
except Exception as e:
    print(f'\n❌ 错误: {e}')
    import traceback
    traceback.print_exc()

db.close()
