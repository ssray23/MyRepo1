// Start a little Web Server on your local computer
// Once you have run this script (i.e. "node myFirst.js") from the terminal or command prompt via "node myFirst.js"
// start your internet browser, and type in the address: http://localhost:8080

// If below code changes, you will have to restart the web server by re-running "node myFirst.js" again from command line
// and revisiting  http://localhost:8080 on your browser again..

var http = require('http');

// The function passed into the http.createServer() method, will be executed when someone tries to access the computer on port 8080.
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end('Hello World of Node JS .. Howdy?');
}).listen(8080);