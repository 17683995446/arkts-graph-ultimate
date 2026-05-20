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
        
        const calls = this.extractCalls(content, methods);
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
        const methodPattern = /(?:public\s+|private\s+|protected\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+\s*)?\{/g;
        let match;
        let currentClassIndex = 0;

        while ((match = methodPattern.exec(content)) !== null) {
            const methodName = match[1];
            
            for (let i = 0; i < classes.length; i++) {
                const classEnd = classes[i + 1] ? 
                    content.indexOf('class ' + classes[i + 1].name) : 
                    content.length;
                const classStart = content.indexOf('class ' + classes[i].name);
                
                if (match.index >= classStart && match.index < classEnd) {
                    currentClassIndex = i;
                    break;
                }
            }

            if (!['if', 'for', 'while', 'switch', 'class', 'struct'].includes(methodName)) {
                methods.push({
                    id: this.results.methods.length,
                    name: `${classes[currentClassIndex]?.name || 'Global'}::${methodName}`,
                    classId: classes[currentClassIndex]?.id || null
                });
            }
        }

        return methods;
    }

    extractCalls(content, methods) {
        const calls = [];
        const seen = new Set();
        
        // 方法位置映射
        const methodPositions = methods.map(m => {
            const methodName = m.name.split('::')[1];
            const pattern = new RegExp(`${methodName}\\s*\\([^)]*\\)\\s*(?::\\s*\\w+\\s*)?\\{`);
            const match = pattern.exec(content);
            return {
                method: m,
                start: match ? content.indexOf(match[0]) : -1,
                end: match ? content.indexOf('{', content.indexOf(match[0])) : -1
            };
        }).filter(p => p.start >= 0);

        // 查找 this.method() 和直接 method() 调用
        const thisCallPattern = /this\.(\w+)\s*\(/g;
        const directCallPattern = /(?<![a-zA-Z0-9_.])(\w+)\s*\(/g;
        
        let match;
        
        // 处理 this.method() 调用
        while ((match = thisCallPattern.exec(content)) !== null) {
            const calledName = match[1];
            
            // 跳过关键字和内置方法
            if (['if', 'for', 'while', 'switch', 'console', 'Math', 'String', 'Array', 'Object'].includes(calledName)) {
                continue;
            }
            
            // 找到调用者方法（在调用点之前的方法）
            const callerMethod = methodPositions
                .filter(p => p.start < match.index && p.end > match.index)
                .sort((a, b) => b.start - a.start)[0]?.method;

            // 找到被调用方法
            const calleeMethod = methods.find(m => 
                m.name.endsWith(`::${calledName}`) || m.name === calledName
            );

            if (callerMethod && calleeMethod && callerMethod.id !== calleeMethod.id) {
                const key = `${callerMethod.id}-${calleeMethod.id}`;
                if (!seen.has(key)) {
                    seen.add(key);
                    calls.push({
                        callerId: callerMethod.id,
                        calleeId: calleeMethod.id
                    });
                }
            }
        }
        
        // 处理直接方法调用（不带 this）
        while ((match = directCallPattern.exec(content)) !== null) {
            const calledName = match[1];
            
            // 跳过关键字和内置方法
            if (['if', 'for', 'while', 'switch', 'console', 'Math', 'String', 'Array', 'Object', 'async', 'await', 'new', 'return', 'throw', 'typeof', 'void'].includes(calledName)) {
                continue;
            }
            
            // 跳过 this 关键字
            if (content[match.index - 1] === '.') {
                continue;
            }
            
            // 找到调用者方法
            const callerMethod = methodPositions
                .filter(p => p.start < match.index && p.end > match.index)
                .sort((a, b) => b.start - a.start)[0]?.method;

            // 找到被调用方法
            const calleeMethod = methods.find(m => 
                m.name.endsWith(`::${calledName}`) || m.name === calledName
            );

            if (callerMethod && calleeMethod && callerMethod.id !== calleeMethod.id) {
                const key = `${callerMethod.id}-${calleeMethod.id}`;
                if (!seen.has(key)) {
                    seen.add(key);
                    calls.push({
                        callerId: callerMethod.id,
                        calleeId: calleeMethod.id
                    });
                }
            }
        }

        return calls;
    }

    extractComponents(content, classes) {
        const components = [];
        const seen = new Set();
        
        // ArkUI 内置组件列表
        const arkUIComponents = [
            'Column', 'Row', 'Stack', 'Flex', 'Grid', 'List', 'ListItem',
            'Text', 'Button', 'Image', 'Input', 'TextInput', 'Search',
            'Slider', 'Switch', 'Checkbox', 'Radio', 'Progress', 'LoadingProgress',
            'Divider', 'Blank', 'Badge', 'QRCode', 'Barcode',
            'Counter', 'DatePicker', 'TimePicker', 'Picker', 'TextPicker',
            'Web', 'Video', 'Audio', 'Camera'
        ];
        
        // 查找 JSX 风格的组件使用
        const jsxPattern = /<(\w+)[^>]*>[\s\S]*?<\/(\w+)>|<(\w+)[^>]*\/>/g;
        let match;
        
        while ((match = jsxPattern.exec(content)) !== null) {
            const openTag = match[1] || match[3];
            const closeTag = match[2];
            
            // 检查是否是自定义组件
            const customComponent = classes.find(c => 
                c.name === openTag && c.type === 'struct'
            );
            
            if (customComponent) {
                // 查找父组件
                let parentId = 0;
                const parentClass = classes.find(c => c.id !== customComponent.id);
                if (parentClass) {
                    parentId = parentClass.id;
                }
                
                const key = `${parentId}-${customComponent.id}`;
                if (!seen.has(key)) {
                    seen.add(key);
                    components.push({
                        parentId: parentId,
                        childId: customComponent.id
                    });
                }
            } else if (arkUIComponents.includes(openTag)) {
                // ArkUI 内置组件也记录
                console.log(`Found ArkUI component: ${openTag}`);
            }
        }
        
        return components;
    }

    analyzeProject() {
        const analyzeDir = (dir) => {
            const files = fs.readdirSync(dir);
            
            for (const file of files) {
                const filePath = path.join(dir, file);
                const stat = fs.statSync(filePath);

                if (stat.isDirectory()) {
                    if (!['node_modules', '.git', 'build', 'dist'].includes(file)) {
                        analyzeDir(filePath);
                    }
                } else if (file.endsWith('.ets') || file.endsWith('.ts') || file.endsWith('.tsx')) {
                    try {
                        this.analyzeFile(filePath);
                    } catch (error) {
                        console.error(`Error analyzing ${filePath}:`, error.message);
                    }
                }
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
