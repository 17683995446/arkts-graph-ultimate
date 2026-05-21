
@Component
export struct CustomComp013 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.process2();
        this.process3();
    }

    onClick1(): void {
        this.value0++;
    }

    onClick2(): void {
        this.value0++;
    }

    build() {
            Button() {}
            Text() {}
    }
}
@Component
export struct CustomComp113 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.fetch3Data();
        this.process3();
    }

    onClick1(): void {
        this.value0++;
    }

    onClick2(): void {
        this.fetch1Data();
        this.fetch0Data();
    }

    build() {
            Column() {}
            List() {}
    }
}