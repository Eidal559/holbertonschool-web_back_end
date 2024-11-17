import { createClient } from 'redis';

// Create Redis client
const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.error('Redis client not connected to the server:', err.message);
});

// Subscribe to the channel
client.subscribe('holberton school channel');

// Handle received messages
client.on('message', (channel, message) => {
    console.log(`${message}`);
    if (message === 'KILL_SERVER') {
        client.unsubscribe();
        client.quit();
    }
});
