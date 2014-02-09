import sys

if (len(sys.argv) == 1):
        with open ('watchlist.dat') as f:
                stock_list = f.readlines()
                stock_list = map(lambda s: s.strip(), stock_list)
                stock_list = list(set(stock_list))
	print 'Current watchlist:'
	print stock_list
	print ''
	sys.exit(0)

if(str(sys.argv[1]) == 'add'):
	#Read the file before addition
	with open ('watchlist.dat') as f:
		stock_list = f.readlines()
		stock_list = map(lambda s: s.strip(), stock_list)
		stock_list = list(set(stock_list))
	print 'Current watchlist:'
	print stock_list
	print ''
	#Add to the watchlist
	stocks = sys.argv[2]
        stocks = stocks.upper()
	stock_list.append(stocks)
	stock_list = list(set(stock_list))
	#Write the new list to the file
	with open('watchlist.dat','w') as f:
		for item in stock_list:
			f.write('%s\n' % item)
        #Read back file to check the stock was added correctly
	print stocks + ' added to the watchlist.  Complete list below:'
	with open('watchlist.dat') as f:
        	stock_list = f.readlines()
		stock_list = map(lambda s: s.strip(), stock_list)
		stock_list = list(set(stock_list))
		print stock_list
		print ''

elif(str(sys.argv[1]) == 'del'):
        #Read the file before removal
        with open ('watchlist.dat') as f:
		stock_list = f.readlines()
		stock_list = map(lambda s: s.strip(), stock_list)
		stock_list = list(set(stock_list))
	print 'Current watchlist:'
        print stock_list
	print ''
        #Remove from the watchlist
	stocks = sys.argv[2]
	stocks = stocks.upper()
	stock_list.remove(stocks)
	stock_list = list(set(stock_list))
	#Write the new list to the file
	with open('watchlist.dat','w') as f:
		for item in stock_list:
			f.write('%s\n' % item)
	#Read back file to check the stock was added correctly
	print stocks + ' removed from the watchlist.  Remaining list below:'
        with open ('watchlist.dat') as f:
                stock_list = f.readlines()
		stock_list = map(lambda s: s.strip(), stock_list)
		stock_list = list(set(stock_list))
		print stock_list
		print ''

else:
	print 'Invalid input selection\n'
	print 'How to use this program:'
	print '[No arguments] will return the watchlist'
	print '[add ABC]: add stock ABC to watchlist'
	print '[del XYZ] remove stock from watchlist\n'
	sys.exit(0)
