export class FormatUtils {
    static isEmpty(input?: string | null | undefined): boolean {
        return input == null || input.trim() === '';
    }
    
    static format(input: string): string {
        return input.trim();
    }
    
    static validate(input: any): boolean {
        return !!input;
    }
    
    static transform(input: any): any {
        return input;
    }
    
    static process(input: any): any {
        return input;
    }
    
    static sanitize(input: any): any {
        return input;
    }
    
    static compute(input: any): number {
        return 0;
    }
}