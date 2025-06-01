const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 9080;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:9090';

// Enable CORS for all routes
app.use(cors());

// Create a config.js file with the backend URL
const configContent = `window.CONFIG = {
  API_URL: "${BACKEND_URL}/ask"
};`;

fs.writeFileSync(path.join(__dirname, 'config.js'), configContent);

// Serve static files from the current directory
app.use(express.static(__dirname));

// Serve index.html for all routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(PORT, () => {
  console.log(`Frontend server running at http://localhost:${PORT}`);
  console.log(`Using backend API at ${BACKEND_URL}`);
});
