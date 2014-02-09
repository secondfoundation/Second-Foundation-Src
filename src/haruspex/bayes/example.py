#!/bin/py
from pylab import *
from pymc import *
import regress

# instantiate regress class, take MCMC chain
M = MCMC(regress)
samples=10000
print "# of MCMC samples: ",samples
M.sample(samples, burn=5000)

# now let's find the traditional least squares comparison
A = numpy.vstack([M.XX, numpy.ones(len(M.XX))]).T
m, c = numpy.linalg.lstsq(A, M.YY)[0]
print ""
print "Traditional Least Squares predicts-- "
print "Alpha: ", c 
print "Beta:  ", m

# save images
from pylab import hist, show,plot
#Matplot.plot(M)

print ""
print "Bayesian Prediction finds-- "
print "Alpha mean: ", mean(M.alpha.value)
print "Beta  mean: ", mean(M.beta.value)
print "Sigma mean: ", mean(M.sigma.value)

# plot this up
#import matplotlib.pyplot as plt
#plt.plot(M.XX, M.YY, 'o', label='Original data', markersize=10)
#plt.plot(M.XX, m*M.XX + c, 'r', label='Traditional Least Squares')
#plt.plot(M.XX, mean(M.beta.value)*M.XX + mean(M.alpha.value), 'b', label='Bayesian Prediction')
#plt.legend()
#plt.show()    

#
# nick
# 1/31/12
#
