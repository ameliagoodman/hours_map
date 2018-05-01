const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/maps';

const client = new pg.Client(connectionString);
client.connect();
const query = client.query(
  'CREATE TABLE locations (location TEXT, link TEXT, pub_date TEXT, lat FLOAT, long FLOAT, added TIMESTAMP DEFAULT now(), PRIMARY KEY (link)'
);
query.on('end', () => { client.end(); });