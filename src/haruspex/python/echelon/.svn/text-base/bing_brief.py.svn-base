#Concatenate this with a program that generates the top trending terms

import sys, urllib, json

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

                i = 0
                for news_result in response_json['SearchResponse']['News']['Results']:
                        i += 1
                        print "<h6><strong>" + news_result['Title'] + "</strong></h6>"
                        print "<p>" + news_result['Snippet'] + "<a href=\"" + news_result['Url'] + "\" target=\"_blank\"> Read More</a>" + "</p>"
                        print "<br>"

if (len(sys.argv) == 1):
        print "Specify a news search query"
else:
        news = BingSearch()
        news.print_news_results(sys.argv[1])

#Increase the maximum number of results then use the algo to reduce it to the "best" article for said keyword
