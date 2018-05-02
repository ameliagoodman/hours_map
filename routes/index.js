var express = require('express');
var router = express.Router();
const pg = require('pg');
const path = require('path');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/maps';


/* GET home page. */
router.get('/', (req, res, next) => {
  res.sendFile('index.html');
});


// GET ALL ARTICLES
router.get('/api/v1/maps', (req, res, next) => {
  const results = [];
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err});
    }
    // SQL Query > Select Data
    const query = client.query('SELECT * FROM locations where pub_date not like \'%02\' and pub_date not like \'%03\' and pub_date not like \'%04\' and pub_date not like \'%05\' and pub_date not like \'%06\' and pub_date not like \'%07\';');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
      return res.json(results);
    });
  });
});

module.exports = router;
