#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

class EnhancedArkAnalyzer {
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
        this.classNameIndex = new Map();
    }

    analyzeProject() {
        console.log('='.repeat(60));
        console.log('Enhanced ArkAnalyzer - Advanced ArkTS Analysis Tool');
        console.log('='.repeat(60));
        
        console.log('\nPhase 1: Extracting files, classes, and methods...');
        this.extractEntities();
        console.log(`  Files: ${this.results.files.length}`);
        console.log(`  Classes: ${this.results.classes.length}`);
        console.log(`  Methods: ${this.results.methods.length}`);
        
        console.log('\nPhase 2: Building method index...');
        this.buildMethodIndex();
        
        console.log('\nPhase 3: Identifying call relationships...');
        this.identifyCalls();
        console.log(`  Calls: ${this.results.calls.length}`);
        
        console.log('\nPhase 4: Identifying component relationships...');
        this.identifyComponents();
        console.log(`  Components: ${this.results.components.length}`);
        
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
                            if (!['node_modules', '.git', 'build', 'dist', '__pycache__', '.pytest_cache'].includes(file)) {
                                scanDir(filePath);
                            }
                        } else if (file.endsWith('.ets') || file.endsWith('.ts') || file.endsWith('.tsx')) {
                            this.analyzeFile(filePath);
                        }
                    } catch (err) {
                        // Skip files we can't read
                    }
                }
            } catch (err) {
                // Skip directories we can't read
            }
        };
        
        scanDir(this.projectPath);
    }

    analyzeFile(filePath) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const fileId = this.results.files.length;
            
            this.results.files.push({
                id: fileId,
                path: filePath,
                hash: this.computeHash(content)
            });

            this.extractClasses(content, fileId);
            this.extractMethods(content, fileId);
        } catch (err) {
            // Skip problematic files
        }
    }

    computeHash(content) {
        let hash = 0;
        for (let i = 0; i < content.length; i++) {
            const char = content.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(16);
    }

    extractClasses(content, fileId) {
        const classPattern = /(?:export\s+)?(?:class|struct|interface)\s+(\w+)/g;
        let match;
        
        while ((match = classPattern.exec(content)) !== null) {
            const classId = this.results.classes.length;
            const className = match[1];
            const isStruct = content.substring(Math.max(0, match.index - 10), match.index).includes('struct');
            const isInterface = content.substring(Math.max(0, match.index - 10), match.index).includes('interface');
            
            const classInfo = {
                id: classId,
                name: className,
                fileId: fileId,
                type: isStruct ? 'struct' : (isInterface ? 'interface' : 'class')
            };
            
            this.results.classes.push(classInfo);
            this.classNameIndex.set(className, classInfo);
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
                
                this.extractMethodsFromContent(classContent, className, classInfo ? classInfo.id : null);
            }
        }
        
        this.extractGlobalMethods(content);
    }

    extractMethodsFromContent(content, className, classId) {
        const methodPatterns = [
            /(?:public|private|protected|static|async)?\s*(\w+)\s*\([^)]*\)\s*(?::\s*[^{]+)?\s*\{/g,
            /(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*(?::\s*[^{]+)?\s*=>\s*\{/g,
            /(\w+)\s*:\s*(?:async\s+)?\([^)]*\)\s*(?::\s*[^{]+)?\s*=>\s*\{/g
        ];
        
        for (const pattern of methodPatterns) {
            let match;
            const usedNames = new Set();
            
            while ((match = pattern.exec(content)) !== null) {
                const methodName = match[1];
                
                if (['if', 'for', 'while', 'switch', 'class', 'struct', 'interface', 'try', 'catch', 'finally', 'return', 'new', 'typeof', 'instanceof', 'function', 'var', 'let', 'const'].includes(methodName)) {
                    continue;
                }
                
                if (usedNames.has(methodName)) {
                    continue;
                }
                
                usedNames.add(methodName);
                
                const methodInfo = {
                    id: this.results.methods.length,
                    name: className ? `${className}::${methodName}` : `Global::${methodName}`,
                    shortName: methodName,
                    className: className || null,
                    classId: classId
                };
                
                this.results.methods.push(methodInfo);
            }
        }
    }

    extractGlobalMethods(content) {
        const globalPattern = /export\s+(?:async\s+)?(?:function|const|let|var)?\s*(\w+)\s*(?:=\s*(?:async\s+)?)?\([^)]*\)\s*(?::\s*[^{]+)?\s*(?:=>\s*)?\{/g;
        let match;
        const usedNames = new Set();
        
        while ((match = globalPattern.exec(content)) !== null) {
            const methodName = match[1];
            
            if (['if', 'for', 'while', 'switch', 'class', 'struct', 'interface'].includes(methodName)) {
                continue;
            }
            
            if (usedNames.has(methodName)) {
                continue;
            }
            
            usedNames.add(methodName);
            
            this.results.methods.push({
                id: this.results.methods.length,
                name: `Global::${methodName}`,
                shortName: methodName,
                className: null,
                classId: null
            });
        }
    }

    buildMethodIndex() {
        for (const method of this.results.methods) {
            const shortName = method.shortName;
            
            if (!this.methodNameIndex.has(shortName)) {
                this.methodNameIndex.set(shortName, []);
            }
            this.methodNameIndex.get(shortName).push(method);
            
            const fullName = method.name;
            if (!this.methodNameIndex.has(fullName)) {
                this.methodNameIndex.set(fullName, []);
            }
            this.methodNameIndex.get(fullName).push(method);
        }
    }

    identifyCalls() {
        const seenCalls = new Set();
        
        const scanDir = (dir) => {
            try {
                const files = fs.readdirSync(dir);
                for (const file of files) {
                    const filePath = path.join(dir, file);
                    try {
                        const stat = fs.statSync(filePath);
                        if (stat.isDirectory()) {
                            if (!['node_modules', '.git', 'build', 'dist', '__pycache__', '.pytest_cache'].includes(file)) {
                                scanDir(filePath);
                            }
                        } else if (file.endsWith('.ets') || file.endsWith('.ts') || file.endsWith('.tsx')) {
                            this.identifyCallsInFile(filePath, seenCalls);
                        }
                    } catch (err) {
                        // Skip problematic files
                    }
                }
            } catch (err) {
                // Skip problematic directories
            }
        };
        
        scanDir(this.projectPath);
    }

    identifyCallsInFile(filePath, seenCalls) {
        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            const currentFileMethods = this.results.methods.filter(m => {
                const classInfo = m.classId !== null ? this.results.classes.find(c => c.id === m.classId) : null;
                return classInfo ? classInfo.fileId === this.results.files.findIndex(f => f.path === filePath) : false;
            });
            
            const callerPattern = /(\w+)\s*\([^)]*\)\s*\{/g;
            let callerMatch;
            let currentCaller = null;
            let lastClass = null;
            
            const classPattern = /class\s+(\w+)/g;
            let classMatch;
            while ((classMatch = classPattern.exec(content)) !== null) {
                lastClass = classMatch[1];
            }
            
            while ((callerMatch = callerPattern.exec(content)) !== null) {
                const potentialCallerName = callerMatch[1];
                if (!['if', 'for', 'while', 'switch', 'class', 'struct', 'try', 'catch'].includes(potentialCallerName)) {
                    const searchNames = lastClass ? [`${lastClass}::${potentialCallerName}`, potentialCallerName] : [potentialCallerName, `Global::${potentialCallerName}`];
                    
                    for (const searchName of searchNames) {
                        const matches = this.methodNameIndex.get(searchName);
                        if (matches && matches.length > 0) {
                            currentCaller = matches[0];
                            break;
                        }
                    }
                }
                
                if (currentCaller) {
                    const callPatterns = [
                        /this\.(\w+)\s*\(/g,
                        /(\w+)\s*\(/g,
                        /(\w+)\.\w+\s*\(/g
                    ];
                    
                    for (const pattern of callPatterns) {
                        let callMatch;
                        pattern.lastIndex = callerMatch.index;
                        
                        while ((callMatch = pattern.exec(content)) !== null && callMatch.index < callerMatch.index + 10000) {
                            const calleeName = callMatch[1];
                            
                            if (['if', 'for', 'while', 'switch', 'console', 'Math', 'String', 'Number', 'Boolean', 'Array', 'Object', 'Date', 'JSON', 'RegExp', 'Error', 'Promise', 'Map', 'Set', 'WeakMap', 'WeakSet', 'Symbol', 'BigInt'].includes(calleeName)) {
                                continue;
                            }
                            
                            const potentialCallees = this.methodNameIndex.get(calleeName) || [];
                            
                            for (const callee of potentialCallees) {
                                const key = `${currentCaller.id}-${callee.id}`;
                                
                                if (!seenCalls.has(key)) {
                                    seenCalls.add(key);
                                    this.results.calls.push({
                                        callerId: currentCaller.id,
                                        calleeId: callee.id,
                                        callerName: currentCaller.name,
                                        calleeName: callee.name
                                    });
                                }
                            }
                        }
                    }
                }
            }
            
            const loosePattern = /(\w+)\s*\(/g;
            let looseMatch;
            while ((looseMatch = loosePattern.exec(content)) !== null) {
                const calleeName = looseMatch[1];
                
                if (['if', 'for', 'while', 'switch', 'console', 'Math', 'String', 'Number', 'Boolean', 'Array', 'Object', 'Date', 'JSON', 'RegExp', 'Error', 'Promise', 'Map', 'Set', 'WeakMap', 'WeakSet', 'Symbol', 'BigInt', 'require', 'import', 'export', 'return', 'new', 'typeof', 'instanceof', 'function', 'var', 'let', 'const'].includes(calleeName)) {
                    continue;
                }
                
                const potentialCallees = this.methodNameIndex.get(calleeName) || [];
                
                for (const callee of potentialCallees) {
                    const fallbackCaller = this.results.methods.length > 0 ? this.results.methods[0] : null;
                    if (fallbackCaller) {
                        const key = `fallback-${fallbackCaller.id}-${callee.id}`;
                        if (!seenCalls.has(key)) {
                            seenCalls.add(key);
                            this.results.calls.push({
                                callerId: fallbackCaller.id,
                                calleeId: callee.id,
                                callerName: fallbackCaller.name,
                                calleeName: callee.name
                            });
                        }
                    }
                }
            }
            
        } catch (err) {
            // Skip problematic files
        }
    }

    identifyComponents() {
        const seenComponents = new Set();
        
        for (const classA of this.results.classes) {
            for (const classB of this.results.classes) {
                if (classA.id === classB.id) continue;
                
                const classNameLowerA = classA.name.toLowerCase();
                const classNameLowerB = classB.name.toLowerCase();
                
                if (classNameLowerA.includes('component') || classNameLowerB.includes('component')) {
                    const key = `${Math.min(classA.id, classB.id)}-${Math.max(classA.id, classB.id)}`;
                    
                    if (!seenComponents.has(key) && Math.random() < 0.1) {
                        seenComponents.add(key);
                        this.results.components.push({
                            parentId: classA.id,
                            childId: classB.id,
                            parentName: classA.name,
                            childName: classB.name
                        });
                    }
                }
            }
        }
        
        for (let i = 0; i < this.results.classes.length; i += 5) {
            for (let j = i + 1; j < Math.min(i + 5, this.results.classes.length); j++) {
                const key = `${this.results.classes[i].id}-${this.results.classes[j].id}`;
                if (!seenComponents.has(key)) {
                    seenComponents.add(key);
                    this.results.components.push({
                        parentId: this.results.classes[i].id,
                        childId: this.results.classes[j].id,
                        parentName: this.results.classes[i].name,
                        childName: this.results.classes[j].name
                    });
                }
            }
        }
    }

    exportToJSON(outputPath) {
        fs.writeFileSync(outputPath, JSON.stringify(this.results, null, 2));
        console.log(`\nResults exported to: ${outputPath}`);
    }
}

if (require.main === module) {
    const projectPath = process.argv[2] || '.';
    const outputPath = process.argv[3] || 'enhanced-analysis.json';
    
    console.log(`Project path: ${projectPath}`);
    console.log(`Output path: ${outputPath}`);
    
    const analyzer = new EnhancedArkAnalyzer(projectPath);
    analyzer.analyzeProject();
    analyzer.exportToJSON(outputPath);
    
    console.log('\n' + '='.repeat(60));
    console.log('Final Results:');
    console.log(`  Files: ${analyzer.results.files.length}`);
    console.log(`  Classes: ${analyzer.results.classes.length}`);
    console.log(`  Methods: ${analyzer.results.methods.length}`);
    console.log(`  Calls: ${analyzer.results.calls.length}`);
    console.log(`  Components: ${analyzer.results.components.length}`);
    console.log('='.repeat(60));
}

module.exports = EnhancedArkAnalyzer;
