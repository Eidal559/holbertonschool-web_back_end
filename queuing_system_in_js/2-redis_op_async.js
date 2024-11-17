import { createClient, print } from 'redis';
import { promisify } from 'util';

// Create Redis client
const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.error('Redis client not connected to the server:', err.message);
});

// Promisify the get method
const getAsync = promisify(client.get).bind(client);

/**
 * Function to set a key-value pair in Redis.
 */
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, print);
}

/**
 * Async function to get the value of a key from Redis.
 */
async function displaySchoolValue(schoolName) {
    try {
        const result = await getAsync(schoolName);
        console.log(result);
    } catch (err) {
        console.error('Error fetching value:', err.message);
    }
}

// Example usage
async function main() {
    displaySchoolValue('Holberton');
    setNewSchool('HolbertonSanFrancisco', '100');
    displaySchoolValue('HolbertonSanFrancisco');
}

main().finally(() => {
    console.log('Closing Redis client...');
    client.quit();
});
