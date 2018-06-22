// const mongodb = require('mongodb').MongoClient;
const monk = require('monk');

const serverless = require('serverless-http');
const express = require('express');

const app = express();
const db = monk(process.env.DB_URI);


app.get('/', (req, res) => res.send('Hello, world!'));

app.get('/deaths', (req, res) => {
  db.get('deaths').find({}).then(docs => res.json(docs));
});

app.post('/deaths', (req, res) => {
  res.sendStatus(400);
});


// app.listen(3000, () => console.log('uri:', process.env.DB_URI));
module.exports.handler = serverless(app);
