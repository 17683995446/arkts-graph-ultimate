@Component
export struct Component10 {
    @State title: string = 'Component 10';
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
        console.log('Component10 clicked!');
        this.logEvent();
    }
    
    logEvent() {
        console.log('Event logged!');
    }
}