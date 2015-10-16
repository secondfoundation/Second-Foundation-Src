"""
Minimize the Rosenbrock banana function.

http://en.wikipedia.org/wiki/Rosenbrock_function
"""

import scipy.optimize as optimize
import numpy as np

def main():
    x0 = np.array([[1.3, 0.7]])

    print "----------------------------------------------------"
    print "          Derivative-Free Optimization              "
    print "----------------------------------------------------"

    #
    # Minimize a function using the downhill simplex algorithm.
    #
    print "Downhill Simplex (Nelder-Mead)"
    xopt = optimize.fmin(optimize.rosen, x0, xtol=1e-8, disp=True)
    print(xopt)

    #
    # Minimize a function using the downhill simplex algorithm.
    #
    print "Powell's Method"
    xopt = optimize.fmin_powell(optimize.rosen, x0, xtol=1e-8, disp=True)
    print(xopt)

    print "----------------------------------------------------"
    print "               Gradient Based Methods               "
    print "----------------------------------------------------"

    #
    # Minimize a function using the downhill simplex algorithm.
    #
    print ""
    print "Conjugate Gradient"
    xopt = optimize.fmin_cg(optimize.rosen, x0, fprime=optimize.rosen_der, gtol=1e-8, disp=True)
    print(xopt)
    #print (allvecs)


    #
    # quasi-newton
    #
    print ""
    print "Quasi-Newton"
    xopt = optimize.fmin_bfgs(optimize.rosen, x0, fprime=optimize.rosen_der, gtol=1e-8, disp=True)
    print(xopt)

    #
    # Minimize a function using Newton
    #
    print ""
    print "Newton"
    xopt = optimize.fmin_ncg(optimize.rosen, x0, fprime=optimize.rosen_der, fhess=optimize.rosen_hess, avextol=1e-8,disp=True)
    print(xopt)

if __name__ == '__main__':
    main()

#
# nick
# 10/15/15
#
