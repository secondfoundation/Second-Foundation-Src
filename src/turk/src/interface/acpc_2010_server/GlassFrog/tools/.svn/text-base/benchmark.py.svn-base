#!/usr/bin/python
import socket
import sys
import time
from threading import Thread

class botThread(Thread):
    def __init__ (self, port):
        Thread.__init__(self)        
        self.port = int(port)
        
    def run(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('129.128.184.126',self.port))
        #.send("SocketPlayer:jdavidso:200:1\r\n")
        s.send("AAAIPlayer:Polaris:200:0:scripts/psyctestscript.sh")
        #while(1):
        #    gamestate = s.recv(512)
        #    print gamestate
        #    s.send(gamestate+":c\r\n")
    

def runBenchmark(num_users):
    connect_msg = "AUTOCONNECT:"
    for i in range(int(num_users)):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('129.128.184.126',9000))        
        s.send(connect_msg+str(i)+"\r\n")
        response = s.recv(512)
        print response
        if(response.split(":")[0] == "ERROR"):
            continue        
        response = s.recv(512)
        print response
        port = response.split(':')[1]
        bot = botThread(port)
        s.close()
        time.sleep(2)
        bot.start()
        #Run the bot here in a thread then wait 2s

def useage():
    print "Useage benchmark.py num_users\nnum_users is the number of users to simulate"

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        useage()
        sys.exit(0)
    else:
        runBenchmark(sys.argv[1])
