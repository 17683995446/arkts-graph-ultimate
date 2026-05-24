
/**
 * 复杂订单列表组件
 * 包含筛选、排序、分页、状态管理等复杂交互
 */
@Component
export struct ComplexOrderList {
  @State orders: Order[] = [];
  @State filteredOrders: Order[] = [];
  @State selectedOrders: Set<number> = new Set();
  @State currentPage: number = 1;
  @State pageSize: number = 10;
  @State totalPages: number = 0;
  @State isLoading: boolean = false;
  @State sortField: string = 'createTime';
  @State sortOrder: string = 'desc';
  @State filterStatus: string = 'all';
  @State searchKeyword: string = '';
  
  /**
   * 加载订单列表
   * 支持分页、筛选、排序的复杂查询
   */
  async loadOrders(): Promise<void> {
    console.log('ComplexOrderList.loadOrders called');
    
    this.isLoading = true;
    
    try {
      // 构建查询参数
      const queryParams = this.buildQueryParams();
      
      // 调用API获取订单
      const response = await this.fetchOrders(queryParams);
      
      // 处理响应数据
      this.orders = this.processOrderData(response.data);
      
      // 应用本地筛选
      this.applyLocalFilters();
      
      // 计算分页
      this.calculatePagination();
      
      // 更新UI
      this.updateUI();
      
    } catch (error) {
      this.handleLoadError(error);
    } finally {
      this.isLoading = false;
    }
  }
  
  /**
   * 应用筛选条件
   * 支持多条件组合筛选
   */
  applyFilters(): void {
    console.log('ComplexOrderList.applyFilters called');
    
    // 清空本地筛选结果
    this.filteredOrders = [];
    
    // 应用状态筛选
    if (this.filterStatus !== 'all') {
      this.filteredOrders = this.orders.filter(
        order => order.status === this.filterStatus
      );
    } else {
      this.filteredOrders = [...this.orders];
    }
    
    // 应用关键词筛选
    if (this.searchKeyword) {
      this.filteredOrders = this.filteredOrders.filter(
        order => this.matchSearchKeyword(order)
      );
    }
    
    // 应用排序
    this.applySorting();
    
    // 重新计算分页
    this.calculatePagination();
  }
  
  /**
   * 应用排序
   * 支持多字段排序
   */
  applySorting(): void {
    this.filteredOrders.sort((a, b) => {
      let comparison = 0;
      
      switch (this.sortField) {
        case 'createTime':
          comparison = new Date(a.createTime).getTime() - new Date(b.createTime).getTime();
          break;
        case 'amount':
          comparison = a.amount - b.amount;
          break;
        case 'status':
          comparison = a.status.localeCompare(b.status);
          break;
      }
      
      return this.sortOrder === 'desc' ? -comparison : comparison;
    });
  }
  
  /**
   * 处理分页
   * 复杂的分页逻辑
   */
  calculatePagination(): void {
    const totalOrders = this.filteredOrders.length;
    this.totalPages = Math.ceil(totalOrders / this.pageSize);
    
    if (this.currentPage > this.totalPages) {
      this.currentPage = this.totalPages || 1;
    }
  }
  
  /**
   * 获取当前页数据
   */
  getCurrentPageData(): Order[] {
    const startIndex = (this.currentPage - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    
    return this.filteredOrders.slice(startIndex, endIndex);
  }
  
  /**
   * 切换页码
   */
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.updateUI();
    }
  }
  
  /**
   * 切换排序
   */
  toggleSort(field: string): void {
    if (this.sortField === field) {
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortOrder = 'desc';
    }
    
    this.applySorting();
    this.updateUI();
  }
  
  /**
   * 切换订单选择
   */
  toggleOrderSelection(orderId: number): void {
    if (this.selectedOrders.has(orderId)) {
      this.selectedOrders.delete(orderId);
    } else {
      this.selectedOrders.add(orderId);
    }
  }
  
  /**
   * 全选/取消全选
   */
  toggleSelectAll(): void {
    const currentPageOrders = this.getCurrentPageData();
    
    if (this.selectedOrders.size === currentPageOrders.length) {
      this.selectedOrders.clear();
    } else {
      currentPageOrders.forEach(order => {
        this.selectedOrders.add(order.id);
      });
    }
  }
  
  /**
   * 批量操作
   * 复杂的批量操作处理
   */
  async batchOperation(operation: string): Promise<void> {
    if (this.selectedOrders.size === 0) {
      this.showToast('Please select orders first');
      return;
    }
    
    const selectedIds = Array.from(this.selectedOrders);
    
    switch (operation) {
      case 'export':
        await this.exportOrders(selectedIds);
        break;
      case 'cancel':
        await this.batchCancelOrders(selectedIds);
        break;
      case 'print':
        await this.batchPrintOrders(selectedIds);
        break;
      case 'merge':
        await this.batchMergeOrders(selectedIds);
        break;
    }
    
    // 清空选择
    this.selectedOrders.clear();
    
    // 重新加载数据
    await this.loadOrders();
  }
  
  // 辅助方法
  buildQueryParams(): any {
    return {
      page: this.currentPage,
      pageSize: this.pageSize,
      sortField: this.sortField,
      sortOrder: this.sortOrder,
      status: this.filterStatus === 'all' ? null : this.filterStatus,
      keyword: this.searchKeyword || null
    };
  }
  
  async fetchOrders(params: any): Promise<any> {
    return { data: [], total: 0 };
  }
  
  processOrderData(data: any[]): Order[] {
    return data;
  }
  
  applyLocalFilters(): void {
    this.filteredOrders = [...this.orders];
  }
  
  updateUI(): void {
    console.log('UI updated');
  }
  
  handleLoadError(error: any): void {
    console.error('Load error:', error);
    this.showToast('Failed to load orders');
  }
  
  matchSearchKeyword(order: Order): boolean {
    const keyword = this.searchKeyword.toLowerCase();
    return (
      order.orderNo.toLowerCase().includes(keyword) ||
      order.customerName.toLowerCase().includes(keyword) ||
      order.productName.toLowerCase().includes(keyword)
    );
  }
  
  showToast(message: string): void {
    console.log('Toast:', message);
  }
  
  async exportOrders(orderIds: number[]): Promise<void> {
    console.log('Exporting orders:', orderIds);
  }
  
  async batchCancelOrders(orderIds: number[]): Promise<void> {
    console.log('Cancelling orders:', orderIds);
  }
  
  async batchPrintOrders(orderIds: number[]): Promise<void> {
    console.log('Printing orders:', orderIds);
  }
  
  async batchMergeOrders(orderIds: number[]): Promise<void> {
    console.log('Merging orders:', orderIds);
  }
  
  build() {
    Column() {
      // 筛选栏
      Row() {
        Text('Search')
        Text('Filter')
        Text('Sort')
      }
      
      // 列表
      List() {
        ForEach(this.getCurrentPageData(), (order: Order) => {
          ListItem() {
            Row() {
              Checkbox()
              Text(order.orderNo)
              Text(order.status)
              Text(order.amount.toString())
            }
          }
          .onClick(() => this.toggleOrderSelection(order.id))
        })
      }
      
      // 分页
      Row() {
        Button('Previous')
          .onClick(() => this.goToPage(this.currentPage - 1))
        
        Text(`${this.currentPage}/${this.totalPages}`)
        
        Button('Next')
          .onClick(() => this.goToPage(this.currentPage + 1))
      }
      
      // 批量操作
      Row() {
        Button('Export')
        Button('Cancel')
        Button('Print')
      }
    }
  }
}
