
export class Model000 {
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
    }

    process3(): void {
        this.process0();
        this.process2();
    }

    process4(): void {
        // processing...
    }
}
export class Model100 {
    private data: any;
    
    constructor() {
        this.data = {};
    }
    

    process0(): void {
        this.process1();
        this.process4();
    }

    process1(): void {
        // processing...
    }

    process2(): void {
        this.process1();
    }

    process3(): void {
        // processing...
    }

    process4(): void {
        this.process3();
    }

    process5(): void {
        // processing...
    }

    process6(): void {
        // processing...
    }
}
export class Model200 {
    private data: any;
    
    constructor() {
        this.data = {};
    }
    

    process0(): void {
        // processing...
    }

    process1(): void {
        this.process3();
        this.process4();
    }

    process2(): void {
        // processing...
    }

    process3(): void {
        // processing...
    }

    process4(): void {
        // processing...
    }

    process5(): void {
        this.process1();
    }

    process6(): void {
        this.process4();
        this.process0();
    }
}