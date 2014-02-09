#
# twitter parsing: observe frequency of positive and negative
#                  word count, and output sentiment estimate
#

import signal
import string
import sys, pycurl, urllib, json

# import custom modules
import twitter_stream
import sentiment

def signal_handler(signal, frame):
	print '\nSIGINT Received: Ctrl+C!'
	print 'Exiting with Grace'
	sys.exit(0)

#
#   BEGIN EXECUTION
#
	
# initalize exception handling
signal.signal(signal.SIGINT, signal_handler)

# get stream
if (len(sys.argv) == 1):
	print 'Specify a comma-separated list of keywords to listen for'
else:  
	twitter_stream.tweet_stream(sys.argv[1])

#
# jay and nick
# 2/15/12
#
