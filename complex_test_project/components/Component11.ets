
@Component
export struct CustomComp011 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.value0++;
    }

    onClick1(): void {
        this.value0++;
    }

    onClick2(): void {
        this.value0++;
    }

    build() {
            Column() {}
            List() {}
    }
}
@Component
export struct CustomComp111 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.process2();
        this.process();
    }

    onClick1(): void {
        this.onClick0();
        this.process3();
    }

    onClick2(): void {
        this.process7();
        this.onClick1();
    }

    onClick3(): void {
        this.formatOutput();
        this.fetch6Data();
    }

    onClick4(): void {
        this.execute11();
        this.fetch4Data();
    }

    onClick5(): void {
        this.fetch9Data();
        this.fetch0Data();
    }

    build() {
            Row() {}
            Button() {}
    }
}