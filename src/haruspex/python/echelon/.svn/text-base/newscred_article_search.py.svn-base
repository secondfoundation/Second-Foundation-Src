# Check out this site for the python guide
# http://newscred.com/developer/quickstarts/python

import sys, newscred

if (len(sys.argv) == 1):
	print 'Specify an article search query'
else:
	# the key on the website, for minimal development
	access_key = "c4bcc3f7c9bf9ec159f51da0a86ca658"
	query = sys.argv[1]

	# Search articles with custom arguments
	options = {}
	options['offset'] = 0
	options['pagesize'] = 10
	options['from_date'] = '2012-01-01'

	options['to_date'] = '2012-01-24'
	options['sort'] = 'relevance'
	
	# other option examples
	# options['sources'] = ['1ce0362f2e764a95b0c7351c05a4eb19', '2c20eeebd3486973559db5b654d87771']
	# options['source_countries'] = ['us', 'uk', 'in', 'qa', 'ca']
	# options['categories'] = ['world', 'u-k', 'u-s', 'sports', 'business', 'technology']

	filtered_articles = newscred.NewsCredArticle.search(access_key=access_key, query=query, options=options)
	
	i = 0
	for article in filtered_articles:
		i += 1
		print "Result Number: " + str(i)
		print "Title: " + article.title
		print "Source: " + article.source
		print "Desc: " + article.description
		print "Category: " + article.category
		print