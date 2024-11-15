const request = require('request');
const { expect } = require('chai');

const baseUrl = 'http://localhost:7865';

describe('API Integration Tests', () => {
  describe('GET /available_payments', () => {
    it('should return the correct payment methods', (done) => {
      request.get(`${baseUrl}/available_payments`, (error, response, body) => {
        const expectedResponse = {
          payment_methods: {
            credit_cards: true,
            paypal: false,
          },
        };
        expect(response.statusCode).to.equal(200);
        expect(JSON.parse(body)).to.deep.equal(expectedResponse);
        done();
      });
    });
  });

  describe('POST /login', () => {
    it('should return a welcome message when userName is provided', (done) => {
      const options = {
        url: `${baseUrl}/login`,
        method: 'POST',
        json: true,
        body: { userName: 'Betty' },
      };

      request(options, (error, response, body) => {
        expect(response.statusCode).to.equal(200);
        expect(body).to.equal('Welcome Betty');
        done();
      });
    });

    it('should return 400 status code when userName is not provided', (done) => {
      const options = {
        url: `${baseUrl}/login`,
        method: 'POST',
        json: true,
        body: {},
      };

      request(options, (error, response, body) => {
        expect(response.statusCode).to.equal(400);
        expect(body).to.equal('Username is required');
        done();
      });
    });
  });
});
