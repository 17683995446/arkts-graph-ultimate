@Component
export struct Component3 {
    @State title: string = 'Component 3';
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
        console.log('Component3 clicked!');
        this.logEvent();
    }
    
    logEvent() {
        console.log('Event logged!');
    }
}