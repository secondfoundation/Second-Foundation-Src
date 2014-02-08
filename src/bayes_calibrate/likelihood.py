#!/usr/bin/env python
#
def likelihood(q,C,p,qi,hi,si):
    """
    likelihood function: P(qi|q,C,p,X)

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
        
    inv_2s2i = 0.5 / si**2
    line2 = - (inv_2s2i * (q - qi - C*hi**p)**2).sum() 
    
    return line2

