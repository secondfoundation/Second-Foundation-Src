import sys, urllib, json
import signal
import pickle

def signal_handler(signal, frame):
	print '\nSIGINT Received: Ctrl+C!'
	print 'Exiting with Grace'
	sys.exit(0)

class BingSearch:
	def __init__(self):
		self.app_key = "3ACAE85BE582DF3D67AA7EAC607DAF3A498F76FE"
		
	def print_news_results(self, raw_query):
		encoded_query = urllib.urlencode({'Query': raw_query})
		url = "http://api.bing.net/json.aspx?"
		url += "AppId=" + self.app_key + "&Version=2.2&Market=en-US&Sources=news&Web.Count=1&JsonType=raw&"
		url += encoded_query
		
		response = urllib.urlopen(url)
		response_text = response.read()
		response_json = json.loads(response_text)

		# trying query
		try:
			i = 0
			for news_result in response_json['SearchResponse']['News']['Results']:
				i += 1
				print "Result Number: " + str(i)
				print "Title: " + news_result['Title']
				print "Snippet: " + news_result['Snippet']
				print "Link: " + news_result['Url']
				print
		# query failed, catching exception
		except:
			news_result = "invalid query"
			e = sys.exc_info()[1]
			print e

	def get_news_pages(self, raw_query):
		encoded_query = urllib.urlencode({'Query': raw_query})
		url = "http://api.bing.net/json.aspx?"
		url += "AppId=" + self.app_key + "&Version=2.2&Market=en-US&Sources=news&Web.Count=1&JsonType=raw&"
		url += encoded_query

		response = urllib.urlopen(url)
		response_text = response.read()
		response_json = json.loads(response_text)

		# trying query
		try:
			i = 0
			list = []
			for news_result in response_json['SearchResponse']['News']['Results']:
				i += 1
				element = news_result['Url']
				list.append(element)
			with open('news.tmp', 'wb') as f:
				pickle.dump(list,f)
		# query failed, catching exception
		except:
			news_result = "invalid query"
			e = sys.exc_info()[1]
			print e


if(len(sys.argv) == 1):
	print "Specify a news search query"
elif(str(sys.argv[1]) == 'see'):	
	signal.signal(signal.SIGINT, signal_handler)
	news = BingSearch()
	news.print_news_results(sys.argv[2])			
elif(str(sys.argv[1]) == 'get'):
	signal.signal(signal.SIGINT, signal_handler)
	news = BingSearch()
	news.get_news_pages(sys.argv[2])
else:
	print 'Use \'see\' argument to see summary of news results'
	print 'Use \'get\' argument to get web pages of news results'
