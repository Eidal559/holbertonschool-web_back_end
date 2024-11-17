import { createClient } from 'redis';
import kue from 'kue';
import express from 'express';
import { promisify } from 'util';

const app = express();
const queue = kue.createQueue();
const redisClient = createClient();
const PORT = 1245;

const DEFAULT_SEATS = 50;
let reservationEnabled = true;

// Promisified Redis methods
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize available seats
async function initializeSeats() {
    await setAsync('available_seats', DEFAULT_SEATS);
}

// Function to reserve a seat
async function reserveSeat(number) {
    await setAsync('available_seats', number);
}

// Function to get current available seats
async function getCurrentAvailableSeats() {
    const seats = await getAsync('available_seats');
    return parseInt(seats, 10);
}

// GET /available_seats: Returns the number of available seats
app.get('/available_seats', async (req, res) => {
    const seats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats: seats });
});

// GET /reserve_seat: Queues a reservation request
app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        res.json({ status: 'Reservation in process' });
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
});

// GET /process: Processes the queue
app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });

    queue.process('reserve_seat', async (job, done) => {
        const currentSeats = await getCurrentAvailableSeats();

        if (currentSeats <= 0) {
            reservationEnabled = false;
            done(new Error('Not enough seats available'));
            return;
        }

        const updatedSeats = currentSeats - 1;
        await reserveSeat(updatedSeats);

        if (updatedSeats === 0) {
            reservationEnabled = false;
        }

        done();
    });
});

// Start the server
app.listen(PORT, async () => {
    await initializeSeats();
    console.log(`API server is running on http://localhost:${PORT}`);
});
