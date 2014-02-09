#!/bin/py
# run through the data and find big movers
import sys

# open file object for price data
file_object = open("price_data.dat", "r")

# threshold of 'significant'
thresh=20

# for each line in file 
for line in file_object:
    a = line.split(None,2)

    # unpack
    id  = a[0]
    val = a[1]
    name= a[2]
    
    if(val != '-'):
        if(val != 'None'):
        
            # now open old file for comparison
            old_file_object = open("old_price_data.dat", "r")

            # for each line in file 
            for old_line in old_file_object:
                b = old_line.split(None,2)

                # unpack
                old_id  = b[0]
                old_val = b[1]
                old_name= b[2]

                if(old_val != '-'):    
                    if(old_val != 'None'):    
                        if(id == old_id):

                            # sanity check
                            if(old_name != name):
                                print 'PARADOX! Something has gone horribly wrong'
                                sys.exit(1)
                            
                            # otherwise, smooth sailing
                            mag = abs(float(val)-float(old_val))
                            if(mag >= thresh):
                                print 'Contract: '+str(name)+' has moved '+str(float(val)-float(old_val))+' points '+'starting at '+str(old_val)+' and ending at '+str(val)
                                print ""

file_object.close()
