import { createClient, print } from 'redis';

// Create Redis client
const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (err) => {
    console.error('Redis client not connected to the server:', err.message);
});

/**
 * Function to set a key-value pair in Redis.
 * Uses the `print` callback for logging.
 */
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, print);
}

/**
 * Function to get the value of a key from Redis.
 * Logs the result to the console.
 */
function displaySchoolValue(schoolName) {
    client.get(schoolName, (err, result) => {
        if (err) {
            console.error('Error fetching value:', err.message);
        } else {
            console.log(result);
        }
    });
}

// Example usage
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
