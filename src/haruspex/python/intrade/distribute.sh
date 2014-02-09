#!/bin/bash
# bash script to grab file from thymos
# "I am a prototype of a much larger system"

# grab command line
switch=$*

# clean up
#rm notable*

# email subject
SUBJECT="Haruspex"
EMAIL="nicholas.malaya@gmail.com"
EMAIL_j="jayawilson85@gmail.com"
EMAIL_r="rufino.a.mendoza@gmail.com"
EMAIL_m="richard.matsui@gmail.com"

# get file
#wget tri.dynalias.org/download/intrade/notable

# write date to file
/bin/date > data/cur_time

# get count of number of news items we have
counter=$(wc -l < notable )
  
# check that the file has found news...
if [ "$counter" = "0" ]; then
    # echo "Apologies: No News Today" | /usr/bin/mail -s $SUBJECT $EMAIL   -aFrom:nick@ices.utexas.edu
    # noop
    two=2
else

    # just send to nick
    if [ "$*" = "0" ]; then
	cat data/header   cds notable tweet data/ending data/cur_time | /usr/bin/mail -s $SUBJECT $EMAIL   -aFrom:nick@ices.utexas.edu
    else # send to all 
	cat data/header   cds notable tweet data/ending data/cur_time | /usr/bin/mail -s $SUBJECT $EMAIL   -aFrom:nick@ices.utexas.edu
	cat data/header_j cds notable tweet data/ending data/cur_time | /usr/bin/mail -s $SUBJECT $EMAIL_j -aFrom:nick@ices.utexas.edu
	cat data/header_r cds notable tweet data/ending data/cur_time | /usr/bin/mail -s $SUBJECT $EMAIL_r -aFrom:nick@ices.utexas.edu
	#cat data/header_m cds notable tweet data/ending data/cur_time | /usr/bin/mail -s $SUBJECT $EMAIL_m -aFrom:nick@ices.utexas.edu
    fi
fi

# steady as she goes...
exit 0

# nick  
# 2/7/12

