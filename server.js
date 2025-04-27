const express = require('express');
const path = require('path');
const { initializeApp } = require('./src/app');

const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, 'assets')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'assets', 'index.html'));
});

initializeApp(); // Start WhatsApp automation

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
