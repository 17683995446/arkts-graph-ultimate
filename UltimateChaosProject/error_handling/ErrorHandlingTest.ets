
@Component
export struct ErrorHandlingTest {
  // try-catch 嵌套
  nestedTryCatch(): void {
    try {
      try {
        this.riskyOperation1();
      } catch (e1) {
        try {
          this.recoveryOperation1();
        } catch (e2) {
          this.finalCleanup();
        }
      }
    } catch (e3) {
      this.handleCriticalError(e3);
    }
  }
  
  // 条件异常
  conditionalException(condition: boolean): void {
    if (condition) {
      throw new Error('Conditional error');
    }
  }
  
  // 异步错误处理
  async asyncErrorHandling(): Promise<void> {
    try {
      await this.asyncRiskyOperation();
    } catch (e) {
      await this.handleAsyncError(e);
    }
  }
  
  // 多个catch分支
  multiCatch(error: Error): void {
    try {
      this.uncertainOperation();
    } catch (e) {
      if (e instanceof TypeError) {
        this.handleTypeError(e);
      } else if (e instanceof ReferenceError) {
        this.handleReferenceError(e);
      } else if (e instanceof RangeError) {
        this.handleRangeError(e);
      } else {
        this.handleGenericError(e);
      }
    }
  }
  
  riskyOperation1(): void { console.log('risky operation 1'); }
  recoveryOperation1(): void { console.log('recovery operation 1'); }
  finalCleanup(): void { console.log('final cleanup'); }
  handleCriticalError(e: any): void { console.log('critical error:', e); }
  uncertainOperation(): void { console.log('uncertain operation'); }
  handleTypeError(e: any): void { console.log('type error:', e); }
  handleReferenceError(e: any): void { console.log('reference error:', e); }
  handleRangeError(e: any): void { console.log('range error:', e); }
  handleGenericError(e: any): void { console.log('generic error:', e); }
  asyncRiskyOperation(): Promise<void> { return Promise.resolve(); }
  async handleAsyncError(e: any): Promise<void> { console.log('async error:', e); }
  
  build() {
    Column() {
      Text('Error Handling Test')
    }
  }
}
