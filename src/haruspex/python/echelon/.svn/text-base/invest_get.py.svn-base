#Search program for Investopedia terms
import bing, urllib, pickle

def get_body(res_num):
        html_lowered = res_num.lower();
        begin = html_lowered.find('<body>')
        end = html_lowered.find('</body>')
        if begin == -1 or end == -1:
                return None
        else:
                return res_num[begin+len('<body>'):end].strip()

#Load search terms from file
with open('dict.dat') as f:
	gp_list = f.readlines()
	gp_list = map(lambda s: s.strip(), gp_list)
	gp_list = list(set(gp_list))
print 'Running search for:'

list=[]
for x in gp_list:
	print x
	list.append('<---NEW CATEGORY--->')
	list.append(x)
	news = bing.BingSearch()
	news.get_news_pages(x)
	with open('news.tmp', 'rb') as f:
		links = pickle.load(f)
	for url in links:
		res_num=""
		for line in urllib.urlopen(url):
			res_num+=line
		body = get_body(res_num)
		list.append(body)
	list.append('<---END CATEGORY--->')
	list.append('')
	#Write the new list to the file
	with open('news.dat','w') as f:
		for item in list:
			f.write('%s\n' % item)
#Read back file to check the page were downloaded correctly
with open('news.dat', 'r') as f:
	for line in f:
		print line
