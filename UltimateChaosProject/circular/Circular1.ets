
@Component
export struct Circular1 {
  private data1: number = 1;
  
  method1A(): void {
    console.log('Circular1.method1A');
    // 调用同一个类的其他方法
    this.method1B();
    // 调用其他类的依赖
    Circular2.method2A();
  }
  
  method1B(): void {
    console.log('Circular1.method1B');
    this.method1C();
  }
  
  method1C(): void {
    console.log('Circular1.method1C');
    Circular2.method2B();
  }
  
  build() {
    Column() {
      Text('Circular 1')
    }
  }
}
