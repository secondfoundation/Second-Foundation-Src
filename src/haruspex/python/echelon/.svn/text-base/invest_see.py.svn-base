#Search program for Investopedia terms
import bing

#Load search terms from file
with open('dict.dat') as f:
        gp_list = f.readlines()
        gp_list = map(lambda s: s.strip(), gp_list)
        gp_list = list(set(gp_list))
print 'Running search for:'
print gp_list
print ''

for x in gp_list:
	print x
	news = bing.BingSearch()
        news.print_news_results(x)
	print ''
