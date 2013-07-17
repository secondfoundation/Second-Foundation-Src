#!/bin/bash
#
#
size=200

for i in `seq 1 50`;
do
    second="$(echo "$i/50" | bc -l)"
    #echo $second
    python pop.py $size $second	
done   


#
# nick: run several models
#