#!/usr/bin/env python3
"""
增强版复杂测试项目生成器
生成有真实调用关系的复杂代码
"""
import random
from pathlib import Path

class EnhancedProjectGenerator:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.stats = {
            'files': 0,
            'classes': 0,
            'methods': 0,
            'calls': 0,
            'components': 0
        }
        self.all_methods = []  # 存储所有生成的方法名，用于生成调用关系
        
    def generate(self):
        print("开始生成增强版复杂测试项目...")
        
        self._create_directories()
        
        # 生成不同层次的代码
        self._generate_base_classes()      # 基础类
        self._generate_data_models(20)      # 数据模型
        self._generate_services(20)         # 服务层
        self._generate_business_logic(15)   # 业务逻辑
        self._generate_components(15)       # UI组件
        
        print(f"\n生成完成统计:")
        print(f"  文件数: {self.stats['files']}")
        print(f"  类数: {self.stats['classes']}")
        print(f"  方法数: {self.stats['methods']}")
        print(f"  调用关系: {self.stats['calls']}")
        print(f"  组件数: {self.stats['components']}")
        
    def _create_directories(self):
        dirs = ['base', 'models', 'services', 'business', 'components']
        for d in dirs:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)
    
    def _generate_base_classes(self):
        """生成基础类库"""
        content = """
export class BaseClass {
    protected id: string = '';
    
    init(): void {
        this.id = this.generateId();
    }
    
    generateId(): string {
        return Math.random().toString(36).substring(2);
    }
    
    toJSON(): object {
        return { id: this.id };
    }
    
    fromJSON(json: any): void {
        if (json.id) this.id = json.id;
    }
}

export class BaseService {
    protected cache: Map<string, any> = new Map();
    
    setCache(key: string, value: any): void {
        this.cache.set(key, value);
    }
    
    getCache(key: string): any {
        return this.cache.get(key);
    }
    
    clearCache(): void {
        this.cache.clear();
    }
    
    hasCache(key: string): boolean {
        return this.cache.has(key);
    }
}
"""
        self._write_file('base', 'base.ets', content)
        self.stats['classes'] += 2
        self.stats['methods'] += 9
    
    def _generate_data_models(self, count):
        """生成数据模型"""
        for i in range(count):
            filename = f"model_{i:02d}.ets"
            content = self._generate_model_content(i)
            self._write_file('models', filename, content)
            
    def _generate_model_content(self, index):
        classes = []
        num_classes = random.randint(2, 4)
        
        for c in range(num_classes):
            class_name = f"Model{c}{index:02d}"
            methods = []
            num_methods = random.randint(4, 8)
            
            for m in range(num_methods):
                method_name = f"process{m}"
                # 生成调用其他方法的代码
                calls = []
                if self.all_methods and random.random() > 0.5:
                    other_methods = random.sample(self.all_methods, min(2, len(self.all_methods)))
                    for om in other_methods:
                        if random.random() > 0.6:
                            calls.append(f"        this.{om}();")
                
                method = f"""
    {method_name}(): void {{
{chr(10).join(calls) if calls else '        // processing...'}
    }}"""
                methods.append(method)
                self.all_methods.append(method_name)
                self.stats['methods'] += 1
            
            cls = f"""
export class {class_name} {{
    private data: any;
    
    constructor() {{
        this.data = {{}};
    }}
    
{chr(10).join(methods)}
}}"""
            classes.append(cls)
            self.stats['classes'] += 1
        
        return ''.join(classes)
    
    def _generate_services(self, count):
        """生成服务层"""
        for i in range(count):
            filename = f"service_{i:02d}.ets"
            content = self._generate_service_content(i)
            self._write_file('services', filename, content)
            
    def _generate_service_content(self, index):
        classes = []
        num_classes = random.randint(2, 3)
        
        for c in range(num_classes):
            class_name = f"Service{c}{index:02d}"
            methods = []
            num_methods = random.randint(5, 10)
            
            for m in range(num_methods):
                method_name = f"fetch{m}Data"
                
                # 生成调用其他服务或自己的方法
                calls = []
                if self.all_methods and random.random() > 0.4:
                    other_methods = random.sample(self.all_methods, min(2, len(self.all_methods)))
                    for om in other_methods:
                        if random.random() > 0.5:
                            calls.append(f"        this.{om}();")
                
                method = f"""
    async {method_name}(id: string): Promise<any> {{
{chr(10).join(calls) if calls else '        const result = await fetch("/api/" + id);'}
        return result;
    }}"""
                methods.append(method)
                self.all_methods.append(method_name)
                self.stats['methods'] += 1
                
                if calls:
                    self.stats['calls'] += len(calls)
            
            # 添加一些内部调用方法
            internal_methods = [
                """
    validateInput(data: any): boolean {
        return data !== null && data !== undefined;
    }""",
                """
    formatOutput(data: any): any {
        return JSON.stringify(data);
    }"""
            ]
            methods.extend(internal_methods)
            self.all_methods.extend(['validateInput', 'formatOutput'])
            self.stats['methods'] += 2
            
            cls = f"""
export class {class_name} {{
{chr(10).join(methods)}
}}"""
            classes.append(cls)
            self.stats['classes'] += 1
        
        return ''.join(classes)
    
    def _generate_business_logic(self, count):
        """生成业务逻辑层"""
        for i in range(count):
            filename = f"business_{i:02d}.ets"
            content = self._generate_business_content(i)
            self._write_file('business', filename, content)
            
    def _generate_business_content(self, index):
        classes = []
        num_classes = random.randint(2, 3)
        
        for c in range(num_classes):
            class_name = f"Business{c}{index:02d}"
            methods = []
            num_methods = random.randint(6, 12)
            
            for m in range(num_methods):
                method_name = f"execute{m}"
                
                # 生成复杂的调用链
                calls = []
                if self.all_methods and random.random() > 0.3:
                    other_methods = random.sample(self.all_methods, min(3, len(self.all_methods)))
                    for om in other_methods:
                        calls.append(f"        this.{om}();")
                
                method = f"""
    {method_name}(params: any): any {{
        if (this.validate(params)) {{
{chr(10).join(calls) if calls else '            const result = this.process(params);'}
            return result;
        }}
        return null;
    }}"""
                methods.append(method)
                self.all_methods.append(method_name)
                self.stats['methods'] += 1
                
                if calls:
                    self.stats['calls'] += len(calls)
            
            # 验证和处理方法
            helper_methods = [
                """
    validate(params: any): boolean {
        return params !== null;
    }""",
                """
    process(params: any): any {
        return { success: true, data: params };
    }"""
            ]
            methods.extend(helper_methods)
            self.all_methods.extend(['validate', 'process'])
            self.stats['methods'] += 2
            
            cls = f"""
export class {class_name} {{
{chr(10).join(methods)}
}}"""
            classes.append(cls)
            self.stats['classes'] += 1
        
        return ''.join(classes)
    
    def _generate_components(self, count):
        """生成 UI 组件"""
        for i in range(count):
            filename = f"Component{i:02d}.ets"
            content = self._generate_component_content(i)
            self._write_file('components', filename, content)
            
    def _generate_component_content(self, index):
        components = []
        num_components = random.randint(2, 3)
        
        for c in range(num_components):
            comp_name = f"CustomComp{c}{index:02d}"
            
            # 状态变量
            states = [f"@State value{c}: number = 0;" for c in range(3)]
            
            # 方法
            methods = []
            num_methods = random.randint(3, 6)
            
            for m in range(num_methods):
                method_name = f"onClick{m}"
                
                # 生成方法调用
                calls = []
                if self.all_methods and random.random() > 0.4:
                    other_methods = random.sample(self.all_methods, min(2, len(self.all_methods)))
                    for om in other_methods:
                        calls.append(f"        this.{om}();")
                
                method = f"""
    {method_name}(): void {{
{chr(10).join(calls) if calls else '        this.value0++;'}
    }}"""
                methods.append(method)
                self.all_methods.append(method_name)
                self.stats['methods'] += 1
                
                if calls:
                    self.stats['calls'] += len(calls)
            
            # build 方法中使用子组件
            child_components = random.sample(['Text', 'Button', 'Column', 'Row', 'List'], 2)
            build_parts = [f"            {comp}() {{}}" for comp in child_components]
            
            component = f"""
@Component
export struct {comp_name} {{
{chr(10).join(states)}

{chr(10).join(methods)}

    build() {{
{chr(10).join(build_parts)}
    }}
}}"""
            components.append(component)
            self.stats['classes'] += 1
            self.stats['components'] += 1
        
        return ''.join(components)
    
    def _write_file(self, subdir, filename, content):
        filepath = self.output_dir / subdir / filename
        filepath.write_text(content, encoding='utf-8')
        self.stats['files'] += 1

if __name__ == '__main__':
    generator = EnhancedProjectGenerator('/workspace/complex_test_project')
    generator.generate()
