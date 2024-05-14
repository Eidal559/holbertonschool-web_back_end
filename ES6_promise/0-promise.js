function getResponseFromAPI() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const response = "This is the response from the API";

      resolve(response);

    }, 2000);
  });
}

  export default getResponseFromAPI;
