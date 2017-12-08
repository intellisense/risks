let webpack = require('webpack');
let WebpackDevServer = require('webpack-dev-server');
let config = require('./webpack.config');

// Dev server address specified in webpack.config.js
let listenAddr = 'localhost';
// Dev server port specified in webpack.config.js
let listenPort = 3000;

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  inline: true,
  headers: { 'Access-Control-Allow-Origin': '*' },
  historyApiFallback: true
}).listen(listenPort, listenAddr, function (err, result) {
  if (err) {
    console.log(err);
  }
  console.log('Listening at ' + listenAddr + ':' + listenPort);
});
