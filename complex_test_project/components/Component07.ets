
@Component
export struct CustomComp007 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.value0++;
    }

    onClick1(): void {
        this.execute4();
        this.execute6();
    }

    onClick2(): void {
        this.execute1();
        this.fetch1Data();
    }

    onClick3(): void {
        this.execute0();
        this.validateInput();
    }

    onClick4(): void {
        this.value0++;
    }

    build() {
            Button() {}
            List() {}
    }
}
@Component
export struct CustomComp107 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.onClick0();
        this.process1();
    }

    onClick1(): void {
        this.value0++;
    }

    onClick2(): void {
        this.validate();
        this.process1();
    }

    build() {
            Text() {}
            Column() {}
    }
}