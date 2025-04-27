const puppeteer = require('puppeteer');
let successCount = 0;
let failCount = 0;
let pendingCount = 0;

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
      await page.keyboard.type(client.number);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(1000);

      const personalizedMessage = messageTemplate.replace('{{name}}', client.name);
      for (const char of personalizedMessage) {
        await page.keyboard.type(char);
        await delay(Math.random() * 150); // random typing delay
      }
      await page.keyboard.press('Enter');
      console.log(`✅ Message sent to ${client.name}`);

      successCount++;
    } catch (error) {
      console.error(`❌ Failed to send message to ${client.name}:`, error);
      failCount++;
    }
    pendingCount--;
    // Optional: Update stats real-time
    updateBlastStats();
  }

  await browser.close();
}

function updateBlastStats() {
  // Could update stats on a real-time dashboard (like via WebSocket)
  console.log(`Success: ${successCount}, Fail: ${failCount}, Pending: ${pendingCount}`);
}

module.exports = { sendBlastMessages };
