
/**
 * 极度混乱的文件1 - 超长方法名、超多层嵌套
 */
@Component
export struct ExtremelyLongClassNameForTestingPurposesBecauseWeNeedReallyLongNamesToBreakThings {
    private aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble: number = 0;
    
    // 超长方法名
    thisIsAnExtremelyLongMethodNameThatIsWayTooLongAndProbablyShouldBeShorterButWeAreMakingItEvenLongerJustToSeeWhatHappens(): void {
        console.log('超长方法');
        this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble = 42;
        
        // 多层嵌套
        if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 0) {
            if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 10) {
                if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 20) {
                    if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 30) {
                        if (this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble > 40) {
                            console.log('嵌套到了第5层！');
                        }
                    }
                }
            }
        }
    }
    
    anotherLongMethodThatAlsoDoesNotNeedToBeSoLongButHereWeAreAgain(): void {
        let result = this.aVeryLongVariableNameThatIsUnnecessarilyLongButWeAreMakingItEvenLongerOnPurposeToCauseTrouble + 1;
        console.log(result);
    }
    
    build() {
        Column() {
            Text('超级混乱组件');
        }
    }
}

// 另一个类
@Component
export struct AnotherChaosClass {
    private counter: number = 0;
    
    method1(): void {
        this.method2();
    }
    
    method2(): void {
        this.method3();
    }
    
    method3(): void {
        this.method4();
    }
    
    method4(): void {
        this.method5();
    }
    
    method5(): void {
        this.counter++;
    }
    
    build() {
        Row() {}
    }
}
