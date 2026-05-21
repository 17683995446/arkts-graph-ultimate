
@Component
export struct RecursiveTest {
  private depth: number = 0;
  private maxDepth: number = 100;
  
  // 直接递归
  recursiveMethodA(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodA(n - 1);
  }
  
  // 间接递归
  recursiveMethodB(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodC(n - 1);
  }
  
  recursiveMethodC(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodB(n - 1);
  }
  
  // 多路径递归
  recursiveMethodD(n: number): number {
    if (n <= 0) {
      return 0;
    }
    
    let result = n;
    
    // 多个递归路径
    if (n % 2 == 0) {
      result += this.recursiveMethodD(n / 2);
    } else {
      result += this.recursiveMethodD(n - 1);
      result += this.recursiveMethodE(n - 1);
    }
    
    return result;
  }
  
  recursiveMethodE(n: number): number {
    if (n <= 0) {
      return 0;
    }
    return n + this.recursiveMethodD(n - 1);
  }
  
  build() {
    Column() {
      Text('Recursive Test')
    }
  }
}
