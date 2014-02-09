#!/bin/bash

# move to correct dir
cd /h2/nick/bin/msg/intrade/

# update the files in preparation for email alerts
/bin/rm notable

# archive old price data
/bin/mv price_data.dat old_price_data.dat

# update prices
/usr/bin/python intrade.py 0

# run cds spread analysis
/usr/bin/python cds.py

# run the twitter parser
/usr/bin/python parse.py > notable

# grab trending tweets
echo "---------------------------------------------------------------" > tweet
echo "Trending on Twitter (Manhattan):" >> tweet
echo "---------------------------------------------------------------" >> tweet
echo " "                   >> tweet
/usr/bin/python trends.py  >> tweet
echo " "                   >> tweet

# email
./distribute.sh $*

# nick
#
# built : 2/07/12
# fixed : 2/15/12
# +tweet: 4/01/12
#