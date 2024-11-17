import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Define the job data
const jobData = {
    phoneNumber: '1234567890',
    message: 'This is a test notification message'
};

// Create a job with the data
const job = queue.create('push_notification_code', jobData)
    .save((err) => {
        if (err) {
            console.error('Job creation failed:', err);
        } else {
            console.log(`Notification job created: ${job.id}`);
        }
    });

// Handle job completion
job.on('complete', () => {
    console.log('Notification job completed');
});

// Handle job failure
job.on('failed', () => {
    console.log('Notification job failed');
});
