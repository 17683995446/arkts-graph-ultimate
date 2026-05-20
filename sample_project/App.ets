@Entry
@Component
struct App {
    build() {
        Column() {
            Text("Hello World")
                .fontSize(30)
            Counter()
        }
        .width('100%')
        .height('100%')
    }
}

@Component
struct Counter {
    @State count: number = 0

    build() {
        Row() {
            Button("-")
                .onClick(() => {
                    this.count--
                })
            Text(this.count.toString())
                .fontSize(24)
                .width(50)
                .textAlign(TextAlign.Center)
            Button("+")
                .onClick(() => {
                    this.count++
                })
        }
        .padding(10)
    }
}
