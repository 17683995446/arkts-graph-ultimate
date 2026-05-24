
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
