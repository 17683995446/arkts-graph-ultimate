@Component
export struct Component14 {
    @State title: string = 'Component 14';
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
        console.log('Component14 clicked!');
        this.logEvent();
    }
    
    logEvent() {
        console.log('Event logged!');
    }
}