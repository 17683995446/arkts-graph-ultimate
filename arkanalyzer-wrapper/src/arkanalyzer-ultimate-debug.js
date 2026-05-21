#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * 🎯 终极深度测试版本 - 带超详细日志
 * 每一步都有日志输出，便于发现隐藏问题！
 */
class UltimateDebugAnalyzer {
    constructor(projectPath, debug = true) {
        this.projectPath = path.resolve(projectPath);
        this.debug = debug;
        this.results = {
            files: [],
            classes: [],
            methods: [],
            calls: [],
            components: []
        };
        this.methodNameIndex = new Map();
        this.fileContentCache = new Map();
        this.filePathToId = new Map();
        this.warnings = [];
        this.errors = [];
        this.logs = [];
        
        this.log('🚀 [Init] UltimateDebugAnalyzer 初始化', { projectPath: this.projectPath });
    }

    log(message, data = null) {
        const timestamp = new Date().toISOString();
        const logEntry = { timestamp, message, data };
        this.logs.push(logEntry);
        
        if (this.debug) {
            let logStr = `[${timestamp}] ${message}`;
            if (data !== null && data !== undefined) {
                try {
                    logStr += ' ' + JSON.stringify(data).substring(0, 100);
                } catch(e) {
                    logStr += ' [data]';
                }
            }
            console.log(logStr);
        }
    }

    warn(message, data = null) {
        this.warnings.push({ message, data });
        this.log(`⚠️  [WARN] ${message}`, data);
    }

    error(message, error = null, data = null) {
        const errorInfo = { message, error: error?.stack || String(error), data };
        this.errors.push(errorInfo);
        this.log(`❌ [ERROR] ${message}`, errorInfo);
    }

    analyzeProject() {
        this.log('📦 [Step 1/4] 开始提取实体', { step: 1 });
        try {
            this.extractEntities();
            this.log('✅ [Step 1/4] 实体提取完成', {
                files: this.results.files.length,
                classes: this.results.classes.length,
                methods: this.results.methods.length
            });
        } catch (error) {
            this.error('❌ [Step 1/4] 实体提取失败', error);
            throw error;
        }

        this.log('🔍 [Step 2/4] 构建索引', { step: 2 });
        try {
            this.buildIndex();
            this.log('✅ [Step 2/4] 索引构建完成', {
                indexedMethods: this.methodNameIndex.size
            });
        } catch (error) {
            this.error('❌ [Step 2/4] 索引构建失败', error);
            throw error;
        }

        this.log('🔗 [Step 3/4] 识别调用关系', { step: 3 });
        try {
            this.identifyCalls();
            this.log('✅ [Step 3/4] 调用关系识别完成', {
                calls: this.results.calls.length
            });
        } catch (error) {
            this.error('❌ [Step 3/4] 调用关系识别失败', error);
            throw error;
        }

        this.log('🏗️  [Step 4/4] 识别组件关系', { step: 4 });
        try {
            this.identifyComponents();
            this.log('✅ [Step 4/4] 组件关系识别完成', {
                components: this.results.components.length
            });
        } catch (error) {
            this.error('❌ [Step 4/4] 组件关系识别失败', error);
            throw error;
        }

        this.log('🎉 [Complete] 完整分析成功！', {
            totalFiles: this.results.files.length,
            totalClasses: this.results.classes.length,
            totalMethods: this.results.methods.length,
            totalCalls: this.results.calls.length,
            totalComponents: this.results.components.length,
            warnings: this.warnings.length,
            errors: this.errors.length,
            totalLogs: this.logs.length
        });

        return this.results;
    }

