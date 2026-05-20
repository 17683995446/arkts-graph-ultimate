@Component
export struct Component1 {
    @State title: string = 'Component 1';
    @State count: number = 0;
    
    build() {
        Column() {
            Text(this.title);
            Button('Increment')
                .onClick(() => {
                    this.count++;
                    this.handleClick();
                });
            Text(`Count: ${this.count}`);
        };
    }
    
    handleClick() {
        console.log('Component1 clicked!');
        this.logEvent();
    }
    
    logEvent() {
        console.log('Event logged!');
    }
}