
/**
 * 极度混乱的文件6 - 混合UI组件与业务逻辑
 */
import { UserService } from '../user/UserService.ets';

@Component
export struct MixedClass {
    @State count: number = 0;
    private data: number[] = [];
    
    // 业务逻辑方法
    fetchData(): Promise<void> {
        console.log('获取数据');
        return Promise.resolve();
    }
    
    processData(): number[] {
        console.log('处理数据');
        return this.data;
    }
    
    updateUI(): void {
        this.count++;
    }
    
    // 更多方法
    method1(): void {
        console.log('method1');
    }
    
    method2(): void {
        this.method1();
    }
    
    method3(): void {
        this.method2();
    }
    
    build() {
        Column() {
            Text('混合组件');
            Button('点击')
                .onClick(() => {
                    this.updateUI();
                });
            Text(this.count.toString());
            List() {
                ListItem() {
                    Text('项1');
                }
                ListItem() {
                    Text('项2');
                }
            }
        }
    }
}

@Component
export struct AnotherMixedClass {
    @State text: string = "";
    
    changeText(newText: string): void {
        this.text = newText;
    }
    
    reset(): void {
        this.text = "";
    }
    
    build() {
        Row() {
            TextInput()
                .onChange((value: string) => {
                    this.changeText(value);
                });
            Button('重置')
                .onClick(() => {
                    this.reset();
                });
        }
    }
}
