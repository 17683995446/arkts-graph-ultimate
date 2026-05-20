export class ApiService9 {
    async fetchUsers(): Promise<any[]> {
        const response = await this.get('/users');
        return response;
    }
    
    async createUser(user: any): Promise<any> {
        return await this.post('/users', user);
    }
    
    async updateUser(id: number, user: any): Promise<any> {
        return await this.put(`/users/${id}`, user);
    }
    
    async deleteUser(id: number): Promise<void> {
        return await this.delete(`/users/${id}`);
    }
    
    async get(url: string): Promise<any> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([]);
            }, 100);
        });
    }
    
    async post(url: string, data: any): Promise<any> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(data);
            }, 100);
        });
    }
    
    async put(url: string, data: any): Promise<any> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(data);
            }, 100);
        });
    }
    
    async delete(url: string): Promise<void> {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve();
            }, 100);
        });
    }
}