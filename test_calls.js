#!/usr/bin/env node

const content = `
export class Models0000 {

    method0(): void {
        for (let i = 0; i < 10; i++) { }
        this.process0();
    }

    method1(): void {
        this.anotherMethod();
    }
}
`;

console.log("测试 this 调用识别...");

const callPattern = /this\.(\w+)\s*\(/g;
let match;
let count = 0;

while ((match = callPattern.exec(content)) !== null) {
    console.log(`找到调用: this.${match[1]}() at ${match.index}`);
    count++;
}

console.log(`\n总共找到 ${count} 个调用`);

// 测试所有方法
console.log("\n所有方法:");
const methodPattern = /(?<=\n)\s*(async\s+)?(\w+)\s*\([^)]*\)(?::\s*\w+)?\s*\{/g;
const methods = [];
while ((match = methodPattern.exec(content)) !== null) {
    const methodName = match[2];
    if (!['if', 'for', 'while', 'switch', 'class', 'struct'].includes(methodName)) {
        methods.push(`${methodName}`);
        console.log(`  - ${methodName}`);
    }
}

console.log("\n方法集:", methods);
