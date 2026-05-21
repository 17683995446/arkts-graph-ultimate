import { B } from './module-b';
export class A {
    doSomething() {
        return new B().getValue();
    }
    getValue() { return 42; }
}
