import string
import sys, pycurl, urllib, json
import glob

#
# read in file from $data path and return $list of words
#
def read_sentiment_data(data_path):

	# initalize return object (list of strings)
	list = []

	# open file
	file_object = open(data_path, "r")

	# read line by line
	for line in file_object:
		# if the line has a ';' it is a comment: ignore!
		if(string.count(line,";") == 0):

			# remove the trailing newline 
			cut = line.split("\n")

			# add to list
			list.append(cut[0])

	# send in the cleaning crew -- done here
	file_object.close()
	return list

#
# run through $pos and $neg lists
# return (# pos)/(# neg) in $msg
#
def parse_tweet(msg):

	pos_list = glob.pos
	neg_list = glob.neg

	# intialize to zero
	n=0
	p=0

	nlist = ""
	plist = ""
	
	# count total number of words
	words = len(msg.split())
	
	# if no words, prevent crash (fucking twitter idiots)
	if(words == 0):
		words=1

	# count pos	
	for i in range(len(pos_list)):
		t = string.count(msg,pos_list[i])
		# got one!
		if(t > 0):
			p += t			
			plist += pos_list[i]+" "

	# count neg
	for i in range(len(neg_list)):
		t = string.count(msg,neg_list[i])
		# got one!
		if(t > 0):
			n += t			
			nlist += neg_list[i]+" "


	# return model
	coef = (float(p)-float(n))/float(words)
	print "Tweet: ", msg
	print "Positive Sentiment Indicators: " + plist
	print "Negative Sentiment Indicators: " + nlist
	print "Coefficient measured at      : ", coef
	return coef
	
