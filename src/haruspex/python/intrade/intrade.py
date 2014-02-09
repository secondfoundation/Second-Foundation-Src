#!/bin/py
# talk to intrade with python
#
# The basic human need to be watched was once satisfied by God. 
# Now, the same functionality can be replicated with data-mining algorithms.
#


import urllib2
import pprint
import sys
import xml.dom.minidom as minidom
from xml.dom.minidom import Node

#
# Print out all tags found in xml
#
# requires:
#       xml file name
#       'tag'-- EventClass, EventGroup, Event or Contract
#
def getTitles(xml,tag):
    doc = minidom.parse(xml)
    node = doc.documentElement
    books = doc.getElementsByTagName(tag)

    titles = []
    for book in books:

        # only run if we are looking at 'contracts'
        if(tag == 'contract'):
            for (name,val) in book.attributes.items():
                # if we hit an id #
                if(name == 'id'):
                    price = get_price(val)
                    print val, price
            
        titleObj = book.getElementsByTagName("name")[0]
        titles.append(titleObj)

    print "******************"
    print "%s" % tag
    print "******************"
    for title in titles:
        nodes = title.childNodes
        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                print node.data
    print ""


# -------------------------------------------------------
#
# Create file with all id and prices listed
#
# requires:
#       xml file name
#       'tag'-- EventClass, EventGroup, Event or Contract
#
# ------------------------------------------------------
def create_price_file(xml,tag):
    doc = minidom.parse(xml)
    node = doc.documentElement
    books = doc.getElementsByTagName(tag)

    # open file object
    file_object = open("price_data.dat", "w")

    # create price vector
    a=[]
    
    # create index
    ind=0

    doc=""
    titles = []
    for book in books:
        # append to price vector
        a.append(['-','-','-'])

        # only run if we are looking at 'contracts'
        if(tag == 'contract'):
            for (name,val) in book.attributes.items():
                # if we hit an id #
                if(name == 'id'):                    
                    price = get_price(val)
                    
                    # save id
                    a[ind][0]=val
                    
                    # save price
                    a[ind][1]=price

        # add to index
        ind=ind+1
        titleObj = book.getElementsByTagName("name")[0]
        titles.append(titleObj)

    ind=0
    for title in titles:
        nodes = title.childNodes
        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                # save contract name
                a[ind][2]=node.data
        ind=ind+1

    # save this to file
    for i in range(ind):
        file_object.write(str(a[i][0])+' '+str(a[i][1])+' '+str(a[i][2])+'\n')
                    
    # done here, close file and exit subroutine
    file_object.close()


#
# get an options price xml file from web
#
def get_price(id):
    # option price hotline:
    url ='http://api.intrade.com/jsp/XML/MarketData/ContractBookXML.jsp'    
    url =url+'?id='+str(id)

    # get price xml
    res=""
    for line in urllib2.urlopen(url):
        res+=line

    doc = minidom.parseString(res)
    price = pull_price(doc,"contractInfo")
    return price

#
# pull options price from xml
#
def pull_price(doc,tag):
    node = doc.documentElement
    books = doc.getElementsByTagName(tag)
 
    titles = []
    for book in books:

        # only run if we are looking at 'contractsInfo'
        for (name,val) in book.attributes.items():
            # if we hit a last trade price, grab that price quote
            if(name == 'lstTrdPrc'):
               return val


#
# write an xml file
#
def write_to_file(doc, name):
    file_object = open(name, "w")
    file_object.write(doc)
    file_object.close()

#
# build an xml data file from web query (saved as contract_data.xml)
#
def build_xml():
    # xml messages
    message_log = '<xmlrequest requestOp="getLogin" > \n\
       <membershipNumber>11342906</membershipNumber> \n\
       <password>Mars21</password> \n\
       </xmlrequest>'

    message_balance_start = '<xmlrequest requestOp="getBalance"> \n\
       <sessionData>'
    message_balance_end   = '</sessionData> \n\
       </xmlrequest>'

    # vars
    res=""
    url='http://api.intrade.com/xml/handler.jsp'

    # get log on id
    for line in urllib2.urlopen(url, message_log):
        res+=line
        
    doc = minidom.parseString(res)

    # print session id
    print "session id: " 
    print doc.getElementsByTagName("sessionData")[0].childNodes[0].data
    print "" 
        
    # now lets see our remaining balance
    balance_list = [message_balance_start, message_balance_end]
    message_balance = doc.getElementsByTagName("sessionData")[0].childNodes[0].data
    message_balance = message_balance.join(balance_list)
    res=""
    for line in urllib2.urlopen(url, message_balance):
        res+=line

    # print balance
    # achtung! broken, somehow
    # doc = minidom.parseString(res)
    # print 'available: '
    # print doc.getElementsByTagName("available")[0].childNodes[0].data
    # print "" 
    # print 'frozen: '
    # print doc.getElementsByTagName("frozen")[0].childNodes[0].data
    # print "" 

    # gather data book
    # 
    # From API notes:
    # As this is a large file, this should only be retrieved at start-up 
    # and not more than one time per 15 minutes.
    #
    # Let's write it as a file and use that
    #
    res=""
    url_data='https://www.intrade.com/jsp/XML/MarketData/xml.jsp'
    for line in urllib2.urlopen(url_data):
        res += line
            
    write_to_file(res,'contract_data.xml')

#
# program execution initialized!
#
if (len(sys.argv) == 1):
  print 'usage: [0] gather fresh data [1]: restart from xml file'
  sys.exit(0)

if(float(sys.argv[1]) == 0):
    print 'creating contract_data.xml'
    build_xml()
elif(float(sys.argv[1]) == 1):
    print 'restarting from saved file (contract_data.xml)'
    print ''
else:
    print "invalid input selection"
    sys.exit(0)

# This XML data_book file is organized as follows:
# <MarketData>
# <EventClass>
# <EventGroup>
# <Event>
# <contract>

#getTitles("contract_data.xml","EventClass")
#getTitles("contract_data.xml","EventGroup")
#getTitles("contract_data.xml","Event")
#getTitles("contract_data.xml","contract")
create_price_file("contract_data.xml","contract")

#print get_price(721155)

#
# now that we have the data_book
# we can look at the prices of options
#


#
# nick 
# 1/25/12
#
