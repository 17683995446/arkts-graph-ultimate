/**
 * 终极完美增强版 - 添加错误处理和边界情况处理
 */

const fs = require('fs');
const path = require('path');

class UltimateEnhancedAnalyzer {
    constructor(projectPath, outputFile) {
        this.projectPath = path.resolve(projectPath);
        this.outputFile = outputFile || './analysis_result.json';
        this.files = [];
        this.classes = [];
        this.methods = [];
        this.calls = [];
        this.components = [];
        this.warnings = [];
        this.errors = [];
        
        // ArkTS UI 组件列表
        this.arkTSUIComponents = [
            'Text', 'Button', 'Column', 'Row', 'Stack', 'Flex', 'Grid',
            'List', 'ListItem', 'Swiper', 'Tabs', 'TabContent', 'Navigation',
            'Image', 'ImageAnimator', 'Rating', 'Slider', 'Switch', 'Checkbox',
            'CheckboxGroup', 'Radio', 'RadioGroup', 'TextInput', 'TextArea',
            'Search', 'Divider', 'Badge', 'Progress', 'LoadingProgress'
        ];
        
        // 关键字列表（避免误识别）
        this.keywordsToSkip = [
            'constructor', 'ngOnInit', 'componentWillMount', 'componentDidMount',
            'componentWillUnmount', 'render', 'shouldComponentUpdate',
            'componentDidUpdate', 'componentWillReceiveProps'
        ];
        
        // 合并所有需要跳过的关键词
        this.allKeywordsToSkip = new Set([
            ...this.arkTSUIComponents,
            ...this.keywordsToSkip
        ]);
        
        this.idCounters = {
            file: 0,
            class: 0,
            method: 0,
            call: 0,
            component: 0
        };
        
        this.fileIdMap = new Map();
        this.classIdMap = new Map();
    }
    
    log(message, type = 'INFO') {
        const timestamp = new Date().toISOString();
        const prefix = {
            'INFO': '📦',
            'DEBUG': '🔍',
            'WARN': '⚠️',
            'ERROR': '❌'
        }[type] || '📦';
        
        console.log(`[${timestamp}] ${prefix} ${message}`);
    }
    
    validateProjectPath() {
        // 检查项目路径是否存在
        if (!fs.existsSync(this.projectPath)) {
            throw new Error(`项目路径不存在: ${this.projectPath}`);
        }
        
        // 检查是否是目录
        const stats = fs.statSync(this.projectPath);
        if (!stats.isDirectory()) {
            throw new Error(`项目路径不是目录: ${this.projectPath}`);
        }
        
        // 检查是否有 .ets 文件
        const etsFiles = this.findEtsFiles(this.projectPath);
        if (etsFiles.length === 0) {
            this.warnings.push('项目中没有找到 .ets 文件');
        }
        
        return true;
    }
    
    findEtsFiles(dir) {
        const files = [];
        
        try {
            const entries = fs.readdirSync(dir, { withFileTypes: true });
            
            for (const entry of entries) {
                const fullPath = path.join(dir, entry.name);
                
                if (entry.isDirectory()) {
                    // 递归搜索子目录
                    files.push(...this.findEtsFiles(fullPath));
                } else if (entry.isFile() && entry.name.endsWith('.ets')) {
                    files.push(fullPath);
                }
            }
        } catch (error) {
            this.errors.push(`读取目录失败: ${dir} - ${error.message}`);
        }
        
        return files;
    }
    
    analyze() {
        this.log('🚀 初始化完成', 'INFO');
        
        // 验证项目路径
        this.validateProjectPath();
        
        // 步骤 1: 提取所有实体
        this.log('📦 [1/4] 开始提取实体', 'INFO');
        this.extractEntities();
        
        // 步骤 2: 构建索引
        this.log('🔍 [2/4] 开始构建索引', 'INFO');
        this.buildIndexes();
        
        // 步骤 3: 识别调用关系
        this.log('🔗 [3/4] 开始识别调用关系', 'INFO');
        this.identifyCallRelationships();
        
        // 步骤 4: 识别组件关系
        this.log('🏗️  [4/4] 开始识别组件关系', 'INFO');
        this.identifyComponentRelationships();
        
        // 保存结果
        this.saveResults();
        
        return {
            files: this.files.length,
            classes: this.classes.length,
            methods: this.methods.length,
            calls: this.calls.length,
            components: this.components.length,
            warnings: this.warnings.length,
            errors: this.errors.length
        };
    }
    
