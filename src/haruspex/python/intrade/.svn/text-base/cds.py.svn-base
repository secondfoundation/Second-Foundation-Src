#!/bin/py
# talk to cma, get cds spreads

import urllib2
import pprint
import sys
import xml.dom.minidom as minidom
from xml.dom.minidom import Node

def risk(s): 
    spread=float(s)
    spread = spread/(100.*100)
    time = 5

    # recovery rate % (0 < x < 100)
    # apparently 40% is 'industry standard'
    recovery = 40

    # calculate implied annual risk 
    risk = (spread)/(1-recovery/100.)

    # with the implied risk above the risk-free rate established, 
    # let's now assume the subsequent year default events constitute 
    # a bernoulli trial and therefore adhere to a binomial distribution 
    # (probability mass function)
    pmf=(1-risk)**(time)

    # cumulative year risk is the probability of a SINGLE default event!
    cumulative_risk = 1-pmf
    return str(cumulative_risk)


#
# program execution initialized!
#
#if (len(sys.argv) == 1):
#  print 'usage: [0] gather fresh data [1]: restart from xml file'
#  sys.exit(0)

solution=[]

flag=0
res=""
url_data='http://www.cmavision.com/#'
for line in urllib2.urlopen(url_data):
    res += line

    # grab the first widening spread
    if (line.find("#id_1") != -1) :
        if(line.find("#id_10") == -1) :
            l = line.split(">")
            l = l[2].split("<")
            solution.append(l[0])

            # set flag to gather data
            flag=1

    # grab the first widening spread
    if (line.find("#id_6") != -1) :
        l = line.split(">")
        l = l[2].split("<")
        solution.append(l[0])
        
        # set flag to gather data
        flag=1

    # we are in the money: grab data!
    if(flag > 0):
        if(flag == 1):
            flag=flag+1
        else:
            l = line.split(">")
            l = l[1].split("<")
            solution.append(l[0])
            flag=flag+1

            if(flag == 5):
                flag=0

# now we write the output
f = open('cds', 'w')
f.write("Largest Widening CDS Spread  : ")
f.write(solution[0])
f.write("\n5 Yr Mid (bps)               : ")
f.write(solution[1])
f.write("\nChange (%)                   : ")
f.write(solution[3])
f.write("\nCPD (%)                      : ")
f.write(risk(solution[1]))
f.write("\n\nLargest Tightening CDS Spread:\n")
f.write(solution[4])
f.write("\n5 Yr Mid (bps)               : ")
f.write(solution[5])
f.write("\nChange (%)                   : ")
f.write(solution[7])
f.write("\nCPD (%)                      : ")
f.write(risk(solution[5]))
f.write("\n\n")

# close file, go home
f.close()

#
# nick 
# 6/27/12
#
