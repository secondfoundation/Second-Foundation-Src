#!/usr/bin/python

# Very basic agent that always responds with the same action.  Please note that
# this is a *very* simple agent.  It attempts to take actions even on messages
# from the server where it shouldn't be acting.  This will generate warning
# messages in the logs.

import random
import string
import sys
import getopt
import socket
from re import sub

def main(server_address, port):
    '''
    Connect to the server.
    '''
    
    rclf = '\r\n'
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_address,port))
    s.send("Version:1.0.0"+rclf)
    while True:
        state = s.recv(512).strip();
        print state
        response = state+":c"+rclf
        print response
        s.send(response)
    s.close()

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
