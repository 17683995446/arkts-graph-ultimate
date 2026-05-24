#!/usr/bin/env python3
"""
超混乱、超复杂的真实场景测试项目生成器
包含各种极端情况和混乱结构
"""
import os
import random
import string
from datetime import datetime

class ChaosUltimateProjectGenerator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.file_count = 0
        self.class_count = 0
        self.method_count = 0
        self.call_count = 0

    def generate_random_name(self, prefix="Test"):
        """生成随机混乱名称"""
        length = random.randint(5, 30)
        name_chars = string.ascii_letters + string.digits
        name = ''.join(random.choice(name_chars) for _ in range(length))
        return f"{prefix}_{name}"

    def generate_chaos_file_1(self):
        """生成混乱文件1: 超长方法名、超多层嵌套"""
        content = '''
/**
 * 极度混乱的文件1 - 超长方法名、超多层嵌套
 */
@Component
export struct ExtremelyLongClassNameForTestingPurposesBecauseWeNeedReallyLongNamesToBreakThings {
    private aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble: number = 0;
    
    // 超长方法名
    thisIsAnExtremelyLongMethodNameThatIsWayTooLongAndProbablyShouldBeShorterButWeAreMakingItEvenLongerJustToSeeWhatHappens(): void {
        console.log('超长方法');
        this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble = 42;
        
        // 多层嵌套
        if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 0) {
            if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 10) {
                if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 20) {
                    if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 30) {
                        if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 40) {
                            console.log('嵌套到了第5层！');
                        }
                    }
                }
            }
        }
    }
    
    anotherLongMethodThatAlsoDoesNotNeedToBeSoLongButHereWeAreAgain(): void {
        let result = this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble + 1;
        console.log(result);
    }
    
    build() {
        Column() {
            Text('超级混乱组件');
        }
    }
}

// 另一个类
@Component
export struct AnotherChaosClass {
    private counter: number = 0;
    
    method1(): void {
        this.method2();
    }
    
    method2(): void {
        this.method3();
    }
    
    method3(): void {
        this.method4();
    }
    
    method4(): void {
        this.method5();
    }
    
    method5(): void {
        this.counter++;
    }
    
    build() {
        Row() {}
    }
}
'''
        file_path = os.path.join(self.project_path, "chaos1", "ExtremelyLongNames.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.file_count += 1
        self.class_count += 2
        self.method_count += 8

    def generate_chaos_file_2(self):
        """生成混乱文件2: 循环依赖、递归调用"""
        content = '''
/**
 * 极度混乱的文件2 - 循环依赖、递归调用
 */
@Component
export struct CircularClassA {
    private value: number = 0;
    
    methodA(): void {
        console.log('A');
        CircularClassB.callB();
    }
    
    static callA(): void {
        console.log('Static A');
    }
    
    // 直接递归
    recursiveA(n: number): number {
        if (n <= 0) return 0;
        return n + this.recursiveA(n - 1);
    }
    
    build() {
        Column() {}
    }
}

@Component
export struct CircularClassB {
    private data: string = "";
    
    methodB(): void {
        console.log('B');
        CircularClassA.callA();
    }
    
    static callB(): void {
        console.log('Static B');
    }
    
    // 间接递归
    indirectRecursiveB(n: number): number {
        if (n <= 0) return 0;
        return n + this.recursiveHelper(n - 1);
    }
    
    recursiveHelper(n: number): number {
        if (n <= 0) return 0;
        return n + this.indirectRecursiveB(n - 1);
    }
    
    build() {
        Row() {}
    }
}

@Component
export struct CircularClassC {
    private list: number[] = [];
    
    methodC(): void {
        console.log('C');
    }
    
    build() {
        Stack() {}
    }
}
'''
        file_path = os.path.join(self.project_path, "chaos2", "CircularClasses.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.file_count += 1
        self.class_count += 3
        self.method_count += 9

    def generate_chaos_file_3(self):
        """生成混乱文件3: 大量注释、空行、空白字符"""
        content = '''
/**
 * 极度混乱的文件3
 *
 * 这个文件包含大量注释
 * 包含很多空行
 * 包含很多空白字符
 * 目的是测试解析器的鲁棒性
 */
 
 
 
 
 // 这是一些普通注释
 /* 这是一些块注释 */
 
 
 
/**
 * 更复杂的块注释
 * 包含多行内容
 * 甚至空行
 *
 */
 

 
 
 
 
 

@Component
export struct CommentHeavyClass {
    // 类注释
    // 更多注释
    // 更多更多注释
    
 
 
 
    private data: number = 42;
    
    // 方法注释
    methodWithLotsOfComments(): void {
        console.log('开始');
        
        // 中间注释
        
        this.someMethod();
        
        // 结束注释
        console.log('结束');
    }
    
    someMethod(): void {
        // 什么也不做
    }
    
    
 
 
    build() {
        Column() {
            Text('注释重的组件');
        }
    }
}
'''
        file_path = os.path.join(self.project_path, "chaos3", "CommentHeavy.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.file_count += 1
        self.class_count += 1
        self.method_count += 3

    def generate_chaos_file_4(self):
        """生成混乱文件4: 重复方法名、重载、各种签名"""
        content = '''
/**
 * 极度混乱的文件4 - 重复方法名、重载
 */
@Component
export struct OverloadedClass {
    private value: string = "";
    
    // 重复的方法名（不同参数）
    doSomething(): void {
        console.log('doSomething 0');
    }
    
    doSomething(x: number): void {
        console.log('doSomething 1: ' + x);
    }
    
    doSomething(x: number, y: number): void {
        console.log('doSomething 2: ' + x + ',' + y);
    }
    
    doSomething(s: string): void {
        console.log('doSomething str: ' + s);
    }
    
    doSomething(b: boolean): void {
        console.log('doSomething bool: ' + b);
    }
    
    // 更多方法
    anotherMethod(): void {
        this.doSomething();
        this.doSomething(42);
        this.doSomething(10, 20);
        this.doSomething('test');
        this.doSomething(true);
    }
    
    // 还有更多
    yetAnotherMethod(): void {
        console.log('又一个方法');
    }
    
    build() {
        Flex() {}
    }
}

// 另一个类
@Component
export struct AnotherOverloadedClass {
    private count: number = 0;
    
    func(): void {
        this.count++;
    }
    
    func(x: number): void {
        this.count += x;
    }
    
    build() {
        Grid() {}
    }
}
'''
        file_path = os.path.join(self.project_path, "chaos4", "OverloadedMethods.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.file_count += 1
        self.class_count += 2
        self.method_count += 11

    def generate_chaos_file_5(self):
        """生成混乱文件5: 极端格式、无空格、一行到底"""
        content = '''
/**
 * 极度混乱的文件5 - 极端格式
 */
@Component export struct NoSpaceClass { private a:number=0; private b:string=""; method():void{console.log('无空格');} build(){Column(){}}}
@Component export struct OneLineClass{private count:number=0;inc():void{this.count++;}dec():void{this.count--;}build(){Row(){}}}
@Component export struct NormalClass{private value:number=42;get():number{return this.value;}set(v:number):void{this.value=v;}build(){Stack(){}}}
'''
        file_path = os.path.join(self.project_path, "chaos5", "ExtremeFormat.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.file_count += 1
        self.class_count += 3
        self.method_count += 7

    def generate_chaos_file_6(self):
        """生成混乱文件6: 混合UI组件与业务逻辑"""
        content = '''
/**
 * 极度混乱的文件6 - 混合UI组件与业务逻辑
 */
import { UserService } from '../user/UserService.ets';

@Component
export struct MixedClass {
    @State count: number = 0;
    private data: number[] = [];
    
    // 业务逻辑方法
    fetchData(): Promise<void> {
        console.log('获取数据');
        return Promise.resolve();
    }
    
    processData(): number[] {
        console.log('处理数据');
        return this.data;
    }
    
    updateUI(): void {
        this.count++;
    }
    
    // 更多方法
    method1(): void {
        console.log('method1');
    }
    
    method2(): void {
        this.method1();
    }
    
    method3(): void {
        this.method2();
    }
    
    build() {
        Column() {
            Text('混合组件');
            Button('点击')
                .onClick(() => {
                    this.updateUI();
                });
            Text(this.count.toString());
            List() {
                ListItem() {
                    Text('项1');
                }
                ListItem() {
                    Text('项2');
                }
            }
        }
    }
}

@Component
export struct AnotherMixedClass {
    @State text: string = "";
    
    changeText(newText: string): void {
        this.text = newText;
    }
    
    reset(): void {
        this.text = "";
    }
    
    build() {
        Row() {
            TextInput()
                .onChange((value: string) => {
                    this.changeText(value);
                });
            Button('重置')
                .onClick(() => {
                    this.reset();
                });
        }
    }
}
'''
        file_path = os.path.join(self.project_path, "chaos6", "MixedUI.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.file_count += 1
        self.class_count += 2
        self.method_count += 8

    def generate_chaos_file_7(self):
        """生成混乱文件7: 空文件、只有注释的文件"""
        content1 = '''
// 这个文件只有注释
// 没有任何类或方法
// 只有注释
'''
        file_path1 = os.path.join(self.project_path, "chaos7", "OnlyComments.ets")
        os.makedirs(os.path.dirname(file_path1), exist_ok=True)
        with open(file_path1, 'w', encoding='utf-8') as f:
            f.write(content1)
        self.file_count += 1
        
        content2 = ''
        file_path2 = os.path.join(self.project_path, "chaos7", "EmptyFile.ets")
        with open(file_path2, 'w', encoding='utf-8') as f:
            f.write(content2)
        self.file_count += 1
        
        content3 = '''
// 几乎为空，只有一个空类
@Component
export struct EmptyClass {
    build() {
    }
}
'''
        file_path3 = os.path.join(self.project_path, "chaos7", "AlmostEmpty.ets")
        with open(file_path3, 'w', encoding='utf-8') as f:
            f.write(content3)
        self.file_count += 1
        self.class_count += 1
        self.method_count += 1

    def generate(self):
        """生成整个项目"""
        print("=" * 80)
        print("🎯 开始生成超混乱、超复杂的真实场景测试项目")
        print("=" * 80)
        
        self.generate_chaos_file_1()
        print("✅ 生成文件1: 超长方法名、超多层嵌套")
        
        self.generate_chaos_file_2()
        print("✅ 生成文件2: 循环依赖、递归调用")
        
        self.generate_chaos_file_3()
        print("✅ 生成文件3: 大量注释、空行、空白字符")
        
        self.generate_chaos_file_4()
        print("✅ 生成文件4: 重复方法名、重载")
        
        self.generate_chaos_file_5()
        print("✅ 生成文件5: 极端格式、无空格、一行到底")
        
        self.generate_chaos_file_6()
        print("✅ 生成文件6: 混合UI组件与业务逻辑")
        
        self.generate_chaos_file_7()
        print("✅ 生成文件7: 空文件、只有注释")
        
        print("\n" + "=" * 80)
        print("🎉 超混乱项目生成完成！")
        print("=" * 80)
        print(f"   文件数: {self.file_count}")
        print(f"   类数: {self.class_count}")
        print(f"   方法数: {self.method_count}")
        print("=" * 80)

if __name__ == "__main__":
    generator = ChaosUltimateProjectGenerator("/workspace/UltimateChaosProject")
    generator.generate()
