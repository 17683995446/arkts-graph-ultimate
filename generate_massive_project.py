#!/usr/bin/env python3
"""
超大规模测试项目生成器
生成500+文件进行压力测试
"""
import random
from pathlib import Path

class MassiveProjectGenerator:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.stats = {
            'files': 0,
            'classes': 0,
            'methods': 0,
            'calls': 0,
            'components': 0
        }
        
    def generate(self):
        print("开始生成超大规模测试项目...")
        
        # 创建目录结构
        self._create_directories()
        
        # 生成各个模块（每个模块生成大量文件）
        modules = [
            ('models', 80),      # 80个数据模型文件
            ('services', 70),    # 70个服务文件
            ('components', 60),  # 60个组件文件
            ('controllers', 50), # 50个控制器
            ('utils', 60),      # 60个工具类
            ('managers', 40),    # 40个管理器
            ('providers', 40),   # 40个提供者
            ('business', 50),   # 50个业务逻辑
            ('middleware', 30),  # 30个中间件
            ('types', 20),      # 20个类型定义
        ]
        
        for module_name, file_count in modules:
            print(f"生成 {module_name} ({file_count} 文件)...")
            self._generate_module(module_name, file_count)
        
        print(f"\n生成完成统计:")
        print(f"  文件数: {self.stats['files']}")
        print(f"  类数: {self.stats['classes']}")
        print(f"  方法数: {self.stats['methods']}")
        print(f"  调用关系: {self.stats['calls']}")
        print(f"  组件数: {self.stats['components']}")
        
    def _create_directories(self):
        dirs = ['models', 'services', 'components', 'controllers', 
                'utils', 'managers', 'providers', 'business', 
                'middleware', 'types', 'base']
        for d in dirs:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)
    
    def _generate_module(self, module_name, file_count):
        for i in range(file_count):
            filename = f"{module_name[:-1]}_{i:03d}.ets"
            content = self._generate_file_content(module_name, i)
            self._write_file(module_name, filename, content)
    
    def _generate_file_content(self, module, index):
        class_count = random.randint(2, 5)
        classes = []
        
        for c in range(class_count):
            class_name = f"{module.title()}{c}{index:03d}"
            methods = []
            method_count = random.randint(5, 15)
            
            for m in range(method_count):
                method_name = f"method{m}"
                
                # 生成方法体
                method_body = self._generate_method_body(m)
                methods.append(f"""
    {method_name}(): void {{
{chr(10).join(method_body)}
    }}""")
                self.stats['methods'] += 1
                
                # 生成一些调用关系
                if random.random() > 0.7:
                    self.stats['calls'] += 1
            
            # 生成组件特有内容
            is_component = module in ['components', 'providers']
            if is_component:
                self.stats['components'] += 1
            
            cls = f"""
export class {class_name} {{
{chr(10).join(methods)}
}}"""
            classes.append(cls)
            self.stats['classes'] += 1
        
        return ''.join(classes)
    
    def _generate_method_body(self, method_index):
        """生成方法体"""
        body = []
        statements = random.randint(3, 8)
        
        for _ in range(statements):
            stmt_type = random.choice(['assignment', 'call', 'condition', 'loop'])
            
            if stmt_type == 'assignment':
                body.append(f"        const x{method_index} = {random.randint(1, 100)};")
            elif stmt_type == 'call':
                body.append(f"        this.process{method_index}();")
            elif stmt_type == 'condition':
                body.append(f"        if (x{method_index} > 0) {{ }}")
            elif stmt_type == 'loop':
                body.append(f"        for (let i = 0; i < 10; i++) {{ }}")
        
        return body
    
    def _write_file(self, subdir, filename, content):
        filepath = self.output_dir / subdir / filename
        filepath.write_text(content, encoding='utf-8')
        self.stats['files'] += 1

if __name__ == '__main__':
    generator = MassiveProjectGenerator('/workspace/massive_test_project')
    generator.generate()
