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

// 原版（有bug）
console.log("\n原版正则:");
const oldPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\{/g;
let count = 0;
let match;
while ((match = oldPattern.exec(content)) !== null) {
    console.log(`  ${match[1]}`);
    count++;
}
console.log(`总共 ${count} 个`);

// 修复版：需要空白字符在方法名前面
console.log("\n修复版正则（需要空白字符）:");
const newPattern = /(?:^|\n)\s*(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\s*\{/gm;
count = 0;
while ((match = newPattern.exec(content)) !== null) {
    console.log(`  ${match[1]}`);
    count++;
}
console.log(`总共 ${count} 个`);

// 更好的方案：使用单词边界
console.log("\n使用单词边界:");
const wordBoundaryPattern = /(?<=\n\s+)(async\s+)?(\w+)\s*\([^)]*\)(?::\s*\w+)?\s*\{/g;
count = 0;
while ((match = wordBoundaryPattern.exec(content)) !== null) {
    console.log(`  ${match[2]}`);
    count++;
}
console.log(`总共 ${count} 个`);

// 简单有效：查找 方法名(): 或 方法名(): void {
console.log("\n简单有效方案:");
const simplePattern = /(\w+)\s*\(\s*\)\s*(?::\s*\w+)?\s*\{/g;
count = 0;
while ((match = simplePattern.exec(content)) !== null) {
    const name = match[1];
    if (!['if', 'for', 'while', 'switch', 'class', 'struct'].includes(name)) {
        console.log(`  ${name}`);
        count++;
    }
}
console.log(`总共 ${count} 个有效方法`);
