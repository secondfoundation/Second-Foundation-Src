import sys, dateutil, mysqlutil, morningstar, optionshouse, couchdb

start_date_string = sys.argv[1]
num_days = int(sys.argv[2])

date = dateutil.create_date(start_date_string)
db = mysqlutil.db_connect("root", "root", "opt")

s = couchdb.Server()
couch = s['options_test']

# get next n days of earnings
for day_num in range(0, num_days):
	date = dateutil.next_weekday(date)
	date_string = dateutil.to_string(date)
	earnings_list = morningstar.get_earnings_for_date(date_string)

	for earnings_json in earnings_list:	
		earnings_json['date'] = date_string
		# company name not saved in this table
		del earnings_json['name']
		earnings_json['docType'] = 'earnings'
		
		symbol = earnings_json['symbol']
		key = symbol + ':' + date_string;
		
		# mysqlutil.insert_dict(earnings, None, 'earnings', db)
		results = couch.view('_design/earnings/_view/by_symbol_date', key = key)
		if len(results) == 1:
			result = results.rows[0]
			earnings_doc = result.value
			new_eps = earnings_json['actual_eps']

			if earnings_doc['actual_eps'] == 'N/A' and new_eps != 'N/A':
				earnings_doc['actual_eps'] = new_eps
				couch.save(earnings_doc)
				print 'Updated actual EPS to ' + new_eps + ' for key ' + key				
		elif len(results) > 1:
			print 'Document for key ' + key + ' not updated, duplicate results:'
			print results	
		else:
			couch.save(earnings_json)
			print 'Saved earnings for key ' + key