import sys, urllib2, urllib, json

class GoogleNews:
	def __init__(self):
		# generated using www.powered.com
		self.api_key = "ABQIAAAAZc_Mvna_WVgPgkwT1gSwjRRAl9AE7WC-Ben74K5qwJFz3kM_zBSBEb843fK-2olACIeRbL4GuxsVxg"
		self.user_ip = ""
		
	def print_search_results(self, raw_query):	
		query_map = {'q': raw_query}
		encoded_query = urllib.urlencode(query_map)

		url = "https://ajax.googleapis.com/ajax/services/search/news?v=1.0&"
		url += encoded_query
		url += "&key=" + self.api_key + "&userip=" + self.user_ip
		
		# my old company as the referrer, doesn't really matter but didn't want to use reddwerks for some reason
		request = urllib2.Request(url, None, {'Referer': 'http://www.powered.com/'})
		response = urllib2.urlopen(url)

		# Process the JSON string.
		response_text = response.read()
		response_json = json.loads(response_text)
		for result in response_json['responseData']['results']:
			print result['title']
			print
			
if (len(sys.argv) == 1):
	print "Specify a news search query"
else:		
	news = GoogleNews()
	news.print_search_results(sys.argv[1])			