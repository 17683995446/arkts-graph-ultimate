export class SpecialChars {
    chinese = "测试中文";
    japanese = "日本語";
    korean = "한국어";
    emoji = "🚀🔥💻";
    math = "∑∞∫√π";
    symbols = "©®™§¶†‡";
    
    workWithText() {
        let text = this.chinese + this.japanese + this.korean;
        console.log(text);
    }
}
