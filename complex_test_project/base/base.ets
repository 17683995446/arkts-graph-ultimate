
export class BaseClass {
    protected id: string = '';
    
    init(): void {
        this.id = this.generateId();
    }
    
    generateId(): string {
        return Math.random().toString(36).substring(2);
    }
    
    toJSON(): object {
        return { id: this.id };
    }
    
    fromJSON(json: any): void {
        if (json.id) this.id = json.id;
    }
}

export class BaseService {
    protected cache: Map<string, any> = new Map();
    
    setCache(key: string, value: any): void {
        this.cache.set(key, value);
    }
    
    getCache(key: string): any {
        return this.cache.get(key);
    }
    
    clearCache(): void {
        this.cache.clear();
    }
    
    hasCache(key: string): boolean {
        return this.cache.has(key);
    }
}
