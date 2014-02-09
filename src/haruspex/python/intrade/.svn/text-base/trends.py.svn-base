#
# query and parse trending topics on twitter
#
# https://dev.twitter.com/docs/api
# https://dev.twitter.com/docs/api/1/get/trends/:woeid
#
import urllib2
import json

#Available WOEIDs at https://api.twitter.com/1/trends/available.json?lat=41&long=-74
#Of course feel free to change coordinates
#As of 5/3/12 only offers major cities, not counties such as
#Mountain View, Santa Clara County WOEID=2488836

#url = 'http://api.twitter.com/1/trends/1.json'

# austin
#url = 'http://api.twitter.com/1/trends/2357536.json'

# san fran
#url = 'http://api.twitter.com/1/trends/2487956.json'

# singapore
#url = 'http://api.twitter.com/1/trends/23424948.json'

# manhattan
url = 'http://api.twitter.com/1/trends/2459115.json'

# daily digest
#url = 'https://api.twitter.com/1/trends/daily.json'

# download the json string
json_string = urllib2.urlopen(url).read()

# de-serialize the string so that we can work with it
the_data = json.loads(json_string)

# get the list of trends
trends = the_data[0]['trends']

# print the name of each trend
for trend in trends:
    print trend['name']

#
# nick
# 5/1/12
#
