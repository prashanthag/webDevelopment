var express = require('express')
var path = require('path')
var serveStatic = require('serve-static')
var app = express();
//app.use(serveStatic('./vue-js', {'index': ['index.html', 'vue.js','index.js','index.css']}))
app.use(serveStatic('./vue-js', {'index': ['index.html']}))
app.use(serveStatic(path.join(__dirname,'vue-js')))

//Import the mongoose module
var mongoose = require('mongoose');

//Set up default mongoose connection
//var mongoDB = 'mongodb://localhosjt/db';
var mongoDB = 'mongodb://localhost/db';
mongoose.connect(mongoDB, { useNewUrlParser: true });

//Get the default connection
var db = mongoose.connection;

//Bind connection to error event (to get notification of connection errors)
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

app.listen(9000)
