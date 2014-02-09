import sys, pycurl, urllib, json
import string
import sentiment
import glob

# credentials
USER = "jayawilson85"
PASS = "blargness1"

class Client:
	def __init__(self, keyword_list):
		query_map = {'track': keyword_list}
		encoded_query = urllib.urlencode(query_map)
	
		stream_url = "https://stream.twitter.com/1/statuses/filter.json?" + encoded_query
		self.buffer = ""
		self.conn = pycurl.Curl()
		self.conn.setopt(pycurl.USERPWD, "%s:%s" % (USER, PASS))
		self.conn.setopt(pycurl.URL, stream_url)
		self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
		self.conn.perform()

	def on_receive(self, data):
		self.buffer += data
		# chunks of data will end with new line
		if data.endswith("\r\n") and self.buffer.strip():
			# parse string into JSON object
			content = json.loads(self.buffer)
			
			# grab tweet, calc sentiment, output
			tweet = content['text']
			coef = sentiment.parse_tweet(tweet)

			print ""			
			self.buffer = ""

# RELEASE THE TWEET!
def tweet_stream(tweet):

	# read in lists of postitive and negative sentiment 	
	glob.pos = sentiment.read_sentiment_data("data/positive-words.txt")
	glob.neg = sentiment.read_sentiment_data("data/negative-words.txt")

	# stream tweets
	client = Client(sys.argv[1])
		
