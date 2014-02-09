import yf, stats

def correlation(ticker1, ticker2, start, end):
	t1 = yf.get_historical_prices(ticker1, start, end)
	t2 = yf.get_historical_prices(ticker2, start, end)
	
	a = get_open_as_float(t1)
	b = get_open_as_float(t2)
	return stats.correlation(a, b)
	
def get_open_as_float(historical_data):	
	historical_data = historical_data[1:]
	return [float(day[1]) for day in historical_data]