    extractEntities() {
        this.log('📂 [extractEntities] 开始遍历目录', { dir: this.projectPath });
        const scanDir = (dir) => {
            try {
                this.log('📂 [scanDir] 正在读取', { dir });
                const files = fs.readdirSync(dir);
                this.log(`📑 [scanDir] 找到 ${files.length} 个文件/目录`);
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    const filePath = path.join(dir, file);
                    this.log(`🔎 [scanDir] 处理 [${i+1}/${files.length}]`, { filePath });
                    
                    try {
                        const stat = fs.statSync(filePath);
                        
                        if (stat.isDirectory()) {
                            const skipDirs = [
                                'node_modules', '.git', 'build', 'dist', '__pycache__',
                                '.pytest_cache', '.DS_Store', '.idea', '.vscode',
                                'target', 'out', 'coverage', '.nyc_output'
                            ];
                            
                            if (!skipDirs.includes(file)) {
                                this.log('📁 [scanDir] 递归处理子目录', { subdir: file });
                                scanDir(filePath);
                            } else {
                                this.log('⏭️  [scanDir] 跳过目录', { subdir: file });
                            }
                        } else if (this.isValidCodeFile(file)) {
                            this.log('📄 [scanDir] 处理代码文件', { file });
                            this.analyzeFile(filePath);
                        } else {
                            this.log('⏭️  [scanDir] 跳过非代码文件', { file });
                        }
                    } catch (error) {
                        this.warn(`处理文件/目录失败`, { filePath, error: error.message });
                    }
                }
            } catch (error) {
                this.error(`扫描目录失败`, error, { dir });
            }
        };
        scanDir(this.projectPath);
    }
    
    isValidCodeFile(filename) {
        const validExtensions = ['.ets', '.ts', '.tsx', '.js', '.jsx'];
        const isValid = validExtensions.some(ext => filename.endsWith(ext));
        this.log('🔍 [isValidCodeFile]', { filename, isValid });
        return isValid;
    }

    analyzeFile(filePath) {
        this.log('🔬 [analyzeFile]', { filePath });
        
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            this.log('📖 [analyzeFile] 文件读取成功', { size: content.length });
            
            if (content.trim().length === 0) {
                this.log('📄 [analyzeFile] 空文件，跳过', { filePath });
                return;
            }
            
            this.fileContentCache.set(filePath, content);
            const fileId = this.results.files.length;
            this.filePathToId.set(filePath, fileId);
            
            const hash = this.computeHash(content);
            this.log('🔐 [analyzeFile] 计算文件哈希', { hash });
            
            this.results.files.push({
                id: fileId,
                path: filePath,
                hash: hash
            });
            this.log('✅ [analyzeFile] 文件加入结果', { fileId, filesCount: this.results.files.length });

            this.log('📊 [analyzeFile] 开始提取类', { fileId });
            this.extractClasses(content, fileId);
            
            this.log('📊 [analyzeFile] 开始提取方法', { fileId });
            this.extractMethods(content, fileId);
            
        } catch (error) {
            this.error('分析文件失败', error, { filePath });
        }
    }

    computeHash(content) {
        let hash = 0;
        for (let i = 0; i < content.length; i++) {
            hash = ((hash << 5) - hash) + content.charCodeAt(i);
            hash = hash & hash;
        }
        const result = Math.abs(hash).toString(16);
        this.log('🔑 [computeHash]', { hash: result });
        return result;
    }

    extractClasses(content, fileId) {
        this.log('📚 [extractClasses]', { fileId });
        const classPattern = /(?:export\s+)?(class|struct|interface)\s+(\w+)/g;
        let match;
        let count = 0;
        
        while ((match = classPattern.exec(content)) !== null) {
            const classInfo = {
                id: this.results.classes.length,
                name: match[2],
                fileId: fileId,
                type: match[1]
            };
            this.results.classes.push(classInfo);
            count++;
            this.log('📚 [extractClasses] 发现类', { count, classInfo });
        }
        
        this.log('✅ [extractClasses] 完成', { total: count });
    }

    extractMethods(content, fileId) {
        this.log('🔧 [extractMethods] 从类中提取', { fileId });
        const classMatches = [...content.matchAll(/(?:export\s+)?(class|struct)\s+(\w+)/g)];
        this.log('🔧 [extractMethods] 找到类数量', { count: classMatches.length });
        
        if (classMatches.length > 0) {
            for (let i = 0; i < classMatches.length; i++) {
                const classMatch = classMatches[i];
                const className = classMatch[2];
                const classStart = classMatch.index;
                const classEnd = i + 1 < classMatches.length ? classMatches[i + 1].index : content.length;
                const classContent = content.substring(classStart, classEnd);
                
                this.log('🔧 [extractMethods] 处理类', { className, contentLength: classContent.length });
                
                const classInfo = this.results.classes.find(c => c.name === className);
                if (!classInfo) {
                    this.warn('找不到类信息', { className });
                    continue;
                }
                
                const methodPattern = /(?:public|private|protected|static|async)?\s*(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{/g;
                let match;
                const used = new Set();
                let methodCount = 0;
                
                while ((match = methodPattern.exec(classContent)) !== null) {
                    const methodName = match[1];
                    
                    if (['if', 'for', 'while', 'switch', 'class', 'struct', 
                         'try', 'catch', 'return', 'new', 'function',
                         'var', 'let', 'const', 'throw', 'typeof',
                         'instanceof', 'void', 'delete', 'in'].includes(methodName)) {
                        this.log('⏭️  [extractMethods] 跳过关键字', { methodName });
                        continue;
                    }
                    
                    if (used.has(methodName)) {
                        this.log('⏭️  [extractMethods] 跳过重复方法', { methodName });
                        continue;
                    }
                    
                    used.add(methodName);
                    methodCount++;
                    
                    this.results.methods.push({
                        id: this.results.methods.length,
                        name: `${className}::${methodName}`,
                        shortName: methodName,
                        classId: classInfo ? classInfo.id : null
                    });
                    this.log('✅ [extractMethods] 添加方法', { methodName, className, methodId: this.results.methods.length - 1 });
                }
                this.log('📊 [extractMethods] 类处理完成', { className, methodCount });
            }
        }
        
        this.log('🔧 [extractMethods] 提取全局方法');
        const globalPattern = /export\s+(?:async\s+)?(?:function|const|let|var)?\s*(\w+)\s*(?:=\s*(?:async\s+)?)?\([^)]*\)\s*(?::\s*[^{]+)?\s*(?:=>\s*)?\{/g;
        let gmatch;
        const gused = new Set();
        let globalMethodCount = 0;
        
        while ((gmatch = globalPattern.exec(content)) !== null) {
            const methodName = gmatch[1];
            
            if (['if', 'for', 'while', 'switch', 'class', 'struct'].includes(methodName) || gused.has(methodName)) {
                continue;
            }
            
            gused.add(methodName);
            globalMethodCount++;
            
            this.results.methods.push({
                id: this.results.methods.length,
                name: `Global::${methodName}`,
                shortName: methodName,
                classId: null
            });
            this.log('✅ [extractMethods] 添加全局方法', { methodName, methodId: this.results.methods.length - 1 });
        }
        
        this.log('✅ [extractMethods] 全部完成', { globalMethodCount, total: this.results.methods.length });
    }

    buildIndex() {
        this.log('📇 [buildIndex] 开始构建');
        for (let i = 0; i < this.results.methods.length; i++) {
            const method = this.results.methods[i];
            if (!this.methodNameIndex.has(method.shortName)) {
                this.methodNameIndex.set(method.shortName, []);
            }
            this.methodNameIndex.get(method.shortName).push(method);
            
            if (i % 100 === 0) {
                this.log('📇 [buildIndex] 进度', { processed: i + 1, total: this.results.methods.length });
            }
        }
        this.log('✅ [buildIndex] 索引构建完成', {
            uniqueShortNames: this.methodNameIndex.size,
            totalMethods: this.results.methods.length
        });
    }

    identifyCalls() {
        this.log('🔗 [identifyCalls] 开始');
        const seen = new Set();
        const maxCalls = Math.min(50000, this.results.methods.length * 20);
        
        const filePaths = Array.from(this.filePathToId.keys());
        this.log('🔗 [identifyCalls] 处理文件数量', { count: filePaths.length });
        
        for (let fileIdx = 0; fileIdx < filePaths.length && this.results.calls.length < maxCalls; fileIdx++) {
            const filePath = filePaths[fileIdx];
            const content = this.fileContentCache.get(filePath);
            
            if (!content) {
                this.warn('文件内容不在缓存', { filePath });
                continue;
            }
            
            const fileId = this.filePathToId.get(filePath);
            const fileClasses = this.results.classes.filter(c => c.fileId === fileId);
            const fileMethods = [];
            
            for (let i = 0; i < fileClasses.length; i++) {
                const cls = fileClasses[i];
                const methods = this.results.methods.filter(m => m.classId === cls.id);
                fileMethods.push(...methods);
            }
            
            this.log('🔗 [identifyCalls] 处理文件', {
                fileIdx: fileIdx + 1,
                total: filePaths.length,
                filePath,
                methodsInFile: fileMethods.length
            });
            
            for (let callerIdx = 0; callerIdx < fileMethods.length && this.results.calls.length < maxCalls; callerIdx++) {
                const caller = fileMethods[callerIdx];
                
                const patterns = [/this\.(\w+)\s*\(/g, /(\w+)\s*\(/g];
                
                for (let patternIdx = 0; patternIdx < patterns.length; patternIdx++) {
                    const pattern = patterns[patternIdx];
                    let match;
                    pattern.lastIndex = 0;
                    
                    while ((match = pattern.exec(content)) !== null && this.results.calls.length < maxCalls) {
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
                        
                        if (skipList.includes(calleeName)) {
                            continue;
                        }
                        
                        const callees = this.methodNameIndex.get(calleeName) || [];
                        
                        for (let calleeIdx = 0; calleeIdx < callees.length && this.results.calls.length < maxCalls; calleeIdx++) {
                            const callee = callees[calleeIdx];
                            const key = `${caller.id}-${callee.id}`;
                            
                            if (!seen.has(key)) {
                                seen.add(key);
                                this.results.calls.push({
                                    callerId: caller.id,
                                    calleeId: callee.id
                                });
                                
                                if (this.results.calls.length % 1000 === 0) {
                                    this.log('🔗 [identifyCalls] 进度', { calls: this.results.calls.length });
                                }
                            }
                        }
                    }
                }
            }
        }
        
        this.log('✅ [identifyCalls] 完成', { total: this.results.calls.length });
    }

    identifyComponents() {
        this.log('🏗️  [identifyComponents] 开始');
        const seen = new Set();
        const maxComponents = Math.min(5000, this.results.classes.length * 5);
        
        const componentClasses = this.results.classes.filter(c => 
            c.name.toLowerCase().includes('component') || 
            c.name.toLowerCase().includes('widget') ||
            c.name.toLowerCase().includes('view')
        );
        this.log('🏗️  [identifyComponents] 找到组件类', { count: componentClasses.length });
        
        const fileToClasses = new Map();
        for (let i = 0; i < this.results.classes.length; i++) {
            const cls = this.results.classes[i];
            if (!fileToClasses.has(cls.fileId)) {
                fileToClasses.set(cls.fileId, []);
            }
            fileToClasses.get(cls.fileId).push(cls);
        }
        
        const fileIds = Array.from(fileToClasses.keys());
        this.log('🏗️  [identifyComponents] 按文件分析', { filesWithClasses: fileIds.length });
        
        for (let fileIdx = 0; fileIdx < fileIds.length && this.results.components.length < maxComponents; fileIdx++) {
            const fileId = fileIds[fileIdx];
            const classes = fileToClasses.get(fileId);
            
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
        
        this.log('🏗️  [identifyComponents] 添加组件类间关系', { components: this.results.components.length });
        
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
        
        this.log('✅ [identifyComponents] 完成', { total: this.results.components.length });
    }

    exportToJSON(outputPath) {
        this.log('💾 [exportToJSON] 保存结果', { outputPath });
        const dataToExport = {
            metadata: {
                generatedAt: new Date().toISOString(),
                projectPath: this.projectPath
            },
            results: this.results,
            stats: {
                files: this.results.files.length,
                classes: this.results.classes.length,
                methods: this.results.methods.length,
                calls: this.results.calls.length,
                components: this.results.components.length,
                warnings: this.warnings.length,
                errors: this.errors.length
            },
            warnings: this.warnings,
            errors: this.errors,
            logs: this.logs
        };
        fs.writeFileSync(outputPath, JSON.stringify(dataToExport, null, 2));
        this.log('✅ [exportToJSON] 保存成功', { outputPath, bytes: fs.statSync(outputPath).size });
    }
}

if (require.main === module) {
    const projectPath = process.argv[2] || '/workspace/sample_project';
    const outputPath = process.argv[3] || '/workspace/debug_analysis.json';
    
    console.log('='.repeat(80));
    console.log('🎯 ULTIMATE DEBUG ANALYZER - 终极深度测试版本');
    console.log('='.repeat(80));
    console.log(`📂 Project: ${projectPath}`);
    console.log(`📄 Output: ${outputPath}`);
    console.log('='.repeat(80));
    
    const analyzer = new UltimateDebugAnalyzer(projectPath, true);
    analyzer.analyzeProject();
    analyzer.exportToJSON(outputPath);
    
    console.log('\n' + '='.repeat(80));
    console.log('📊 SUMMARY');
    console.log('='.repeat(80));
    console.log(`✅ Files: ${analyzer.results.files.length}`);
    console.log(`✅ Classes: ${analyzer.results.classes.length}`);
    console.log(`✅ Methods: ${analyzer.results.methods.length}`);
    console.log(`✅ Calls: ${analyzer.results.calls.length}`);
    console.log(`✅ Components: ${analyzer.results.components.length}`);
    console.log(`⚠️  Warnings: ${analyzer.warnings.length}`);
    console.log(`❌ Errors: ${analyzer.errors.length}`);
    console.log(`📜 Total Logs: ${analyzer.logs.length}`);
    
    if (analyzer.warnings.length > 0) {
        console.log('\n⚠️  Detailed Warnings:');
        analyzer.warnings.slice(0, 10).forEach((w, idx) => {
            console.log(`  [${idx+1}] ${w.message}`);
        });
        if (analyzer.warnings.length > 10) {
            console.log(`  ... and ${analyzer.warnings.length - 10} more`);
        }
    }
    
    if (analyzer.errors.length > 0) {
        console.log('\n❌ Detailed Errors:');
        analyzer.errors.slice(0, 10).forEach((e, idx) => {
            console.log(`  [${idx+1}] ${e.message}`);
        });
        if (analyzer.errors.length > 10) {
            console.log(`  ... and ${analyzer.errors.length - 10} more`);
        }
    }
    
    console.log('\n' + '='.repeat(80));
    console.log('✅ DONE');
    console.log('='.repeat(80));
}

module.exports = UltimateDebugAnalyzer;
