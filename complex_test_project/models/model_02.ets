
export class Model002 {
    private data: any;
    
    constructor() {
        this.data = {};
    }
    

    process0(): void {
        // processing...
    }

    process1(): void {
        // processing...
    }

    process2(): void {
        this.process0();
        this.process2();
    }

    process3(): void {
        // processing...
    }

    process4(): void {
        this.process1();
        this.process5();
    }
}
export class Model102 {
    private data: any;
    
    constructor() {
        this.data = {};
    }
    

    process0(): void {
        // processing...
    }

    process1(): void {
        // processing...
    }

    process2(): void {
        // processing...
    }

    process3(): void {
        this.process1();
    }

    process4(): void {
        // processing...
    }

    process5(): void {
        // processing...
    }

    process6(): void {
        this.process4();
    }
}
export class Model202 {
    private data: any;
    
    constructor() {
        this.data = {};
    }
    

    process0(): void {
        this.process2();
        this.process2();
    }

    process1(): void {
        // processing...
    }

    process2(): void {
        this.process3();
    }

    process3(): void {
        // processing...
    }

    process4(): void {
        this.process4();
        this.process0();
    }

    process5(): void {
        // processing...
    }
}