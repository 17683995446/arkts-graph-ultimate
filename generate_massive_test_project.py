#!/usr/bin/env python3
import os
import random
from pathlib import Path
from typing import List, Dict

class MassiveTestProjectGenerator:
    def __init__(self, base_path: Path, num_files: int = 5000):
        self.base_path = base_path
        self.num_files = num_files
        self.class_names = []
        self.method_names = []
        self.generate_names()
    
    def generate_names(self):
        base_class_names = [
            'User', 'Product', 'Order', 'Cart', 'Payment', 'Inventory', 'Shipping',
            'Auth', 'Session', 'Token', 'Cache', 'Logger', 'Config', 'Database',
            'Network', 'Http', 'Api', 'Service', 'Repository', 'Controller',
            'ViewModel', 'Component', 'Widget', 'Screen', 'Page', 'Router',
            'State', 'Store', 'Action', 'Reducer', 'Effect', 'Middleware',
            'Validator', 'Serializer', 'Parser', 'Encoder', 'Decoder', 'Formatter',
            'Converter', 'Transformer', 'Filter', 'Sorter', 'Pager', 'Searcher',
            'Uploader', 'Downloader', 'Importer', 'Exporter', 'Backup', 'Restore',
            'Notification', 'Message', 'Alert', 'Dialog', 'Toast', 'Snackbar',
            'Employee', 'Department', 'Salary', 'Attendance', 'Performance', 'Report',
            'Analytics', 'Dashboard', 'Chart', 'Graph', 'Table', 'Grid',
            'Menu', 'Toolbar', 'Sidebar', 'Header', 'Footer', 'Modal',
            'Form', 'Input', 'Select', 'Checkbox', 'Radio', 'Button',
            'Table', 'Row', 'Column', 'Cell', 'Header', 'Footer',
            'Pagination', 'Loading', 'Spinner', 'Progress', 'Skeleton', 'Placeholder',
            'Error', 'Warning', 'Info', 'Success', 'Debug', 'Trace',
            'Request', 'Response', 'Header', 'Body', 'Query', 'Param',
            'Database', 'Connection', 'Transaction', 'Query', 'Result', 'Cursor',
            'Cache', 'Memory', 'Disk', 'File', 'Stream', 'Buffer',
            'Thread', 'Process', 'Task', 'Job', 'Queue', 'Worker',
            'Event', 'Handler', 'Listener', 'Emitter', 'Observer', 'Subject',
            'Builder', 'Factory', 'Singleton', 'Adapter', 'Bridge', 'Decorator',
            'Strategy', 'Template', 'Chain', 'Command', 'Iterator', 'Mediator'
        ]
        
        base_method_names = [
            'initialize', 'create', 'read', 'update', 'delete', 'list', 'search',
            'getById', 'getByName', 'getByEmail', 'getByDate', 'getByStatus',
            'save', 'persist', 'flush', 'commit', 'rollback', 'beginTransaction',
            'validate', 'sanitize', 'normalize', 'format', 'parse', 'serialize',
            'deserialize', 'encode', 'decode', 'encrypt', 'decrypt', 'hash',
            'generateId', 'generateToken', 'generateHash', 'generateSalt',
            'connect', 'disconnect', 'send', 'receive', 'request', 'response',
            'fetch', 'post', 'put', 'patch', 'delete', 'get',
            'load', 'unload', 'mount', 'unmount', 'render', 'rebuild',
            'updateState', 'setState', 'getState', 'resetState', 'subscribe',
            'publish', 'notify', 'emit', 'on', 'off', 'once',
            'logInfo', 'logWarn', 'logError', 'logDebug', 'logTrace',
            'cacheGet', 'cacheSet', 'cacheDelete', 'cacheClear', 'cacheInvalidate',
            'checkPermission', 'authorize', 'authenticate', 'login', 'logout',
            'calculate', 'compute', 'aggregate', 'sum', 'average', 'count',
            'filter', 'sort', 'slice', 'map', 'reduce', 'groupBy',
            'upload', 'download', 'importData', 'exportData', 'backup', 'restore',
            'validateInput', 'processData', 'transformData', 'convertData', 'formatData',
            'parseJSON', 'stringifyJSON', 'parseXML', 'buildXML', 'parseCSV', 'buildCSV',
            'encryptData', 'decryptData', 'signData', 'verifyData', 'hashPassword', 'verifyPassword',
            'createUser', 'updateUser', 'deleteUser', 'getUser', 'listUsers', 'searchUsers',
            'createOrder', 'updateOrder', 'cancelOrder', 'getOrder', 'listOrders', 'searchOrders',
            'createProduct', 'updateProduct', 'deleteProduct', 'getProduct', 'listProducts', 'searchProducts',
            'processPayment', 'refundPayment', 'getPayment', 'listPayments', 'searchPayments',
            'createSession', 'validateSession', 'destroySession', 'getSession', 'listSessions',
            'sendEmail', 'sendSMS', 'sendNotification', 'pushNotification', 'broadcastEvent',
            'startTransaction', 'commitTransaction', 'rollbackTransaction', 'saveTransaction', 'restoreTransaction',
            'acquireLock', 'releaseLock', 'waitForLock', 'checkLock', 'forceUnlock',
            'startTask', 'pauseTask', 'resumeTask', 'cancelTask', 'getTaskStatus', 'listTasks',
            'scheduleJob', 'unscheduleJob', 'runJob', 'getJobStatus', 'listJobs', 'searchJobs',
            'createCache', 'readCache', 'updateCache', 'deleteCache', 'clearCache', 'warmCache',
            'analyzeData', 'visualizeData', 'reportData', 'exportReport', 'importReport',
            'monitorSystem', 'healthCheck', 'metricsCheck', 'performanceCheck', 'securityCheck'
        ]
        
        for i in range(500):
            self.class_names.append(f"{random.choice(base_class_names)}{i}")
        for i in range(1000):
            self.method_names.append(f"{random.choice(base_method_names)}{i}")
    
    def generate_realistic_class(self, class_name: str) -> str:
        methods = []
        num_methods = random.randint(5, 20)
        
        for i in range(num_methods):
            method_name = random.choice(self.method_names)
            is_async = random.choice([True, False])
            has_return_type = random.choice([True, False])
            has_params = random.choice([True, False])
            
            params = []
            if has_params:
                num_params = random.randint(1, 8)
                param_types = ['string', 'number', 'boolean', 'object', 'any', 'Array<string>', 
                              'Promise<void>', 'Array<number>', 'Map<string, any>', 'Set<any>']
                for j in range(num_params):
                    param_name = f"param{j}"
                    param_type = random.choice(param_types)
                    params.append(f"{param_name}: {param_type}")
            
            return_type = ''
            if has_return_type:
                return_types = ['void', 'string', 'number', 'boolean', 'object', 'Promise<void>', 
                              'Array<any>', 'Promise<string>', 'Promise<number>']
                return_type = f": {random.choice(return_types)}"
            
            async_prefix = 'async ' if is_async else ''
            
            body = self.generate_method_body()
            
            methods.append(f"""
  {async_prefix}{method_name}({', '.join(params)}){return_type} {{
{body}
  }}""")
        
        decorators = []
        if random.choice([True, False]):
            decorators.append('@Observed')
        if random.choice([True, False]):
            decorators.append('@Component')
        if random.choice([True, False]):
            decorators.append('@Track')
        
        decorator_str = '\n'.join(decorators)
        
        return f"""{decorator_str}
export class {class_name} {{
  private state: object = {{}};
  private cache: Map<string, any> = new Map();
  private config: object = {{}};
  private logger: any;
  private database: any;
{''.join(methods)}
}}
"""
    
    def generate_method_body(self) -> str:
        statements = []
        num_statements = random.randint(3, 15)
        
        for _ in range(num_statements):
            statement_type = random.choice([
                'call', 'assignment', 'if', 'for', 'try', 'return', 'log', 'async_call', 'promise'
            ])
            
            if statement_type == 'call':
                callee = random.choice(self.method_names)
                has_this = random.choice([True, False])
                this_prefix = 'this.' if has_this else ''
                args = [f"'{random.choice(['a', 'b', 'c', 'd', 'e', 'f'])}'" for _ in range(random.randint(0, 3))]
                statements.append(f"    {this_prefix}{callee}({', '.join(args)});")
            
            elif statement_type == 'async_call':
                callee = random.choice(self.method_names)
                has_this = random.choice([True, False])
                this_prefix = 'this.' if has_this else ''
                args = [f"'{random.choice(['async', 'data'])}'" for _ in range(random.randint(0, 2))]
                statements.append(f"    await {this_prefix}{callee}({', '.join(args)});")
            
            elif statement_type == 'assignment':
                var_name = f"temp{random.randint(0, 19)}"
                var_value = random.choice([
                    "''", "0", "1", "true", "false", "null", "undefined", 
                    "{}", "[]", "{{}}", "{{}}", "new Map()", "new Set()"
                ])
                statements.append(f"    const {var_name} = {var_value};")
            
            elif statement_type == 'if':
                condition = random.choice([
                    'true', 'false', 'this.state', 'this.cache.size > 0',
                    'result !== null', 'error === null', 'count > 0',
                    'data.length > 0', 'isValid', 'isLoading'
                ])
                statements.append(f"    if ({condition}) {{")
                statements.append(f"      // handle true case")
                statements.append(f"    }} else {{")
                statements.append(f"      // handle false case")
                statements.append(f"    }}")
            
            elif statement_type == 'for':
                loop_var = random.choice(['i', 'j', 'k', 'index', 'idx'])
                statements.append(f"    for (let {loop_var} = 0; {loop_var} < 10; {loop_var}++) {{")
                statements.append(f"      const item = data[{loop_var}];")
                statements.append(f"      // process item")
                statements.append(f"    }}")
            
            elif statement_type == 'promise':
                statements.append(f"    return new Promise((resolve, reject) => {{")
                statements.append(f"      // async operation")
                statements.append(f"      resolve(result);")
                statements.append(f"    }});")
            
            elif statement_type == 'try':
                statements.append(f"    try {{")
                statements.append(f"      const result = await this.processData();")
                statements.append(f"    }} catch (error) {{")
                statements.append(f"      console.error('Error:', error);")
                statements.append(f"      throw error;")
                statements.append(f"    }} finally {{")
                statements.append(f"      // cleanup")
                statements.append(f"    }}")
            
            elif statement_type == 'return':
                statements.append(f"    return result;")
            
            elif statement_type == 'log':
                statements.append(f"    console.log('Processing...');")
        
        return '\n'.join(statements)
    
    def generate_realistic_file(self, file_path: Path, file_type: str = 'class') -> None:
        os.makedirs(file_path.parent, exist_ok=True)
        
        if file_type == 'class':
            class_name = random.choice(self.class_names)
            content = self.generate_realistic_class(class_name)
        elif file_type == 'util':
            content = self.generate_util_file()
        elif file_type == 'component':
            content = self.generate_component_file()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_util_file(self) -> str:
        functions = []
        num_functions = random.randint(10, 30)
        
        for i in range(num_functions):
            func_name = random.choice(self.method_names)
            is_async = random.choice([True, False])
            async_prefix = 'async ' if is_async else ''
            
            body = self.generate_method_body()
            
            functions.append(f"""
export {async_prefix}function {func_name}() {{
{body}
}}""")
        
        return ''.join(functions)
    
    def generate_component_file(self) -> str:
        component_name = random.choice(self.class_names) + 'Component'
        
        return f"""@Component
export struct {component_name} {{
  @State title: string = '';
  @State count: number = 0;
  @State dataList: Array<any> = [];
  @State isLoading: boolean = false;
  
  aboutToAppear() {{
    this.loadData();
  }}
  
  async loadData() {{
    this.isLoading = true;
    // load data from API
    this.isLoading = false;
  }}
  
  build() {{
    Column() {{
      Text(this.title)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .width('100%');
      
      if (this.isLoading) {{
        LoadingProgress()
          .width(50)
          .height(50);
      }} else {{
        ForEach(this.dataList, (item: any) => {{
          Text(item.name)
            .fontSize(16)
            .padding(10);
        }}, (item: any) => item.id);
      }}
      
      Button('Refresh')
        .onClick(() => {{
          this.loadData();
        }})
        .margin({{ top: 10 }});
    }}
    .width('100%')
    .height('100%')
    .padding(16);
  }}
}}
"""
    
    def generate(self) -> None:
        directories = [
            'models', 'services', 'controllers', 'views', 'components',
            'utils', 'helpers', 'constants', 'types', 'interfaces',
            'repositories', 'validators', 'serializers', 'middlewares',
            'configs', 'storages', 'caches', 'loggers', 'notifications',
            'apis', 'clients', 'adapters', 'factories', 'builders',
            'managers', 'handlers', 'processors', 'generators', 'parsers',
            'renderers', 'validators', 'transformers', 'converters', 'formatters'
        ]
        
        file_types = ['class', 'class', 'class', 'class', 'util', 'component']
        
        print(f"Generating {self.num_files} MASSIVE ArkTS files in {self.base_path}...")
        
        for i in range(self.num_files):
            dir_name = random.choice(directories)
            file_type = random.choice(file_types)
            file_name = f"{random.choice(self.class_names).lower()}_{i:05d}.ets"
            file_path = self.base_path / dir_name / file_name
            
            self.generate_realistic_file(file_path, file_type)
            
            if (i + 1) % 500 == 0:
                print(f"  Generated {i + 1}/{self.num_files} files ({(i+1)/self.num_files*100:.1f}%)")
        
        print("MASSIVE Project generation complete!")
        print(f"Total size: {sum(f.stat().st_size for f in self.base_path.rglob('*.ets')) / 1024 / 1024:.2f} MB")


if __name__ == '__main__':
    generator = MassiveTestProjectGenerator(Path('/workspace/massive_test_project'), num_files=5000)
    generator.generate()
