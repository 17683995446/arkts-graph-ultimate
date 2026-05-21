#!/usr/bin/env node

const path = require('path');
const fs = require('fs');
const FirstPrinciplesArkAnalyzer = require('./arkanalyzer-wrapper/src/arkanalyzer-first-principles');

console.log('='.repeat(60));
console.log('🧨 深度混乱测试 - 发现真实Bug');
console.log('='.repeat(60));

const projectPath = path.resolve('/workspace/ChaosTestProject');
const outputPath = path.resolve('/workspace/chaos-analysis-result.json');

console.log(`\n测试项目: ${projectPath}`);
console.log('='.repeat(60));

const bugsFound = [];
let warnings = [];

try {
    console.log('\n启动分析...');
    const start = Date.now();
    
    // 创建分析器实例
    const analyzer = new FirstPrinciplesArkAnalyzer(projectPath);
    
    // 测试各阶段
    console.log('\n📦 Phase 1: 提取实体...');
    try {
        analyzer.extractEntities();
        console.log(`  文件: ${analyzer.results.files.length}`);
        console.log(`  类: ${analyzer.results.classes.length}`);
        console.log(`  方法: ${analyzer.results.methods.length}`);
        
        // 检查是否有异常的数据
        analyzer.results.files.forEach(file => {
            if (!file.path) {
                bugsFound.push({
                    type: '数据完整性',
                    severity: 'HIGH',
                    message: `文件缺少path字段: ${JSON.stringify(file)}`
                });
            }
        });
        
    } catch (error) {
        bugsFound.push({
            type: '提取实体',
            severity: 'CRITICAL',
            message: `extractEntities()崩溃: ${error.message}`,
            stack: error.stack
        });
    }
    
    console.log('\n🔍 Phase 2: 构建索引...');
    try {
        analyzer.buildIndex();
        console.log('  索引构建完成');
    } catch (error) {
        bugsFound.push({
            type: '构建索引',
            severity: 'CRITICAL',
            message: `buildIndex()崩溃: ${error.message}`,
            stack: error.stack
        });
    }
    
    console.log('\n🔗 Phase 3: 识别调用关系...');
    try {
        analyzer.identifyCalls();
        console.log(`  调用关系: ${analyzer.results.calls.length}`);
    } catch (error) {
        bugsFound.push({
            type: '调用关系',
            severity: 'CRITICAL',
            message: `identifyCalls()崩溃: ${error.message}`,
            stack: error.stack
        });
    }
    
    console.log('\n🏗️  Phase 4: 识别组件关系...');
    try {
        analyzer.identifyComponents();
        console.log(`  组件关系: ${analyzer.results.components.length}`);
    } catch (error) {
        bugsFound.push({
            type: '组件关系',
            severity: 'CRITICAL',
            message: `identifyComponents()崩溃: ${error.message}`,
            stack: error.stack
        });
    }
    
    const elapsed = (Date.now() - start) / 1000;
    console.log(`\n⏱️  总耗时: ${elapsed.toFixed(2)}秒`);
    
    // 分析结果，寻找潜在问题
    console.log('\n' + '='.repeat(60));
    console.log('🔍 分析结果，寻找潜在问题...');
    console.log('='.repeat(60));
    
    const results = analyzer.results;
    
    // 检查1: 文件数量太少
    if (results.files.length === 0) {
        bugsFound.push({
            type: '文件识别',
            severity: 'HIGH',
            message: '没有识别到任何文件！'
        });
    } else if (results.files.length < 50) {
        warnings.push({
            type: '文件识别',
            message: `只识别了${results.files.length}个文件，可能存在漏识别`
        });
    }
    
    // 检查2: 方法数量为0
    if (results.methods.length === 0) {
        bugsFound.push({
            type: '方法识别',
            severity: 'HIGH',
            message: '没有识别到任何方法！'
        });
    }
    
    // 检查3: 类数量异常
    if (results.files.length > 10 && results.classes.length === 0) {
        bugsFound.push({
            type: '类识别',
            severity: 'MEDIUM',
            message: '有文件但没有类，可能存在识别问题'
        });
    }
    
    // 检查4: 空对象
    ['files', 'classes', 'methods', 'calls', 'components'].forEach(key => {
        if (results[key] === null || results[key] === undefined) {
            bugsFound.push({
                type: '完整性',
                severity: 'CRITICAL',
                message: `${key} 为 null/undefined`
            });
        }
    });
    
    // 检查5: 异常的调用关系
    if (results.calls.length > 0) {
        const invalidCalls = results.calls.filter(call => {
            return call.callerId === null || call.callerId === undefined || 
                   call.calleeId === null || call.calleeId === undefined;
        });
        
        if (invalidCalls.length > 0) {
            warnings.push({
                type: '调用关系',
                message: `发现 ${invalidCalls.length} 个可能无效的调用关系`
            });
        }
    }
    
    // 检查6: 超大JSON输出
    try {
        const jsonOutput = JSON.stringify(results);
        const sizeKB = Buffer.byteLength(jsonOutput, 'utf8') / 1024;
        console.log(`\n📊 输出JSON大小: ${sizeKB.toFixed(2)} KB`);
        
        if (sizeKB > 50000) { // 50MB
            warnings.push({
                type: '输出大小',
                message: '输出JSON超大，可能存在性能或内存问题'
            });
        }
    } catch (error) {
        bugsFound.push({
            type: 'JSON序列化',
            severity: 'CRITICAL',
            message: `无法序列化结果: ${error.message}`
        });
    }
    
    // 导出结果
    console.log(`\n📄 导出结果到: ${outputPath}`);
    analyzer.exportToJSON(outputPath);
    
} catch (error) {
    bugsFound.push({
        type: '主流程',
        severity: 'CRITICAL',
        message: `整个分析过程崩溃: ${error.message}`,
        stack: error.stack
    });
}

// 输出报告
console.log('\n' + '='.repeat(60));
console.log('🧨 混乱测试报告');
console.log('='.repeat(60));

if (bugsFound.length === 0 && warnings.length === 0) {
    console.log('\n🎉 完美！没有发现Bug！');
} else {
    if (bugsFound.length > 0) {
        console.log(`\n🚨 发现 ${bugsFound.length} 个Bug:`);
        console.log('-'*60);
        bugsFound.forEach((bug, index) => {
            console.log(`\n[${index + 1}] [${bug.severity}] ${bug.type}:`);
            console.log(`   ${bug.message}`);
            if (bug.stack) {
                console.log(`   ${bug.stack.split('\n').slice(0, 3).join('\n   ')}`);
            }
        });
    }
    
    if (warnings.length > 0) {
        console.log(`\n⚠️  发现 ${warnings.length} 个警告:`);
        console.log('-'*60);
        warnings.forEach((warning, index) => {
            console.log(`\n[${index + 1}] ${warning.type}:`);
            console.log(`   ${warning.message}`);
        });
    }
}

// 保存报告
const report = {
    timestamp: new Date().toISOString(),
    bugs: bugsFound,
    warnings: warnings,
    summary: {
        bugCount: bugsFound.length,
        warningCount: warnings.length,
        status: bugsFound.length > 0 ? 'NEEDS_FIX' : 'GOOD'
    }
};

fs.writeFileSync(
    '/workspace/chaos-test-report.json',
    JSON.stringify(report, null, 2)
);

console.log('\n📝 报告已保存到: /workspace/chaos-test-report.json');

if (bugsFound.length > 0) {
    console.log('\n❌ 发现问题！需要修复。');
} else {
    console.log('\n✅ 系统表现出色！');
}
