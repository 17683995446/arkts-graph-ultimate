export class MathUtils {
    static add(a: number, b: number): number {
        return a + b
    }

    static multiply(a: number, b: number): number {
        return a * b
    }
}

export class StringUtils {
    static capitalize(str: string): string {
        return str.charAt(0).toUpperCase() + str.slice(1)
    }

    static truncate(str: string, length: number): string {
        if (str.length <= length) return str
        return str.slice(0, length) + "..."
    }
}
