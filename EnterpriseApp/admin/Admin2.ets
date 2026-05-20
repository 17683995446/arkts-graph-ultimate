import { Logger } from '../common/Logger';
import { Database } from '../common/Database';
import { Network } from '../common/Network';

export class Admin21Service {
    private logger: Logger;
    private db: Database;
    private network: Network;

    constructor() {
        this.logger = new Logger();
        this.db = new Database();
        this.network = new Network();
    }

    initialize(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    fetchData(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    processRequest(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    saveState(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    validateInput(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    transformData(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    handleError(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

    cleanup(input?: any): Promise<any> {
        this.logger.log('Starting...');
        try {
            const data = this.db.query('SELECT * FROM table');
            const result = this.network.post('/api', data);
            this.logger.log('Completed!');
            return Promise.resolve(result);
        } catch (error) {
            this.handleError(error);
            return Promise.reject(error);
        }
    }

}
