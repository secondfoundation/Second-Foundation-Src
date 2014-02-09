import sys, json, httplib, time, datetime, mysqlutil, couchdb

class OH:
	def __init__(self):
		# only works for one session
		# need to look at how the login is being done
		self.authToken = "502294fa-10b1-4cd5-ae2c-c46f13a440d6"
		self.account = "1880009"
		self.host = "trading.optionshouse.com"
		
 		s = couchdb.Server()
		self.couch = s['options_test']
		
		# maps from json structure name to db column name
		self.quote_columns = {}
		self.quote_columns['symbolId'] = 'symbol_sid'
		self.quote_columns['symbol'] = 'symbol'
		self.quote_columns['last'] = 'last_price'
		self.quote_columns['open'] = 'open_price'
		self.quote_columns['prevClose'] = 'prev_close_price'
		self.quote_columns['volume'] = 'volume'
		self.quote_columns['avg10dayVolume'] = 'av_10'
		self.quote_columns['peRatio'] = 'pe_ratio'
		self.quote_columns['pbRatio'] = 'pb_ratio'
		self.quote_columns['beta'] = 'beta'
		self.quote_columns['marketCap'] = 'market_cap'
		self.quote_columns['day200movingAvg'] = 'ma_200'
		self.quote_columns['day50movingAvg'] = 'ma_50'
		self.quote_columns['day21movingAvg'] = 'ma_21'
		
		self.symbol_columns = {}
		self.symbol_columns['symbol'] = 'symbol'
		self.symbol_columns['shortDescription'] = 'name'
		self.symbol_columns['industryName'] = 'industry'
		self.symbol_columns['exchange'] = 'exchange'
		self.symbol_columns['symbolType'] = 'type'
		
		self.series_columns = {}
		self.series_columns['symbol'] = 'symbol'
		self.series_columns['symbolId'] = 'symbol_sid'
		self.series_columns['symbolLast'] = 'symbol_last_price'
		self.series_columns['series'] = 'series_name'
		self.series_columns['id'] = 'series_id'
		self.series_columns['expDate'] = 'exp_date_str'
		self.series_columns['expDay'] = 'exp_date_day'
		self.series_columns['expMonth'] = 'exp_date_month'
		self.series_columns['expYear'] = 'exp_date_year'
		self.series_columns['strikePrice'] = 'strike_raw'
		self.series_columns['strikeString'] = 'strike_decimal'
		self.series_columns['cbid'] = 'call_bid'
		self.series_columns['cask'] = 'call_ask'
		self.series_columns['clast'] = 'call_last'
		self.series_columns['cchange'] = 'call_change'
		self.series_columns['callAskSize'] = 'call_ask_size'
		self.series_columns['callBidSize'] = 'call_bid_size'
		self.series_columns['cvol'] = 'call_volume'
		self.series_columns['coi'] = 'call_open_interest'
		self.series_columns['cdelt'] = 'call_delta'
		self.series_columns['civ'] = 'call_implied_volatility'
		self.series_columns['cthet'] = 'call_theta'
		self.series_columns['cgam'] = 'call_gamma'
		self.series_columns['cveg'] = 'call_vega'
		self.series_columns['pbid'] = 'put_bid'
		self.series_columns['pask'] = 'put_ask'
		self.series_columns['plast'] = 'put_last'
		self.series_columns['pchange'] = 'put_change'
		self.series_columns['putAskSize'] = 'put_ask_size'
		self.series_columns['putBidSize'] = 'put_bid_size'
		self.series_columns['pvol'] = 'put_volume'
		self.series_columns['poi'] = 'put_open_interest'
		self.series_columns['pdelt'] = 'put_delta'
		self.series_columns['piv'] = 'put_implied_volatility'
		self.series_columns['pthet'] = 'put_theta'
		self.series_columns['pgam'] = 'put_gamma'
		self.series_columns['pveg'] = 'put_vega'
	
	def is_market_open(self):
		now = datetime.datetime.now()	
		return (9 <= now.hour <= 15) or (now.hour == 8 and now.minute >= 30)
		
	def get_moneyness(self, series_json):
		strike = float(series_json['strikeString'])
		stock_price = series_json['symbolLast']
		return stock_price >= strike
		
	def get_response(self, action_string, data):
		action = {}
		action['action'] = action_string
		action['data'] = data
		
		ezList = {}
		ezList['EZList'] = [action]
		
 		req_payload = json.dumps(ezList)
		conn = httplib.HTTPSConnection(self.host)
		conn.request("POST", "/m", req_payload)
		
		return json.loads(conn.getresponse().read())			
		
	def get_stock_quote(self, symbol):
		data = {}
		data['authToken'] = self.authToken
		data['account'] = self.account
		data['symbol'] = symbol
		data['description'] = True
		data['fundamentals'] = True
		data['bs'] = True
		data['showDivEarnDetails'] = True
		
		quote_json = self.get_response('view.quote', data)
		print quote_json
		return quote_json['EZMessage']['data']['quote']
	
	def get_chain(self, symbol, ntm):	
		data = {}
		data['authToken'] = self.authToken
		data['account'] = self.account
		data['symbol'] = symbol
		data['weeklies'] = False
		data['quarterlies'] = False
		data['nonstandard'] = False
		data['greeks'] = True
		data['bs'] = True
		data['quotesAfter'] = 0
		data['ntm'] = ntm
		data['nextGen'] = True
		
		chain_json = self.get_response('view.chain', data)
		# print chain_json
		return chain_json['EZMessage']['data']['optionQuote']
		
	def save_chain_quote(self, symbol, db):
		quote_json = self.get_stock_quote(symbol)		
		# look up primary key for this symbol
		symbol_row = self.get_symbol(symbol, db)
	
		symbolId = symbol_row[0][0]
		# add primary key field to json map
		quote_json['symbolId'] = symbolId
		
		mysqlutil.insert_dict(quote_json, self.quote_columns, 'quote', db)
		self.couch.save(quote_json)
	
		chain_json = self.get_chain(symbol, 10)
	
	    # last_exp = ""
		for series_json in chain_json:
			quote = quote_json['last']
			timestamp = str(datetime.datetime.now())
			
			# exp = series_json['exp']
			# add symbol foreign key
			series_json['symbolId'] = symbolId
			# add symbol last quote info for convenience
			series_json['symbol'] = symbol
			series_json['symbolLast'] = quote
			series_json['timestamp'] = timestamp
			
			# save in couchdb and mysql
			mysqlutil.insert_dict(series_json, self.series_columns, 'series', db)

			series_json['docType'] = 'chain'
			series_json['_id'] = timestamp + ':' + symbol + ':' + quote
			
			self.couch.save(series_json)
			
	def get_symbol(self, symbol, db):
		# check if symbol is saved
		query = "select * from symbol where symbol = '" + symbol + "'"
		results = mysqlutil.db_get(query, db)

		# if not saved, insert it
		if (len(results) == 0):
			quote_json = self.get_stock_quote(symbol)
			mysqlutil.insert_dict(quote_json, self.symbol_columns, 'symbol', db)
			query = "select * from symbol where symbol = '" + symbol + "'"
			results = mysqlutil.db_get(query, db)

		return results			

	def save_stock_quote(self, symbol, db):
		symbol_row = self.get_symbol(symbol, db)				
		quote_json = self.get_stock_quote(symbol)		
		quote_json['symbolId'] = symbol_row[0][0] 
		mysqlutil.insert_dict(quote_json, self.quote_columns, 'quote', db)	
		
		# also save in couch db
		quote_json['docType'] = 'quote'	
		self.couch.save(quote_json)
			
	def save_chain_quotes(self, symbols, db, throttle):
		self.save_symbol_data(self.save_chain_quote, symbols, db, throttle)
		
	def save_stock_quotes(self, symbols, db, throttle):
		self.save_symbol_data(self.save_stock_quote, symbols, db, throttle)		
			
	def save_symbol_data(self, symbol_save_func, symbols, db, throttle):
		max_symbol_retries = 3
		# sanity
		max_total_retries = 30
		
		total_retries = 0		
		for symbol in symbols:			
			symbol_retries = 0 
			retry = True
			while (retry and symbol_retries <= max_symbol_retries and total_retries <= max_total_retries):
				# don't pound the server
				time.sleep(throttle)
				# false unless a network-related error occurs
				# these could be intermittent 
				retry = False
				try:
					symbol_save_func(symbol, db)
				except IOError, e:
					print str(e)
					print "Network Error: will retry symbol " + symbol
					symbol_retries += 1
					total_retries += 1					
					retry = True
				except Exception, e:
					print str(e)
					print "Unexpected Error: will skip symbol " + symbol 
		
if (len(sys.argv) == 1):
	print "Commands: chain [symbol], quote [symbol]"
else:
	oh = OH()
	command = sys.argv[1]
	symbol_file = sys.argv[2]
	try:
		# try to treat arg as a file name
		f = open(symbol_file, 'r')
		symbols = f.read()
		symbols = symbols.split(',')
	except:
		# treat arg as a single symbol name
		symbols = [symbol_file]
		
	# substitute your own db creds
	db = mysqlutil.db_connect("root", "root", "opt")
	
	if (command == 'quote'):
		oh.save_stock_quotes(symbols, db, 0.6)
	elif (command == 'chain'):		
		oh.save_chain_quotes(symbols, db, 0.6)							
		
	