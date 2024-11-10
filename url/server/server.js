const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

// Initialize the Express app
const app = express();
const PORT = process.env.PORT || 3001;

// Set up SQLite database connection
const db = new sqlite3.Database('./database.db', (err) => {
    if (err) {
        console.error('Error opening database:', err);
    } else {
        console.log('Database connected successfully');
    }
});

// Create table if it doesn't exist
db.run(`CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)`);

// Middlewares
app.use(cors());
app.use(bodyParser.json());

// Function to generate a short code
const generateShortCode = () => Math.random().toString(36).substring(2, 8);

// Route to shorten the URL
app.post('/shorten', (req, res) => {
    const { longUrl } = req.body;
    if (!longUrl) {
        return res.status(400).json({ error: 'No URL provided' });
    }

    const shortCode = generateShortCode();
    db.run(
        'INSERT INTO urls (long_url, short_code) VALUES (?, ?)',
        [longUrl, shortCode],
        function (err) {
            if (err) {
                console.error('Error inserting data:', err);
                return res.status(500).json({ error: 'Failed to shorten URL' });
            }

            const shortUrl = `http://localhost:${PORT}/${shortCode}`;
            console.log(`URL shortened: ${longUrl} -> ${shortUrl}`);

            res.json({ shortUrl, shortCode });
        }
    );
});

// Route to redirect to the original URL using short code
app.get('/:shortCode', (req, res) => {
    const { shortCode } = req.params;
    db.get('SELECT long_url FROM urls WHERE short_code = ?', [shortCode], (err, row) => {
        if (err) {
            console.error('Error querying database:', err);
            return res.status(500).send('Server error');
        }

        if (row) {
            console.log(`Redirecting shortCode ${shortCode} to ${row.long_url}`);
            res.redirect(row.long_url);
        } else {
            console.warn(`Short code not found: ${shortCode}`);
            res.status(404).send('URL not found');
        }
    });
});

// Route to view all stored URLs (for testing purposes)
app.get('/urls', (req, res) => {
    db.all('SELECT * FROM urls', [], (err, rows) => {
        if (err) {
            console.error('Error querying database:', err);
            return res.status(500).send('Server error');
        }
        res.json(rows);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
