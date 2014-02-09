#!/usr/bin/python
import random
import string
import sys
import getopt
from re import sub

#XML Stuff
from xml.dom.minidom import parse

# Here are the email package modules we'll need
import smtplib
from email.MIMEImage import MIMEImage
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate

def genBenchmarkKeys(num_users, config):
    for i in range(int(num_users)):
        username = "User"+str(i)
        key = str(i)
        seed = genSeed(i)
        addEntry(username,key,seed, config)    

def genSeed(key):
    random.seed(key)    
    return str(random.randint(10000,99999))

def genKey(username):
    random.seed(username)
    length=10
    chars=string.letters + string.digits    
    key = ''.join([random.choice(chars) for i in range(length)])
    key = key.upper()
    key = key.replace('I','1')
    key = key.replace('O','0')
    return key

def addEntry(username, key, seed, config):
    if(testDuplicate(username)):        
        return False

    filename = "keys/keys.xml"
    dom = parse(filename)

    keyElement = dom.createElement("Key")

    keyValueElement = dom.createElement("KeyValue")
    keyValue = dom.createTextNode(key)
    keyValueElement.appendChild(keyValue)
    keyElement.appendChild(keyValueElement)

    usernameElement = dom.createElement("UserName")
    usernameValue = dom.createTextNode(username)
    usernameElement.appendChild(usernameValue)
    keyElement.appendChild(usernameElement)

    seedElement = dom.createElement("Seed")
    seedValue = dom.createTextNode(seed)
    seedElement.appendChild(seedValue)
    keyElement.appendChild(seedElement)

    configElement = dom.createElement("Config")
    configValue = dom.createTextNode(config)
    configElement.appendChild(configValue)
    keyElement.appendChild(configElement)

    dom.childNodes[0].appendChild(keyElement)

    file = dom.toprettyxml(" ","\n","UTF-8")
    file = sub("\s*\n\s*\n","\n",file)
    fp = open(filename,'w')
    fp.write(file)
    fp.close()
    return True

def testDuplicate(username):
    filename = "keys/keys.xml"
    dom = parse(filename)

    keys = dom.getElementsByTagName("Key")
    for key in keys:
        usernode = key.getElementsByTagName("UserName")[0].childNodes
        for node in usernode:
            if node.nodeType == node.TEXT_NODE:
                if username == str(node.data).strip().upper():
                    return True
    return False

def sendEmail(recipient,key,resend):
    '''
    Email the key to the submitter
    '''
    URL = 'SOME LAUNCH URL'
    admin_list = ''

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Successful registration'
    msg['From'] = 'Poker Registration <dontemailpolaris@mailinator.com>'
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    html = '''
<html>
 <head></head>
 <body>
  <p>Thank you for registering.<br>
  Your key is : <b>'''+key+'''</b><br><br>
  <p>Please proceed to the following URL <a href="'''+URL+'''" target ="_blank">'''+URL+'''</a> to begin.
  <p>Note: Some webmail clients display the link above incorrectly.  If you are having trouble, the plain text link is<br>
  '''+URL+'''
  </p>
 </body>
</html>
    '''
    text = '''
Your key is '''+key+'''
Please proceed to the following URL to begin: '''+URL
    
    msghtml = MIMEText(html,'html')
    msgtext = MIMEText(text,'text')
    msg.attach(msghtml)
    msg.attach(msgtext)
    
    if not resend and len(admin_list) > 0 :
        reg_msg = MIMEMultipart()
        reg_msg['Subject'] = 'New registration'
        reg_msg['From'] = 'Poker Registration <dontemailpolaris@mailinator.com>'
        reg_msg['To'] = admin_list
        reg_msg['Date'] = formatdate(localtime=True)
        reg_html = '''
<html>
 <head></head>
 <body>
  <p>New registration<br><br>
  key: <b>'''+key+'''</b><br>
  email: <b>'''+recipient+'''</b>
  </p>
 </body>
</html>
    '''
        reg_text = 'New registration.\nkey:'+key+'\nemail:'+recipient+'\n'
        reg_msghtml = MIMEText(reg_html,'html')
        reg_msgtext = MIMEText(reg_text,'text')
        reg_msg.attach(reg_msghtml)
        reg_msg.attach(reg_msgtext)
        
    # Send the email via our own SMTP server.
    s = smtplib.SMTP()
    s.connect()
    s.sendmail('dontemailpolaris@mailinator.com', recipient, msg.as_string())
    if not resend:
        s.sendmail('dontemailpolaris@mailinator.com', admin_list, reg_msg.as_string())
    s.close()

