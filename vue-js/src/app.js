var express = require('express')
var path = require('path')
var serveStatic = require('serve-static')
var app = express();
//app.use(serveStatic('./vue-js', {'index': ['index.html', 'vue.js','index.js','index.css']}))
app.use(serveStatic('./src', {'index': ['index.html']}))
//app.use(serveStatic(path.join(__dirname,'vue-js')))


app.listen(9000)
