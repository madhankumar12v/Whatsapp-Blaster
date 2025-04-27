const puppeteer = require('puppeteer');

let browser, page;

async function loginToWhatsApp() {
  browser = await puppeteer.launch({
    headless: false,
    args: ['--start-maximized']
  });

  page = await browser.newPage();
  await page.goto('https://web.whatsapp.com');
  
  console.log('Please scan QR code...');

  await page.waitForSelector('canvas[aria-label="Scan me!"]', { timeout: 0 });
  await page.waitForSelector(`span[title="${process.env.WHATSAPP_USER_NAME}"]`, { timeout: 0 });

  console.log('Logged into WhatsApp successfully!');
}

module.exports = { loginToWhatsApp, page };
