#!/usr/bin/python
import sys
import socket
import time

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate

def monitorServer():
    '''The server is on port 9000 of the machine this script should be running
    on.  The script will try and ping the server every 1/2 hour and if there is
    no response from the server, then an email will be sent to those on the
    admin list to bring it back up'''
    
    admin_list = ['j.a.davidson@gmail.com']
    server_port = 9000
    server_query = "GETINFO\r\n"
    query_delay = 1800
    response = ""
    while(1):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect(('127.0.0.1',server_port))
            s.send(server_query)
            response = s.recv(512)
            print response
            s.close()
        except socket.error:
            print "Server down"
            for administrator in admin_list:
                sender = "jdavidso@cs.ualberta.ca"                
                msg = MIMEMultipart()
                msg['Subject'] = "Poker Server Down"
                msg['From'] = sender
                msg['To'] = administrator
                msg['Reply-To'] = 'jdavidso@cs.ualberta.ca'
                msg['Date'] = formatdate(localtime=True)
                msg.preamble = 'Poker Server Down'                
                msgText = MIMEText("Poker Server is Down.\nLast respose was %s"%(response))                                
                msg.attach(msgText)            
                email_smtp = s = smtplib.SMTP('localhost')
                email_smtp.sendmail(sender, administrator, msg.as_string())
                email_smtp.quit()            
            sys.exit()
        time.sleep(query_delay)        
         
if __name__ == "__main__":
    monitorServer()
