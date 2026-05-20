#!/usr/bin/env node

/**
 * 最终版 ArkAnalyzer - 简单健壮的跨文件调用关系识别
 */
const fs = require('fs');
const path = require('path');

class FinalArkAnalyzer {
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
        console.log('ArkAnalyzer 最终版');
        console.log('='.repeat(60));
        
        // 阶段1: 收集所有文件的方法
        console.log('\n阶段 1: 扫描文件和收集方法...');
        const allMethods = this.collectAllMethods();
        console.log(`  发现 ${allMethods.length} 个方法`);
        
        // 阶段2: 提取实体信息
        console.log('\n阶段 2: 提取文件和类信息...');
        this.extractEntities();
        console.log(`  文件: ${this.results.files.length}`);
        console.log(`  类: ${this.results.classes.length}`);
        console.log(`  方法: ${this.results.methods.length}`);
        
        // 阶段3: 识别调用关系
        console.log('\n阶段 3: 识别调用关系...');
        this.identifyCalls(allMethods);
        console.log(`  识别到 ${this.results.calls.length} 个调用关系`);
        
        return this.results;
    }
    
    collectAllMethods() {
        const methods = [];
        
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
                            
                            // 提取所有类定义
                            const classMatches = [...content.matchAll(/(?:export\s+)?class\s+(\w+)/g)];
                            
                            if (classMatches.length === 0) {
                                // 全局方法
                                const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\{/g;
                                let match;
                                while ((match = methodPattern.exec(content)) !== null) {
                                    const methodName = match[1];
                                    if (!['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
                                        methods.push({
                                            name: `Global::${methodName}`,
                                            filePath: filePath
                                        });
                                    }
                                }
                            } else {
                                // 为每个类提取方法
                                for (const classMatch of classMatches) {
                                    const className = classMatch[1];
                                    const classStart = classMatch.index;
                                    
                                    // 找类的结束位置
                                    let classEnd = content.length;
                                    const nextClassIndex = classMatches.indexOf(classMatch) + 1;
                                    if (nextClassIndex < classMatches.length) {
                                        classEnd = classMatches[nextClassIndex].index;
                                    }
                                    
                                    // 提取该类中的方法
                                    const classContent = content.substring(classStart, classEnd);
                                    const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\{/g;
                                    let match;
                                    
                                    while ((match = methodPattern.exec(classContent)) !== null) {
                                        const methodName = match[1];
                                        if (!['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
                                            methods.push({
                                                name: `${className}::${methodName}`,
                                                filePath: filePath
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
        return methods;
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
                            
                            // 方法 - 提取所有类中的方法
                            const classMatches = [...content.matchAll(/(?:export\s+)?class\s+(\w+)/g)];
                            
                            if (classMatches.length === 0) {
                                // 全局方法
                                const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\{/g;
                                while ((match = methodPattern.exec(content)) !== null) {
                                    const methodName = match[1];
                                    if (!['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
                                        this.results.methods.push({
                                            id: this.results.methods.length,
                                            name: `Global::${methodName}`,
                                            classId: null
                                        });
                                    }
                                }
                            } else {
                                // 为每个类提取方法
                                for (const classMatch of classMatches) {
                                    const className = classMatch[1];
                                    const classStart = classMatch.index;
                                    
                                    // 找类的结束位置
                                    let classEnd = content.length;
                                    const nextClassIndex = classMatches.indexOf(classMatch) + 1;
                                    if (nextClassIndex < classMatches.length) {
                                        classEnd = classMatches[nextClassIndex].index;
                                    }
                                    
                                    // 提取该类中的方法
                                    const classContent = content.substring(classStart, classEnd);
                                    const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\{/g;
                                    let methodMatch;
                                    
                                    while ((methodMatch = methodPattern.exec(classContent)) !== null) {
                                        const methodName = methodMatch[1];
                                        if (!['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
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
    
    identifyCalls(allMethods) {
        // 建立方法名到ID的映射
        const methodNameToId = new Map();
        this.results.methods.forEach(m => {
            methodNameToId.set(m.name, m.id);
        });
        
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
                                
                                // 找被调用的方法
                                let calleeMethod = null;
                                for (const m of allMethods) {
                                    if (m.name.endsWith(`::${calledName}`)) {
                                        calleeMethod = m;
                                        break;
                                    }
                                }
                                
                                if (calleeMethod) {
                                    const calleeId = methodNameToId.get(calleeMethod.name);
                                    if (calleeId !== undefined) {
                                        this.results.calls.push({
                                            callerId: 0,  // 简化版本
                                            calleeId: calleeId
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
    const outputPath = process.argv[3] || 'final-analysis.json';
    
    console.log(`项目路径: ${projectPath}`);
    console.log(`输出路径: ${outputPath}`);
    
    const analyzer = new FinalArkAnalyzer(projectPath);
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

module.exports = FinalArkAnalyzer;
