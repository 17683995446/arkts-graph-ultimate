
@Component
export struct CustomComp001 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.value0++;
    }

    onClick1(): void {
        this.formatOutput();
        this.fetch3Data();
    }

    onClick2(): void {
        this.value0++;
    }

    onClick3(): void {
        this.validate();
        this.fetch2Data();
    }

    onClick4(): void {
        this.value0++;
    }

    onClick5(): void {
        this.validateInput();
        this.process2();
    }

    build() {
            List() {}
            Button() {}
    }
}
@Component
export struct CustomComp101 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.process1();
        this.process1();
    }

    onClick1(): void {
        this.execute2();
        this.process2();
    }

    onClick2(): void {
        this.execute5();
        this.process4();
    }

    build() {
            List() {}
            Text() {}
    }
}