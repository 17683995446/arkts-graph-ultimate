
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
