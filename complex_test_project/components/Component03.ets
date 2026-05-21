
@Component
export struct CustomComp003 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.process1();
        this.process1();
    }

    onClick1(): void {
        this.onClick0();
        this.execute5();
    }

    onClick2(): void {
        this.execute7();
        this.fetch9Data();
    }

    build() {
            List() {}
            Button() {}
    }
}
@Component
export struct CustomComp103 {
@State value0: number = 0;
@State value1: number = 0;
@State value2: number = 0;


    onClick0(): void {
        this.value0++;
    }

    onClick1(): void {
        this.process0();
        this.fetch5Data();
    }

    onClick2(): void {
        this.execute2();
        this.fetch2Data();
    }

    build() {
            Button() {}
            Text() {}
    }
}