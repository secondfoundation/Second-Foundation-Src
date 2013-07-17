#!/bin/py
#
# model a virus: find R_half 
#
import math
import random
import numpy as np
import sys

#
# create a lattice of humans 
# with one randomly infected
#
def build(isize):
    
    # everyone starts uninfected
    # arrays first by rows then by columns
    lattice = np.zeros((isize,isize))
    sp      = np.zeros((isize,isize))

    # some poor bastard is bitten by a monkey:
    a = random.randint(0, isize-1)
    b = random.randint(0, isize-1)
    lattice[a][b] = 1 
    sp[a][b]      = 1
    return lattice,sp
    
#
# each adjacent tab has a vir% change of infection
#
def spread(lat,sp,vir,isize):
    
    # spread matrix
    sp_new = np.zeros((isize,isize))

    # loop over matrix and infect
    for i in range(isize):
        for j in range(isize):

            # find the newly infected
            if(sp[i][j] == 1):
                # try to infect all 4 neighbors

                # i-1     
                if(i > -1):
                    # is he not infected?
                    if(lat[i-1][j] == 0):
                        # try to infect!
                        if(random.random() <= vir):
                            lat[i-1][j]    = 1
                            sp_new[i-1][j] = 1

                # i+1     
                if(i+1 < isize-1):
                    # is he not infected?
                    if(lat[i+1][j] == 0):
                        # try to infect!
                        if(random.random() <= vir):
                            lat[i+1][j]    = 1
                            sp_new[i+1][j] = 1

                # j-1     
                if(j > -1):
                    # is he not infected?
                    if(lat[i][j-1] == 0):
                        # try to infect!
                        if(random.random() <= vir):
                            lat[i][j-1]    = 1
                            sp_new[i][j-1] = 1

                # j+1     
                if(j+1 < isize-1):
                    # is he not infected?
                    if(lat[i][j+1] == 0):
                        # try to infect!
                        if(random.random() <= vir):
                            lat[i][j+1]    = 1
                            sp_new[i][j+1] = 1
    # end and return
    return lat, sp_new
            

#
# kill individuals who have  
# had the virus longer than 
# 1 time unit
#
def extinguish(old,isize,total):
    count = int(0)
    
    # loop over matrix and infect
    for i in range(isize):
        for j in range(isize):

            # new infection
            if(old[i][j] == 1 ):
                count = count + 1    

    # append to casualty list
    total = total + count

    # no one left!
    if(total == isize*isize):
        count = 0

    return count,total

#
# display the horror, the horror
#
def display(lat, step):
    step = step + 1
    #print ""
    #print "Day:", step
    #print lat
    return step

#
# gather statistics
#
def stats(cas,isize):
    #print 'Percentage infected:', float(cas)/(float(isize*isize))
    return float(cas)/(float(isize*isize))


#
# run for the number of times indicated
#
def run(isize,virulence):

    lattice,spread_matrix = build(isize)

    if(virulence > 1 or virulence < 0):
        print "Inconceivable!"
        sys.exit(1)

    # the virus lives!
    not_extinct = int(1)
    day         = 0
    casualties  = 1
    while(not_extinct):
        lattice,spread_matrix = spread(lattice,spread_matrix,virulence,isize)
        day = display(lattice,day)

        # old virus carriers stop trying to infect
        not_extinct,casualties = extinguish(spread_matrix,isize,casualties)


    # gather statistics
    pc = stats(casualties,isize)
    return pc

# -----------------------
# main program
# -----------------------
#
# edit these parameters:
#
# population will be size^2
isize       = int(10)
# or grab from command line
if(len(sys.argv) > 1):
    isize = int(sys.argv[1])

# efficacy of the virus:
virulence  = float(.7)
# or grab from command line
if(len(sys.argv) > 2):
    virulence = float(sys.argv[2])

# number of iterations to gather statistics on
it = int(100)

# do not edit below!
avg=0
std=0
for i in range(it):
    s = run(isize,virulence)
    avg = avg + s    
    std = std + s*s

avg = avg/it
std = math.sqrt(std-avg*avg)/it
print virulence,avg,std

#
# nick
# 9/12/12
#
