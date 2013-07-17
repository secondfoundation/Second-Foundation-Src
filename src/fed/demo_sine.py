from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer
import pickle
import math
import scipy as sp
import numpy as np
import pylab as pl

x = np.linspace(0, 4*np.pi, 4000)
ds = SupervisedDataSet(1,1)

for i in x:
    ds.addSample(i,np.sin(i))
print ds

n = buildNetwork(ds.indim,30,30,ds.outdim,recurrent=True,hiddenclass=TanhLayer)
t = BackpropTrainer(n,learningrate=0.01,momentum=0.5,verbose=True)
t.trainOnDataset(ds,100)
t.testOnData(verbose=True)

fileObject = open('trained_net', 'w')
pickle.dump(n, fileObject)
fileObject.close()

fileObject = open('trained_net','r')
net = pickle.load(fileObject)

y = []
for i in x:
    y.append(net.activate(i))

pl.plot(x,y)
pl.plot(x,np.sin(x))
pl.show()
