#!/usr/bin/env python3
import random
import tempfile
from pathlib import Path
from datetime import datetime, timedelta


class ChaosTestProjectGenerator:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.project_path = base_path / "ChaosTestProject"
    
    def generate_chaos_files(self):
        self.project_path.mkdir(parents=True, exist_ok=True)
        
        # 1. 损坏的语法文件
        self.generate_broken_syntax_files()
        
        # 2. 特殊字符和编码问题
        self.generate_special_encoding_files()
        
        # 3. 空文件和几乎空的文件
        self.generate_empty_near_empty_files()
        
        # 4. 超级大文件
        self.generate_huge_files()
        
        # 5. 深层嵌套目录
        self.generate_deep_nested_directories()
        
        # 6. 循环导入
        self.generate_circular_imports()
        
        # 7. 混合语言文件
        self.generate_mixed_language_files()
        
        # 8. 混乱格式的代码
        self.generate_messy_formatting_files()
        
        # 9. 极端文件命名
        self.generate_extreme_named_files()
        
        # 10. 时间戳和临时文件
        self.generate_temporary_style_files()
        
        total_files = sum(1 for _ in self.project_path.rglob("*") if _.is_file())
        print(f"✅ 生成完成！共 {total_files} 个混乱测试文件！")
        
        return self.project_path
    
    def generate_broken_syntax_files(self):
        dir_path = self.project_path / "broken-syntax"
        dir_path.mkdir(exist_ok=True)
        
        # 文件1: 不完整的类
        file1 = dir_path / "incomplete-class.ets"
        file1.write_text("""export class Incomplete {
    someMethod() {
        console.log('missing closing bracket!
// oops, no closing
""")
        
        # 文件2: 不匹配的括号
        file2 = dir_path / "unmatched-parens.ets"
        file2.write_text("""export function badMath() {
    return (5 + (3 * 2; // missing a closing )
}
export function nestedProblem() {
    let x = (1 + (2 + (3 + 4;
}
""")
        
        # 文件3: 错误的装饰器语法
        file3 = dir_path / "wrong-decorators.ets"
        file3.write_text("""@Component
export struct BadComponent { // no closing }
@State count = 0;
    build() {
        Text('Hi');
    }
// missing closing
""")
        
        # 文件4: 不完整的字符串
        file4 = dir_path / "broken-strings.ets"
        file4.write_text("""export class Strings {
    getGreeting() {
        return 'Hello world; // missing closing quote
    }
    
    getMessage() {
        return "This is a string with no end;
    }
}
""")
        
        print("  - 损坏的语法文件生成完成")
    
    def generate_special_encoding_files(self):
        dir_path = self.project_path / "encoding-chaos"
        dir_path.mkdir(exist_ok=True)
        
        # 各种特殊字符
        file1 = dir_path / "special-chars.ets"
        special_content = """export class SpecialChars {
    chinese = "测试中文";
    japanese = "日本語";
    korean = "한국어";
    emoji = "🚀🔥💻";
    math = "∑∞∫√π";
    symbols = "©®™§¶†‡";
    
    workWithText() {
        let text = this.chinese + this.japanese + this.korean;
        console.log(text);
    }
}
"""
        file1.write_text(special_content, encoding='utf-8')
        
        # 混合换行和缩进
        file2 = dir_path / "weird-newlines.ets"
        file2.write_text("""export class WeirdNewlines {
\r\ndoThing() {\r\n
\n  console.log('mixed');\r
  return\r\n
    true;\r\n
}\n
}
""")
        
        print("  - 特殊编码文件生成完成")
    
    def generate_empty_near_empty_files(self):
        dir_path = self.project_path / "empty-files"
        dir_path.mkdir(exist_ok=True)
        
        # 完全空
        file1 = dir_path / "completely-empty.ets"
        file1.write_text("")
        
        # 只有空格和换行
        file2 = dir_path / "only-whitespace.ets"
        file2.write_text("\n\n   \t  \n   \n\n")
        
        # 只有注释
        file3 = dir_path / "only-comments.ets"
        file3.write_text("""// This file has nothing but comments
// Another line
/* 
   Multi-line
*/
// The end
""")
        
        # 只有import语句
        file4 = dir_path / "only-imports.ets"
        file4.write_text("""import { Foo } from '../common';
import * as utils from '../utils';
import type { Bar } from '../types';
// nothing else!
""")
        
        print("  - 空文件和几乎空文件生成完成")
    
    def generate_huge_files(self):
        dir_path = self.project_path / "huge-files"
        dir_path.mkdir(exist_ok=True)
        
        # 一个包含超多方法的类
        huge_class = dir_path / "mega-class.ets"
        content = "export class MegaClass {\n"
        
        for i in range(1000):
            content += f"  method{i}() {{ console.log('Method {i}'); }}\n"
        
        content += "}\n"
        huge_class.write_text(content)
        
        # 一个包含超级多行的文件
        huge_data = dir_path / "data-lines.ets"
        data_content = "export const MASSIVE_DATA = [\n"
        
        for i in range(2000):
            data_content += f"  {{ id: {i}, name: 'Item {i}', value: {i * 2} }},\n"
        
        data_content += "];\n"
        huge_data.write_text(data_content)
        
        print("  - 超大文件生成完成")
    
    def generate_deep_nested_directories(self):
        # 创建非常深的目录结构
        current = self.project_path / "deeply-nested"
        
        for depth in range(30):  # 30层嵌套
            current = current / f"level-{depth+1}"
            current.mkdir(parents=True, exist_ok=True)
            
            # 在每一层都放一些文件
            for f in range(3):
                file_path = current / f"file-{f}.ets"
                file_content = f"""export class Level{depth+1}File{f} {{
    value = {depth * 100 + f};
    getValue() {{ return this.value; }}
}}
"""
                file_path.write_text(file_content)
        
        print("  - 深层嵌套目录生成完成")
    
    def generate_circular_imports(self):
        dir_path = self.project_path / "circular-imports"
        dir_path.mkdir(exist_ok=True)
        
        # A import B, B import A
        file_a = dir_path / "module-a.ets"
        file_a.write_text("""import { B } from './module-b';
export class A {
    doSomething() {
        return new B().getValue();
    }
    getValue() { return 42; }
}
""")
        
        file_b = dir_path / "module-b.ets"
        file_b.write_text("""import { A } from './module-a';
export class B {
    doSomething() {
        return new A().getValue();
    }
    getValue() { return 1337; }
}
""")
        
        # 三层循环导入
        file_c = dir_path / "module-c.ets"
        file_c.write_text("""import { D } from './module-d';
export class C {
    value = new D().value;
}
""")
        
        file_d = dir_path / "module-d.ets"
        file_d.write_text("""import { E } from './module-e';
export class D {
    value = new E().value;
}
""")
        
        file_e = dir_path / "module-e.ets"
        file_e.write_text("""import { C } from './module-c';
export class E {
    value = new C().value;
}
""")
        
        print("  - 循环导入文件生成完成")
    
    def generate_mixed_language_files(self):
        dir_path = self.project_path / "mixed-languages"
        dir_path.mkdir(exist_ok=True)
        
        # 混合语法文件
        file1 = dir_path / "mixed-code.ets"
        file1.write_text("""export class Mixed {
    test() {
        // JS风格
        var x = 1;
        let y = 2;
        
        // TS类型
        let z: number = 3;
        
        // ArkUI装饰器
        @Component
        struct X { /* ... */ }
        
        // 混合注释
        /* C-style */
        // line comment
    }
}
""")
        
        # 奇怪文件扩展名
        strange1 = dir_path / "data.etstxt"
        strange1.write_text("export const data = 'not ets';")
        
        strange2 = dir_path / "script.ts.js"
        strange2.write_text("console.log('weird extension');")
        
        print("  - 混合语言文件生成完成")
    
    def generate_messy_formatting_files(self):
        dir_path = self.project_path / "messy-formatting"
        dir_path.mkdir(exist_ok=True)
        
        # 没有缩进的代码
        file1 = dir_path / "no-indent.ets"
        file1.write_text("""export class Ugly {
doSomething() {
return 42;
}
anotherMethod() {
if(true) {
return 'bad';
}
}
}
""")
        
        # 疯狂缩进
        file2 = dir_path / "crazy-indent.ets"
        file2.write_text("""export class Crazy {
            doThing() {
                                  console.log('indented');
            }
                    another() {
return 'test';
                    }
}
""")
        
        # 超长行
        file3 = dir_path / "long-line.ets"
        long_content = "export const REALLY_LONG = " + "x" * 500 + ";\n"
        file3.write_text(long_content)
        
        # 空行混乱
        file4 = dir_path / "empty-lines.ets"
        file4.write_text("""export class EmptyLines {


    method1() {


    }
    
    

    method2() {


    }


}
""")
        
        print("  - 混乱格式文件生成完成")
    
    def generate_extreme_named_files(self):
        dir_path = self.project_path / "extreme-names"
        dir_path.mkdir(exist_ok=True)
        
        # 超长文件名
        long_name = "ThisIsAReallyLongClassNameThatShouldBeHandled" + "X" * 50
        file1 = dir_path / (long_name + ".ets")
        file1.write_text(f"""export class {long_name} {{
    value = 'long name test';
}}
""")
        
        # 包含特殊字符的文件名
        import string
        safe_chars = set(string.ascii_letters + string.digits + "_-.")
        
        # 创建一些带点和下划线的
        weird1 = dir_path / "file..with..many..dots.ets"
        weird1.write_text("export class DotFile { }")
        
        weird2 = dir_path / "___triple-underscore___.ets"
        weird2.write_text("export class UnderScore { }")
        
        weird3 = dir_path / "mixedCase-With-Dashes_and_underscores.ets"
        weird3.write_text("export class MixedNames { }")
        
        # 包含数字开头的
        file_num = dir_path / "123number-start.ets"
        file_num.write_text("export class StartWithNumber { }")
        
        print("  - 极端文件名生成完成")
    
    def generate_temporary_style_files(self):
        dir_path = self.project_path / "temporary-style"
        dir_path.mkdir(exist_ok=True)
        
        # ~备份文件
        file1 = dir_path / "backup.ets~"
        file1.write_text("export class Backup { }")
        
        # #临时文件
        file2 = dir_path / "#temp-file#.ets"
        file2.write_text("export class TempFile { }")
        
        # .swp文件
        file3 = dir_path / ".editor-swap.ets.swp"
        file3.write_text("export class Swap { }")
        
        # 带有~和#的真实文件
        file4 = dir_path / "normal-file.ets"
        file4.write_text("""export class Normal {
    doWork() { return 'this is normal'; }
}
""")
        
        print("  - 临时风格文件生成完成")


if __name__ == "__main__":
    print("="*60)
    print("🎯 生成极端混乱复杂的测试项目")
    print("="*60)
    
    base_path = Path("/workspace")
    generator = ChaosTestProjectGenerator(base_path)
    chaos_project = generator.generate_chaos_files()
    
    print(f"\n✅ 混乱测试项目创建完成: {chaos_project}")
    print("\n准备好进行极端测试！")
