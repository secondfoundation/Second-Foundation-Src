#!/bin/py
## Regression module
## Run with example
from pymc import *
from numpy import *

# Build a vector of 10000 normal deviates with variance (3)^2 and mean 0
mu    = 0
sigma = 2
v     = random.normal(mu,sigma,10000)

# intercept/slope of the linear function
a = 1
b = 4

# number of data points we have
samples = 10

print 'Using: ', samples, ' data points'
print 'True Alpha is: ', a
print 'True Beta  is: ', b
print 'True Sigma is: ', sigma

ylist=[]
xlist=[]

# build linear function -- y = alpha + beta*x
for i in range(samples):
    ylist.append(a + b*i)
    xlist.append(i)

# add random forcing (epsilon) to perfectly linear function
for i in range(samples):
    ylist[i]+=v[i]
    #print xlist[i], ylist[i]

# convert list to numpy array
YY = array(ylist)
XX = array(xlist)

# priors
# y = alpha + beta*x + epsilon
sigma = Uniform('sigma', 0.0, 200.0, value=5)
alpha = Normal('alpha', 0.0, 0.001, value=0)
beta = Normal('beta', 0.0, 0.001, value=0)

#model
@deterministic(plot=False)
def modelled_yy(XX=XX, beta=beta, alpha=alpha):
    return beta*XX + alpha

#likelihood
y = Normal('y', mu=modelled_yy, tau=1.0/sigma**2, value=YY, observed=True)

# 
# nick
# 1/31/12
#
