import { createClient } from 'redis';

async function connectRedis() {
    const client = createClient();

    client.on('connect', () => {
        console.log('Redis client connected to the server');
    });

    client.on('error', (err) => {
        console.error('Redis client not connected to the server:', err.message);
    });

    try {
        await client.connect();
    } catch (err) {
        console.error('Connection failed:', err.message);
    }
}

connectRedis();
