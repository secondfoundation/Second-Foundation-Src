#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import pylab
import matplotlib.mlab as mlab
import matplotlib.ticker as ticker
from scipy import stats

# local files that will be imported
import prior
import likelihood

# -------------------------------------------------------------
# MCMC sampling Function
# -------------------------------------------------------------

class BayesianRichardsonExtrapolation(object):
    "Computes the Bayesian Richardson extrapolation posterior log density."
    def __init__(self, qi, hi, si, dtype=np.double):
        """
        Initialize for approximations qi on grids hi with sample errors si.
        """

        # Store incoming parameters 
        N = len(qi)
        self.qi = np.array(qi, dtype)
        self.hi = np.empty(N,  dtype); self.hi = hi
        self.si = np.empty(N,  dtype); self.si = si

    def __call__(self, params, dtype=np.double):
        q, C, p = params

        from math import log, pi
        from scipy.special import gamma

        return (
            prior.prior(q,C,p,self.qi,self.hi,self.si) + 
            likelihood.likelihood(q,C,p,self.qi,self.hi,self.si)
            )

# -------------------------------------------------------------
# Main Function
# -------------------------------------------------------------
#
# Stop module loading when imported.  Otherwise continue running.
if __name__ != '__main__': raise SystemExit, 0

# Example of sampling Bayesian Richardson extrapolation density using emcee
from emcee import EnsembleSampler
from math import ceil, floor, sqrt

print("\nInitializing data and priors defining the sampling problem")
# -------------------------------------------------------------
# Data Input
# -------------------------------------------------------------
#
# U_{CH} (Observed Centerline Velocity)
#
qi = np.array([1.16828362427, 1.16429173392, 1.16367827195])

#
# Normalized Grid Spacing {coarsest, coarse, nominal} (h)
#
hi = np.array([1,0.707,0.5])    

#
# Sigma_{U_{CH}} (Statistical Uncertainty Estimate)
#
si = np.array([0.00012830929872, 0.000398271811878, 0.000128204772095])

#
# initalize the Bayesian Calibration Procedure 
#
bre = BayesianRichardsonExtrapolation(qi, hi, si)

print("\nInitializing walkers")
nwalk = 100
params0       = np.tile([qi[-1], 0, 3], nwalk).reshape(nwalk, 3)
params0.T[0] += np.random.rand(nwalk) * 0.025    # Perturb q
params0.T[1] += np.random.rand(nwalk) * 0.1      # Perturb C
params0.T[2] += np.random.rand(nwalk) * 2.5      # Perturb p...
params0.T[2]  = np.absolute(params0.T[2])        # ...and force >= 0

print("\nInitializing the sampler and burning in walkers")
s = EnsembleSampler(nwalk, params0.shape[-1], bre, threads=4)
pos, prob, state = s.run_mcmc(params0, 5000)
s.reset()

print("\nSampling the posterior density for the problem:")
print bre.__dict__
s.run_mcmc(pos, 10000)
print("Mean acceptance fraction was %.3f" % s.acceptance_fraction.mean())

#
# 1d Marginals
#
print("\nDetails for posterior one-dimensional marginals:")
def textual_boxplot(label, unordered, header):
    n, d = np.size(unordered), np.sort(unordered)
    if (header): print((10*" %15s") % ("", "min", "P5", "P25", "P50", "P75", "P95", "max", "mean", "stddev"))
    print((" %15s" + 9*" %+.8e") % (label,
                                    d[0],
                                    d[[floor(1.*n/20), ceil(1.*n/20)]].mean(),
                                    d[[floor(1.*n/4), ceil(1.*n/4)]].mean(),
                                    d[[floor(2.*n/4), ceil(2.*n/4)]].mean(),
                                    d[[floor(3.*n/4), ceil(3.*n/4)]].mean(),
                                    d[[floor(19.*n/20), ceil(19.*n/20)]].mean(),
                                    d[-1],
                                    d.mean(),
                                    d.std()))

textual_boxplot("q", s.flatchain[:,0], header=True)
textual_boxplot("C", s.flatchain[:,1], header=False)
textual_boxplot("p", s.flatchain[:,2], header=False)

qchain = s.flatchain[:,0]
Cchain = s.flatchain[:,1]
pchain = s.flatchain[:,2]

qbins = np.linspace(np.min(qchain), np.max(qchain), 200)
Cbins = np.linspace(np.min(Cchain), np.max(Cchain), 200)
pbins = np.linspace(np.min(pchain), np.max(pchain), 200)

qkde = stats.gaussian_kde(qchain)
Ckde = stats.gaussian_kde(Cchain)
pkde = stats.gaussian_kde(pchain)

qpdf = qkde.evaluate(qbins)
Cpdf = Ckde.evaluate(Cbins)
ppdf = pkde.evaluate(pbins)

qbounds = np.array([1.1622, 1.1642])
Cbounds = np.array([-6e-3, -4e-3])
pbounds = np.array([1, 9])

qticks = np.linspace(qbounds[0], qbounds[1], 3)
Cticks = np.linspace(Cbounds[0], Cbounds[1], 3)
pticks = np.linspace(pbounds[0], pbounds[1], 5)

#--------------------------------------------------------
# Plots: Three sets of results are plotted:
#
# * Views of posterior PDF
#
#--------------------------------------------------------
print("\nPrinting PDF output")
#----------------------------------
# FIGURE: Marginals and samples
#----------------------------------
pyplot.figure()

formatter = ticker.ScalarFormatter()
formatter.set_scientific(True)
formatter.set_powerlimits((-2,3))

