#!/usr/bin/env python3
import sys
import time
import json
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
import shutil
import os

class RealOpenSourceTest:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def log_error(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] ERROR: {message}")
    
    def run_ark_analyzer(self, project_path: Path, output_path: Path) -> dict:
        """运行ArkAnalyzer"""
        wrapper_path = Path('/workspace/arkanalyzer-wrapper/src/cli.js')
        cmd = ['node', str(wrapper_path), str(project_path), str(output_path)]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            raise RuntimeError(f"ArkAnalyzer failed: {result.stderr}")
        
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_real_openharmony_project(self) -> dict:
        """测试真实OpenHarmony项目"""
        self.log(f"\n{'='*60}")
        self.log("TEST 1: Real OpenHarmony Project Analysis")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Real OpenHarmony Project",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()
            temp_project = Path(temp_dir) / "openharmony_app"
            
            self.log("Creating simulated OpenHarmony app structure...")
            
            # 创建OpenHarmony应用结构
            structures = {
                'entry/src/main/ets': [
                    ('Index.ets', """
@Entry
@Component
struct Index {
  @State message: string = 'Hello World'
  
  aboutToAppear() {
    this.loadData()
  }
  
  loadData() {
    console.info('Loading data...')
  }
  
  build() {
    Column() {
      Text(this.message)
        .fontSize(50)
        .fontWeight(FontWeight.Bold)
    }
    .width('100%')
    .height('100%')
  }
}
"""),
                    ('UserModel.ets', """
export class UserModel {
  private id: string = ''
  private name: string = ''
  private email: string = ''
  
  constructor(id: string, name: string, email: string) {
    this.id = id
    this.name = name
    this.email = email
  }
  
  getId(): string {
    return this.id
  }
  
  setId(id: string): void {
    this.id = id
  }
  
  getName(): string {
    return this.name
  }
  
  setName(name: string): void {
    this.name = name
  }
  
  validate(): boolean {
    return this.id.length > 0 && this.email.includes('@')
  }
}
"""),
                    ('NetworkService.ets', """
import http from '@ohos.net.http'

export class NetworkService {
  private baseUrl: string = 'https://api.example.com'
  
  async fetchUser(id: string): Promise<any> {
    try {
      const request = http.createHttp()
      const response = await request.request(
        this.baseUrl + '/users/' + id
      )
      return JSON.parse(response.result as string)
    } catch (error) {
      console.error('Network error:', error)
      return null
    }
  }
  
  async postData(endpoint: string, data: any): Promise<boolean> {
    try {
      const request = http.createHttp()
      await request.request(
        this.baseUrl + endpoint,
        {
          method: http.RequestMethod.POST,
          extraData: data
        }
      )
      return true
    } catch (error) {
      console.error('Post error:', error)
      return false
    }
  }
}
"""),
                    ('StorageService.ets', """
import preferences from '@ohos.data.preferences'

export class StorageService {
  private prefs: any = null
  
  async init() {
    this.prefs = await preferences.getPreferences('myApp')
  }
  
  async saveString(key: string, value: string): Promise<void> {
    await this.prefs.put(key, value)
    await this.prefs.flush()
  }
  
  async getString(key: string): Promise<string | null> {
    return await this.prefs.get(key, null)
  }
  
  async remove(key: string): Promise<void> {
    await this.prefs.delete(key)
    await this.prefs.flush()
  }
  
  async clear(): Promise<void> {
    await this.prefs.clear()
    await this.prefs.flush()
  }
}
"""),
                    ('Logger.ets', """
export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3
}

export class Logger {
  private static level: LogLevel = LogLevel.INFO
  
  static setLevel(level: LogLevel): void {
    this.level = level
  }
  
  static debug(message: string): void {
    if (this.level <= LogLevel.DEBUG) {
      console.debug('[DEBUG]', message)
    }
  }
  
  static info(message: string): void {
    if (this.level <= LogLevel.INFO) {
      console.info('[INFO]', message)
    }
  }
  
  static warn(message: string): void {
    if (this.level <= LogLevel.WARN) {
      console.warn('[WARN]', message)
    }
  }
  
  static error(message: string, error?: Error): void {
    if (this.level <= LogLevel.ERROR) {
      console.error('[ERROR]', message, error?.stack)
    }
  }
}
"""),
                ],
                'entry/src/main/ets/pages': [
                    ('HomePage.ets', """
@Entry
@Component
struct HomePage {
  @State userName: string = ''
  @State isLoading: boolean = false
  
  aboutToAppear() {
    this.loadUserData()
  }
  
  async loadUserData(): Promise<void> {
    this.isLoading = true
    try {
      const storage = new StorageService()
      this.userName = await storage.getString('userName') || 'Guest'
    } catch (error) {
      Logger.error('Failed to load user data', error)
    } finally {
      this.isLoading = false
    }
  }
  
  build() {
    Column() {
      if (this.isLoading) {
        LoadingProgress()
          .width(50)
          .height(50)
      } else {
        Text('Welcome, ' + this.userName)
          .fontSize(30)
      }
    }
    .width('100%')
    .height('100%')
  }
}
"""),
                    ('SettingsPage.ets', """
@Entry
@Component
struct SettingsPage {
  @State notifications: boolean = true
  @State darkMode: boolean = false
  
  build() {
    Column() {
      Toggle({ type: ToggleType.Switch, isOn: this.notifications })
        .onChange((isOn: boolean) => {
          this.notifications = isOn
          this.saveSettings()
        })
      
      Toggle({ type: ToggleType.Switch, isOn: this.darkMode })
        .onChange((isOn: boolean) => {
          this.darkMode = isOn
          this.saveSettings()
        })
    }
    .width('100%')
    .padding(20)
  }
  
  saveSettings(): void {
    const storage = new StorageService()
    storage.saveString('notifications', String(this.notifications))
    storage.saveString('darkMode', String(this.darkMode))
  }
}
"""),
                ],
                'entry/src/main/ets/model': [
                    ('ProductModel.ets', """
export interface Product {
  id: string
  name: string
  price: number
  category: string
  inStock: boolean
}

export class ProductModel implements Product {
  id: string
  name: string
  price: number
  category: string
  inStock: boolean
  
  constructor(product: Product) {
    this.id = product.id
    this.name = product.name
    this.price = product.price
    this.category = product.category
    this.inStock = product.inStock
  }
  
  getFormattedPrice(): string {
    return '$' + this.price.toFixed(2)
  }
  
  isAffordable(budget: number): boolean {
    return this.price <= budget
  }
  
  static fromJSON(json: any): ProductModel {
    return new ProductModel({
      id: json.id,
      name: json.name,
      price: json.price,
      category: json.category,
      inStock: json.inStock
    })
  }
}
"""),
                    ('OrderModel.ets', """
import { ProductModel } from './ProductModel'

export interface OrderItem {
  product: ProductModel
  quantity: number
}

export class OrderModel {
  id: string
  items: OrderItem[] = []
  status: string = 'pending'
  createdAt: Date = new Date()
  
  addItem(product: ProductModel, quantity: number): void {
    const existing = this.items.find(
      item => item.product.id === product.id
    )
    
    if (existing) {
      existing.quantity += quantity
    } else {
      this.items.push({ product, quantity })
    }
  }
  
  removeItem(productId: string): void {
    this.items = this.items.filter(
      item => item.product.id !== productId
    )
  }
  
  getTotal(): number {
    return this.items.reduce(
      (sum, item) => sum + item.product.price * item.quantity,
      0
    )
  }
  
  getItemCount(): number {
    return this.items.reduce(
      (sum, item) => sum + item.quantity,
      0
    )
  }
  
  clear(): void {
    this.items = []
    this.status = 'cancelled'
  }
}
"""),
                ],
                'entry/src/main/ets/utils': [
                    ('DateUtils.ets', """
export class DateUtils {
  static formatDate(date: Date): string {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  
  static formatTime(date: Date): string {
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')
    return `${hours}:${minutes}:${seconds}`
  }
  
  static formatDateTime(date: Date): string {
    return this.formatDate(date) + ' ' + this.formatTime(date)
  }
  
  static parseDate(dateStr: string): Date | null {
    try {
      return new Date(dateStr)
    } catch (error) {
      return null
    }
  }
  
  static getDaysDiff(date1: Date, date2: Date): number {
    const diff = Math.abs(date2.getTime() - date1.getTime())
    return Math.ceil(diff / (1000 * 60 * 60 * 24))
  }
}
"""),
                    ('StringUtils.ets', """
export class StringUtils {
  static isEmpty(str: string | null | undefined): boolean {
    return !str || str.trim().length === 0
  }
  
  static isNotEmpty(str: string | null | undefined): boolean {
    return !this.isEmpty(str)
  }
  
  static truncate(str: string, maxLength: number): string {
    if (str.length <= maxLength) {
      return str
    }
    return str.substring(0, maxLength - 3) + '...'
  }
  
  static capitalize(str: string): string {
    if (this.isEmpty(str)) {
      return str
    }
    return str.charAt(0).toUpperCase() + str.slice(1)
  }
  
  static camelCase(str: string): string {
    return str
      .replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) => {
        return index === 0 ? word.toLowerCase() : word.toUpperCase()
      })
      .replace(/\s+/g, '')
  }
  
  static snakeCase(str: string): string {
    return str
      .replace(/\W+/g, ' ')
      .split(/ |\B(?=[A-Z])/)
      .map(word => word.toLowerCase())
      .join('_')
  }
  
  static validateEmail(email: string): boolean {
    const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/
    return emailRegex.test(email)
  }
  
  static validatePhone(phone: string): boolean {
    const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\\s./0-9]*$/
    return phoneRegex.test(phone)
  }
}
"""),
                ],
            }
            
            # 创建目录和文件
            for dir_path, files in structures.items():
                full_dir = temp_project / dir_path
                full_dir.mkdir(parents=True, exist_ok=True)
                
                for file_name, content in files:
                    file_path = full_dir / file_name
                    file_path.write_text(content, encoding='utf-8')
            
            # 创建配置文件
            config_path = temp_project / 'entry' / 'src' / 'main' / 'module.json'
            config_path.write_text("""
{
  "app": {
    "bundleName": "com.example.app",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0"
  },
  "module": {
    "mainAbility": "Entry",
    "deviceTypes": [
      "phone",
      "tablet"
    ]
  }
}
""", encoding='utf-8')
            
            self.log("OpenHarmony app structure created")
            
            # 分析项目
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            self.log("Analyzing OpenHarmony project...")
            start = time.time()
            data = self.run_ark_analyzer(temp_project, Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files: {len(data.get('files', []))}")
            self.log(f"Classes: {len(data.get('classes', []))}")
            self.log(f"Methods: {len(data.get('methods', []))}")
            self.log(f"Calls: {len(data.get('calls', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = True
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'calls': len(data.get('calls', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Real OpenHarmony test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_multiple_projects_batch(self) -> dict:
        """测试批量多项目分析"""
        self.log(f"\n{'='*60}")
        self.log("TEST 2: Multiple Projects Batch Analysis")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Multiple Projects Batch",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            # 测试不同项目
            projects = [
                ('sample', Path('/workspace/sample_project')),
                ('realistic', Path('/workspace/realistic_test_project')),
                ('massive', Path('/workspace/massive_test_project')),
            ]
            
            batch_results = {}
            total_time = 0
            
            for name, project_path in projects:
                if not project_path.exists():
                    self.log(f"  Skipping {name}: not found")
                    continue
                
                self.log(f"\n  Analyzing {name}...")
                
                temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
                temp_output.close()
                
                start = time.time()
                data = self.run_ark_analyzer(project_path, Path(temp_output.name))
                elapsed = time.time() - start
                
                total_time += elapsed
                
                batch_results[name] = {
                    'time': elapsed,
                    'files': len(data.get('files', [])),
                    'classes': len(data.get('classes', [])),
                    'methods': len(data.get('methods', []))
                }
                
                self.log(f"    Time: {elapsed:.2f}s, Files: {batch_results[name]['files']}")
                
                Path(temp_output.name).unlink(missing_ok=True)
            
            self.log(f"\nTotal batch analysis time: {total_time:.2f}s")
            
            result['success'] = len(batch_results) > 0
            result['stats'] = {
                'projects': len(batch_results),
                'total_time': total_time,
                'results': batch_results
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Multiple projects test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_nested_directory_structure(self) -> dict:
        """测试深层嵌套目录结构"""
        self.log(f"\n{'='*60}")
        self.log("TEST 3: Deep Nested Directory Structure")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Deep Nested Directory",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建深层嵌套结构
            deep_path = temp_dir
            for i in range(15):
                deep_path = deep_path / f'level{i+1}'
                deep_path.mkdir()
                
                # 在每层创建一些文件
                for j in range(3):
                    file_path = deep_path / f'file{i}_{j}.ets'
                    file_path.write_text(f"""
export class Nested{i}Class{j} {{
  nestedMethod{j}() {{
    console.log('Level {i}, File {j}');
  }}
}}
""", encoding='utf-8')
            
            self.log("Created 15-level deep nested structure")
            
            # 分析深层结构
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Expected files: ~45")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            # 验证是否找到了所有文件
            expected_min = 40
            found = len(data.get('files', []))
            success = found >= expected_min
            
            if not success:
                self.log_warning(f"Expected at least {expected_min} files, found {found}")
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'expected': expected_min,
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Deep nested test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_symlinks_and_special_files(self) -> dict:
        """测试符号链接和特殊文件"""
        self.log(f"\n{'='*60}")
        self.log("TEST 4: Symlinks and Special Files")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Symlinks and Special Files",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建正常文件
            normal_file = Path(temp_dir) / 'normal.ets'
            normal_file.write_text("""
export class NormalClass {
  normalMethod() {
    console.log('Normal');
  }
}
""", encoding='utf-8')
            
            # 创建符号链接
            link_file = Path(temp_dir) / 'linked.ets'
            if os.name != 'nt':  # Windows不支持符号链接
                try:
                    os.symlink(str(normal_file), str(link_file))
                    self.log("Created symlink")
                except:
                    self.log("Could not create symlink (may require admin)")
                    # 创建一个普通文件代替
                    link_file.write_text(normal_file.read_text())
            else:
                link_file.write_text(normal_file.read_text())
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = True
            result['stats'] = {
                'files': len(data.get('files', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Symlinks test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_mixed_file_types(self) -> dict:
        """测试混合文件类型"""
        self.log(f"\n{'='*60}")
        self.log("TEST 5: Mixed File Types")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Mixed File Types",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建不同类型的文件
            file_types = {
                '.ets': """
export class EtsClass {
  etsMethod() {
    console.log('ETS file');
  }
}
""",
                '.ts': """
export class TsClass {
  tsMethod() {
    console.log('TS file');
  }
}
""",
                '.tsx': """
export class TsxClass {
  tsxMethod() {
    console.log('TSX file');
  }
}
""",
                '.js': """
class JsClass {
  jsMethod() {
    console.log('JS file');
  }
}
module.exports = JsClass;
""",
                '.txt': "This is a text file",
                '.json': '{"key": "value"}',
                '.md': "# Markdown File",
            }
            
            for ext, content in file_types.items():
                file_path = Path(temp_dir) / f'file{ext}' if ext != '.md' else Path(temp_dir) / 'README.md'
                file_path.write_text(content, encoding='utf-8')
            
            self.log("Created mixed file types")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            
            # 验证只处理了代码文件
            expected_code_files = 4  # .ets, .ts, .tsx, .js
            found = len(data.get('files', []))
            
            success = found == expected_code_files
            if not success:
                self.log_warning(f"Expected {expected_code_files} code files, found {found}")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'expected': expected_code_files,
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Mixed file types test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def test_special_characters_in_code(self) -> dict:
        """测试代码中的特殊字符"""
        self.log(f"\n{'='*60}")
        self.log("TEST 6: Special Characters in Code")
        self.log(f"{'='*60}")
        
        result = {
            'test_name': "Special Characters",
            'success': False,
            'start_time': time.time(),
            'end_time': None
        }
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # 创建包含各种特殊字符的文件
            special_file = Path(temp_dir) / 'special.ets'
            special_content = """
// 测试各种特殊字符
export class SpecialClass {
  // 中文注释：这是一个测试类
  // 日本語コメント：テストクラス
  // 한국어 주석: 테스트 클래스
  // Emoji: 🚀 💻 📱
  // Unicode: \u4e2d\u6587 \u00e9\u00e8
  
  specialMethod() {
    const str1 = "双引号字符串"
    const str2 = '单引号字符串'
    const str3 = `模板字符串`
    
    const emoji = "🚀"
    const math = "2 + 2 = 4"
    const url = "https://example.com?param=中文"
    
    console.log(str1, str2, str3)
    console.log("Special chars:", emoji, math, url)
  }
  
  handleUnicode() {
    const chars = [
      'a', 'b', 'c', '1', '2', '3',
      '\u4e2d\u6587', '\u65e5\u672c\u8a9e',
      '\ud55c\uae00', '\ud83c\udf0d'
    ]
    return chars.join('')
  }
}
"""
            special_file.write_text(special_content, encoding='utf-8')
            
            self.log("Created file with special characters")
            
            # 分析
            temp_output = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
            temp_output.close()
            
            start = time.time()
            data = self.run_ark_analyzer(Path(temp_dir), Path(temp_output.name))
            elapsed = time.time() - start
            
            self.log(f"Analysis completed in {elapsed:.2f}s")
            self.log(f"Files found: {len(data.get('files', []))}")
            self.log(f"Classes found: {len(data.get('classes', []))}")
            self.log(f"Methods found: {len(data.get('methods', []))}")
            
            # 验证
            success = (
                len(data.get('files', [])) == 1 and
                len(data.get('classes', [])) == 1 and
                len(data.get('methods', [])) >= 2
            )
            
            if not success:
                self.log_warning("Special characters may have affected parsing")
            
            # 清理
            shutil.rmtree(temp_dir)
            Path(temp_output.name).unlink(missing_ok=True)
            
            result['success'] = success
            result['stats'] = {
                'files': len(data.get('files', [])),
                'classes': len(data.get('classes', [])),
                'methods': len(data.get('methods', [])),
                'time': elapsed
            }
            
        except Exception as e:
            result['error'] = str(e)
            self.log_error(f"Special characters test failed: {e}")
        finally:
            result['end_time'] = time.time()
        
        self.results.append(result)
        return result
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("\n" + "="*60)
        self.log("REAL OPEN SOURCE TEST SUITE")
        self.log("="*60)
        self.log(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_real_openharmony_project()
        self.test_multiple_projects_batch()
        self.test_nested_directory_structure()
        self.test_symlinks_and_special_files()
        self.test_mixed_file_types()
        self.test_special_characters_in_code()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        total_time = time.time() - self.start_time
        
        print("\n" + "="*60)
        print("REAL OPEN SOURCE TEST SUMMARY")
        print("="*60)
        print(f"Total time: {total_time:.2f}s")
        print(f"Tests run: {len(self.results)}")
        
        success_count = sum(1 for r in self.results if r['success'])
        print(f"Successful: {success_count}/{len(self.results)}")
        
        print("\nDetailed results:")
        for result in self.results:
            status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
            duration = result['end_time'] - result['start_time'] if result['end_time'] else 'N/A'
            print(f"  {result['test_name']}: {status} ({duration:.2f}s)")


if __name__ == '__main__':
    test = RealOpenSourceTest()
    test.run_all_tests()
