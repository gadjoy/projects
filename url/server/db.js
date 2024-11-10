// db.js
const { Pool } = require('pg');

const pool = new Pool({
    user: 'yourUsername',       // Confirmed from POSTGRES_USER
    host: 'localhost',          // Host remains localhost
    database: 'url_shortener',  // Confirmed from POSTGRES_DB
    password: 'yourPassword',   // Confirmed from POSTGRES_PASSWORD
    port: 5432,                 // Default PostgreSQL port
});

module.exports = pool;
