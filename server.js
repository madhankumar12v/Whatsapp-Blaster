// Import required libraries
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const puppeteer = require('puppeteer');
const dotenv = require('dotenv');
const { sendBlastMessages } = require('./src/messages/messageSender');
const { showLoginPage, login } = require('./src/auth/login');

// Load environment variables
dotenv.config();

// Initialize Express app
const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse incoming requests
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'assets')));

// Serve the login page
app.get('/login', showLoginPage);

// Handle login
app.post('/login', login);

// Serve the dashboard page (only if logged in)
app.get('/dashboard', (req, res) => {
  // Check if user is logged in
  if (!loggedIn) {
    return res.redirect('/login');
  }
  res.sendFile(path.join(__dirname, 'assets/dashboard.html'));
});

// API endpoint to trigger WhatsApp message blast
app.post('/send-blast', async (req, res) => {
  // Extract data from the request body
  const { clients, messageTemplate } = req.body;

  try {
    // Send messages using Puppeteer and the message sender function
    await sendBlastMessages(clients, messageTemplate);
    res.status(200).json({ success: true, message: 'Blast sent successfully' });
  } catch (error) {
    console.error('Error sending blast:', error);
    res.status(500).json({ success: false, message: 'Failed to send blast' });
  }
});

// Handle real-time tracking (Example endpoint)
app.get('/tracking', (req, res) => {
  // You can provide real-time stats like success/fail counts
  res.json({
    successCount: successCount,
    failCount: failCount,
    pendingCount: pendingCount,
  });
});

// Handle logging out (reset login status)
app.get('/logout', (req, res) => {
  loggedIn = false;
  res.redirect('/login');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// Handle unhandled routes
app.use((req, res, next) => {
  res.status(404).send('Page Not Found');
});
