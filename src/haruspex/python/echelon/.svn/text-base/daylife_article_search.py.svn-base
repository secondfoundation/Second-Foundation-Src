import sys, json, hashlib, urllib

class Daylife:
	def __init__(self):
		self.access_key = "8a1628869da6cb0b035b7fa6df57f1f9"
		self.shared_secret = "4fb8aad6379490d7cfb6fdd1a15767b6"
	
	def get_related_articles(self, raw_query, query_params):
		# signature depends on key and secret, as well as the raw query that was performed		
		signature = hashlib.md5(self.access_key + self.shared_secret + raw_query).hexdigest()
		
		query_map = {'query': raw_query}
		encoded_query = urllib.urlencode(query_map)
		
		search_url = "http://freeapi.daylife.com/jsonrest/publicapi/4.10/search_getRelatedArticles"	
		search_url = search_url + "?" + encoded_query + query_params + "&accesskey=" + self.access_key + "&signature=" + signature
		
		# no need to use pycurl to stream response, can wait for server to close connection
		response = urllib.urlopen(search_url)
		self.print_response_summary(response)
		
	def print_response_summary(self, response):
		response_text = response.read()
		response_json = json.loads(response_text)
		
		i = 0
		for article in response_json['response']['payload']['article']:
			i += 1
			# print some interesting fields
			print "Result Number: " + str(i)
			print "ID: " + article['article_id']
			print "Relevance: " + str(article['search_score'])
			print "Timestamp: " + article['timestamp']
			print "Headline: " + article['headline']
			print "Source: " + article['source']['name']
			print "Excerpt: " + article['excerpt']
			print "Link: " + article['url']
			print
		
if (len(sys.argv) == 1):
	print "Specify an article search query"
else:	
	# hard code some other params for now
	query_params = "&start_time=2012-01-17&end_time=2012-01-24&sort=relevance"	
	# other optional params that can be specified, blank for now
	# note default limit is 10 articles
	empty_params = "&offset=&limit=&source_filter_id=&include_image=&include_scores=&sliding_excerpt=&has_image=&block_nsfw=&source_whitelist=&source_blacklist="
		
	daylife = Daylife()
	daylife.get_related_articles(sys.argv[1], query_params + empty_params)	
			
