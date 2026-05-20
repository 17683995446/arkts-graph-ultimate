export class Database {
    query(sql: string): any[] {
        console.log(`Executing query: ${sql}`);
        return [];
    }
    insert(table: string, data: any) {
        console.log(`Inserting into ${table}`, data);
    }
}