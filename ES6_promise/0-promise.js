function getResponseFromAPI() {
    return new Promise((resolve, reject) => {
      // Simulate API call or any asynchronous operation
      setTimeout(() => {
        // Simulate a successful response
        const response = "This is the response from the API";

        // Resolve the promise with the response
        resolve(response);

      }, 2000); // Simulated delay of 2 seconds
    });
  }

  export default getResponseFromAPI;
