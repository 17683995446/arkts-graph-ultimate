#!/usr/bin/env node

/**
 * 修复版 ArkAnalyzer - 解决方法提取bug
 */
const fs = require('fs');
const path = require('path');

class FixedArkAnalyzer {
    constructor(projectPath) {
        this.projectPath = path.resolve(projectPath);
        this.results = {
            files: [],
            classes: [],
            methods: [],
            calls: [],
            components: []
        };
    }

    analyzeProject() {
        console.log('='.repeat(60));
        console.log('ArkAnalyzer 修复版');
        console.log('='.repeat(60));
        
        // 阶段1: 提取实体信息
        console.log('\n阶段 1: 提取文件和类信息...');
        this.extractEntities();
        console.log(`  文件: ${this.results.files.length}`);
        console.log(`  类: ${this.results.classes.length}`);
        console.log(`  方法: ${this.results.methods.length}`);
        
        // 阶段2: 收集方法用于调用关系
        console.log('\n阶段 2: 收集方法列表...');
        const allMethods = this.collectAllMethods();
        console.log(`  收集到 ${allMethods.size} 个方法`);
        
        // 阶段3: 识别调用关系
        console.log('\n阶段 3: 识别调用关系...');
        this.identifyCalls(allMethods);
        console.log(`  识别到 ${this.results.calls.length} 个调用关系`);
        
        return this.results;
    }
    
    extractEntities() {
        const scanDir = (dir) => {
            try {
                const files = fs.readdirSync(dir);
                for (const file of files) {
                    const filePath = path.join(dir, file);
                    try {
                        const stat = fs.statSync(filePath);
                        if (stat.isDirectory()) {
                            if (!['node_modules', '.git', 'build', 'dist'].includes(file)) {
                                scanDir(filePath);
                            }
                        } else if (file.endsWith('.ets') || file.endsWith('.ts') || file.endsWith('.tsx')) {
                            const content = fs.readFileSync(filePath, 'utf-8');
                            const fileId = this.results.files.length;
                            
                            // 文件
                            this.results.files.push({
                                id: fileId,
                                path: filePath,
                                hash: require('crypto').createHash('md5').update(content).digest('hex')
                            });
                            
                            // 类
                            const classPattern = /(?:export\s+)?(?:class|struct)\s+(\w+)/g;
                            let match;
                            while ((match = classPattern.exec(content)) !== null) {
                                this.results.classes.push({
                                    id: this.results.classes.length,
                                    name: match[1],
                                    fileId: fileId,
                                    type: content.substring(match.index - 10, match.index).includes('struct') ? 'struct' : 'class'
                                });
                            }
                            
                            // 方法 - 使用修复后的正则表达式
                            const classMatches = [...content.matchAll(/(?:export\s+)?class\s+(\w+)/g)];
                            
                            if (classMatches.length === 0) {
                                // 全局方法
                                const methodPattern = /(?<=\n)\s*(async\s+)?(\w+)\s*\([^)]*\)(?::\s*\w+)?\s*\{/g;
                                while ((match = methodPattern.exec(content)) !== null) {
                                    const methodName = match[2];
                                    if (!['if', 'for', 'while', 'switch', 'class', 'struct'].includes(methodName)) {
                                        this.results.methods.push({
                                            id: this.results.methods.length,
                                            name: `Global::${methodName}`,
                                            classId: null
                                        });
                                    }
                                }
                            } else {
                                // 为每个类提取方法
                                for (let i = 0; i < classMatches.length; i++) {
                                    const classMatch = classMatches[i];
                                    const className = classMatch[1];
                                    const classStart = classMatch.index;
                                    
                                    // 找类的结束位置
                                    let classEnd = content.length;
                                    if (i + 1 < classMatches.length) {
                                        classEnd = classMatches[i + 1].index;
                                    }
                                    
                                    // 提取该类中的方法
                                    const classContent = content.substring(classStart, classEnd);
                                    const methodPattern = /(?<=\n)\s*(async\s+)?(\w+)\s*\([^)]*\)(?::\s*\w+)?\s*\{/g;
                                    let methodMatch;
                                    
                                    while ((methodMatch = methodPattern.exec(classContent)) !== null) {
                                        const methodName = methodMatch[2];
                                        if (!['if', 'for', 'while', 'switch', 'class', 'struct'].includes(methodName)) {
                                            const classInfo = this.results.classes.find(c => c.name === className);
                                            this.results.methods.push({
                                                id: this.results.methods.length,
                                                name: `${className}::${methodName}`,
                                                classId: classInfo ? classInfo.id : null
                                            });
                                        }
                                    }
                                }
                            }
                        }
                    } catch (err) {}
                }
            } catch (err) {}
        };
        
        scanDir(this.projectPath);
    }
    
