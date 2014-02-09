import sys, urllib, json
import bing_news_search

with open('watchlist.dat') as f:
        stock_list = f.readlines()
        stock_list = map(lambda s: s.strip(), stock_list)
        stock_list = list(set(stock_list))

print 'Running search for:'
print stock_list

for x in stock_list:
        news = bing_news_search.BingSearch()
        news.print_news_results(x)
