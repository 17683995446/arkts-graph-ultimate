#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class ArkAnalyzer {
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

    analyzeFile(filePath) {
        const content = fs.readFileSync(filePath, 'utf-8');
        const fileId = this.results.files.length;
        
        this.results.files.push({
            id: fileId,
            path: filePath,
            hash: this.computeHash(content)
        });

        const classes = this.extractClasses(content, fileId);
        this.results.classes.push(...classes);
        
        const methods = this.extractMethods(content, classes);
        this.results.methods.push(...methods);
        
        const calls = this.extractCallsSimple(content, methods);
        this.results.calls.push(...calls);
        
        const components = this.extractComponents(content, classes);
        this.results.components.push(...components);

        return {
            fileId,
            classes: classes.length,
            methods: methods.length,
            calls: calls.length,
            components: components.length
        };
    }

    computeHash(content) {
        const crypto = require('crypto');
        return crypto.createHash('md5').update(content).digest('hex');
    }

    extractClasses(content, fileId) {
        const classes = [];
        const classPattern = /(?:export\s+)?(?:class|struct)\s+(\w+)/g;
        let match;
        
        while ((match = classPattern.exec(content)) !== null) {
            classes.push({
                id: this.results.classes.length,
                name: match[1],
                fileId: fileId,
                type: content.substring(match.index - 10, match.index).includes('struct') ? 'struct' : 'class'
            });
        }
        
        return classes;
    }

    extractMethods(content, classes) {
        const methods = [];
        
        // 简单方法模式：方法名 (参数) { 或 async 方法名 (参数) {
        const methodPattern = /(?:async\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+\s*)?\{/g;
        let match;
        let currentClass = null;

        while ((match = methodPattern.exec(content)) !== null) {
            const methodName = match[1];
            
            // 跳过关键字
            if (['if', 'for', 'while', 'switch', 'class', 'struct', 'constructor'].includes(methodName)) {
                continue;
            }
            
            // 确定所属类
            let classId = null;
            let className = 'Global';
            
            // 在当前位置之前查找最近的类定义
            const beforeMatch = content.substring(0, match.index);
            const lastClassMatch = beforeMatch.match(/export\s+class\s+(\w+)|class\s+(\w+)/g);
            if (lastClassMatch && lastClassMatch.length > 0) {
                const lastClass = lastClassMatch[lastClassMatch.length - 1];
                const classNameMatch = lastClass.match(/(\w+)$/);
                if (classNameMatch) {
                    className = classNameMatch[1];
                    const foundClass = classes.find(c => c.name === className);
                    if (foundClass) {
                        classId = foundClass.id;
                    }
                }
            }
            
            const fullMethodName = `${className}::${methodName}`;
            
            // 检查是否已存在
            if (!methods.find(m => m.name === fullMethodName)) {
                methods.push({
                    id: this.results.methods.length,
                    name: fullMethodName,
                    classId: classId,
                    className: className,
                    shortName: methodName,
                    index: match.index
                });
            }
        }

        return methods;
    }

    extractCallsSimple(content, methods) {
        const calls = [];
        const seen = new Set();
        
        if (methods.length === 0) {
            console.log('No methods found!');
            return calls;
        }
        
        console.log(`Processing ${methods.length} methods for calls...`);
        
        // 方法名到方法对象的映射（按shortName）
        const methodMap = new Map();
        methods.forEach(m => {
            if (!methodMap.has(m.shortName)) {
                methodMap.set(m.shortName, []);
            }
            methodMap.get(m.shortName).push(m);
        });
        
        // 收集所有方法的shortName
        const methodShortNames = methods.map(m => m.shortName);
        
        // 查找所有 this.method() 调用
        const thisCallPattern = /this\.(\w+)\s*\(/g;
        let match;
        
        while ((match = thisCallPattern.exec(content)) !== null) {
            const calledName = match[1];
            const callIndex = match.index;
            
            // 找到所有调用点之前的方法
            const callerCandidates = methods.filter(m => m.index < callIndex);
            
            if (callerCandidates.length === 0) {
                console.log(`Call to ${calledName}() at ${callIndex} - no callers found`);
                continue;
            }
            
            // 按位置排序，取最后一个（最近的）
            callerCandidates.sort((a, b) => b.index - a.index);
            const caller = callerCandidates[0];
            
            // 找到被调用的方法
            const calleeMethods = methodMap.get(calledName);
            if (!calleeMethods || calleeMethods.length === 0) {
                console.log(`Called method ${calledName}() not found in method map`);
                continue;
            }
            
            // 找第一个与调用者不同的方法
            let callee = calleeMethods[0];
            for (const cm of calleeMethods) {
                if (cm.id !== caller.id) {
                    callee = cm;
                    break;
                }
            }
            
            // 避免重复
            const key = `${caller.id}-${callee.id}`;
            if (caller.id !== callee.id && !seen.has(key)) {
                seen.add(key);
                calls.push({
                    callerId: caller.id,
                    calleeId: callee.id
                });
                console.log(`Found call: ${caller.shortName}() -> ${callee.shortName}()`);
            }
        }
        
        console.log(`Total calls found: ${calls.length}`);
        return calls;
    }

    extractComponents(content, classes) {
        const components = [];
        const seen = new Set();
        
        // 查找 JSX 风格的组件使用 <Component 或 <Component()
        const jsxPattern = /<(\w+)[^>]*>(?:[\s\S]*?)<\/\1>|<(\w+)[^>]*\/>/g;
        let match;
        
        while ((match = jsxPattern.exec(content)) !== null) {
            const componentName = match[1] || match[2];
            
            // 查找是否是自定义组件
            const componentClass = classes.find(c => c.name === componentName && c.type === 'struct');
            
            if (componentClass) {
                // 查找父组件
                let parentClass = classes.find(c => c.id !== componentClass.id);
                let parentId = parentClass ? parentClass.id : 0;
                
                const key = `${parentId}-${componentClass.id}`;
                if (!seen.has(key)) {
                    seen.add(key);
                    components.push({
                        parentId: parentId,
                        childId: componentClass.id
                    });
                }
            }
        }
        
        return components;
    }

    analyzeProject() {
        const analyzeDir = (dir) => {
            try {
                const files = fs.readdirSync(dir);
                
                for (const file of files) {
                    const filePath = path.join(dir, file);
                    try {
                        const stat = fs.statSync(filePath);

                        if (stat.isDirectory()) {
                            if (!['node_modules', '.git', 'build', 'dist', '.DS_Store'].includes(file)) {
                                analyzeDir(filePath);
                            }
                        } else if (file.endsWith('.ets') || file.endsWith('.ts') || file.endsWith('.tsx')) {
                            try {
                                this.analyzeFile(filePath);
                            } catch (error) {
                                console.error(`Error analyzing ${filePath}:`, error.message);
                            }
                        }
                    } catch (err) {
                        // 忽略访问错误
                    }
                }
            } catch (err) {
                console.error(`Cannot read directory ${dir}:`, err.message);
            }
        };

        analyzeDir(this.projectPath);
        return this.results;
    }

    exportToJSON(outputPath) {
        fs.writeFileSync(outputPath, JSON.stringify(this.results, null, 2));
        console.log(`Analysis results exported to ${outputPath}`);
    }
}

if (require.main === module) {
    const projectPath = process.argv[2] || '.';
    const outputPath = process.argv[3] || 'analysis-results.json';
    
    console.log('Starting ArkAnalyzer...');
    console.log(`Project path: ${projectPath}`);
    console.log(`Output path: ${outputPath}`);
    
    const analyzer = new ArkAnalyzer(projectPath);
    const results = analyzer.analyzeProject();
    
    analyzer.exportToJSON(outputPath);
    
    console.log('\nAnalysis Summary:');
    console.log(`- Files: ${results.files.length}`);
    console.log(`- Classes: ${results.classes.length}`);
    console.log(`- Methods: ${results.methods.length}`);
    console.log(`- Calls: ${results.calls.length}`);
    console.log(`- Components: ${results.components.length}`);
}

module.exports = ArkAnalyzer;
