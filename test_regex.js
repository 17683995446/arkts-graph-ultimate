#!/usr/bin/env node

const content = `
export class Models0000 {

    method0(): void {
        for (let i = 0; i < 10; i++) { }
        this.process0();
    }

    method1(): void {
        for (let i = 0; i < 10; i++) { }
        if (x1 > 0) { }
    }
}
`;

console.log("测试正则表达式匹配...");

const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\{/g;
let match;
let count = 0;

while ((match = methodPattern.exec(content)) !== null) {
    console.log(`找到方法: ${match[1]} at index ${match.index}`);
    count++;
}

console.log(`\n总共找到 ${count} 个方法`);

// 尝试简化版
console.log("\n尝试简化版...");
const simplePattern = /(\w+)\s*\([^)]*\)\s*\{/g;
count = 0;

while ((match = simplePattern.exec(content)) !== null) {
    console.log(`找到: ${match[1]} at index ${match.index}`);
    count++;
}

console.log(`\n总共找到 ${count} 个`);

// 测试class匹配
console.log("\n测试class匹配...");
const classMatches = [...content.matchAll(/(?:export\s+)?class\s+(\w+)/g)];
console.log(`找到 ${classMatches.length} 个类`);
classMatches.forEach(m => {
    console.log(`类: ${m[1]} at ${m.index}`);
});
