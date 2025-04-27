const { page } = require('../auth/login');

async function sendMessage(phoneNumber, message) {
  await page.goto(`https://web.whatsapp.com/send?phone=${phoneNumber}&text=${encodeURIComponent(message)}`, {
    waitUntil: 'networkidle2'
  });

  await page.waitForSelector('span[data-icon="send"]', { timeout: 60000 });
  await page.click('span[data-icon="send"]');

  console.log(`📩 Sent to ${phoneNumber}`);
}

module.exports = { sendMessage };
