#!/usr/bin/python
import random
import string
import sys
import getopt
import socket
from re import sub

#XML Stuff
from xml.dom.minidom import parse

def writeConfig(id, hands, gamedef, seed, botlist):

    template = "../config/TEMPLATE.config.xml"
    
    dom = parse(template)

    roomElement = dom.createElement("Room")

    nameElement = dom.createElement("Name")
    nameValue = dom.createTextNode(id)
    nameElement.appendChild(nameValue)
    roomElement.appendChild(nameElement)

    handsElement = dom.createElement("Hands")
    handsValue = dom.createTextNode(str(hands))
    handsElement.appendChild(handsValue)
    roomElement.appendChild(handsElement)

    gamedefElement = dom.createElement("Gamedef")
    gamedefValue = dom.createTextNode(gamedef)
    gamedefElement.appendChild(gamedefValue)
    roomElement.appendChild(gamedefElement)

    seedElement = dom.createElement("Seed")
    seedValue = dom.createTextNode(str(seed))
    seedElement.appendChild(seedValue)
    roomElement.appendChild(seedElement)

    dom.childNodes[0].appendChild(roomElement)
    
    botlistElement = dom.createElement("BotList")
    for bot in botlist :
        botElement = dom.createElement("Bot")
        
        typeElement = dom.createElement("Type")
        typeValue = dom.createTextNode(bot[0])
        typeElement.appendChild(typeValue)
        botElement.appendChild(typeElement)

        nameElement = dom.createElement("Name")
        nameValue = dom.createTextNode(bot[1])
        nameElement.appendChild(nameValue)
        botElement.appendChild(nameElement)

        buyInElement = dom.createElement("BuyIn")
        buyInValue = dom.createTextNode(bot[2])
        buyInElement.appendChild(buyInValue)
        botElement.appendChild(buyInElement)

        locationElement = dom.createElement("Location")
        locationValue = dom.createTextNode(bot[3])
        locationElement.appendChild(locationValue)
        botElement.appendChild(locationElement)

        execElement = dom.createElement("Executable")
        execValue = dom.createTextNode(bot[4])
        execElement.appendChild(execValue)
        botElement.appendChild(execElement)

        botlistElement.appendChild(botElement)

    dom.childNodes[0].appendChild(botlistElement)

    file = dom.toprettyxml(" ","\n","UTF-8")
    file = sub("\s*\n\s*\n","\n",file)
    fp = open("../config/"+id+".config.xml",'w')
    fp.write(file)
    fp.close()
    return True

def createMatch(server_address, port, args, no_run):
    '''
    Connect to the server using the args specified.
    '''
    
    rclf = '\r\n'
    if(len(args) == 1):
        message = "CONFIG:"+args[0]+rclf
    else:
        arg_string = ''
        for arg in args:
            #Arg is a botlist, parse as such
            if(type(arg) == list):
                for bots in arg:
                    bot = ''
                    for item in bots:
                        bot += item+" "
                    bot = bot[0:-1]+'|'
                    arg_string += bot
                arg_string = arg_string[0:-1]                  
            else:
                arg_string += str(arg)
            arg_string += ':'
            
        arg_string = arg_string[0:-1]
        message = "NEW:"+arg_string+rclf
    if no_run:
        print message
        return
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_address,port))
    s.send(message)
    response = s.recv(512)
    print response
    s.close()
        
def usage():
    print '''
    Creates a match on the server for the specified bots
    Usage:  matchConstructor id hands gamedef seed <bots>

    id      -  An identifier for the match
    hands   -  Number of hands you wish to play
    gamedef -  A gamedef file you wish the server to use for the match
    seed    -  A seed for the game, if using random, specify RANDOM
    <bots>  -  A list of bots for the match. A bot is specified as such:
               TYPE NAME BUYIN LOCATION EXECUTABLE
               
               TYPE use 0 or AAAIPLAYER unless you want to override the bot type, see server documentation for creation of custom types.               
               NAME specifies the bot name in the logfile
               BUYIN specifies the amount used to buy in.
               LOCATION specifies the machine on which the bot is located (LOCAL can be used for bots on the same machine as the server)
               EXECUTABLE specifies a path to an executable to be run for when the bot is loaded.  The executable should take two arguments, the server ip and connection port
               
    [Options]
    --config        Specify a config file instead of individual arguments
    --write-config  Write out the matches into the config file format
    --server=       Specify an address for the server, default is 127.0.0.1
    --port=         Specify a port for the server, default is 9000
    --no-run        Dont actually connect to the server, just test
    '''    

def main(argv):
    try:
        optlist, args = getopt.gnu_getopt(argv,'',['config', 'write-config', 'server=', 'port=', 'no-run',])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(-1)
    if len(args) < 1:
        usage()
        sys.exit(-1)
        
    seed = 'UKNOWN'
    use_config = False
    write_config = False
    no_run = False
    port = 9000
    server_address = '127.0.0.1'

    for option, value in optlist:
        if option == '--config':
            use_config = True
            config = args[0]
        if option == '--write-config':
            write_config = True
        if option == '--server=':
            server_address = value
        if option == '--port=':
            port = int(value)
        if option == '--no-run':
            no_run = True

    if use_config:
        createMatch(server_address, port, [config], no_run)
        return
    
    elif len(args) < 4 :
        usage()
        sys.exit(-1)
    else:
        id = args[0]
        hands = args[1]
        gamedef = args[2]
        seed = args[3]
        if seed == 'RANDOM':
            seed = str(random.randint(10000,99999))
        else:
            seed = seed

        
        i = 4
        botlist = []
        while i < len(args):
            bot_type = args[i]
            if bot_type == '0':
                bot_type = 'AAAIPLAYER'
            bot_name = args[i+1]
            bot_buyin = args[i+2]
            bot_location = args[i+3]
            if bot_location == 'LOCAL':
                bot_location = '127.0.0.1'
            bot_executable = args[i+4]
            botlist.append([bot_type, bot_name, bot_buyin, bot_location, bot_executable])
            i+= 5
            
        if write_config:
            writeConfig(id, hands, gamedef, seed, botlist)
            
        createMatch(server_address, port, [id,hands,gamedef,seed,botlist], no_run)

if __name__ == '__main__':
    main(sys.argv[1:])
