const { expect } = require('chai');
const getPaymentTokenFromAPI = require('./6-payment_token');

describe('getPaymentTokenFromAPI', () => {
  it('should return a resolved promise with a success response when success is true', (done) => {
    getPaymentTokenFromAPI(true)
      .then((response) => {
        // Verify the response object
        expect(response).to.deep.equal({ data: 'Successful response from the API' });
        done(); // Call done to indicate the test is complete
      })
      .catch((error) => done(error)); // Handle any unexpected errors
  });
});
