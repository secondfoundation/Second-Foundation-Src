#!/usr/bin/python
import sys
import string
from random import randint

def usage():
    print '''
    Generate a string of N*20 characters where each character is either W or S for Weak and Strong.
    The string is done is batches of 20, 10 M and 10P to gurantee fairness
    Usage:  sequenceGenerator N where N is a number for the length.
    '''    

def main(argv):
    length = argv[0]
    sequence = ""
    fp = open("config_pool.txt" ,"w");
    for i in range(int(length)):
        w_count = 10;
        s_count = 10;
        for j in range(20):
            if w_count <= 0:
                sequence += 'S'
            elif s_count <= 0:
                sequence += 'W'
            else:
                if randint(0,1) == 0:
                    sequence += 'S'
                    s_count -= 1
                else:
                    sequence += 'W'
                    w_count -= 1
    fp.write(sequence);
    fp.close()
            

if __name__ == "__main__":
    main(sys.argv[1:])
