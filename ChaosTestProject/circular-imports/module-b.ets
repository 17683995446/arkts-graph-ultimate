import { A } from './module-a';
export class B {
    doSomething() {
        return new A().getValue();
    }
    getValue() { return 1337; }
}