pylab.subplot(3,3,1)
pyplot.plot(qbins, qpdf, linewidth=2, color="k", label="Post")

pyplot.xlim(qbounds)
pylab.gca().set_xticks(qticks)
pylab.gca().xaxis.set_major_formatter(formatter)
pylab.gca().set_yticks([])
pyplot.xlabel('$q$', fontsize=24)

pylab.subplot(3,3,2)
H, qe, Ce = np.histogram2d(qchain, Cchain, bins=(200,200))

qv = 0.5*(qe[0:-1] + qe[1:len(qe)]);
Cv = 0.5*(Ce[0:-1] + Ce[1:len(Ce)]);

pyplot.contour(Cv,qv,H,5,colors='k')

pyplot.xlim(Cbounds)
pylab.gca().set_xticks(Cticks)
pylab.gca().set_xticklabels([])

pyplot.ylim(qbounds)
pylab.gca().set_yticks(qticks)
pylab.gca().set_yticklabels([])

pylab.subplot(3,3,3)
H, qe, pe = np.histogram2d(qchain, pchain, bins=(200,200))

qv = 0.5*(qe[0:-1] + qe[1:len(qe)]);
pv = 0.5*(pe[0:-1] + pe[1:len(pe)]);

pyplot.contour(pv,qv,H,5,colors='k')

pyplot.xlim(pbounds)
pylab.gca().set_xticks(pticks)
pylab.gca().set_xticklabels([])

pyplot.ylim(qbounds)
pylab.gca().set_yticks(qticks)
pylab.gca().set_yticklabels([])

pylab.subplot(3,3,5)
pyplot.plot(Cbins, Cpdf, linewidth=2, color="k",label="Post")

# prior
#pyplot.plot(Cbins, Cpri, linewidth=2, color="k", linestyle="dashed", label="Prior")

pylab.gca().xaxis.set_major_formatter(formatter)
pylab.gca().set_yticks([])
pyplot.xlabel('$C$', fontsize=24)

pyplot.xlim(Cbounds)
pylab.gca().set_xticks(Cticks)

pylab.subplot(3,3,6)
H, Ce, pe = np.histogram2d(Cchain, pchain, bins=(200,200))

Cv = 0.5*(Ce[0:-1] + Ce[1:len(Ce)]);
pv = 0.5*(pe[0:-1] + pe[1:len(pe)]);

pyplot.contour(pv,Cv,H,5,colors='k')

pyplot.xlim(pbounds)
pylab.gca().set_xticks(pticks)
pylab.gca().set_xticklabels([])

pyplot.ylim(Cbounds)
pylab.gca().set_yticks(Cticks)
pylab.gca().set_yticklabels([])

pylab.subplot(3,3,9)
pyplot.plot(pbins, ppdf, linewidth=2, color="k", label="Post")

# prior
#pyplot.plot(pbins, ppri, linewidth=2, color="k", linestyle="dashed",label="Prior")

pylab.gca().xaxis.set_major_formatter(formatter)
pylab.gca().set_yticks([])
pyplot.xlabel('$p$', fontsize=24)

pyplot.xlim(pbounds)
pylab.gca().set_xticks(pticks)

pyplot.savefig('joint_post.pdf', bbox_inches='tight')

#----------------------------------
# FIGURE: Marginal posterior for q
#----------------------------------
pyplot.figure()
pyplot.plot(qbins, qpdf, linewidth=3, label="Post")
#pyplot.plot(qbins, qpri, linewidth=3, label="Prior")

pylab.gca().xaxis.set_major_formatter(formatter)
pylab.gca().yaxis.set_major_formatter(formatter)

pyplot.legend(loc=2, prop={'size':24})
pyplot.xlabel('$q$', fontsize=30)
pyplot.ylabel('$\pi(q)$', fontsize=30)
pylab.xticklabels = pylab.getp(pylab.gca(), 'xticklabels')
pylab.yticklabels = pylab.getp(pylab.gca(), 'yticklabels')
pylab.setp(pylab.yticklabels, fontsize=24)
pylab.setp(pylab.xticklabels, fontsize=24)

# make sure 'offsets' have right font size
offset = pylab.gca().xaxis.get_offset_text()
pylab.setp(offset, fontsize=24)

offset = pylab.gca().yaxis.get_offset_text()
pylab.setp(offset, fontsize=24)

pyplot.xlim(qbounds)
pylab.gca().set_xticks(qticks)

pyplot.savefig('U_post.pdf', bbox_inches='tight')

#----------------------------------
# FIGURE: Marginal posterior for p
#----------------------------------
pyplot.figure()
pyplot.plot(pbins, ppdf, linewidth=3, label="Post")
#pyplot.plot(pbins, ppri, linewidth=3, label="Prior")

pylab.gca().xaxis.set_major_formatter(formatter)
pylab.gca().yaxis.set_major_formatter(formatter)

pyplot.legend(loc=1, prop={'size':24})
pyplot.xlabel('$p$', fontsize=30)
pyplot.ylabel('$\pi(p)$', fontsize=30)
pylab.xticklabels = pylab.getp(pylab.gca(), 'xticklabels')
pylab.yticklabels = pylab.getp(pylab.gca(), 'yticklabels')
pylab.setp(pylab.yticklabels, fontsize=24)
pylab.setp(pylab.xticklabels, fontsize=24)

pyplot.xlim(pbounds)
pylab.gca().set_xticks(pticks)

pyplot.savefig('p_post.pdf', bbox_inches='tight')
