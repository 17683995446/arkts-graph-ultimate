
@Component
export struct CustomComp004 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.process5();
        this.fetch3Data();
    }

    onClick1(): void {
        this.value0++;
    }

    onClick2(): void {
        this.process3();
        this.onClick2();
    }

    onClick3(): void {
        this.formatOutput();
        this.fetch4Data();
    }

    onClick4(): void {
        this.value0++;
    }

    build() {
            Button() {}
            Column() {}
    }
}
@Component
export struct CustomComp104 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.execute1();
        this.fetch0Data();
    }

    onClick1(): void {
        this.value0++;
    }

    onClick2(): void {
        this.value0++;
    }

    build() {
            List() {}
            Row() {}
    }
}