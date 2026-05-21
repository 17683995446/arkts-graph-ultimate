@Component
export struct BadComponent { // no closing }
@State count = 0;
    build() {
        Text('Hi');
    }
// missing closing
