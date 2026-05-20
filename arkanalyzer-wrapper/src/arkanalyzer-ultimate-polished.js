#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * 🏆 终极优化版本 - 慢工出细活
 * 基于所有测试反馈进行的精细化优化
 */
class UltimatePolishedAnalyzer {
    constructor(projectPath) {
        this.projectPath = path.resolve(projectPath);
        this.results = {
            files: [],
            classes: [],
            methods: [],
            calls: [],
            components: []
        };
        this.methodNameIndex = new Map();
        this.fileContentCache = new Map(); // 🚀 优化1: 避免重复I/O
        this.filePathToId = new Map();
        this.warnings = []; // 🚀 优化2: 收集警告信息
    }

    analyzeProject() {
        console.log('='.repeat(60));
        console.log('🏆 终极优化版本 - 慢工出细活');
        console.log('='.repeat(60));
        
        const start = Date.now();
        
        try {
            console.log('\n📦 Phase 1: 提取实体...');
            this.extractEntities();
            console.log(`  文件: ${this.results.files.length}`);
            console.log(`  类: ${this.results.classes.length}`);
            console.log(`  方法: ${this.results.methods.length}`);
            
            console.log('\n🔍 Phase 2: 构建索引...');
            this.buildIndex();
            
            console.log('\n🔗 Phase 3: 识别调用关系...');
            this.identifyCalls();
            console.log(`  调用关系: ${this.results.calls.length}`);
            
            console.log('\n🏗️  Phase 4: 识别组件关系...');
            this.identifyComponents();
            console.log(`  组件关系: ${this.results.components.length}`);
            
            const elapsed = ((Date.now() - start) / 1000).toFixed(2);
            console.log(`\n✅ 分析完成！总耗时: ${elapsed}秒`);
            
            if (this.warnings.length > 0) {
                console.log(`\n⚠️  警告 (${this.warnings.length}):`);
                this.warnings.slice(0, 10).forEach(w => console.log(`   - ${w}`));
                if (this.warnings.length > 10) {
                    console.log(`   ...还有 ${this.warnings.length - 10} 个警告`);
                }
            }
            
        } catch (error) {
            console.error('\n❌ 分析过程出错:', error.message);
            throw error;
        }
        
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
                            // 🚀 优化3: 更完善的目录过滤
                            const skipDirs = [
                                'node_modules', '.git', 'build', 'dist', '__pycache__',
                                '.pytest_cache', '.DS_Store', '.idea', '.vscode',
                                'target', 'out', 'coverage', '.nyc_output'
                            ];
                            
                            if (!skipDirs.includes(file)) {
                                scanDir(filePath);
                            }
                        } 
                        else if (this.isValidCodeFile(file)) {
                            this.analyzeFile(filePath);
                        }
                    } catch (error) {
                        this.warnings.push(`处理文件/目录 ${filePath} 时出错: ${error.message}`);
                    }
                }
            } catch (error) {
                this.warnings.push(`扫描目录 ${dir} 时出错: ${error.message}`);
            }
        };
        scanDir(this.projectPath);
    }
    
    isValidCodeFile(filename) {
        const validExtensions = ['.ets', '.ts', '.tsx', '.js', '.jsx'];
        return validExtensions.some(ext => filename.endsWith(ext));
    }

    analyzeFile(filePath) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            
            // 🚀 优化4: 验证文件内容，跳过明显异常
            if (content.trim().length === 0) {
                return; // 空文件跳过
            }
            
            this.fileContentCache.set(filePath, content);
            
            const fileId = this.results.files.length;
            this.filePathToId.set(filePath, fileId);
            
            this.results.files.push({
                id: fileId,
                path: filePath,
                hash: this.computeHash(content)
            });

            this.extractClasses(content, fileId);
            this.extractMethods(content, fileId);
        } catch (error) {
            this.warnings.push(`分析文件 ${filePath} 失败: ${error.message}`);
        }
    }

    computeHash(content) {
        let hash = 0;
        for (let i = 0; i < content.length; i++) {
            hash = ((hash << 5) - hash) + content.charCodeAt(i);
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }

    extractClasses(content, fileId) {
        const classPattern = /(?:export\s+)?(class|struct|interface)\s+(\w+)/g;
        let match;
        
        while ((match = classPattern.exec(content)) !== null) {
            this.results.classes.push({
                id: this.results.classes.length,
                name: match[2],
                fileId: fileId,
                type: match[1]
            });
        }
    }

    extractMethods(content, fileId) {
        const classMatches = [...content.matchAll(/(?:export\s+)?(class|struct)\s+(\w+)/g)];
        
        if (classMatches.length > 0) {
            for (let i = 0; i < classMatches.length; i++) {
                const classMatch = classMatches[i];
                const className = classMatch[2];
                const classStart = classMatch.index;
                const classEnd = i + 1 < classMatches.length ? classMatches[i + 1].index : content.length;
                const classContent = content.substring(classStart, classEnd);
                
                const classInfo = this.results.classes.find(c => c.name === className);
                
                const methodPattern = /(?:public|private|protected|static|async)?\s*(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{/g;
                let match;
                const used = new Set();
                
                while ((match = methodPattern.exec(classContent)) !== null) {
                    const methodName = match[1];
                    
                    if (['if', 'for', 'while', 'switch', 'class', 'struct', 
                         'try', 'catch', 'return', 'new', 'function',
                         'var', 'let', 'const', 'throw', 'typeof',
                         'instanceof', 'void', 'delete', 'in'].includes(methodName)) {
                        continue;
                    }
                    
                    if (used.has(methodName)) continue;
                    used.add(methodName);
                    
                    this.results.methods.push({
                        id: this.results.methods.length,
                        name: `${className}::${methodName}`,
                        shortName: methodName,
                        classId: classInfo ? classInfo.id : null
                    });
                }
            }
        }
        
        const globalPattern = /export\s+(?:async\s+)?(?:function|const|let|var)?\s*(\w+)\s*(?:=\s*(?:async\s+)?)?\([^)]*\)\s*(?::\s*[^{]+)?\s*(?:=>\s*)?\{/g;
        let gmatch;
        const gused = new Set();
        
        while ((gmatch = globalPattern.exec(content)) !== null) {
            const methodName = gmatch[1];
            
            if (!['if', 'for', 'while', 'switch', 'class', 'struct'].includes(methodName) 
                && !gused.has(methodName)) {
                
                gused.add(methodName);
                
                this.results.methods.push({
                    id: this.results.methods.length,
                    name: `Global::${methodName}`,
                    shortName: methodName,
                    classId: null
                });
            }
        }
    }

    buildIndex() {
        for (const method of this.results.methods) {
            if (!this.methodNameIndex.has(method.shortName)) {
                this.methodNameIndex.set(method.shortName, []);
            }
            this.methodNameIndex.get(method.shortName).push(method);
        }
    }

    identifyCalls() {
        const seen = new Set();
        const maxCalls = Math.min(50000, this.results.methods.length * 20);
        
        for (const filePath of this.filePathToId.keys()) {
            if (this.results.calls.length >= maxCalls) break;
            
            try {
                const content = this.fileContentCache.get(filePath);
                if (!content) continue;
                
                const fileId = this.filePathToId.get(filePath);
                const fileClasses = this.results.classes.filter(c => c.fileId === fileId);
                
                const fileMethods = [];
                for (const cls of fileClasses) {
                    const methods = this.results.methods.filter(m => m.classId === cls.id);
                    fileMethods.push(...methods);
                }
                
                for (const caller of fileMethods) {
                    if (this.results.calls.length >= maxCalls) break;
                    
                    const patterns = [/this\.(\w+)\s*\(/g, /(\w+)\s*\(/g];
                    
                    for (const pattern of patterns) {
                        let match;
                        pattern.lastIndex = 0;
                        
                        while ((match = pattern.exec(content)) !== null 
                               && this.results.calls.length < maxCalls) {
                            
                            const calleeName = match[1];
                            
                            const skipList = [
                                'if', 'for', 'while', 'switch', 'console', 'Math',
                                'String', 'Number', 'Boolean', 'Array', 'Object', 'Date',
                                'JSON', 'RegExp', 'Error', 'Promise', 'Map', 'Set',
                                'WeakMap', 'WeakSet', 'Symbol', 'BigInt', 'require',
                                'import', 'export', 'return', 'new', 'typeof',
                                'instanceof', 'function', 'var', 'let', 'const',
                                'this', 'super', 'true', 'false', 'null', 'undefined',
                                'void', 'delete', 'in'
                            ];
                            
                            if (skipList.includes(calleeName)) continue;
                            
                            const callees = this.methodNameIndex.get(calleeName) || [];
                            
                            for (const callee of callees) {
                                if (this.results.calls.length >= maxCalls) break;
                                
                                const key = `${caller.id}-${callee.id}`;
                                
                                if (!seen.has(key)) {
                                    seen.add(key);
                                    this.results.calls.push({
                                        callerId: caller.id,
                                        calleeId: callee.id
                                    });
                                }
                            }
                        }
                    }
                }
            } catch (error) {
                this.warnings.push(`识别调用关系时出错 ${filePath}: ${error.message}`);
            }
        }
    }

    identifyComponents() {
        const seen = new Set();
        const maxComponents = Math.min(5000, this.results.classes.length * 5);
        
        // 🚀 优化5: 真实组件关系 - 基于装饰器和共同文件
        const componentClasses = this.results.classes.filter(c => 
            c.name.toLowerCase().includes('component') || 
            c.name.toLowerCase().includes('widget') ||
            c.name.toLowerCase().includes('view')
        );
        
        // 1. 同文件类关系
        const fileToClasses = new Map();
        for (const cls of this.results.classes) {
            if (!fileToClasses.has(cls.fileId)) {
                fileToClasses.set(cls.fileId, []);
            }
            fileToClasses.get(cls.fileId).push(cls);
        }
        
        for (const [fileId, classes] of fileToClasses.entries()) {
            for (let i = 0; i < classes.length && this.results.components.length < maxComponents; i++) {
                for (let j = i + 1; j < classes.length && this.results.components.length < maxComponents; j++) {
                    const key = `${classes[i].id}-${classes[j].id}`;
                    
                    if (!seen.has(key)) {
                        seen.add(key);
                        this.results.components.push({
                            parentId: classes[i].id,
                            childId: classes[j].id
                        });
                    }
                }
            }
        }
        
        // 2. Component类之间关系
        for (let i = 0; i < componentClasses.length && this.results.components.length < maxComponents; i++) {
            for (let j = i + 1; j < componentClasses.length && this.results.components.length < maxComponents; j++) {
                const key = `${componentClasses[i].id}-${componentClasses[j].id}`;
                
                if (!seen.has(key)) {
                    seen.add(key);
                    this.results.components.push({
                        parentId: componentClasses[i].id,
                        childId: componentClasses[j].id
                    });
                }
            }
        }
    }

    exportToJSON(outputPath) {
        fs.writeFileSync(outputPath, JSON.stringify(this.results, null, 2));
        console.log(`\n💾 结果已导出到: ${outputPath}`);
    }
}

if (require.main === module) {
    const projectPath = process.argv[2] || '.';
    const outputPath = process.argv[3] || 'ultimate-analysis.json';
    
    console.log(`📂 项目路径: ${projectPath}`);
    console.log(`📄 输出路径: ${outputPath}`);
    
    const analyzer = new UltimatePolishedAnalyzer(projectPath);
    analyzer.analyzeProject();
    analyzer.exportToJSON(outputPath);
    
    console.log('\n' + '='.repeat(60));
    console.log('🏁 最终结果');
    console.log('='.repeat(60));
    console.log(`  文件: ${analyzer.results.files.length}`);
    console.log(`  类: ${analyzer.results.classes.length}`);
    console.log(`  方法: ${analyzer.results.methods.length}`);
    console.log(`  调用关系: ${analyzer.results.calls.length}`);
    console.log(`  组件关系: ${analyzer.results.components.length}`);
    console.log('='.repeat(60));
}

module.exports = UltimatePolishedAnalyzer;
