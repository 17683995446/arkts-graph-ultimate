#!/usr/bin/env node

const path = require('path');
const fs = require('fs');
const UltimatePolishedAnalyzer = require('./arkanalyzer-wrapper/src/arkanalyzer-ultimate-polished');

console.log('='.repeat(60));
console.log('🧪 分层测试1: 静态走读与核心逻辑');
console.log('='.repeat(60));

// 测试各种边界情况
const testCases = [
    { name: 'Sample Project', path: '/workspace/sample_project' },
    { name: 'Enterprise App', path: '/workspace/EnterpriseApp' },
    { name: 'Chaos Project', path: '/workspace/ChaosTestProject' }
];

for (const test of testCases) {
    console.log(`\n🔍 测试: ${test.name}`);
    console.log('='.repeat(60));
    
    const analyzer = new UltimatePolishedAnalyzer(test.path);
    const results = analyzer.analyzeProject();
    
    console.log('\n📊 结果统计:');
    console.log(`  - 文件: ${results.files.length}`);
    console.log(`  - 类: ${results.classes.length}`);
    console.log(`  - 方法: ${results.methods.length}`);
    console.log(`  - 调用关系: ${results.calls.length}`);
    console.log(`  - 组件关系: ${results.components.length}`);
    
    // 检查数据完整性
    let issues = [];
    
    // 检查类是否有 fileId
    const classesMissingFileId = results.classes.filter(c => c.fileId == null);
    if (classesMissingFileId.length > 0) {
        issues.push(`${classesMissingFileId.length} 个类缺少 fileId`);
    }
    
    // 检查方法是否有 classId 当它们属于类时
    const methodClassIds = results.methods.filter(m => m.classId != null).map(m => m.classId);
    const validClassIds = results.classes.map(c => c.id);
    const invalidMethodClassIds = methodClassIds.filter(id => !validClassIds.includes(id));
    if (invalidMethodClassIds.length > 0) {
        issues.push(`${invalidMethodClassIds.length} 个方法有无效的 classId`);
    }
    
    if (issues.length > 0) {
        console.log('\n⚠️  发现问题:');
        issues.forEach(issue => console.log(`  - ${issue}`));
    } else {
        console.log('\n✅ 没有发现问题');
    }
}

console.log('\n' + '='.repeat(60));
console.log('🧪 测试1完成');
console.log('='.repeat(60));
