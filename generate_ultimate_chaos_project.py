#!/usr/bin/env python3
"""
超大规模、超复杂、极端混乱测试项目生成器
用于测试系统在极端复杂场景下的表现
"""

import os
import random
import string
from pathlib import Path

class UltimateChaosProjectGenerator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.file_count = 0
        self.class_count = 0
        self.method_count = 0
        self.call_count = 0
        self.complexity_level = "EXTREME"
        
    def generate_random_name(self, prefix="Test"):
        """生成随机名称"""
        suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 20)))
        return f"{prefix}_{suffix}"
    
    def generate_complex_file(self, file_path, file_index, complexity="EXTREME"):
        """生成超复杂ArkTS文件"""
        self.file_count += 1
        
        # 根据复杂度级别决定内容规模
        if complexity == "EXTREME":
            class_count_in_file = random.randint(20, 50)
            method_count_per_class = random.randint(30, 60)
            call_count_per_method = random.randint(20, 50)
        else:
            class_count_in_file = random.randint(10, 20)
            method_count_per_class = random.randint(15, 30)
            call_count_per_method = random.randint(10, 20)
        
        classes_html = []
        
        for i in range(class_count_in_file):
            self.class_count += 1
            class_name = self.generate_random_name("Class")
            class_html = self.generate_complex_class(
                class_name, 
                file_index, 
                i, 
                method_count_per_class,
                call_count_per_method
            )
            classes_html.append(class_html)
        
        file_content = f"""// @ts-nocheck
// 超复杂测试文件 #{file_index}
// 文件名: {os.path.basename(file_path)}
// 类数量: {class_count_in_file}
// 复杂度级别: {complexity}
// 注释: 本文件包含大量类、方法、调用关系，用于测试系统处理复杂场景的能力

{chr(10).join(classes_html)}
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
    
    def generate_complex_class(self, class_name, file_index, class_index, method_count, call_count):
        """生成超复杂类"""
        methods = []
        
        for i in range(method_count):
            self.method_count += 1
            method_name = self.generate_random_name("method")
            
            # 生成随机数量的调用
            call_htmls = []
            actual_call_count = random.randint(1, call_count)
            
            for j in range(actual_call_count):
                self.call_count += 1
                target_class = self.generate_random_name("Class")
                target_method = self.generate_random_name("method")
                
                # 多种调用方式
                call_type = random.choice(['this', 'static', 'callback', 'async'])
                
                if call_type == 'this':
                    call_htmls.append(f"      // 调用类型: this调用")
                    call_htmls.append(f"      this.{target_method}();")
                elif call_type == 'static':
                    call_htmls.append(f"      // 调用类型: 静态调用")
                    call_htmls.append(f"      {target_class}.{target_method}();")
                elif call_type == 'callback':
                    call_htmls.append(f"      // 调用类型: 回调调用")
                    call_htmls.append(f"      this.processCallback({target_method});")
                else:
                    call_htmls.append(f"      // 调用类型: 异步调用")
                    call_htmls.append(f"      this.asyncCall().then(() => this.{target_method}());")
            
            # 添加条件分支
            if i % 3 == 0:
                call_htmls.append(f"      if (this.checkCondition()) {{")
                call_htmls.append(f"        this.handleSpecialCase();")
                call_htmls.append(f"      }}")
            
            # 添加循环
            if i % 5 == 0:
                call_htmls.append(f"      for (let i = 0; i < 10; i++) {{")
                call_htmls.append(f"        this.processItem(i);")
                call_htmls.append(f"      }}")
            
            # 添加异常处理
            if i % 7 == 0:
                call_htmls.append(f"      try {{")
                call_htmls.append(f"        this.riskyOperation();")
                call_htmls.append(f"      }} catch (e) {{")
                call_htmls.append(f"        this.handleError(e);")
                call_htmls.append(f"      }}")
            
            method_html = f"""
  // 方法 #{i} in {class_name}, 文件索引: {file_index}, 类索引: {class_index}
  {method_name}(): void {{
    console.log('Executing {method_name}');
{chr(10).join(call_htmls)}
  }}
