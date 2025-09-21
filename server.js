const express = require('express');
const path = require('path');
const app = express();

// Servir les fichiers statiques
app.use(express.static(__dirname));

// Routes principales
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'auth_interface.html'));
});

app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'modern_dashboard.html'));
});

app.get('/analysis', (req, res) => {
    res.sendFile(path.join(__dirname, 'analysis_interface.html'));
});

// Port
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
