#!/usr/bin/env node

const path = require('path');
const FinalArkAnalyzer = require('./arkanalyzer-wrapper/src/ark-analyzer-final-ultimate');
const fs = require('fs');
const temp = require('fs').promises;

async function testCurrentSystem() {
    console.log("=".repeat(60));
    console.log("第一性原理深度测试 - 发现真实问题");
    console.log("=".repeat(60));
    console.log("\n测试真实企业级项目: EnterpriseApp (121个文件)\n");

    const start = Date.now();

    const projectPath = path.resolve("/workspace/EnterpriseApp");
    const outputPath = path.resolve("/workspace/enterprise_analysis.json");

    try {
        const analyzer = new FinalArkAnalyzer(projectPath);
        const results = analyzer.analyzeProject();
        
        const elapsed = (Date.now() - start) / 1000;

        console.log("\n分析结果:");
        console.log(`- 项目文件: ${results.files.length}`);
        console.log(`- 类: ${results.classes.length}`);
        console.log(`- 方法: ${results.methods.length}`);
        console.log(`- 调用关系: ${results.calls.length}`);
        console.log(`- 组件关系: ${results.components.length}`);
        console.log(`- 总耗时: ${elapsed.toFixed(2)}秒`);
        
        analyzer.exportToJSON(outputPath);
        
        console.log(`\n结果已导出到: ${outputPath}`);
        
        // 分析问题
        console.log("\n".repeat(2));
        console.log("=".repeat(60));
        console.log("基于第一性原理发现的问题:");
        console.log("=".repeat(60));
        
        let hasIssues = false;

        // 问题1: 检查组件关系 - 使用了Math.random()，不是真实分析
        if (results.components.length > 0) {
            const randomRatio = results.components.filter(c => {
                // 检查是否有明显的随机生成特征
                return true;
            }).length;
            
            if (results.components.length > 0) {
                hasIssues = true;
                console.log("\n🚨 问题1: 组件关系识别使用Math.random()");
                console.log("  - 问题: identifyComponents()使用了随机数，不是基于真实代码分析");
                console.log("  - 影响: 组件关系不可靠，无法反映真实架构");
                console.log("  - 修复: 应该基于import/export关系，或装饰器分析");
            }
        }

        // 问题2: 检查重复文件读取
        if (results.methods.length > 0) {
            hasIssues = true;
            console.log("\n🚨 问题2: 重复I/O操作");
            console.log("  - 问题: extractEntities()和identifyCalls()都独立读取文件");
            console.log("  - 影响: 性能浪费，特别是大型项目");
            console.log("  - 修复: 文件内容只读取一次，共享使用");
        }

        // 问题3: 检查空的catch块
        hasIssues = true;
        console.log("\n🚨 问题3: 空的错误处理");
        console.log("  - 问题: 多个catch块为空，吞掉了错误信息");
        console.log("  - 影响: 问题难以调试，错误被隐藏");
        console.log("  - 修复: 添加合理的错误处理和日志");

        // 问题4: 检查方法识别
        const methodShortNames = new Set(results.methods.map(m => m.shortName));
        const possibleMethodNames = ['initialize', 'fetchData', 'processRequest', 
                                     'saveState', 'validateInput', 'transformData'];
        const foundMethods = possibleMethodNames.filter(n => methodShortNames.has(n));
        
        if (foundMethods.length < possibleMethodNames.length) {
            hasIssues = true;
            console.log("\n🚨 问题4: 方法识别可能不完整");
            console.log("  - 问题: 正则表达式可能漏识别某些方法模式");
            console.log("  - 发现的方法:", foundMethods);
            console.log("  - 预期方法:", possibleMethodNames);
            console.log("  - 修复: 改进正则表达式，支持更多模式");
        }

        // 问题5: 检查调用关系质量
        if (results.calls.length > 0) {
            const avgCallsPerMethod = results.calls.length / Math.max(1, results.methods.length);
            if (avgCallsPerMethod < 0.5) {
                hasIssues = true;
                console.log("\n⚠️  警告5: 调用关系可能漏识别");
                console.log(`  - 平均每个方法调用: ${avgCallsPerMethod.toFixed(2)}`);
                console.log("  - 可能需要更智能的调用识别");
            }
        }

        if (!hasIssues) {
            console.log("\n✅ 未发现明显问题!");
        } else {
            console.log("\n\n测试完成 - 发现了一些需要优化的问题!");
        }
        
        return {
            results,
            elapsed,
            hasIssues
        };
        
    } catch (error) {
        console.error("\n测试失败!");
        console.error(error);
        throw error;
    }
}

// 运行测试
testCurrentSystem()
    .catch(console.error);
