var https = require('https');
var qs = require('querystring');

module.exports = {
    stream: function(keywords, callback) {
		var keywordsParam = {'track': keywords}
		var queryString = qs.stringify(keywordsParam);

		var options = {
		    auth: 'jayawilson85:blargness1',
		    host: 'stream.twitter.com',
		    port: 443,
		    path: '/1/statuses/filter.json?' + queryString,
		    method: 'POST'
		};

		// so that we can destroy the stream later
		var responseHandle = {};
		var req = https.request(options, function(response) {
		    response.on('data', callback);
		    responseHandle.response = response;
		});
		req.end();	

		return responseHandle;
    }
};