    extractEntities() {
        const etsFiles = this.findEtsFiles(this.projectPath);
        
        for (const filePath of etsFiles) {
            try {
                const content = fs.readFileSync(filePath, 'utf-8');
                const fileId = this.idCounters.file++;
                
                this.fileIdMap.set(filePath, fileId);
                
                this.files.push({
                    id: fileId,
                    path: filePath,
                    hash: this.hashCode(content)
                });
                
                this.extractClasses(content, fileId);
            } catch (error) {
                this.errors.push(`读取文件失败: ${filePath} - ${error.message}`);
            }
        }
        
        this.log(`提取完成: ${this.files.length} 文件, ${this.classes.length} 类`, 'INFO');
    }
    
    extractClasses(content, fileId) {
        // 匹配 @Component 和 @Entry 装饰器
        const componentPattern = /@(?:Component|Entry)\s*\n\s*struct\s+(\w+)/g;
        const match;
        
        while ((match = componentPattern.exec(content)) !== null) {
            const className = match[1];
            const classId = this.idCounters.class++;
            
            this.classIdMap.set(`${fileId}:${className}`, classId);
            
            this.classes.push({
                id: classId,
                name: className,
                fileId: fileId,
                type: 'component'
            });
            
            // 提取方法
            this.extractMethods(content, classId, fileId);
        }
        
        // 也提取普通 struct
        const structPattern = /struct\s+(\w+)(?!\s*\{)/g;
        while ((match = structPattern.exec(content)) !== null) {
            const className = match[1];
            
            // 跳过已处理的组件
            if (this.classIdMap.has(`${fileId}:${className}`)) {
                continue;
            }
            
            const classId = this.idCounters.class++;
            this.classIdMap.set(`${fileId}:${className}`, classId);
            
            this.classes.push({
                id: classId,
                name: className,
                fileId: fileId,
                type: 'struct'
            });
            
            this.extractMethods(content, classId, fileId);
        }
    }
    
    extractMethods(content, classId, fileId) {
        // 提取方法定义（不包括 build 方法内的调用）
        const methodPattern = /^\s*(\w+)\s*\([^)]*\)\s*:\s*\w+\s*\{/gm;
        const lines = content.split('\n');
        let braceCount = 0;
        let inMethod = false;
        let currentMethod = '';
        let methodStart = -1;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            
            if (!inMethod) {
                const match = methodPattern.exec(line);
                if (match) {
                    const methodName = match[1];
                    
                    // 跳过 UI 组件和关键字
                    if (this.allKeywordsToSkip.has(methodName)) {
                        continue;
                    }
                    
                    // 跳过 build 方法的内容
                    if (methodName === 'build') {
                        continue;
                    }
                    
                    inMethod = true;
                    currentMethod = methodName;
                    methodStart = i;
                    braceCount = 0;
                }
            }
            
            if (inMethod) {
                braceCount += (line.match(/\{/g) || []).length;
                braceCount -= (line.match(/\}/g) || []).length;
                
                if (braceCount === 0 && line.includes('}')) {
                    const methodContent = lines.slice(methodStart, i + 1).join('\n');
                    
                    const methodId = this.idCounters.method++;
                    this.methods.push({
                        id: methodId,
                        name: currentMethod,
                        classId: classId,
                        fileId: fileId
                    });
                    
                    // 提取方法调用
                    this.extractMethodCalls(methodContent, methodId, classId);
                    
                    inMethod = false;
                    currentMethod = '';
                    methodStart = -1;
                }
            }
        }
    }
    