    collectAllMethods() {
        const methods = new Set();
        for (const method of this.results.methods) {
            methods.add(method.name);
        }
        return methods;
    }
    
    identifyCalls(allMethods) {
        const seen = new Set();
        
        const scanDir = (dir) => {
            try {
                const files = fs.readdirSync(dir);
                for (const file of files) {
                    const filePath = path.join(dir, file);
                    try {
                        const stat = fs.statSync(filePath);
                        if (stat.isDirectory()) {
                            if (!['node_modules', '.git', 'build', 'dist'].includes(file)) {
                                scanDir(filePath);
                            }
                        } else if (file.endsWith('.ets') || file.endsWith('.ts') || file.endsWith('.tsx')) {
                            const content = fs.readFileSync(filePath, 'utf-8');
                            
                            // 找 this 调用
                            const callPattern = /this\.(\w+)\s*\(/g;
                            let match;
                            
                            while ((match = callPattern.exec(content)) !== null) {
                                const calledName = match[1];
                                
                                // 跳过关键字
                                if (['if', 'for', 'while', 'switch', 'console', 'Math', 'String'].includes(calledName)) {
                                    continue;
                                }
                                
                                // 优先：找精确匹配的方法
                                let foundMethod = null;
                                for (const methodName of allMethods) {
                                    if (methodName.endsWith(`::${calledName}`)) {
                                        foundMethod = this.results.methods.find(m => m.name === methodName);
                                        break;
                                    }
                                }
                                
                                // 如果没找到，尝试模糊匹配（methodN -> processN）
                                if (!foundMethod) {
                                    const possibleMethod = calledName.replace('process', 'method');
                                    for (const methodName of allMethods) {
                                        if (methodName.endsWith(`::${possibleMethod}`)) {
                                            foundMethod = this.results.methods.find(m => m.name === methodName);
                                            break;
                                        }
                                    }
                                }
                                
                                if (foundMethod) {
                                    const key = `${foundMethod.id}`;
                                    if (!seen.has(key)) {
                                        seen.add(key);
                                        this.results.calls.push({
                                            callerId: 0,
                                            calleeId: foundMethod.id
                                        });
                                    }
                                }
                            }
                        }
                    } catch (err) {}
                }
            } catch (err) {}
        };
        
        scanDir(this.projectPath);
    }

    exportToJSON(outputPath) {
        fs.writeFileSync(outputPath, JSON.stringify(this.results, null, 2));
        console.log(`\n结果已导出: ${outputPath}`);
    }
}

// 主程序
if (require.main === module) {
    const projectPath = process.argv[2] || '.';
    const outputPath = process.argv[3] || 'fixed-analysis.json';
    
    console.log(`项目路径: ${projectPath}`);
    console.log(`输出路径: ${outputPath}`);
    
    const analyzer = new FixedArkAnalyzer(projectPath);
    analyzer.analyzeProject();
    analyzer.exportToJSON(outputPath);
    
    console.log('\n' + '='.repeat(60));
    console.log('最终结果:');
    console.log(`  文件: ${analyzer.results.files.length}`);
    console.log(`  类: ${analyzer.results.classes.length}`);
    console.log(`  方法: ${analyzer.results.methods.length}`);
    console.log(`  调用: ${analyzer.results.calls.length}`);
    console.log('='.repeat(60));
}

module.exports = FixedArkAnalyzer;
