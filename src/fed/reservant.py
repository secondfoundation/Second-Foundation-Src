#!/bin/py
#
# Reservant is Latin, for Reserve.
#
# http://stackoverflow.com/questions/8139822/how-to-load-training-data-in-pybrain
#
#
# In this case the neural network has 3 inputs and 1 output. 
# The csv file has 4 values on each line separated by a comma. 
# The first 3 values are input values and the last one is the output.
#
# To calculate the number of hidden nodes we use a 
# general rule of: (Number of inputs + outputs) * (2/3)"
#

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer
import pylab as pl

#
# will always have only a single output: the federal funds rate
# number of features can vary
#
# you will never require more than twice the number 
# of hidden units as you have inputs
#
# ftp://ftp.sas.com/pub/neural/FAQ3.html#A_hu
features=int(3)
hidden  =int(60)
steps   =int(10000)
ds = SupervisedDataSet(features,1)

#tf = open('raw_dat/matrix.dat','r')
tf = open('raw_dat/diff.dat','r')

gdp=[]
cpi=[]
une=[]
i=0
time=[]
fund=[]

for line in tf.readlines():
    data = [float(x) for x in line.strip().split('\t') if x != '']
    #print data
    time.append(i)
    i=i+1

    # first feature is GDP
    gdp.append(data[0])

    # second feature is cpi
    cpi.append(data[1])

    # third feature is unemployment
    une.append(data[2])
    
    fund.append(data[3])

    indata =  tuple(data[:features])
    outdata = tuple(data[features:])
    ds.addSample(indata,outdata)

# this builds a network that has the number of features as input, 
# a *SINGLE* defined hidden layer and a single output neuron. 
n = buildNetwork(ds.indim,hidden,hidden,ds.outdim)
t = BackpropTrainer(n,learningrate=0.01,momentum=0.8,verbose=True)
t.trainOnDataset(ds,steps)
t.testOnData(verbose=True)

# let's plot what we have
import matplotlib.pyplot as plt

# lets ask for a prediction: GDP,CPI, Unemployment
#print n.activate([.02,.02,-.002])

x = []
y = []
#print range(len(time))
for i in range(len(time)):
    #print n.activate([gdp(i),cpi(i),une(i)])
    x.append(.25*time[i]+1954.5)
    y.append(n.activate([gdp[i],cpi[i],une[i]]))

pl.plot(x,fund)
pl.plot(x,y)
plt.title('Neural Network Predictor')
plt.legend(['Federal Funds Rate % Change','Predicted Rate Change'])
pl.show()

#plt.plot(time,gdp,'x',time,cpi,'o',time,une,'.')
#plt.show()

#
# nick and jay
#
# 8/28/12
#
