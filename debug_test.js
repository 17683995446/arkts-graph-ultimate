#!/usr/bin/env node

const fs = require('fs');

class DebugAnalyzer {
    analyzeFile(filePath) {
        const content = fs.readFileSync(filePath, 'utf-8');
        
        // 方法识别
        const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+\s*)?\{/g;
        const methods = [];
        let match;

        while ((match = methodPattern.exec(content)) !== null) {
            const methodName = match[1];
            
            if (['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
                continue;
            }
            
            methods.push({
                name: methodName,
                index: match.index
            });
        }
        
        return { methods };
    }
}

const analyzer = new DebugAnalyzer();
const result = analyzer.analyzeFile('/workspace/complex_test_project/business/business_00.ets');

console.log('=== 识别到的方法 ===');
result.methods.forEach(m => {
    console.log(`${m.name} at ${m.index}`);
});

console.log('\n=== this 调用 ===');
const content = fs.readFileSync('/workspace/complex_test_project/business/business_00.ets', 'utf-8');
const thisPattern = /this\.(\w+)\s*\(/g;
let match;
while ((match = thisPattern.exec(content)) !== null) {
    console.log(`this.${match[1]}() at ${match.index}`);
}
