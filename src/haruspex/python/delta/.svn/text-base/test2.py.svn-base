import matplotlib.pyplot as plt
import numpy as np
import random

def iterate(line1,ax,fig):
    a = -1
    i =  0
    x = np.linspace(0, 0, 100)
    ar = np.array(x)

    while(a <= 0 ):
        #    line1.set_ydata(np.sin(x + phase))
        ar[i]=.1*i 
        line1.set_ydata(ar)
        print len(ar)
        line1.set_ydata(np.sin(x + i))
        fig.canvas.draw()
        i=i+1
        #print ar

def init():    
    x = np.linspace(0, 6*np.pi, 100)
    y = np.sin(x)

    # You probably won't need this if you're embedding things in a tkinter plot...
    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma    
    return line1, ax, fig

#for phase in np.linspace(0, 500, 500):
(l, ax, f) = init()
iterate(l,ax,f)

#
# 1) append to data set
#
# 2) make iterate take no arg (go global)
#
# http://stackoverflow.com/questions/4098131/matplotlib-update-a-plot/4098938#4098938
