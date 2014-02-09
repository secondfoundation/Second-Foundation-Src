#!/usr/bin/python
import socket
import string
import sys
import getopt
import socket

def queryMatch(server_address, port, command, no_run):
    '''
    Connect to the server using the args specified.
    '''
    
    rclf = '\r\n'
    message = command+rclf
    if no_run:
        print message
        return
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((server_address,port))
    s.send(message)
    response = ''
    while 1:
        line = ''
        try:
            line = s.recv(1024)
        except socket.timeout:
            break

        if line == '':
            break

        response += line
    
    print response
    s.close()

def usage():
    '''
    Prints the usage
    '''
    print '''
    Query the status of a room or all the rooms running on the server
    Usage:  queryMatch.py roomname

    Use LIST as a roomname to get a report on all the rooms
    Use CLEAR to clear the status lists on the server
    Use CLEARALL to clear key and  port lists as well as status lists
               
    [Options]
    --server=       Specify an address for the server, default is 127.0.0.1
    --port=         Specify a port for the server, default is 9000
    --no-run        Dont actually connect to the server, just test the command
    '''    

def main(argv):
    try:
        optlist, args = getopt.gnu_getopt(argv,'',['server=', 'port=', 'no-run',])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(-1)
    if len(args) < 1:
        usage()
        sys.exit(-1)
        
    no_run = False
    port = 9000
    server_address = '127.0.0.1'

    for option, value in optlist:
        if option == '--server=':
            server_address = value
        if option == '--port=':
            port = int(value)
        if option == '--no-run':
            no_run = True
            
    command = 'STATUS:'
    if str.upper(args[0]) == 'LIST':
        command = 'LIST'
    elif str.upper(args[0]) == 'CLEAR':
        command = 'CLEAR'
    elif str.upper(args[0]) == 'CLEARALL':
        command = 'CLEAR:ALL'
    else:
        command += args[0]

    queryMatch(server_address, port, command, no_run)
    
if __name__ == '__main__':
    main(sys.argv[1:])
