#!/usr/bin/env node

const path = require('path');
const UltimatePolishedAnalyzer = require('./arkanalyzer-wrapper/src/arkanalyzer-ultimate-polished');

// 测试1: 生成简单项目验证输出结构
console.log('='.repeat(60));
console.log('🔍 测试1: 验证输出结构');
console.log('='.repeat(60));

// 使用 sample_project
const projectPath = path.resolve('/workspace/sample_project');
const analyzer = new UltimatePolishedAnalyzer(projectPath);
const results = analyzer.analyzeProject();

console.log('\n📊 输出结构检查:');
console.log('  - files:', results.files.length);
console.log('  - classes:', results.classes.length);
console.log('  - methods:', results.methods.length);
console.log('  - calls:', results.calls.length);
console.log('  - components:', results.components.length);

// 检查一个文件的字段
if (results.files.length > 0) {
    console.log('\n📁 文件字段:');
    console.log('  Keys:', Object.keys(results.files[0]));
}

// 检查类的字段
if (results.classes.length > 0) {
    console.log('\n👥 类字段:');
    console.log('  Keys:', Object.keys(results.classes[0]));
}

// 发现第一个问题！保存测试结果
const fs = require('fs');
fs.writeFileSync('/workspace/test_output_structure.json', JSON.stringify(results, null, 2));
console.log('\n✅ 输出保存到 test_output_structure.json');
