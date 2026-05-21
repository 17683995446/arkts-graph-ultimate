
@Component
export struct AsyncComplexTest {
  // Promise链式调用
  promiseChain(): Promise<number> {
    return this.operation1()
      .then(result1 => this.operation2(result1))
      .then(result2 => this.operation3(result2))
      .then(result3 => this.operation4(result3))
      .then(result4 => this.finalOperation(result4))
      .catch(error => this.handleError(error));
  }
  
  // async-await嵌套
  async nestedAsyncAwait(): Promise<void> {
    const result1 = await this.fetchData1();
    const result2 = await this.fetchData2();
    
    if (result2.status === 'success') {
      const result3 = await this.processData(result2);
      await this.saveData(result3);
    }
  }
  
  // 并行Promise
  async parallelPromises(): Promise<any[]> {
    const [data1, data2, data3] = await Promise.all([
      this.fetchData1(),
      this.fetchData2(),
      this.fetchData3()
    ]);
    return [data1, data2, data3];
  }
  
  // 竞态条件
  async raceCondition(): Promise<string> {
    const result = await Promise.race([
      this.timeout(1000),
      this.fetchData1(),
      this.fetchData2()
    ]);
    return result;
  }
  
  operation1(): Promise<number> { return Promise.resolve(1); }
  operation2(n: number): Promise<number> { return Promise.resolve(n + 1); }
  operation3(n: number): Promise<number> { return Promise.resolve(n + 2); }
  operation4(n: number): Promise<number> { return Promise.resolve(n + 3); }
  finalOperation(n: number): Promise<number> { return Promise.resolve(n + 4); }
  handleError(e: any): any { console.error(e); return null; }
  fetchData1(): Promise<any> { return Promise.resolve({}); }
  fetchData2(): Promise<any> { return Promise.resolve({}); }
  fetchData3(): Promise<any> { return Promise.resolve({}); }
  processData(data: any): Promise<any> { return Promise.resolve(data); }
  saveData(data: any): Promise<void> { return Promise.resolve(); }
  timeout(ms: number): Promise<void> { return new Promise(resolve => setTimeout(resolve, ms)); }
  
  build() {
    Column() {
      Text('Async Complex Test')
    }
  }
}
