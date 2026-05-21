#!/usr/bin/env python3
"""
超大规模混乱测试项目生成器
用于测试系统在极端情况下的表现
"""

import os
import random
import string

class ExtremeChaosProjectGenerator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.file_count = 0
        self.class_count = 0
        self.method_count = 0
        self.call_count = 0
        
    def generate_random_name(self, prefix="Test"):
        """生成随机名称"""
        suffix = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 12)))
        return f"{prefix}_{suffix}"
    
    def generate_file(self, file_path, file_index):
        """生成单个ArkTS文件"""
        self.file_count += 1
        
        class_count_in_file = random.randint(5, 15)
        classes_html = []
        
        for i in range(class_count_in_file):
            self.class_count += 1
            class_name = self.generate_random_name("Class")
            class_html = self.generate_class(class_name, file_index, i)
            classes_html.append(class_html)
        
        file_content = f"""// @ts-nocheck
// 极端混乱测试文件 #{file_index}
// 文件名: {os.path.basename(file_path)}
// 类数量: {class_count_in_file}

{chr(10).join(classes_html)}
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
    
    def generate_class(self, class_name, file_index, class_index):
        """生成类"""
        method_count = random.randint(8, 20)
        methods = []
        
        for i in range(method_count):
            self.method_count += 1
            method_name = self.generate_random_name("method")
            method_calls = random.randint(3, 12)
            call_htmls = []
            
            for j in range(method_calls):
                self.call_count += 1
                target_class = self.generate_random_name("Class")
                target_method = self.generate_random_name("method")
                call_htmls.append(f"      this.{target_method}();")
                call_htmls.append(f"      Other{target_class}.{target_method}();")
            
            method_html = f"""
  {method_name}(): void {{
    // 方法 #{i} in {class_name}
{chr(10).join(call_htmls)}
  }}
"""
            methods.append(method_html)
        
        # 生成组件使用
        components = []
        component_count = random.randint(3, 8)
        for i in range(component_count):
            comp_name = random.choice(['Column', 'Row', 'Stack', 'Flex', 'Grid'])
            components.append(f"    <{comp_name}>")
            components.append(f"      <Text>Component {i}</Text>")
            components.append(f"    </{comp_name}>")
        
        return f"""
@Component
export struct {class_name} {{
  // 文件索引: {file_index}, 类索引: {class_index}
  private data: number = {random.randint(1, 1000)};
  private name: string = "{self.generate_random_name()}";
  private enabled: boolean = {random.choice(['true', 'false'])};
  
{chr(10).join(methods)}
  
  build() {{
{chr(10).join(components)}
  }}
}}
"""

    def generate_index_file(self):
        """生成入口文件"""
        index_path = os.path.join(self.project_path, "entry/src/main/ets/pages/Index.ets")
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        imports = []
        for i in range(min(self.file_count, 20)):
            imports.append(f"import {{ TestClass{i} }} from '../test/Test{i}.ets';")
        
        content = f"""// 入口文件
// 总文件数: {self.file_count}
// 总类数: {self.class_count}
// 总方法数: {self.method_count}
// 总调用数: {self.call_count}

{chr(10).join(imports)}

@Entry
@Component
struct Index {{
  build() {{
    Column() {{
      Text('Extreme Chaos Test')
      Button('Start Test')
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
  "name": "extreme-chaos-test",
  "version": "1.0.0",
  "description": "超大规模混乱测试项目",
  "main": "index.ets",
  "author": "Test Generator",
  "files": {self.file_count},
  "classes": {self.class_count},
  "methods": {self.method_count},
  "calls": {self.call_count}
}}
"""
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config)

    def generate(self, file_count=50):
        """生成整个项目"""
        print(f"🚀 开始生成超大规模混乱测试项目...")
        print(f"📊 目标文件数: {file_count}")
        
        # 生成测试文件
        test_dir = os.path.join(self.project_path, "entry/src/main/ets/test")
        os.makedirs(test_dir, exist_ok=True)
        
        for i in range(file_count):
            file_path = os.path.join(test_dir, f"Test{i}.ets")
            self.generate_file(file_path, i)
            if (i + 1) % 10 == 0:
                print(f"  ✅ 已生成 {i + 1}/{file_count} 个文件...")
        
        # 生成入口文件
        self.generate_index_file()
        
        # 生成配置
        self.generate_config()
        
        print(f"\n🎉 生成完成!")
        print(f"  📄 文件数: {self.file_count}")
        print(f"  🏛️  类数: {self.class_count}")
        print(f"  ⚙️  方法数: {self.method_count}")
        print(f"  🔗 调用数: {self.call_count}")

if __name__ == "__main__":
    generator = ExtremeChaosProjectGenerator("/workspace/ExtremeChaosProject")
    generator.generate(file_count=50)
