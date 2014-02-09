#!/bin/bash
# bash script to run default test cases
# remember that nostests -s prints all stdio
cd ..

MACHINE=$(hostname -s 2>&1)
echo Running on $MACHINE

case $MACHINE in
    magus)
	~/lib/python/nosetests -v -s;;

    thymos)
	nosetests -v;;

         *)	 
	 #nosetests -v #tests/test_sim.py;;
	nosetests -v #tests/test_sim.py;;
esac

