import sys, datetime, math, morningstar, yf, yfutils, stats, dateutil	

def yfDate(date):
	return str(date.year) + str(pad(date.month)) + str(pad(date.day))	
	
def pad(x):
	if (x < 10):
		return '0' + str(x)
	else:
		return x

if (len(sys.argv) == 1):
	print "Use earnings_preview.py earnings [date], with date format YYYY-MM-DD"
else:
	if (sys.argv[1] == 'earnings' or sys.argv[1] == 'e'):
		date_string = sys.argv[2]
		ms = morningstar.Morningstar()
		
		print "Waiting for response from Morningstar..."
		print 
		
		short_period = 30
		long_period = 365
		
		earnings_list = ms.get_earnings_for_date(date_string)
		suspicious_list = []
		
		earnings_date = datetime.date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10]))
		short_back = yfDate(earnings_date + datetime.timedelta(-short_period))
		long_back = yfDate(earnings_date + datetime.timedelta(-long_period))
		earnings_date_string = yfDate(earnings_date)
		
		short_biz_days = int(short_period * (float(5) / 7))
		
		spy_hist = yf.get_historical_prices('SPY', long_back, earnings_date_string)
		spy_long = yfutils.get_open_as_float(spy_hist)	
		spy_short = spy_long[-short_biz_days:]
		
		print str(len(earnings_list)) + " companies reporting on " + date_string + ":"
		print
		
		short_list = []
		long_list = []
		i = 0
		for earnings_info in earnings_list[:]:
			ticker = earnings_info[1]
			comp_hist = yf.get_historical_prices(ticker, long_back, earnings_date_string)
			if (len(comp_hist) != 0):
				company_long = yfutils.get_open_as_float(comp_hist)
				company_short = company_long[-short_biz_days:]
			
				long_corr = stats.correlation(company_long, spy_long)
				short_corr = stats.correlation(company_short, spy_short)
			
				long_list.append(long_corr)
				short_list.append(short_corr)
			
				print ticker + " - Processed " + str((i / float(len(earnings_list))) * 100) + '%'
			else:
				print "Warning: could not get historical prices for ticker: " + ticker
				earnings_list.remove(earnings_info)
			
			i += 1	
		
		corr_change = stats.minus(short_list, long_list)
		# corr_change = [math.fabs(a) for a in corr_change]
		
		print len(corr_change)
		print len(earnings_list)
		
		change_avg = stats.avg(corr_change)	
		change_sigma = stats.sigma(corr_change)
		
		price_changes = []
			
		for i in range(0, len(earnings_list)):
			earnings_list[i].append(long_list[i])
			earnings_list[i].append(short_list[i])
			
			prev_date = yfDate(getPrevWeekday(earnings_date))
			next_date = yfDate(getNextWeekday(earnings_date))
			
			ticker = earnings_list[i][1]
			
			before_quote = yf.get_historical_prices(ticker, prev_date, prev_date)
			before_quote = yfutils.get_open_as_float(before_quote)
			
			after_quote = yf.get_historical_prices(ticker, next_date, next_date)
			after_quote = yfutils.get_open_as_float(after_quote)
			
			if (len(after_quote) > 0 and len(before_quote) > 0):
				price_change = (after_quote[0] - before_quote[0]) / before_quote[0] * 100
				price_changes.append(price_change)
				earnings_list[i].append(price_change)
			else:
				print "Warning: could not get before and after quote for " + ticker
				del corr_change[i]
				
			if (short_list[i] - long_list[i] > change_avg + change_sigma):
				suspicious_list.append(earnings_list[i])
			
		print	
		print str(len(suspicious_list)) + " correlation increases greater than 1 standard deviation (" + str(change_sigma) + ") of the avg correlation change (" + str(change_avg) + "): "
		print "format: [name, ticker, expected eps, actual eps, 2 year corr, 3 month corr, % change]"
		print
			
		for earnings_info in suspicious_list:	
			print earnings_info	
			
		print
		print "Correlation of correlation change with price change " + str(stats.correlation(corr_change, price_changes))	