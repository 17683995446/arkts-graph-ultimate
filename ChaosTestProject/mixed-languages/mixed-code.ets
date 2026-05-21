export class Mixed {
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
