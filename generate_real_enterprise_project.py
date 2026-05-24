#!/usr/bin/env python3
"""
真实企业级复杂场景测试项目生成器
模拟真实的企业级应用场景，包含真实的业务逻辑和复杂依赖关系
"""

import os
import random
import string
from datetime import datetime

class RealEnterpriseProjectGenerator:
    def __init__(self, project_path):
        self.project_path = project_path
        self.file_count = 0
        self.class_count = 0
        self.method_count = 0
        self.call_count = 0
        self.complexity_level = "ENTERPRISE"
        
    def generate_random_name(self, prefix="Entity"):
        """生成随机但有意义的名称"""
        suffixes = {
            "Entity": ["User", "Order", "Product", "Payment", "Inventory", "Shipping", "Customer", "Review", "Cart"],
            "Service": ["UserService", "OrderService", "PaymentService", "InventoryService", "ShippingService", "AuthService"],
            "Manager": ["SessionManager", "CacheManager", "ConfigManager", "LogManager", "MetricManager"],
            "Handler": ["RequestHandler", "ResponseHandler", "ErrorHandler", "ValidationHandler"],
            "Repository": ["UserRepository", "OrderRepository", "ProductRepository", "PaymentRepository"],
            "Controller": ["UserController", "OrderController", "ProductController", "AdminController"],
            "Component": ["Header", "Footer", "Sidebar", "Modal", "Card", "Form", "List", "Grid"],
        }
        
        if prefix in suffixes:
            return random.choice(suffixes[prefix])
        else:
            return f"{prefix}_{random.randint(1, 1000)}"
    
    def generate_user_module(self):
        """生成用户管理模块"""
        print(f"  📦 生成用户管理模块...")
        
        content = """
/**
 * 用户管理模块
 * 负责用户注册、登录、权限管理、会话管理等核心功能
 */
import router from '@system.router';
import fetch from '@system.fetch';

@Component
export struct UserService {
  // 用户会话管理
  private sessionId: string = '';
  private userId: number = 0;
  private permissions: string[] = [];
  
  /**
   * 用户登录
   * 包含：参数验证、API调用、会话管理、权限加载、错误处理
   */
  async login(username: string, password: string): Promise<boolean> {
    console.log('UserService.login called');
    
    // 参数验证
    if (!this.validateCredentials(username, password)) {
      console.error('Invalid credentials');
      return false;
    }
    
    // 尝试登录
    try {
      const response = await this.callLoginAPI(username, password);
      
      if (response.code === 200) {
        this.sessionId = response.data.sessionId;
        this.userId = response.data.userId;
        
        // 加载用户权限
        await this.loadUserPermissions();
        
        // 更新会话状态
        await this.updateSessionState();
        
        // 记录登录日志
        this.logUserLogin();
        
        return true;
      } else {
        this.handleLoginError(response.code);
        return false;
      }
    } catch (error) {
      this.handleException(error);
      return false;
    }
  }
  
  /**
   * 用户注册
   * 包含：数据验证、密码加密、API调用、邮件验证、异常处理
   */
  async register(userData: object): Promise<number> {
    console.log('UserService.register called');
    
    // 验证数据完整性
    if (!this.validateUserData(userData)) {
      throw new Error('Invalid user data');
    }
    
    // 加密密码
    const encryptedPassword = this.encryptPassword(userData.password);
    userData.password = encryptedPassword;
    
    // 检查用户名唯一性
    const isUnique = await this.checkUsernameUniqueness(userData.username);
    if (!isUnique) {
      throw new Error('Username already exists');
    }
    
    // 检查邮箱唯一性
    const emailUnique = await this.checkEmailUniqueness(userData.email);
    if (!emailUnique) {
      throw new Error('Email already exists');
    }
    
    try {
      // 创建用户
      const userId = await this.createUser(userData);
      
      // 发送验证邮件
      await this.sendVerificationEmail(userData.email);
      
      // 初始化用户配置
      await this.initializeUserConfig(userId);
      
      // 记录注册日志
      this.logUserRegistration(userId);
      
      return userId;
    } catch (error) {
      this.handleRegistrationError(error);
      throw error;
    }
  }
  
  /**
   * 加载用户权限
   * 复杂的权限树结构和继承关系
   */
  async loadUserPermissions(): Promise<void> {
    try {
      const permissionData = await this.fetchPermissions();
      
      // 处理权限继承
      this.permissions = this.processPermissionTree(permissionData);
      
      // 缓存权限
      await this.cachePermissions();
      
      // 验证权限
      this.validatePermissions();
    } catch (error) {
      this.handlePermissionError(error);
    }
  }
  
  /**
   * 处理权限树
   * 复杂的树形结构和递归处理
   */
  processPermissionTree(permissionData: any[]): string[] {
    const permissions = [];
    
    for (const node of permissionData) {
      permissions.push(node.code);
      
      // 处理子权限（递归）
      if (node.children && node.children.length > 0) {
        const childPermissions = this.processPermissionTree(node.children);
        permissions.push(...childPermissions);
      }
      
      // 处理继承权限
      if (node.inherited && node.inherited.length > 0) {
        permissions.push(...node.inherited);
      }
    }
    
    return [...new Set(permissions)]; // 去重
  }
  
  // 辅助方法
  validateCredentials(username: string, password: string): boolean {
    return username.length >= 3 && password.length >= 6;
  }
  
  async callLoginAPI(username: string, password: string): Promise<any> {
    return { code: 200, data: { sessionId: '123', userId: 1 } };
  }
  
  async updateSessionState(): Promise<void> {
    console.log('Session state updated');
  }
  
  logUserLogin(): void {
    console.log('User logged in at', new Date());
  }
  
  handleLoginError(code: number): void {
    console.error('Login error:', code);
  }
  
  validateUserData(userData: any): boolean {
    return userData.username && userData.password && userData.email;
  }
  
  encryptPassword(password: string): string {
    return password.split('').reverse().join('');
  }
  
  async checkUsernameUniqueness(username: string): Promise<boolean> {
    return true;
  }
  
  async checkEmailUniqueness(email: string): Promise<boolean> {
    return true;
  }
  
  async createUser(userData: any): Promise<number> {
    return 1;
  }
  
  async sendVerificationEmail(email: string): Promise<void> {
    console.log('Verification email sent to', email);
  }
  
  async initializeUserConfig(userId: number): Promise<void> {
    console.log('User config initialized for', userId);
  }
  
  logUserRegistration(userId: number): void {
    console.log('User registered:', userId);
  }
  
  handleRegistrationError(error: any): void {
    console.error('Registration error:', error);
  }
  
  async fetchPermissions(): Promise<any[]> {
    return [];
  }
  
  async cachePermissions(): Promise<void> {
    console.log('Permissions cached');
  }
  
  validatePermissions(): void {
    console.log('Permissions validated');
  }
  
  handlePermissionError(error: any): void {
    console.error('Permission error:', error);
  }
  
  handleException(error: any): void {
    console.error('Exception:', error);
  }
  
  build() {
    Column() {
      Text('User Service')
    }
  }
}
"""
        
        file_path = os.path.join(self.project_path, "user", "UserService.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 10
        self.call_count += 25

    def generate_order_module(self):
        """生成订单管理模块"""
        print(f"  📦 生成订单管理模块...")
        
        content = """
/**
 * 订单管理模块
 * 负责订单创建、支付、取消、退款等完整流程
 */
@Component
export struct OrderService {
  private orderId: number = 0;
  private orderStatus: string = 'pending';
  private paymentStatus: string = 'unpaid';
  
  /**
   * 创建订单
   * 复杂的业务流程：库存检查、价格计算、促销应用、订单验证
   */
  async createOrder(orderData: object): Promise<number> {
    console.log('OrderService.createOrder called');
    
    // 1. 验证订单数据
    this.validateOrderData(orderData);
    
    // 2. 检查商品库存
    const inventoryCheck = await this.checkInventory(orderData.items);
    if (!inventoryCheck.available) {
      throw new Error('Insufficient inventory');
    }
    
    // 3. 计算订单价格
    const priceCalculation = await this.calculateOrderPrice(orderData);
    
    // 4. 应用促销活动
    const promotionalDiscount = await this.applyPromotions(
      priceCalculation.subtotal,
      orderData.promotionCodes
    );
    
    // 5. 计算最终价格
    const finalPrice = priceCalculation.subtotal - promotionalDiscount;
    
    // 6. 验证价格
    this.validateFinalPrice(finalPrice, orderData.expectedPrice);
    
    // 7. 创建订单记录
    const orderId = await this.saveOrder(orderData, {
      subtotal: priceCalculation.subtotal,
      discount: promotionalDiscount,
      finalPrice: finalPrice
    });
    
    // 8. 锁定库存
    await this.lockInventory(orderData.items);
    
    // 9. 发送订单通知
    await this.sendOrderNotification(orderId);
    
    // 10. 记录订单日志
    this.logOrderCreation(orderId);
    
    return orderId;
  }
  
  /**
   * 订单支付
   * 复杂的支付流程：支付方式选择、支付验证、第三方支付集成
   */
  async processPayment(orderId: number, paymentMethod: string): Promise<boolean> {
    console.log('OrderService.processPayment called');
    
    // 获取订单信息
    const order = await this.getOrderById(orderId);
    
    // 验证订单状态
    if (!this.isOrderPayable(order)) {
      throw new Error('Order cannot be paid');
    }
    
    // 验证支付方式
    this.validatePaymentMethod(paymentMethod);
    
    // 准备支付参数
    const paymentParams = await this.preparePaymentParams(order, paymentMethod);
    
    // 调用支付网关
    const paymentResult = await this.callPaymentGateway(paymentParams);
    
    // 处理支付结果
    if (paymentResult.success) {
      // 更新订单支付状态
      await this.updatePaymentStatus(orderId, 'paid');
      
      // 更新订单状态
      await this.updateOrderStatus(orderId, 'paid');
      
      // 释放库存（如果需要）
      await this.releaseInventory(orderId);
      
      // 发送支付成功通知
      await this.sendPaymentNotification(orderId);
      
      // 记录支付日志
      this.logPayment(orderId, paymentMethod);
      
      return true;
    } else {
      // 处理支付失败
      await this.handlePaymentFailure(orderId, paymentResult.error);
      return false;
    }
  }
  
  /**
   * 订单取消
   * 复杂的取消逻辑：状态检查、库存释放、退款处理
   */
  async cancelOrder(orderId: number, reason: string): Promise<boolean> {
    console.log('OrderService.cancelOrder called');
    
    const order = await this.getOrderById(orderId);
    
    // 检查是否可以取消
    if (!this.canCancelOrder(order)) {
      throw new Error('Order cannot be cancelled');
    }
    
    // 根据订单状态处理
    if (order.paymentStatus === 'paid') {
      // 已支付订单，需要退款
      await this.processRefund(orderId);
    }
    
    // 释放库存
    await this.releaseInventory(orderId);
    
    // 更新订单状态
    await this.updateOrderStatus(orderId, 'cancelled');
    
    // 发送取消通知
    await this.sendCancelNotification(orderId, reason);
    
    // 记录取消日志
    this.logOrderCancellation(orderId, reason);
    
    return true;
  }
  
  /**
   * 订单退款
   * 复杂的退款逻辑：退款验证、退款计算、退款处理
   */
  async processRefund(orderId: number): Promise<void> {
    const order = await this.getOrderById(orderId);
    
    // 计算退款金额
    const refundAmount = this.calculateRefundAmount(order);
    
    // 验证退款金额
    this.validateRefundAmount(refundAmount);
    
    // 发起退款
    const refundResult = await this.callRefundAPI(orderId, refundAmount);
    
    if (refundResult.success) {
      // 更新退款状态
      await this.updateRefundStatus(orderId, 'refunded');
      
      // 发送退款通知
      await this.sendRefundNotification(orderId, refundAmount);
      
      // 记录退款日志
      this.logRefund(orderId, refundAmount);
    } else {
      throw new Error('Refund failed');
    }
  }
  
  // 辅助方法
  validateOrderData(orderData: any): void {
    console.log('Validating order data');
  }
  
  async checkInventory(items: any[]): Promise<any> {
    return { available: true };
  }
  
  async calculateOrderPrice(orderData: any): Promise<any> {
    return { subtotal: 100 };
  }
  
  async applyPromotions(subtotal: number, codes: string[]): Promise<number> {
    return 0;
  }
  
  validateFinalPrice(finalPrice: number, expectedPrice: number): void {
    if (Math.abs(finalPrice - expectedPrice) > 0.01) {
      throw new Error('Price mismatch');
    }
  }
  
  async saveOrder(orderData: any, priceInfo: any): Promise<number> {
    return 1;
  }
  
  async lockInventory(items: any[]): Promise<void> {
    console.log('Inventory locked');
  }
  
  async sendOrderNotification(orderId: number): Promise<void> {
    console.log('Order notification sent');
  }
  
  logOrderCreation(orderId: number): void {
    console.log('Order created:', orderId);
  }
  
  async getOrderById(orderId: number): Promise<any> {
    return { orderId, paymentStatus: 'unpaid' };
  }
  
  isOrderPayable(order: any): boolean {
    return order.paymentStatus === 'unpaid';
  }
  
  validatePaymentMethod(method: string): void {
    if (!['alipay', 'wechat', 'card'].includes(method)) {
      throw new Error('Invalid payment method');
    }
  }
  
  async preparePaymentParams(order: any, method: string): Promise<any> {
    return { orderId: order.orderId, method };
  }
  
  async callPaymentGateway(params: any): Promise<any> {
    return { success: true };
  }
  
  async updatePaymentStatus(orderId: number, status: string): Promise<void> {
    console.log('Payment status updated');
  }
  
  async updateOrderStatus(orderId: number, status: string): Promise<void> {
    console.log('Order status updated');
  }
  
  async releaseInventory(orderId: number): Promise<void> {
    console.log('Inventory released');
  }
  
  async sendPaymentNotification(orderId: number): Promise<void> {
    console.log('Payment notification sent');
  }
  
  logPayment(orderId: number, method: string): void {
    console.log('Payment processed');
  }
  
  async handlePaymentFailure(orderId: number, error: any): Promise<void> {
    console.error('Payment failed:', error);
  }
  
  canCancelOrder(order: any): boolean {
    return order.status !== 'shipped' && order.status !== 'completed';
  }
  
  async sendCancelNotification(orderId: number, reason: string): Promise<void> {
    console.log('Cancel notification sent');
  }
  
  logOrderCancellation(orderId: number, reason: string): void {
    console.log('Order cancelled:', orderId);
  }
  
  calculateRefundAmount(order: any): number {
    return order.amount;
  }
  
  validateRefundAmount(amount: number): void {
    if (amount <= 0) {
      throw new Error('Invalid refund amount');
    }
  }
  
  async callRefundAPI(orderId: number, amount: number): Promise<any> {
    return { success: true };
  }
  
  async updateRefundStatus(orderId: number, status: string): Promise<void> {
    console.log('Refund status updated');
  }
  
  async sendRefundNotification(orderId: number, amount: number): Promise<void> {
    console.log('Refund notification sent');
  }
  
  logRefund(orderId: number, amount: number): void {
    console.log('Refund processed');
  }
  
  build() {
    Column() {
      Text('Order Service')
    }
  }
}
"""
        
        file_path = os.path.join(self.project_path, "order", "OrderService.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 8
        self.call_count += 35

    def generate_inventory_module(self):
        """生成库存管理模块"""
        print(f"  📦 生成库存管理模块...")
        
        content = """
/**
 * 库存管理模块
 * 负责库存跟踪、预警、补货等复杂逻辑
 */
@Component
export struct InventoryService {
  private inventory: Map<number, number> = new Map();
  private threshold: number = 10;
  
  /**
   * 库存检查
   * 多仓库库存计算和分配
   */
  async checkInventory(productId: number, quantity: number): Promise<InventoryCheckResult> {
    console.log('InventoryService.checkInventory called');
    
    // 获取各仓库库存
    const warehouseInventory = await this.getWarehouseInventory(productId);
    
    // 计算总库存
    const totalInventory = this.calculateTotalInventory(warehouseInventory);
    
    // 检查库存是否足够
    const available = totalInventory >= quantity;
    
    // 计算可分配库存
    const allocatedQuantity = this.allocateInventory(warehouseInventory, quantity);
    
    // 检查是否需要补货
    const needRestock = this.checkRestockRequirement(totalInventory);
    
    return {
      available,
      totalInventory,
      allocatedQuantity,
      needRestock
    };
  }
  
  /**
   * 锁定库存
   * 用于订单创建时的库存预留
   */
  async lockInventory(productId: number, quantity: number, orderId: number): Promise<boolean> {
    console.log('InventoryService.lockInventory called');
    
    // 检查库存
    const checkResult = await this.checkInventory(productId, quantity);
    
    if (!checkResult.available) {
      return false;
    }
    
    // 锁定库存
    await this.performInventoryLock(productId, quantity);
    
    // 创建库存锁定记录
    await this.createLockRecord(productId, quantity, orderId);
    
    // 发送库存变动通知
    await this.sendInventoryNotification(productId, 'locked', quantity);
    
    return true;
  }
  
  /**
   * 释放库存
   * 订单取消时释放已锁定的库存
   */
  async releaseInventory(productId: number, quantity: number, orderId: number): Promise<void> {
    console.log('InventoryService.releaseInventory called');
    
    // 获取锁定记录
    const lockRecord = await this.getLockRecord(productId, orderId);
    
    if (lockRecord) {
      // 释放库存
      await this.performInventoryRelease(productId, quantity);
      
      // 删除锁定记录
      await this.deleteLockRecord(productId, orderId);
      
      // 发送通知
      await this.sendInventoryNotification(productId, 'released', quantity);
      
      // 记录日志
      this.logInventoryRelease(productId, quantity, orderId);
    }
  }
  
  /**
   * 库存预警
   * 检查低库存商品并发送预警
   */
  async checkLowStock(): Promise<void> {
    console.log('InventoryService.checkLowStock called');
    
    // 获取所有低库存商品
    const lowStockProducts = await this.getLowStockProducts();
    
    for (const product of lowStockProducts) {
      // 计算建议补货量
      const suggestedQuantity = this.calculateRestockQuantity(product);
      
      // 发送预警通知
      await this.sendLowStockAlert(product, suggestedQuantity);
      
      // 创建补货建议
      await this.createRestockSuggestion(product, suggestedQuantity);
      
      // 记录预警
      this.logLowStockAlert(product.productId);
    }
  }
  
  /**
   * 库存同步
   * 多系统间的库存数据同步
   */
  async syncInventory(productId: number): Promise<void> {
    console.log('InventoryService.syncInventory called');
    
    // 从各系统获取库存数据
    const [erpInventory, wmsInventory, onlineInventory] = await Promise.all([
      this.getERPInventory(productId),
      this.getWMSInventory(productId),
      this.getOnlineInventory(productId)
    ]);
    
    // 检测不一致
    const inconsistencies = this.detectInconsistencies(
      erpInventory,
      wmsInventory,
      onlineInventory
    );
    
    if (inconsistencies.length > 0) {
      // 处理不一致
      await this.handleInconsistencies(inconsistencies);
      
      // 记录同步日志
      this.logInventorySync(productId, inconsistencies);
    }
  }
  
  // 辅助方法
  async getWarehouseInventory(productId: number): Promise<any[]> {
    return [];
  }
  
  calculateTotalInventory(warehouseInventory: any[]): number {
    return warehouseInventory.reduce((sum, w) => sum + w.quantity, 0);
  }
  
  allocateInventory(warehouseInventory: any[], quantity: number): number {
    return Math.min(quantity, this.calculateTotalInventory(warehouseInventory));
  }
  
  checkRestockRequirement(totalInventory: number): boolean {
    return totalInventory < this.threshold;
  }
  
  async performInventoryLock(productId: number, quantity: number): Promise<void> {
    console.log('Inventory locked');
  }
  
  async createLockRecord(productId: number, quantity: number, orderId: number): Promise<void> {
    console.log('Lock record created');
  }
  
  async sendInventoryNotification(productId: number, type: string, quantity: number): Promise<void> {
    console.log('Notification sent');
  }
  
  async getLockRecord(productId: number, orderId: number): Promise<any> {
    return { productId, orderId };
  }
  
  async performInventoryRelease(productId: number, quantity: number): Promise<void> {
    console.log('Inventory released');
  }
  
  async deleteLockRecord(productId: number, orderId: number): Promise<void> {
    console.log('Lock record deleted');
  }
  
  logInventoryRelease(productId: number, quantity: number, orderId: number): void {
    console.log('Inventory released');
  }
  
  async getLowStockProducts(): Promise<any[]> {
    return [];
  }
  
  calculateRestockQuantity(product: any): number {
    return product.threshold - product.currentStock;
  }
  
  async sendLowStockAlert(product: any, suggestedQuantity: number): Promise<void> {
    console.log('Low stock alert sent');
  }
  
  async createRestockSuggestion(product: any, suggestedQuantity: number): Promise<void> {
    console.log('Restock suggestion created');
  }
  
  logLowStockAlert(productId: number): void {
    console.log('Low stock alert logged');
  }
  
  async getERPInventory(productId: number): Promise<number> {
    return 100;
  }
  
  async getWMSInventory(productId: number): Promise<number> {
    return 100;
  }
  
  async getOnlineInventory(productId: number): Promise<number> {
    return 100;
  }
  
  detectInconsistencies(erp: number, wms: number, online: number): any[] {
    if (erp !== wms || wms !== online) {
      return [{ erp, wms, online }];
    }
    return [];
  }
  
  async handleInconsistencies(inconsistencies: any[]): Promise<void> {
    console.log('Inconsistencies handled');
  }
  
  logInventorySync(productId: number, inconsistencies: any[]): void {
    console.log('Inventory synced');
  }
  
  build() {
    Column() {
      Text('Inventory Service')
    }
  }
}
"""
        
        file_path = os.path.join(self.project_path, "inventory", "InventoryService.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 8
        self.call_count += 30

    def generate_payment_module(self):
        """生成支付模块"""
        print(f"  📦 生成支付模块...")
        
        content = """
/**
 * 支付服务模块
 * 集成多种支付方式，处理复杂的支付逻辑
 */
@Component
export struct PaymentService {
  private paymentChannels: Map<string, any> = new Map();
  
  /**
   * 发起支付
   * 支持多种支付渠道的复杂支付流程
   */
  async initiatePayment(paymentRequest: PaymentRequest): Promise<PaymentResult> {
    console.log('PaymentService.initiatePayment called');
    
    // 验证支付请求
    this.validatePaymentRequest(paymentRequest);
    
    // 获取支付渠道
    const channel = this.getPaymentChannel(paymentRequest.channel);
    
    // 构建支付参数
    const paymentParams = await this.buildPaymentParams(paymentRequest, channel);
    
    // 调用支付渠道
    const paymentResponse = await this.callPaymentChannel(channel, paymentParams);
    
    // 处理支付响应
    if (paymentResponse.success) {
      // 创建支付记录
      const paymentRecord = await this.createPaymentRecord(paymentRequest, paymentResponse);
      
      // 发送支付通知
      await this.sendPaymentNotification(paymentRecord);
      
      return {
        success: true,
        paymentId: paymentRecord.id,
        paymentUrl: paymentResponse.payUrl
      };
    } else {
      // 处理支付失败
      await this.handlePaymentFailure(paymentRequest, paymentResponse.error);
      
      return {
        success: false,
        error: paymentResponse.error
      };
    }
  }
  
  /**
   * 支付回调处理
   * 处理第三方支付的异步回调
   */
  async handlePaymentCallback(callbackData: any): Promise<void> {
    console.log('PaymentService.handlePaymentCallback called');
    
    // 验证回调签名
    const isValid = await this.verifyCallbackSignature(callbackData);
    
    if (!isValid) {
      throw new Error('Invalid callback signature');
    }
    
    // 解析回调数据
    const paymentResult = this.parseCallbackData(callbackData);
    
    // 查询原支付记录
    const paymentRecord = await this.getPaymentRecord(paymentResult.paymentId);
    
    // 根据支付结果处理
    if (paymentResult.status === 'success') {
      // 更新支付状态
      await this.updatePaymentStatus(paymentRecord.id, 'success');
      
      // 触发支付成功事件
      await this.triggerPaymentSuccessEvent(paymentRecord);
      
      // 发送支付成功通知
      await this.sendPaymentSuccessNotification(paymentRecord);
      
    } else if (paymentResult.status === 'failed') {
      // 更新支付状态
      await this.updatePaymentStatus(paymentRecord.id, 'failed');
      
      // 触发支付失败事件
      await this.triggerPaymentFailureEvent(paymentRecord);
      
    } else if (paymentResult.status === 'pending') {
      // 更新支付状态
      await this.updatePaymentStatus(paymentRecord.id, 'pending');
    }
    
    // 记录回调日志
    this.logPaymentCallback(paymentResult);
  }
  
  /**
   * 申请退款
   * 复杂的退款逻辑和审核流程
   */
  async applyRefund(refundRequest: RefundRequest): Promise<RefundResult> {
    console.log('PaymentService.applyRefund called');
    
    // 验证退款申请
    this.validateRefundRequest(refundRequest);
    
    // 查询原支付记录
    const paymentRecord = await this.getPaymentRecord(refundRequest.paymentId);
    
    // 计算可退款金额
    const refundableAmount = this.calculateRefundableAmount(paymentRecord);
    
    // 验证退款金额
    if (refundRequest.amount > refundableAmount) {
      throw new Error('Refund amount exceeds limit');
    }
    
    // 根据退款金额判断是否需要审核
    const needApproval = this.checkRefundApprovalRequirement(refundRequest.amount);
    
    if (needApproval) {
      // 创建退款审核任务
      const approvalTask = await this.createRefundApprovalTask(refundRequest);
      
      return {
        success: true,
        status: 'pending_approval',
        approvalTaskId: approvalTask.id
      };
    } else {
      // 直接处理退款
      const refundResult = await this.processRefund(refundRequest);
      
      return refundResult;
    }
  }
  
  /**
   * 处理退款
   * 调用支付渠道进行退款
   */
  async processRefund(refundRequest: RefundRequest): Promise<RefundResult> {
    // 获取原支付渠道
    const channel = this.getPaymentChannel(refundRequest.channel);
    
    // 构建退款参数
    const refundParams = await this.buildRefundParams(refundRequest, channel);
    
    // 调用退款接口
    const refundResponse = await this.callRefundChannel(channel, refundParams);
    
    if (refundResponse.success) {
      // 创建退款记录
      const refundRecord = await this.createRefundRecord(refundRequest, refundResponse);
      
      // 更新原支付记录
      await this.updatePaymentRefundStatus(refundRequest.paymentId, refundRecord.amount);
      
      // 发送退款通知
      await this.sendRefundNotification(refundRecord);
      
      return {
        success: true,
        status: 'success',
        refundId: refundRecord.id
      };
    } else {
      return {
        success: false,
        status: 'failed',
        error: refundResponse.error
      };
    }
  }
  
  // 辅助方法
  validatePaymentRequest(request: PaymentRequest): void {
    if (!request.orderId || !request.amount || !request.channel) {
      throw new Error('Invalid payment request');
    }
  }
  
  getPaymentChannel(channel: string): any {
    return { name: channel };
  }
  
  async buildPaymentParams(request: PaymentRequest, channel: any): Promise<any> {
    return { ...request, channel: channel.name };
  }
  
  async callPaymentChannel(channel: any, params: any): Promise<any> {
    return { success: true, payUrl: 'https://pay.example.com' };
  }
  
  async createPaymentRecord(request: PaymentRequest, response: any): Promise<any> {
    return { id: 1, ...request };
  }
  
  async sendPaymentNotification(record: any): Promise<void> {
    console.log('Payment notification sent');
  }
  
  async handlePaymentFailure(request: PaymentRequest, error: any): Promise<void> {
    console.error('Payment failure:', error);
  }
  
  async verifyCallbackSignature(callbackData: any): Promise<boolean> {
    return true;
  }
  
  parseCallbackData(callbackData: any): any {
    return callbackData;
  }
  
  async getPaymentRecord(paymentId: number): Promise<any> {
    return { id: paymentId, amount: 100 };
  }
  
  async updatePaymentStatus(paymentId: number, status: string): Promise<void> {
    console.log('Payment status updated');
  }
  
  async triggerPaymentSuccessEvent(paymentRecord: any): Promise<void> {
    console.log('Payment success event triggered');
  }
  
  async sendPaymentSuccessNotification(paymentRecord: any): Promise<void> {
    console.log('Success notification sent');
  }
  
  async triggerPaymentFailureEvent(paymentRecord: any): Promise<void> {
    console.log('Payment failure event triggered');
  }
  
  logPaymentCallback(result: any): void {
    console.log('Payment callback logged');
  }
  
  validateRefundRequest(request: RefundRequest): void {
    if (!request.paymentId || !request.amount) {
      throw new Error('Invalid refund request');
    }
  }
  
  calculateRefundableAmount(paymentRecord: any): number {
    return paymentRecord.amount;
  }
  
  checkRefundApprovalRequirement(amount: number): boolean {
    return amount > 1000; // 超过1000需要审核
  }
  
  async createRefundApprovalTask(request: RefundRequest): Promise<any> {
    return { id: 1 };
  }
  
  async buildRefundParams(request: RefundRequest, channel: any): Promise<any> {
    return { ...request, channel: channel.name };
  }
  
  async callRefundChannel(channel: any, params: any): Promise<any> {
    return { success: true };
  }
  
  async createRefundRecord(request: RefundRequest, response: any): Promise<any> {
    return { id: 1, ...request };
  }
  
  async updatePaymentRefundStatus(paymentId: number, refundAmount: number): Promise<void> {
    console.log('Refund status updated');
  }
  
  async sendRefundNotification(refundRecord: any): Promise<void> {
    console.log('Refund notification sent');
  }
  
  build() {
    Column() {
      Text('Payment Service')
    }
  }
}
"""
        
        file_path = os.path.join(self.project_path, "payment", "PaymentService.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 7
        self.call_count += 40

    def generate_complex_ui_component(self):
        """生成复杂的UI组件"""
        print(f"  📦 生成复杂UI组件...")
        
        content = """
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
"""
        
        file_path = os.path.join(self.project_path, "components", "ComplexOrderList.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 15
        self.call_count += 45

    def generate_main_page(self):
        """生成主页面"""
        print(f"  📦 生成主页面...")
        
        content = """
/**
 * 主页面
 * 整合所有服务组件
 */
import router from '@system.router';

@Entry
@Component
struct MainPage {
  @State userInfo: UserInfo = null;
  @State isLoggedIn: boolean = false;
  @State cartCount: number = 0;
  
  async aboutToAppear() {
    console.log('MainPage.aboutToAppear');
    await this.initializeApp();
  }
  
  async initializeApp() {
    // 检查登录状态
    await this.checkLoginStatus();
    
    // 加载用户信息
    if (this.isLoggedIn) {
      await this.loadUserInfo();
    }
    
    // 加载购物车数量
    await this.loadCartCount();
    
    // 初始化推送服务
    await this.initializePushService();
    
    // 加载配置
    await this.loadAppConfig();
  }
  
  async checkLoginStatus() {
    console.log('Checking login status');
    this.isLoggedIn = false;
  }
  
  async loadUserInfo() {
    console.log('Loading user info');
  }
  
  async loadCartCount() {
    console.log('Loading cart count');
    this.cartCount = 0;
  }
  
  async initializePushService() {
    console.log('Initializing push service');
  }
  
  async loadAppConfig() {
    console.log('Loading app config');
  }
  
  build() {
    Column() {
      // 头部
      Row() {
        Text('Shopping App')
        
        if (this.isLoggedIn) {
          Text(`Welcome, ${this.userInfo?.name || 'User'}`)
          Button('Cart')
        } else {
          Button('Login')
          Button('Register')
        }
      }
      
      // 轮播图
      Swiper() {
        Image('banner1.jpg')
        Image('banner2.jpg')
        Image('banner3.jpg')
      }
      .autoPlay(true)
      .interval(3000)
      
      // 商品分类
      Grid() {
        GridItem() { Text('Category 1') }
        GridItem() { Text('Category 2') }
        GridItem() { Text('Category 3') }
        GridItem() { Text('Category 4') }
      }
      .columnsTemplate('1fr 1fr 1fr 1fr')
      
      // 推荐商品
      List() {
        ListItem() {
          Column() {
            Image('product1.jpg')
            Text('Product 1')
            Text('Price: $99')
            Button('Add to Cart')
          }
        }
        
        ListItem() {
          Column() {
            Image('product2.jpg')
            Text('Product 2')
            Text('Price: $199')
            Button('Add to Cart')
          }
        }
      }
      
      // 底部导航
      Row() {
        Button('Home')
        Button('Category')
        Button('Cart')
        Button('My')
      }
    }
  }
}
"""
        
        file_path = os.path.join(self.project_path, "pages", "MainPage.ets")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.file_count += 1
        self.class_count += 1
        self.method_count += 8
        self.call_count += 20

    def generate(self):
        """生成整个项目"""
        print("=" * 80)
        print("🚀 开始生成真实企业级复杂场景测试项目...")
        print("=" * 80)
        
        # 生成各个模块
        self.generate_user_module()
        self.generate_order_module()
        self.generate_inventory_module()
        self.generate_payment_module()
        self.generate_complex_ui_component()
        self.generate_main_page()
        
        # 生成配置
        config_path = os.path.join(self.project_path, "package.json")
        config = f"""{{
  "name": "real-enterprise-app",
  "version": "1.0.0",
  "description": "真实企业级复杂场景测试项目",
  "modules": {{
    "user": "用户管理模块",
    "order": "订单管理模块",
    "inventory": "库存管理模块",
    "payment": "支付模块"
  }},
  "statistics": {{
    "files": {self.file_count},
    "classes": {self.class_count},
    "methods": {self.method_count},
    "calls": {self.call_count}
  }}
}}
"""
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config)
        
        print("\n" + "=" * 80)
        print("🎉 生成完成!")
        print("=" * 80)
        print(f"  📄 文件总数: {self.file_count}")
        print(f"  🏛️  类总数: {self.class_count}")
        print(f"  ⚙️  方法总数: {self.method_count}")
        print(f"  🔗 调用总数: {self.call_count}")
        print("=" * 80)

if __name__ == "__main__":
    generator = RealEnterpriseProjectGenerator("/workspace/RealEnterpriseProject")
    generator.generate()