"""
            methods.append(method_html)
        
        # 生成复杂的组件使用
        components = []
        component_count = random.randint(10, 25)
        for i in range(component_count):
            comp_name = random.choice([
                'Column', 'Row', 'Stack', 'Flex', 'Grid',
                'List', 'ListItem', 'Swiper', 'Tabs',
                'Navigation', 'Image', 'Text', 'Button'
            ])
            
            # 添加组件属性
            props = []
            if comp_name == 'Column':
                props.append(f"alignItems(HorizontalAlign.Center)")
            elif comp_name == 'Row':
                props.append(f"justifyContent(FlexAlign.Center)")
            elif comp_name == 'List':
                props.append(f"width('100%')")
            elif comp_name == 'Text':
                props.append(f"'Component {i}'")
            
            if props:
                components.append(f"    <{comp_name}({', '.join(props)})>")
            else:
                components.append(f"    <{comp_name}>")
            
            components.append(f"      <Text>Component {i}</Text>")
            components.append(f"    </{comp_name}>")
        
        return f"""
// 复杂类: {class_name}
// 文件索引: {file_index}, 类索引: {class_index}
// 方法数: {method_count}, 调用数: {call_count}
@Component
export struct {class_name} {{
  // 私有属性
  private data: number = {random.randint(1, 10000)};
  private name: string = "{self.generate_random_name()}";
  private enabled: boolean = {random.choice(['true', 'false'])};
  private items: string[] = {str([self.generate_random_name() for _ in range(5)])};
  private config: object = {{key: "{self.generate_random_name()}"}};
  
  // 复杂的方法集合
{chr(10).join(methods)}
  
  // build方法包含大量组件嵌套
  build() {{
{chr(10).join(components)}
  }}
}}
"""

    def generate_circular_dependencies(self):
        """生成循环依赖场景"""
        print(f"  📦 生成循环依赖测试文件...")
        
        # 创建三个相互依赖的类
        for i in range(3):
            file_path = os.path.join(self.project_path, "circular", f"Circular{i}.ets")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            content = f"""
@Component
export struct Circular{i} {{
  private data{i}: number = {i};
  
  method{i}A(): void {{
    console.log('Circular{i}.method{i}A');
    // 调用同一个类的其他方法
    this.method{i}B();
    // 调用其他类的依赖
    Circular{(i+1)%3}.method{(i+1)%3}A();
  }}
  
  method{i}B(): void {{
    console.log('Circular{i}.method{i}B');
    this.method{i}C();
  }}
  
  method{i}C(): void {{
    console.log('Circular{i}.method{i}C');
    Circular{(i+1)%3}.method{(i+1)%3}B();
  }}
  
