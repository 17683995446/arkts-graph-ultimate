#!/usr/bin/env python3
"""
大规模复杂测试项目生成器
生成 100+ 文件，500+ 类，1000+ 方法
用于压力测试和边界情况测试
"""
import os
import random
from pathlib import Path

class ComplexProjectGenerator:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.stats = {
            'files': 0,
            'classes': 0,
            'methods': 0,
            'components': 0,
            'inheritance': 0,
            'interfaces': 0
        }
        
    def generate(self):
        print("开始生成复杂测试项目...")
        
        # 创建目录结构
        self._create_directories()
        
        # 生成各个模块
        self._generate_models(30)      # 数据模型层
        self._generate_services(25)    # 服务层
        self._generate_components(20)  # UI组件
        self._generate_utils(15)       # 工具类
        self._generate_managers(10)   # 管理器
        
        # 生成复杂依赖关系
        self._generate_controllers(15)
        self._generate_providers(10)
        
        print(f"\n生成完成统计:")
        print(f"  文件数: {self.stats['files']}")
        print(f"  类数: {self.stats['classes']}")
        print(f"  方法数: {self.stats['methods']}")
        print(f"  组件数: {self.stats['components']}")
        print(f"  继承关系: {self.stats['inheritance']}")
        print(f"  接口数: {self.stats['interfaces']}")
        
    def _create_directories(self):
        dirs = [
            'models', 'services', 'components', 
            'utils', 'managers', 'controllers',
            'providers', 'mixins', 'base', 'types'
        ]
        for d in dirs:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)
            
    def _generate_models(self, count):
        print(f"生成 models ({count} 文件)...")
        for i in range(count):
            filename = f"model_{i:03d}.ets"
            content = self._generate_model_file(i)
            self._write_file('models', filename, content)
            
    def _generate_model_file(self, index):
        class_count = random.randint(3, 8)
        classes_code = []
        
        for c in range(class_count):
            class_name = f"Model{c}{index:02d}"
            extends = f"extends BaseModel" if random.random() > 0.3 else ""
            implements = f"implements ISerializable, ICloneable" if random.random() > 0.5 else ""
            
            # 生成属性
            props = []
            for p in range(random.randint(5, 15)):
                prop_type = random.choice(['string', 'number', 'boolean', 'ModelData', 'string[]'])
                props.append(f"  @Prop {prop_type.lower()}{p}: {prop_type};")
            
            # 生成方法
            methods = []
            for m in range(random.randint(3, 10)):
                method_name = f"method{m}"
                params = f"param1: string, param2: number" if m % 2 == 0 else ""
                return_stmt = "return 'result';" if random.random() > 0.3 else ""
                methods.append(f"""
    {method_name}({params}): {random.choice(['string', 'boolean', 'void'])} {{
        this.data{m} = {random.choice(['param1', 'param2', 'true', '"hello"'])};
        {return_stmt}
    }}""")
            
            class_code = f"""
export class {class_name} {extends} {implements} {{
{chr(10).join(props)}

{chr(10).join(methods)}
}}"""
            classes_code.append(class_code)
            self.stats['classes'] += 1
            self.stats['methods'] += len(methods)
            if extends:
                self.stats['inheritance'] += 1
                
        return ''.join(classes_code)
        
    def _generate_services(self, count):
        print(f"生成 services ({count} 文件)...")
        for i in range(count):
            filename = f"service_{i:03d}.ets"
            content = self._generate_service_file(i)
            self._write_file('services', filename, content)
            
    def _generate_service_file(self, index):
        class_count = random.randint(2, 5)
        classes_code = []
        
        for c in range(class_count):
            class_name = f"Service{c}{index:02d}"
            async_methods = []
            
            # 生成异步方法
            for m in range(random.randint(5, 12)):
                method_name = f"fetch{m}Data"
                async_methods.append(f"""
    async {method_name}(id: string): Promise<DataResult> {{
        const response = await fetch('/api/' + id);
        return response.json();
    }}""")
                self.stats['methods'] += 1
            
            # 生成回调方法
            for cb in range(random.randint(3, 8)):
                callback_name = f"onCallback{cb}"
                async_methods.append(f"""
    {callback_name}(callback: (data: any) => void): void {{
        callback(this.cache{cb});
    }}""")
                self.stats['methods'] += 1
                
            class_code = f"""
export class {class_name} {{
{chr(10).join(async_methods)}
}}"""
            classes_code.append(class_code)
            self.stats['classes'] += 1
                
        return ''.join(classes_code)
        
    def _generate_components(self, count):
        print(f"生成 components ({count} 文件)...")
        for i in range(count):
            filename = f"Component{i:03d}.ets"
            content = self._generate_component_file(i)
            self._write_file('components', filename, content)
            
    def _generate_component_file(self, index):
        component_count = random.randint(2, 4)
        components = []
        
        for c in range(component_count):
            comp_name = f"CustomComponent{c}{index:02d}"
            
            # @State 装饰器
            states = [f"@State count{c}: number = 0;" for c in range(random.randint(3, 8))]
            
            # @Link 装饰器
            links = [f"@Link data{c}: any;" for c in range(random.randint(2, 5))]
            
            # build 方法
            build_parts = []
            for b in range(random.randint(5, 12)):
                child_comp = random.choice(['Column', 'Row', 'Text', 'Button', 'List', 'Grid'])
                build_parts.append(f"            {child_comp}() {{}}")
            
            # 生命周期方法
            lifecycle = []
            if random.random() > 0.5:
                lifecycle.append("""
    aboutToAppear(): void {
        console.log('Component about to appear');
    }""")
            if random.random() > 0.5:
                lifecycle.append("""
    aboutToDisappear(): void {
        console.log('Component about to disappear');
    }""")
            
            component = f"""
@Component
export struct {comp_name} {{
{chr(10).join(states)}
{chr(10).join(links)}

{chr(10).join(lifecycle)}

    build() {{
{chr(10).join(build_parts)}
    }}
}}"""
            components.append(component)
            self.stats['classes'] += 1
            self.stats['components'] += 1
            self.stats['methods'] += len(lifecycle) + 1
                
        return ''.join(components)
        
    def _generate_utils(self, count):
        print(f"生成 utils ({count} 文件)...")
        for i in range(count):
            filename = f"util_{i:03d}.ets"
            content = self._generate_util_file(i)
            self._write_file('utils', filename, content)
            
    def _generate_util_file(self, index):
        class_count = random.randint(2, 4)
        classes = []
        
        for c in range(class_count):
            class_name = f"Util{c}{index:02d}"
            static_methods = []
            
            for m in range(random.randint(8, 15)):
                method_name = f"static{m}Method"
                static_methods.append(f"""
    static {method_name}(input: string): string {{
        return input.trim().toUpperCase();
    }}""")
                self.stats['methods'] += 1
                
            util = f"""
export class {class_name} {{
{chr(10).join(static_methods)}
}}"""
            classes.append(util)
            self.stats['classes'] += 1
                
        return ''.join(classes)
        
    def _generate_managers(self, count):
        print(f"生成 managers ({count} 文件)...")
        for i in range(count):
            filename = f"manager_{i:03d}.ets"
            content = self._generate_manager_file(i)
            self._write_file('managers', filename, content)
            
    def _generate_manager_file(self, index):
        class_count = random.randint(2, 3)
        classes = []
        
        for c in range(class_count):
            class_name = f"Manager{c}{index:02d}"
            singleton = random.random() > 0.5
            
            if singleton:
                instance_var = f"private static instance: {class_name};"
                get_instance = f"""
    static getInstance(): {class_name} {{
        if (!{class_name}.instance) {{
            {class_name}.instance = new {class_name}();
        }}
        return {class_name}.instance;
    }}"""
            else:
                instance_var = ""
                get_instance = ""
            
            methods = []
            for m in range(random.randint(10, 20)):
                method_name = f"manage{m}"
                methods.append(f"""
    {method_name}(data: any): boolean {{
        this.cache{m} = data;
        return true;
    }}""")
                self.stats['methods'] += 1
                
            manager = f"""
export class {class_name} {{
{instance_var}
{get_instance}
{chr(10).join(methods)}
}}"""
            classes.append(manager)
            self.stats['classes'] += 1
            if singleton:
                self.stats['inheritance'] += 1
                
        return ''.join(classes)
        
    def _generate_controllers(self, count):
        print(f"生成 controllers ({count} 文件)...")
        for i in range(count):
            filename = f"controller_{i:03d}.ets"
            content = self._generate_controller_file(i)
            self._write_file('controllers', filename, content)
            
    def _generate_controller_file(self, index):
        class_count = random.randint(2, 4)
        classes = []
        
        for c in range(class_count):
            class_name = f"Controller{c}{index:02d}"
            
            # 路由定义
            routes = []
            for r in range(random.randint(5, 10)):
                routes.append(f"  @Route({{ path: '/route{r}', route: '{class_name.lower()}/action{r}' }})")
            
            # Action 方法
            actions = []
            for a in range(random.randint(5, 10)):
                action_name = f"action{a}"
                actions.append(f"""
    @Action
    {action_name}(): void {{
        this.data{a} = 'action triggered';
    }}""")
                self.stats['methods'] += 1
                
            controller = f"""
@Controller
export class {class_name} {{
{chr(10).join(routes)}

{chr(10).join(actions)}
}}"""
            classes.append(controller)
            self.stats['classes'] += 1
            self.stats['interfaces'] += 1
                
        return ''.join(classes)
        
    def _generate_providers(self, count):
        print(f"生成 providers ({count} 文件)...")
        for i in range(count):
            filename = f"provider_{i:03d}.ets"
            content = self._generate_provider_file(i)
            self._write_file('providers', filename, content)
            
    def _generate_provider_file(self, index):
        class_count = random.randint(2, 3)
        classes = []
        
        for c in range(class_count):
            class_name = f"Provider{c}{index:02d}"
            
            # Consume 和 Provide
            provides = []
            consumes = []
            
            for p in range(random.randint(3, 6)):
                provides.append(f"@Provide('{class_name.lower()}_data{p}') data{p}: any = null;")
                consumes.append(f"@Consume('{class_name.lower()}_data{p}') received{p}: any;")
            
            # 方法
            methods = []
            for m in range(random.randint(5, 8)):
                methods.append(f"""
    provide{m}(): void {{
        this.data{m} = 'provided';
    }}""")
                self.stats['methods'] += 1
                
            provider = f"""
@Entry
@Component
export struct {class_name} {{
{chr(10).join(provides)}
{chr(10).join(consumes)}

{chr(10).join(methods)}

    build() {{
        Column() {{
            Text('Provider')
        }}
    }}
}}"""
            classes.append(provider)
            self.stats['classes'] += 1
            self.stats['components'] += 1
                
        return ''.join(classes)
        
    def _write_file(self, subdir, filename, content):
        filepath = self.output_dir / subdir / filename
        filepath.write_text(content, encoding='utf-8')
        self.stats['files'] += 1

if __name__ == '__main__':
    generator = ComplexProjectGenerator('/workspace/complex_test_project')
    generator.generate()
