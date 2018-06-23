// const mongodb = require('mongodb').MongoClient;
const monk = require('monk');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const serverless = require('serverless-http');
const express = require('express');

const app = express();
const db = monk(process.env.DB_URI);

// Middleware
app.use(bodyParser.json({ strict: false }));
app.use(morgan('dev'));

// Routes
app.get('/', (req, res) => res.send('Hello, world!'));
app.get('/deaths', (req, res) => {
  db.get('deaths').find({}).then(docs => res.json(docs));
});
app.post('/deaths', (req, res) => {
  const deaths = db.get('deaths');
  deaths.createIndex('name', { unique: true });
  console.log(req.body)
  deaths.insert([req.body])
    .then((docs) => {
      console.log(`Inserted ${docs}`);
      res.send(200);
    })
    .catch((err) => {
      console.log(err);
      res.sendStatus(500);
    });
});

module.exports.handler = serverless(app);