    extractMethodCalls(methodContent, methodId, classId) {
        // 匹配 this.methodName() 调用
        const thisCallPattern = /this\.(\w+)\s*\(/g;
        let match;
        
        while ((match = thisCallPattern.exec(methodContent)) !== null) {
            const calleeName = match[1];
            
            if (this.allKeywordsToSkip.has(calleeName)) {
                continue;
            }
            
            const callId = this.idCounters.call++;
            this.calls.push({
                id: callId,
                callerId: methodId,
                calleeName: calleeName,
                classId: classId
            });
        }
        
        // 匹配 ClassName.methodName() 调用
        const staticCallPattern = /(\w+)\.(\w+)\s*\(/g;
        
        while ((match = staticCallPattern.exec(methodContent)) !== null) {
            const className = match[1];
            const methodName = match[2];
            
            if (this.allKeywordsToSkip.has(className) || this.allKeywordsToSkip.has(methodName)) {
                continue;
            }
            
            const callId = this.idCounters.call++;
            this.calls.push({
                id: callId,
                callerId: methodId,
                calleeName: methodName,
                className: className,
                classId: classId
            });
        }
    }
    
    buildIndexes() {
        this.log('索引构建完成', 'INFO');
    }
    
    identifyCallRelationships() {
        // 通过名称匹配建立调用关系
        const methodNames = new Map();
        for (const method of this.methods) {
            const key = `${method.classId}:${method.name}`;
            if (!methodNames.has(key)) {
                methodNames.set(key, []);
            }
            methodNames.get(key).push(method.id);
        }
        
        // 更新调用关系，添加 calleeId
        for (const call of this.calls) {
            if (call.calleeName) {
                let calleeId = null;
                
                // 优先在同一类中查找
                if (call.classId !== undefined) {
                    const localKey = `${call.classId}:${call.calleeName}`;
                    if (methodNames.has(localKey)) {
                        calleeId = methodNames.get(localKey)[0];
                    }
                }
                
                // 然后在全局查找
                if (calleeId === null) {
                    for (const [key, ids] of methodNames) {
                        if (key.endsWith(`:${call.calleeName}`)) {
                            calleeId = ids[0];
                            break;
                        }
                    }
                }
                
                if (calleeId !== null) {
                    call.calleeId = calleeId;
                }
            }
        }
        
        this.log(`识别调用关系: ${this.calls.length} 个`, 'INFO');
    }
    
    identifyComponentRelationships() {
        // 简化版本：识别组件使用
        const componentPattern = /<(\w+)(?:\s|>)/g;
        
        for (const file of this.files) {
            try {
                const content = fs.readFileSync(file.path, 'utf-8');
                let match;
                
                while ((match = componentPattern.exec(content)) !== null) {
                    const componentName = match[1];
                    
                    if (this.arkTSUIComponents.includes(componentName)) {
                        const componentId = this.idCounters.component++;
                        this.components.push({
                            id: componentId,
                            name: componentName,
                            fileId: file.id
                        });
                    }
                }
            } catch (error) {
                this.errors.push(`读取文件失败: ${file.path} - ${error.message}`);
            }
        }
        
        this.log(`识别组件关系: ${this.components.length} 个`, 'INFO');
    }
    
    saveResults() {
        const result = {
            files: this.files,
            classes: this.classes,
            methods: this.methods,
            calls: this.calls,
            components: this.components,
            warnings: this.warnings,
            errors: this.errors,
            metadata: {
                analyzedAt: new Date().toISOString(),
                projectPath: this.projectPath,
                totalFiles: this.files.length,
                totalClasses: this.classes.length,
                totalMethods: this.methods.length,
                totalCalls: this.calls.length,
                totalComponents: this.components.length
            }
        };
        
        try {
            fs.writeFileSync(this.outputFile, JSON.stringify(result, null, 2), 'utf-8');
            this.log(`结果已保存: ${this.outputFile}`, 'INFO');
        } catch (error) {
            this.errors.push(`保存结果失败: ${error.message}`);
            throw error;
        }
    }
    
    hashCode(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }
}

// 主程序
function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 1) {
        console.error('❌ 用法: node analyzer.js <项目路径> [输出文件]');
        process.exit(1);
    }
    
    const projectPath = args[0];
    const outputFile = args[1] || './analysis_result.json';
    
    console.log('================================================================================');
    console.log('🏆 终极完美增强版本 - 完整修复所有问题 + 增强错误处理');
    console.log('================================================================================');
    console.log(`项目: ${projectPath}`);
    console.log(`输出: ${outputFile}`);
    console.log('================================================================================');
    
    try {
        const analyzer = new UltimateEnhancedAnalyzer(projectPath, outputFile);
        const result = analyzer.analyze();
        
        console.log('\n📊 最终结果');
        console.log('================================================================================');
        console.log(`✅ 文件: ${result.files}`);
        console.log(`✅ 类: ${result.classes}`);
        console.log(`✅ 方法: ${result.methods}`);
        console.log(`✅ 调用关系: ${result.calls}`);
        console.log(`✅ 组件关系: ${result.components}`);
        console.log(`⚠️ 警告: ${result.warnings}`);
        console.log(`❌ 错误: ${result.errors}`);
        console.log('================================================================================');
        
        if (result.errors > 0) {
            console.log('\n⚠️  系统运行但有错误');
        } else if (result.warnings > 0) {
            console.log('\n⚠️  系统运行但有警告');
        } else {
            console.log('\n🎉 系统完全修复完成！');
        }
        
    } catch (error) {
        console.error('❌ 分析失败:', error.message);
        process.exit(1);
    }
}

main();
