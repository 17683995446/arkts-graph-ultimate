@Component
export struct Component15 {
    @State title: string = 'Component 15';
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
        console.log('Component15 clicked!');
        this.logEvent();
    }
    
    logEvent() {
        console.log('Event logged!');
    }
}