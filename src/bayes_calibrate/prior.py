#!/usr/bin/env python
#
import numpy as np

def prior(q,C,p,qi,hi,si):
    """
    prior probability distribution: P(q,C,p|X)

    (arrays of size three)
    qi = observed centerline velocity 
    hi = resolution parameter (normalized grid spacing)
    si = standard deviation of the statistical noise

    """

    from math import log, pi
    from scipy.special import gamma

    sq = 0.025
    sC = 4*sq
    a  = 3
    b  = 0.5

    # from Jimenez (literature)
    q0 = 1.1627 
    
    inv_2s2q = 0.5 / sq**2
    inv_2s2C = 0.5 / sC**2
    
    # for some reason the p guesses are sometimes negative, this 
    # patches that up
    if(p < 0):
        return -1 * np.inf

    # compute prior
    N = len(qi)
    line1  = b**a
    line1 /= (2*pi)**(1 + N/2) * sq * sC * gamma(a)
    line1  = log(line1)
    line1 -= np.log(si).sum()    
    line1 += (a - 1) * np.log(p)
    line1 += - inv_2s2q * (q - q0)**2
    line1 += - inv_2s2C * C**2 - b * p

    return line1
