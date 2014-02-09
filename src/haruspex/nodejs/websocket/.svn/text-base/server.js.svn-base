var http = require('http');
var socketio = require('socket.io');
var fs = require('fs');
var twitter = require('./twitter');
var sentiment = require('./sentiment');
var express = require('express');
var mongo = require('mongodb');
var urlparser = require('url');

/*
	*** Load sentiment and stop words ***
*/
var dataPath = 'data';
// load positive and negative sentament words (block)
sentiment.parseFiles(dataPath);
// load stopwords (block)
var stopwords;
fs.readFile(dataPath + '/stopwords.txt', function(err, data) {
	stopwords = data.toString().split('\n');
});

/*
	*** create app server and web socket listener ***
*/
var app = express.createServer();
app.use(express.bodyParser());
app.post('/login', login)
app.get('/*', authFilter, express.static(__dirname + '/public'));

// wrap in http server so that socket io can be used
var port = 80;
app.listen(port);
var io = socketio.listen(app);
console.log('Server started on port ' + port);

/*
	*** connect to mongodb ***
*/
var dbserver = new mongo.Server('23.23.187.186', 27017, {});
var dbconn = new mongo.Db('haruspex', dbserver, {});
var dbUsers;
var dbAudit;
dbconn.open( function(err, db) {
	dbUsers = new mongo.Collection(db, 'users');
	dbAudit = new mongo.Collection(db, 'audit');
});

// map of query string to socket ids
var queryListeners = {};
// map of socket id to term infos
var termInfos = {};
// map of socket id to array of non-zero sentiment values
var sentimentPoints = {};

// query string for stream filter
var queryArray = [];

// handle to twitter stream
var twitterStream;

// authenticated users
var authUsers = {};

io.sockets.on('connection', function(socket) { 
	var ip = socket.handshake.address.address;
	console.log('Socket connected: id: ' + socket.id + ' address: ' + ip);
	
	socket.on('startStream', function(data) {
		console.log('Socket started stream: ' + socket.id);
		var q = data.query.toUpperCase();
		var username = data.username;
		
		// add socket to listeners of this query
		if (typeof(queryListeners[q]) == 'undefined') {
			queryListeners[q] = new Array();
		}
		queryListeners[q].push(socket.id);
		socket.query = q;
		socket.username = username;
		
		log(username, ip, 'start-stream', {query: q});
		
		// begin tracking top terms for this user
		termInfos[socket.id] = new TermInfo();
		
		// begin tracking avg sentiment for this user
		sentimentPoints[socket.id] = new Array();
		
		// check if the stream is listening to this query
		if (queryArray.indexOf(q) == -1) {
			console.log('Add term to query string: ' + q);		
			queryArray.push(q);
			refreshStream();
		} else {
			console.log('Add socket listening to ' + q + ' (remaining: ' + queryListeners[q].length + ')');
		}
	});
	
	socket.on('stopStream', function() {
		console.log('Stop streaming for socket ' + socket.id)
		stopSocket(socket.query, socket.id);
		if (typeof(socket.username) != 'undefined') {
			log(socket.username, ip, 'stop-stream', {query: socket.query});
		}
	});
	
	socket.on('disconnect', function() {
		console.log('Disconnected socket ' + socket.id);		
		stopSocket(socket.query, socket.id);
		if (typeof(socket.username) != 'undefined') {
			log(socket.username, ip, 'disconnect', {query: socket.query});
		}
	});
});

// process /login
function login(req, res) {
	var username = req.body.username;
	var password = req.body.password;
	var ip = req.connection.remoteAddress;
	
	dbUsers.findOne({username: username, password:password}, function(err, user) {
		if (user != null) {
			authUsers[username] = 1;
			log(username, ip, 'login', {password: password});
			res.redirect('/secure/stream.html?username=' + username);
		} else {
			console.log('User ' + username + ' failed to authenticate');
			log(username, ip, 'login-fail', {badPassword: password});
			res.redirect('/login.html?fail=true');
		}
	});
}

