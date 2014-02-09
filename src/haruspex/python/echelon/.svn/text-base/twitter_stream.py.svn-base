import sys, pycurl, urllib, json
import signal

USER = "jayawilson85"
PASS = "blargness1"

def signal_handler(signal, frame):
	print '\nSIGINT Received: Ctrl+C!'
	print 'Exiting with Grace'
	sys.exit(0)

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
			print content['text']
			self.buffer = ""

if (len(sys.argv) == 1):
  	print 'Specify a comma-separated list of keywords to listen for'
else:  
  	signal.signal(signal.SIGINT, signal_handler)
  	client = Client(sys.argv[1])

