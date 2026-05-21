#!/usr/bin/env node

const content = `
export class Business000 {

    execute0(params: any): any {
        if (this.validate(params)) {
        this.process1();
        this.fetch5Data();
        this.validateInput();
            return result;
        }
        return null;
    }

    validate(params: any): boolean {
        return params !== null;
    }
}
`;

// 1. 先收集所有方法
const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+\s*)?\{/g;
const methods = [];
let match;

while ((match = methodPattern.exec(content)) !== null) {
    const methodName = match[1];
    if (!['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
        methods.push({
            name: methodName,
            index: match.index
        });
    }
}

console.log('=== 所有方法 ===');
methods.forEach(m => console.log(`${m.name} at ${m.index}`));

// 2. 对于每个 this 调用，找到在它之前的最后一个方法
console.log('\n=== 调用关系 ===');
const thisCallPattern = /this\.(\w+)\s*\(/g;

while ((match = thisCallPattern.exec(content)) !== null) {
    const calledName = match[1];
    const callIndex = match.index;
    
    // 找到调用点之前的方法
    const caller = methods
        .filter(m => m.index < callIndex)
        .sort((a, b) => b.index - a.index)[0];
    
    if (caller && caller.name !== calledName) {
        console.log(`${caller.name}() -> ${calledName}()`);
    }
}
