#Parsing program to sort through Investopedia
import urllib2
import re

#This is the code to parse the List of Terms
def get_glossary(res_num):
	html_lowered = res_num.lower();
	begin = html_lowered.find('<!-- .alphabet -->')
	end = html_lowered.find('<!-- .idx-1 -->')
	if begin == -1 or end == -1:
		return None
	else:
		return res_num[begin+len('<!-- .alphabet -->'):end].strip()

#This is the code to parse the Title
def get_title(res_num):
	html_lowered = res_num.lower();
	begin = html_lowered.find('<title>')
	end = html_lowered.find('</title>')
	if begin == -1 or end == -1:
		return None
	else:
		return res_num[begin+len('<title>'):end].strip()

#We start with the numbers section of Investopedia
url = "http://www.investopedia.com/terms/1/"

res_num=""
for line in urllib2.urlopen(url):
	res_num+=line

title_num = get_title(res_num)
glossary_num = get_glossary(res_num)

##Find all hyperlinks in list then eliminate duplicates
glossary_parsed_num = re.findall(r'href=[\'"]?([^\'" >]+)', glossary_num)
glossary_parsed_num = list(set(glossary_parsed_num))
parent_url = 'http://www.investopedia.com'
tail = ' Definition | Investopedia'
short_tail = ' | Investopedia'

print title_num
gp_list = []
for x in glossary_parsed_num:
	gpn = parent_url + x
	res_num=""
	for line in urllib2.urlopen(gpn):
		res_num+=line
	gpn_title = get_title(res_num)
	gpn_penult = gpn_title.replace(tail,'')
	gpn_final = gpn_penult.replace(short_tail,'')	
	gp_list.append(gpn_final)

#The alphabet section of Investopedia terms begins here
alfa = [chr(i) for i in xrange(ord('a'), ord('z')+1)]

for i, v in enumerate(alfa):
	u = 'http://www.investopedia.com/terms/'
	w = '/'
	invest_alfa_url = u + v + w

	# get url info
	res_alfa=""
	for line in urllib2.urlopen(invest_alfa_url):
		res_alfa+=line

	glossary_alfa = get_glossary(res_alfa)
	title_alfa = get_title(res_alfa)

	glossary_parsed_alfa = re.findall(r'href=[\'"]?([^\'" >]+)', glossary_alfa)
	glossary_parsed_alfa = list(set(glossary_parsed_alfa))

	print title_alfa
	for x in glossary_parsed_alfa:
		gpa = parent_url + x
		res_num=""
		for line in urllib2.urlopen(gpa):
			res_num+=line
		gpa_title = get_title(res_num)
		gpa_penult = gpa_title.replace(tail,'')
		gpa_final = gpa_penult.replace(short_tail,'')
        	gp_list.append(gpa_final)

#Write the new list to the file
with open('dict.dat','w') as f:
	for item in gp_list:
		f.write('%s\n' % item)
#Read back file to check the stock was added correctly
with open('dict.dat') as f:
       	gp_list = f.readlines()
       	gp_list = map(lambda s: s.strip(), gp_list)
       	gp_list = list(set(gp_list))
print gp_list
print ''
