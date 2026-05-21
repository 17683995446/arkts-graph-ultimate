
@Component
export struct Circular0 {
  private data0: number = 0;
  
  method0A(): void {
    console.log('Circular0.method0A');
    // 调用同一个类的其他方法
    this.method0B();
    // 调用其他类的依赖
    Circular1.method1A();
  }
  
  method0B(): void {
    console.log('Circular0.method0B');
    this.method0C();
  }
  
  method0C(): void {
    console.log('Circular0.method0C');
    Circular1.method1B();
  }
  
  build() {
    Column() {
      Text('Circular 0')
    }
  }
}
