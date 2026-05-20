#!/usr/bin/env node

const path = require('path');
const fs = require('fs');

// 使用新的第一性原理优化版本
const FirstPrinciplesArkAnalyzer = require('./arkanalyzer-first-principles');

const projectPath = process.argv[2] || path.join(__dirname, '../../sample_project');
const outputPath = process.argv[3] || path.join(__dirname, 'first-principles-analysis.json');

console.log('='.repeat(60));
console.log('First Principles ArkAnalyzer');
console.log('='.repeat(60));

const analyzer = new FirstPrinciplesArkAnalyzer(projectPath);
const results = analyzer.analyzeProject();

analyzer.exportToJSON(outputPath);

console.log('\nDetailed Summary:');
console.log('-'.repeat(60));
Object.keys(results).forEach(key => {
    if (Array.isArray(results[key])) {
        console.log(`${key.padEnd(15)}: ${results[key].length}`);
    }
});
