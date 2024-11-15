const express = require('express');
const app = express();
const PORT = 7865;

app.use(express.json());

// Root endpoint
app.get('/', (req, res) => {
  res.send('Welcome to the payment system');
});

// GET /available_payments endpoint
app.get('/available_payments', (req, res) => {
  const paymentMethods = {
    payment_methods: {
      credit_cards: true,
      paypal: false,
    },
  };
  res.json(paymentMethods);
});

// POST /login endpoint
app.post('/login', (req, res) => {
  const { userName } = req.body;
  if (userName) {
    res.send(`Welcome ${userName}`);
  } else {
    res.status(400).send('Username is required');
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`API available on localhost port ${PORT}`);
});

module.exports = app;
