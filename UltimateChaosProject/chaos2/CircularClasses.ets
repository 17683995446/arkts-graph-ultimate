
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
