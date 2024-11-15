const request = require('request');
const { expect } = require('chai');

describe('Index page', () => {
  const baseUrl = 'http://localhost:7865';

  it('should return status code 200 for GET /', (done) => {
    request.get(`${baseUrl}/`, (error, response, body) => {
      expect(response.statusCode).to.equal(200);
      expect(body).to.equal('Welcome to the payment system');
      done();
    });
  });
});

describe('Cart page', () => {
  const baseUrl = 'http://localhost:7865/cart';

  it('should return status code 200 when id is a number', (done) => {
    request.get(`${baseUrl}/123`, (error, response, body) => {
      expect(response.statusCode).to.equal(200);
      expect(body).to.equal('Payment methods for cart 123');
      done();
    });
  });

  it('should return status code 404 when id is not a number', (done) => {
    request.get(`${baseUrl}/abc`, (error, response, body) => {
      expect(response.statusCode).to.equal(404);
      done();
    });
  });
});
