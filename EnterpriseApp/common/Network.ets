export class Network {
    get(url: string): Promise<any> {
        console.log(`GET ${url}`);
        return Promise.resolve({});
    }
    post(url: string, data: any): Promise<any> {
        console.log(`POST ${url}`, data);
        return Promise.resolve({});
    }
}