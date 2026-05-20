#!/usr/bin/env node

const path = require('path');
const ArkAnalyzer = require('./ark-analyzer-final-ultimate');

const projectPath = process.argv[2] || path.join(__dirname, '../../sample_project');
const outputPath = process.argv[3] || path.join(__dirname, 'analysis-results.json');

console.log('='.repeat(60));
console.log('ArkAnalyzer - Professional ArkTS Analysis Tool');
console.log('='.repeat(60));

const analyzer = new ArkAnalyzer(projectPath);
const results = analyzer.analyzeProject();

analyzer.exportToJSON(outputPath);

console.log('\nDetailed Summary:');
console.log('-'.repeat(60));
Object.keys(results).forEach(key => {
    if (Array.isArray(results[key])) {
        console.log(`${key.padEnd(15)}: ${results[key].length}`);
    }
});