def getNextConfig():
    '''
    Random config files from a pool
    '''
    fp = open('scripts/config_pool.txt','r')
    config_pool = fp.read()
    config_option = config_pool[0:1]
    config_pool = config_pool[1:]
    fp.close()
    fp = open('scripts/config_pool.txt','w')
    fp.write(config_pool)
    fp.close()
    if config_option == 'W':
        return "SAMPLE.config.xml"
    else:
        return "SAMPLE.config.xml"

        
def usage():
    print '''
    Inputs a username, key, seed and config value into the keys.xml file
    Usage:  keygen.py username1 username2 ...
    Output: SUCCESS or DUPLICATE
    --salt=       Salt a key and seed with a given string
    --seed-only=  Salt only the seed with a given string
    --benchmark=  Generate N benchmark keys where the keys are 0:N
    --config=     Specify a config file. Default is SAMPLE.config.xml
    --no-key      Use the username as the key value
    --test        Test the existance of a duplicate only.
                  Returns SUCCESS or DUPLICATE
    --verbose     Output all the information for the given entry
    --online      The username is an email address, send them the key
    --resend      Resend the username their key.
    --random-config Use a psuedo random config from the config_pool.txt file
    '''    

def main(argv):
    try:
        optlist, args = getopt.gnu_getopt(argv,'',['salt=', 'seed-only=', 'benchmark=', 'config=', 'no-key', 'verbose', 'test', 'online', 'resend', 'random-config'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(-1)
    if(len(args) < 1):
        usage()
        sys.exit(-1)
    salt = ""
    seed_salt = ""
    config = "SAMPLE.config.xml"
    benchmark = False
    num_users = ""
    no_key = False
    verbose = False
    run_test = False
    resend = False
    online = False
    
    for option, value in optlist:
        if option == '--salt':
            salt = value
        if option == '--seed-only':
            seed_salt = value
        if option == '--benchmark':
            benchmark = True
            num_users = value
        if option == '--config':
            config = value
        if option == '--no-key':
            no_key = True
        if option == '--verbose':
            verbose = True
        if option == '--test':
            run_test = True
        if option == '--online':
            online = True
        if option =='--resend':
            resend = True
        if option == '--random-config':
            config = getNextConfig()
    if benchmark:
        genBenchmarkKeys(num_users,config)
        sys.exit(1)
    for username in args:
        username = username.upper()
        if no_key :
            key = username
        else: 
            key = genKey(username+salt)        
        seed = genSeed(key+seed_salt)
        if run_test:
            if not testDuplicate(username):
                print 'SUCCESS'
                if online:
                    sendEmail(username,key,False);
            else:
                if resend:
                    sendEmail(username,key,True);
                    print 'SUCCESS'
                else:
                    print 'DUPLICATE'
        else:
            if addEntry(username, key, seed, config):
                if verbose:
                    print 'SUCCESS:Username:%s:Key:%s:Seed:%s:Config:%s' % (username,key,seed,config)
                else:
                    print 'SUCCESS'
                    if online:
                        sendEmail(username,key,False);
            else:
                if resend:
                    sendEmail(username,key,True);
                    print 'SUCCESS'
                else:
                    print 'DUPLICATE'

if __name__ == "__main__":
    main(sys.argv[1:])
