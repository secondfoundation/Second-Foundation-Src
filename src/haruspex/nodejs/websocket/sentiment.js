var fs = require('fs');

var words = {};

module.exports = {
	getCoefficient: function(tweet) {
		tweetWords = tweet.split(' ');
		
		var p = 0;
		var n = 0;
		
		tweetWords.map( function(tweetWord) {
			if (words[tweetWord] == 0) {
				n++;
			}
			if (words[tweetWord] == 1) {
				p++;
			}
		});
		
		var coef = (p - n) / tweetWords.length * 1.0;
		
		return coef;
	},
	
	parseFiles: function(sentimentPath) {
		fs.readFile(sentimentPath + '/negative-words.txt', function(err, data) {
			negWords = data.toString().split('\n');
			negWords.map( function(word) {
				words[word] = 0;
			});
			
			fs.readFile(sentimentPath + '/positive-words.txt', function(err, data) {
				var posWords = data.toString().split('\n');
				posWords.map( function(word) {				
					words[word] = 1;
				});
			});
		});
		
		return words;
	}
}