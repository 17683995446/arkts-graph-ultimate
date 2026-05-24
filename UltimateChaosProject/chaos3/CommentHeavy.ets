
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
