const { loginToWhatsApp } = require('./auth/login');
const { sendBlastMessages } = require('./messages/messageSender');
const { clients } = require('./clients/clientData');
const { messageTemplate } = require('./messages/messageTemplates');
const { showDashboard } = require('./ui/dashboard');

async function initializeApp() {
  await loginToWhatsApp();
  showDashboard();
  await sendBlastMessages(clients, messageTemplate);
}

module.exports = { initializeApp };
