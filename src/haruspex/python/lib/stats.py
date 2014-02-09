import math

def sigma(x):
	return math.sqrt(var(x))	

def var(x):
	return sum([(a - avg(x)) ** 2 for a in x])/(len(x)-1)

def popsigma(x):
	return math.sqrt(popvar(x))

def popvar(x):
	return avg([(a - avg(x)) ** 2 for a in x])

def sum(x):
	return reduce(lambda a, b: a + b, x)
	
def avg(x):
	return sum(x) * 1.0 / len(x)	

def mult(x, y):
	m = []
	for i in range(0,len(x)):
		m.append(x[i] * y[i])
	return m

def minus(x, y):
	m = []
	for i in range(0,len(x)):
		m.append(x[i] - y[i])
	return m		

def normalize(x):
	return [a - avg(x) for a in x]		

def correlation(x, y):
	return (covar(x, y)) / (popsigma(x) * popsigma(y))

def covar(x, y):
	return avg(mult(normalize(x), normalize(y)))