// process /secure
function authFilter(req, res, next) {
	url = urlparser.parse(req.url, true);	
	if (url.path.indexOf('/secure') != -1) {
		var userToken = url.query.username;
		var isAuth = authUsers[userToken];
		// check if this user has been authenticated
		if (typeof isAuth == 'undefined') {
			console.log('User is not authenticated: ' + userToken);
			res.redirect('/login.html?auth=false');
		} else {
			console.log('User is authenticated: ' + userToken);
			// next filter in connect stack
			next();
		}
	} else {
		next();
	}
}

function stopSocket(q, id) {
	delete termInfos[id];
	delete sentimentPoints[id];

	if (typeof(q) != 'undefined') {
		var i = queryListeners[q].indexOf(id);
		if (i != -1) {
			queryListeners[q].splice(i, 1);
			// check if this was the last socket listening to this query
			if (queryListeners[q].length == 0) {
				console.log('Remove term from query string: ' + q);
				i = queryArray.indexOf(q);
				if (i != -1) {
					queryArray.splice(i, 1);
					refreshStream();
				}
			} else {
				console.log('Remove socket listening to ' + q + ' (remaining: ' + queryListeners[q].length + ')');
			}
		}
	} else {
		console.log('Socket had no query defined: ' + id);
	}
}

function refreshStream() {	
	var queryString = queryArray.toString();
	
	// close current twitter stream if exists
	if (typeof(twitterStream) != 'undefined') {
		twitterStream.response.destroy();
	}
	
	if (queryString.length > 0) {
		console.log('Tracking: ' + queryString);
		twitterStream = twitter.stream(queryString, function(chunk) {
			try {
				var text = JSON.parse(chunk).text
				deliverTweet(text);
			} catch (e) {
				console.log('Error: could not parse tweet JSON: ' + chunk);
			}	
		});
	}
}

function deliverTweet(text) {
	queryArray.map( function(query) {
		if (text.toUpperCase().indexOf(query) != -1) {
			queryListeners[query].map( function(listenerId) {
				var listenerSocket = io.sockets.sockets[listenerId];
				if (typeof(listenerSocket) == 'undefined') {
					console.log('Warning: tried to deliver tweet to disconnected socket: ' + socket.id);
				} else {					
					var info = termInfos[listenerId];
					info.update(query, text);
					var terms = info.topTermCounts(10);
				
					var coef = sentiment.getCoefficient(text);
				
					var avg = 0;
					// only average non-zero sentiment values
					// since sentiment is zero when none of the words appear in the tweet, the average will always tend towards zero
					// if they are included
					if (coef != 0) {					
						var sents = sentimentPoints[listenerId];
						sents.push(coef);
					
						var sum = 0;
						sents.map( function(sent) {
							sum += sent;
						});
						avg = sum / sents.length;
					}
				
					listenerSocket.emit('tweet', {tweet: text, terms: terms, coef: coef, avg: avg});
				}
			});
		}
	});
}

function log(username, ip, action, details) {
	var log = {username: username, ip: ip, action: action, timestamp: new Date().getTime(), details: details};
	dbAudit.insert(log, {}, function(err, records){});
}

function TermInfo() {
	var termCounts = {};
	
	this.update = function(query, text) {
		var terms = text.split(' ');
		terms.map( function(term) {
			if (stopwords.indexOf(term.toLowerCase()) == -1 && term.match(/[0-9a-zA-Z]/) && query.indexOf(term.toUpperCase()) == -1) {
				var count = termCounts[term];
				if (count != null) {
					termCounts[term]++;
				} else {
					termCounts[term] = 1;
				}
			}
		});
	}
	
	this.topTermCounts = function(count) {
		// convoluted way to sort
		var arr = [];
		for (term in termCounts) {
			arr.push({word: term, total: termCounts[term]});
		}
		arr.sort( function(term1, term2) {
			return term1.total - term2.total;
		});
		return arr.slice(arr.length - count, arr.length);
	}
}
