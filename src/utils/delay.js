const { minDelay, maxDelay } = require('../../config/settings');

function randomDelay() {
  const delay = Math.floor(Math.random() * (maxDelay - minDelay) + minDelay);
  return new Promise(resolve => setTimeout(resolve, delay));
}

module.exports = { randomDelay };
