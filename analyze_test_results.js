#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

console.log('='.repeat(80));
console.log('🔍 深度分析：静态代码核验与问题发现');
console.log('='.repeat(80));

console.log('\n📊 读取 Enterprise 项目测试结果...');
const debugData = JSON.parse(fs.readFileSync('/workspace/debug_test_enterprise.json', 'utf-8'));
const results = debugData.results;

console.log('\n' + '='.repeat(80));
console.log('1️⃣ 静态代码核验 - 数据完整性检查');
console.log('='.repeat(80));

const issues = [];

// 问题1：检查类的数据完整性
console.log('\n🔍 检查类数据完整性...');
for (let i = 0; i < Math.min(20, results.classes.length); i++) {
  const cls = results.classes[i];
  console.log(`  - ${cls.name} (fileId: ${cls.fileId})`);
  
  if (cls.fileId === null || cls.fileId === undefined) {
    issues.push({
      type: 'data_integrity',
      severity: 'high',
      message: `类 ${cls.name} 缺少 fileId`,
      data: cls
    });
  }
}

// 问题2：检查方法数据完整性
console.log('\n🔍 检查方法数据完整性...');
const methodClassIds = {};
for (let i = 0; i < Math.min(30, results.methods.length); i++) {
  const method = results.methods[i];
  console.log(`  - ${method.name} (classId: ${method.classId})`);
  
  if (method.classId !== null && !methodClassIds[method.classId]) {
    methodClassIds[method.classId] = 0;
  }
  if (method.classId !== null) {
    methodClassIds[method.classId]++;
  }
}

// 问题3：特殊方法识别问题 - 发现 UI 组件被错误识别为方法！
console.log('\n🔍 分析被识别的方法...');
const suspectedFalsePositives = [];
const commonUIComponents = ['Column', 'Row', 'Text', 'Button', 'Image', 'Divider', 'List', 'ForEach', 'If'];

for (let i = 0; i < results.methods.length; i++) {
  const method = results.methods[i];
  
  for (const uiComp of commonUIComponents) {
    if (method.shortName === uiComp) {
      suspectedFalsePositives.push({
        method: method.name,
        className: method.name.split('::')[0],
        componentName: uiComp
      });
    }
  }
}

console.log(`\n⚠️ 发现 ${suspectedFalsePositives.length} 个可能被错误识别的 UI 组件！`);
if (suspectedFalsePositives.length > 0) {
  issues.push({
    type: 'false_positive',
    severity: 'critical',
    message: 'ArkTS UI 组件被错误识别为方法',
    data: suspectedFalsePositives.slice(0, 10)
  });
}

// 问题4：重复方法识别问题
console.log('\n🔍 检查重复方法名问题...');
const methodCounts = {};
for (let i = 0; i < results.methods.length; i++) {
  const key = results.methods[i].name;
  if (!methodCounts[key]) methodCounts[key] = 0;
  methodCounts[key]++;
}

const duplicates = Object.entries(methodCounts).filter(([k, v]) => v > 1);
console.log(`\n⚠️ 发现 ${duplicates.length} 个重复方法名！`);
if (duplicates.length > 0) {
  issues.push({
    type: 'duplicate_methods',
    severity: 'medium',
    message: '相同方法名被多次识别',
    data: duplicates.slice(0, 10)
  });
}

console.log('\n' + '='.repeat(80));
console.log('📋 发现的问题汇总');
console.log('='.repeat(80));

for (let i = 0; i < issues.length; i++) {
  const issue = issues[i];
  console.log(`\n🚨 [${issue.severity.toUpperCase()}] ${issue.type}:`);
  console.log(`   ${issue.message}`);
  if (issue.data && Array.isArray(issue.data)) {
    console.log(`   样本: ${JSON.stringify(issue.data.slice(0, 3))}`);
  }
}

console.log('\n' + '='.repeat(80));
console.log('🎯 下一步：修复发现的问题');
console.log('='.repeat(80));
console.log('\n1. 更新方法识别逻辑，排除 UI 组件');
console.log('2. 改进类内容提取边界识别');
console.log('3. 增强数据完整性验证');

// 保存问题报告
const report = {
  timestamp: new Date().toISOString(),
  project: 'EnterpriseApp',
  stats: {
    files: results.files.length,
    classes: results.classes.length,
    methods: results.methods.length,
    calls: results.calls.length,
    components: results.components.length
  },
  issues: issues
};

fs.writeFileSync('/workspace/ultimate_analysis_report.json', JSON.stringify(report, null, 2));
console.log(`\n💾 报告保存到：ultimate_analysis_report.json`);
