const puppeteer = require('puppeteer');
const { delay } = require('../utils/delay');
const { randomMouseMove } = require('../utils/whatsappHelper');
const { minDelay, maxDelay } = require('../../config/settings');

async function sendBlastMessages(clients, messageTemplate) {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://web.whatsapp.com');

  console.log('Please scan QR code manually...');

  await page.waitForSelector('._2_1wd'); // Wait for search input after login

  for (const client of clients) {
    try {
      await randomMouseMove(page);

      await page.click('._2_1wd');
      await delay(500);
      await page.keyboard.type(client.number);
      await delay(1000);

      await page.keyboard.press('Enter');
      await delay(1500);

      const personalizedMessage = messageTemplate.replace('{{name}}', client.name);

      for (const char of personalizedMessage) {
        await page.keyboard.type(char);
        await delay(Math.random() * 150); // random small typing delay
      }

      await page.keyboard.press('Enter');
      console.log(`✅ Message sent to ${client.name}`);

      const randomDelay = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;
      await delay(randomDelay);
    } catch (error) {
      console.error(`❌ Failed to send message to ${client.name}:`, error);
    }
  }

  console.log('🎯 All messages sent!');
  await browser.close();
}

module.exports = { sendBlastMessages };
