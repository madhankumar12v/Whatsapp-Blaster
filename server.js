const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const puppeteer = require('puppeteer');
const { delay } = require('./src/utils/delay');
const { randomMouseMove } = require('./src/utils/whatsappHelper');
const { minDelay, maxDelay } = require('./config/settings');
const { clients } = require('./src/clients/clientData');
const { messageTemplate } = require('./src/messages/messageTemplates');
const { showDashboard } = require('./src/ui/dashboard');

require('dotenv').config();

const app = express();

// Middleware to parse JSON requests
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'assets')));

// Root route (serve landing page or dashboard)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'assets', 'index.html'));
});

// Client data for WhatsApp blasting
let clientList = [];

// Handle adding clients via API (for internal use)
app.post('/add-client', (req, res) => {
  const { name, number } = req.body;

  if (!name || !number) {
    return res.status(400).send({ error: 'Name and Number are required' });
  }

  clientList.push({ name, number });
  res.status(200).send({ message: 'Client added successfully' });
});

// Handle WhatsApp Blasting
app.post('/start-blast', async (req, res) => {
  const { clients } = req.body;

  if (!clients || clients.length === 0) {
    return res.status(400).send({ error: 'No clients to send messages' });
  }

  // Start the WhatsApp message sending process
  try {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('https://web.whatsapp.com');

    console.log('Please scan QR code manually...');

    // Wait until the user logs in (check for chat search box)
    await page.waitForSelector('._2_1wd');
    
    for (const client of clients) {
      try {
        await randomMouseMove(page);
        await page.click('._2_1wd');
        await delay(500);
        await page.keyboard.type(client.number);
        await delay(1000);
        await page.keyboard.press('Enter');
        await delay(1500);

        // Personalize the message
        const personalizedMessage = messageTemplate.replace('{{name}}', client.name);

        // Type message letter by letter (human-like)
        for (const char of personalizedMessage) {
          await page.keyboard.type(char);
          await delay(Math.random() * 150); // random typing speed
        }

        await page.keyboard.press('Enter');
        console.log(`✅ Message sent to ${client.name}`);

        // Random delay between messages
        const randomDelay = Math.floor(Math.random() * (maxDelay - minDelay + 1)) + minDelay;
        await delay(randomDelay);

      } catch (error) {
        console.error(`❌ Failed to send message to ${client.name}:`, error);
      }
    }

    console.log('🎯 All messages sent!');
    await browser.close();
    res.json({ message: 'Blast completed successfully!' });
  } catch (error) {
    console.error('Error during blasting:', error);
    res.status(500).send({ error: 'Error during WhatsApp blasting' });
  }
});

// Serve the dashboard after login
app.get('/dashboard', (req, res) => {
  showDashboard();
  res.send('Dashboard is live!');
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🌟 Server started at http://localhost:${PORT}`);
});