  build() {{
    Column() {{
      Text('Circular {i}')
    }}
  }}
}}
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.file_count += 1
            self.class_count += 1
            self.method_count += 3
            self.call_count += 6

    def generate_recursive_calls(self):
        """生成递归调用场景"""
        print(f"  📦 生成递归调用测试文件...")
        
        file_path = os.path.join(self.project_path, "recursive", "RecursiveTest.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        content = """
@Component
export struct RecursiveTest {
  private depth: number = 0;
  private maxDepth: number = 100;
  
  // 直接递归
  recursiveMethodA(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodA(n - 1);
  }
  
  // 间接递归
  recursiveMethodB(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodC(n - 1);
  }
  
  recursiveMethodC(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodB(n - 1);
  }
  
  // 多路径递归
  recursiveMethodD(n: number): number {
    if (n <= 0) {
      return 0;
    }
    
    let result = n;
    
    // 多个递归路径
    if (n % 2 == 0) {
      result += this.recursiveMethodD(n / 2);
    } else {
      result += this.recursiveMethodD(n - 1);
      result += this.recursiveMethodE(n - 1);
    }
    
    return result;
  }
  
  recursiveMethodE(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodD(n - 1);
  }
  
  build() {
    Column() {
      Text('Recursive Test')
    }
  }
}
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 5
        self.call_count += 10

    def generate_error_handling_scenarios(self):
        """生成错误处理场景"""
        print(f"  📦 生成错误处理测试文件...")
        
        file_path = os.path.join(self.project_path, "error_handling", "ErrorHandlingTest.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        content = """
@Component
export struct ErrorHandlingTest {
  // try-catch 嵌套
  nestedTryCatch(): void {
    try {
      try {
        this.riskyOperation1();
      } catch (e1) {
        try {
          this.recoveryOperation1();
        } catch (e2) {
          this.finalCleanup();
        }
      }
    } catch (e3) {
      this.handleCriticalError(e3);
    }
  }
  
  // 条件异常
  conditionalException(condition: boolean): void {
    if (condition) {
      throw new Error('Conditional error');
    }
  }
  
  // 异步错误处理
  async asyncErrorHandling(): Promise<void> {
    try {
      await this.asyncRiskyOperation();
    } catch (e) {
      await this.handleAsyncError(e);
    }
  }
  
  // 多个catch分支
  multiCatch(error: Error): void {
    try {
      this.uncertainOperation();
    } catch (e) {
      if (e instanceof TypeError) {
        this.handleTypeError(e);
      } else if (e instanceof ReferenceError) {
        this.handleReferenceError(e);
      } else if (e instanceof RangeError) {
        this.handleRangeError(e);
      } else {
        this.handleGenericError(e);
      }
    }
  }
  
  riskyOperation1(): void { console.log('risky operation 1'); }
  recoveryOperation1(): void { console.log('recovery operation 1'); }
  finalCleanup(): void { console.log('final cleanup'); }
  handleCriticalError(e: any): void { console.log('critical error:', e); }
  uncertainOperation(): void { console.log('uncertain operation'); }
  handleTypeError(e: any): void { console.log('type error:', e); }
  handleReferenceError(e: any): void { console.log('reference error:', e); }
  handleRangeError(e: any): void { console.log('range error:', e); }
  handleGenericError(e: any): void { console.log('generic error:', e); }
  asyncRiskyOperation(): Promise<void> { return Promise.resolve(); }
  async handleAsyncError(e: any): Promise<void> { console.log('async error:', e); }
  
  build() {
    Column() {
      Text('Error Handling Test')
    }
  }
}
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 5
        self.call_count += 15

    def generate_async_complex_scenarios(self):
        """生成异步复杂场景"""
        print(f"  📦 生成异步复杂场景测试文件...")
        
        file_path = os.path.join(self.project_path, "async", "AsyncComplexTest.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        content = """
@Component
export struct AsyncComplexTest {
  // Promise链式调用
  promiseChain(): Promise<number> {
    return this.operation1()
      .then(result1 => this.operation2(result1))
      .then(result2 => this.operation3(result2))
      .then(result3 => this.operation4(result3))
      .then(result4 => this.finalOperation(result4))
      .catch(error => this.handleError(error));
  }
  
  // async-await嵌套
  async nestedAsyncAwait(): Promise<void> {
    const result1 = await this.fetchData1();
    const result2 = await this.fetchData2();
    
    if (result2.status === 'success') {
      const result3 = await this.processData(result2);
      await this.saveData(result3);
    }
  }
  
  // 并行Promise
  async parallelPromises(): Promise<any[]> {
    const [data1, data2, data3] = await Promise.all([
      this.fetchData1(),
      this.fetchData2(),
      this.fetchData3()
    ]);
    return [data1, data2, data3];
  }
  
  // 竞态条件
  async raceCondition(): Promise<string> {
    const result = await Promise.race([
      this.timeout(1000),
      this.fetchData1(),
      this.fetchData2()
    ]);
    return result;
  }
  
  operation1(): Promise<number> { return Promise.resolve(1); }
  operation2(n: number): Promise<number> { return Promise.resolve(n + 1); }
  operation3(n: number): Promise<number> { return Promise.resolve(n + 2); }
  operation4(n: number): Promise<number> { return Promise.resolve(n + 3); }
  finalOperation(n: number): Promise<number> { return Promise.resolve(n + 4); }
  handleError(e: any): any { console.error(e); return null; }
  fetchData1(): Promise<any> { return Promise.resolve({}); }
  fetchData2(): Promise<any> { return Promise.resolve({}); }
  fetchData3(): Promise<any> { return Promise.resolve({}); }
  processData(data: any): Promise<any> { return Promise.resolve(data); }
  saveData(data: any): Promise<void> { return Promise.resolve(); }
  timeout(ms: number): Promise<void> { return new Promise(resolve => setTimeout(resolve, ms)); }
  
  build() {
    Column() {
      Text('Async Complex Test')
    }
  }
}
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 6
        self.call_count += 20

    def generate_index_file(self):
        """生成入口文件"""
        index_path = os.path.join(self.project_path, "entry/src/main/ets/pages/Index.ets")
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        imports = []
        for i in range(min(self.file_count, 30)):
            imports.append(f"import {{ TestClass{i} }} from '../test/Test{i}.ets';")
        
        content = f"""// 入口文件 - 超复杂测试
// 总文件数: {self.file_count}
// 总类数: {self.class_count}
// 总方法数: {self.method_count}
// 总调用数: {self.call_count}
// 复杂度级别: {self.complexity_level}

{chr(10).join(imports)}

@Entry
@Component
struct Index {{
  build() {{
    Column() {{
      Text('Ultimate Chaos Test - {self.complexity_level}')
      Text('Files: {self.file_count}, Classes: {self.class_count}')
      Button('Start Extreme Test')
        .onClick(() => {{
          console.log('Starting extreme test...');
        }})
    }}
  }}
}}
"""
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_config(self):
        """生成配置文件"""
        config_path = os.path.join(self.project_path, "oh-package.json5")
        config = f"""{{
  "name": "ultimate-chaos-test",
  "version": "1.0.0",
  "description": "超大规模、超复杂、极端混乱测试项目",
  "main": "index.ets",
  "author": "Ultimate Chaos Generator",
  "metadata": {{
    "complexity_level": "{self.complexity_level}",
    "file_count": {self.file_count},
    "class_count": {self.class_count},
    "method_count": {self.method_count},
    "call_count": {self.call_count}
  }}
}}
"""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config)

    def generate(self, file_count=100, complexity="EXTREME"):
        """生成整个项目"""
        print("=" * 80)
        print("🚀 开始生成超大规模、超复杂、极端混乱测试项目...")
        print("=" * 80)
        print(f"📊 目标文件数: {file_count}")
        print(f"🎯 复杂度级别: {complexity}")
        print("=" * 80)
        
        # 创建基础目录
        test_dir = os.path.join(self.project_path, "entry/src/main/ets/test")
        os.makedirs(test_dir, exist_ok=True)
        
        # 生成主测试文件
        print(f"\n📦 生成主测试文件...")
        for i in range(file_count):
            file_path = os.path.join(test_dir, f"Test{i}.ets")
            self.generate_complex_file(file_path, i, complexity)
            
            if (i + 1) % 10 == 0:
                print(f"  ✅ 已生成 {i + 1}/{file_count} 个文件... (类: {self.class_count}, 方法: {self.method_count}, 调用: {self.call_count})")
        
        # 生成特殊场景测试
        print(f"\n📦 生成特殊场景测试...")
        self.generate_circular_dependencies()
        self.generate_recursive_calls()
        self.generate_error_handling_scenarios()
        self.generate_async_complex_scenarios()
        
        # 生成入口文件
        self.generate_index_file()
        
        # 生成配置
        self.generate_config()
        
        print("\n" + "=" * 80)
        print("🎉 生成完成!")
        print("=" * 80)
        print(f"  📄 文件总数: {self.file_count}")
        print(f"  🏛️  类总数: {self.class_count}")
        print(f"  ⚙️  方法总数: {self.method_count}")
        print(f"  🔗 调用总数: {self.call_count}")
        print(f"  🎯 复杂度: {self.complexity_level}")
        print("=" * 80)

if __name__ == "__main__":
    generator = UltimateChaosProjectGenerator("/workspace/UltimateChaosProject")
    generator.generate(file_count=100, complexity="EXTREME")
