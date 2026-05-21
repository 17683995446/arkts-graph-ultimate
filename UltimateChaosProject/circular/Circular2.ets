
@Component
export struct Circular2 {
  private data2: number = 2;
  
  method2A(): void {
    console.log('Circular2.method2A');
    // 调用同一个类的其他方法
    this.method2B();
    // 调用其他类的依赖
    Circular0.method0A();
  }
  
  method2B(): void {
    console.log('Circular2.method2B');
    this.method2C();
  }
  
  method2C(): void {
    console.log('Circular2.method2C');
    Circular0.method0B();
  }
  
  build() {
    Column() {
      Text('Circular 2')
    }
  }
}
