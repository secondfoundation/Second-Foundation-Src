import sys, urllib, mysqlutil, dateutil
	
def parse_tag(html, tag):
	tag_start = html.find("<" + tag)
	tag_end = html.find("</" + tag + ">") + len(tag) + 3
	
	if (tag_start == -1):
		return "", ""
	
	return html[tag_start:tag_end], html[tag_end:]
	
def parse_value(tag):
	value_start = tag.find(">") + 1
	value_end = tag.find("</") - 1
	return tag[value_start:value_end].strip()			
	
def get_earnings_for_date(date):
	# date format: 2012-02-03
	earnings_list = []
	url = "http://www.morningstar.com/earnings/Handler/GetEarningsCalendar.ashx?rptDate=" + date
	resp = urllib.urlopen(url)
	resp_html = resp.read()
	
	# get the next <table>
	[table, rem_doc] = parse_tag(resp_html, "table")
	table_count = 0
	while (table != ""):
		table_count += 1
		# only get company names from the second table, it includes all the companies from the morningstar 
		# commentary table above
		if (table_count == 2):	
			# get table body (only one per table)
			[body, rem_table] = parse_tag(table, "tbody")
			# get next <tr>
			[tr, rem_body] = parse_tag(body, "tr")
			while (tr != ""):
				td_count = 0
				field_map = {}
				# get next <td> (the first one is the one with the name / ticker)
				[td, rem_tr] = parse_tag(tr, "td")
				while (td != ""):
					td_count += 1	
					if (td_count == 1):
						[a, rem_td] = parse_tag(td, "a")						
						link_text = parse_value(a)
						# company name is inside the link, before the <span>
						value_end = link_text.find("<")
						# there's a bunch of other crap in there as well to strip off
						company_name = link_text[0:value_end].strip()[0:-2]
						field_map['name'] = company_name
					
						[span, rem_a] = parse_tag(a, "span")
						inner = parse_value(span)
						# strip off junk characters (not sure what these are)
						symbol = inner[0:-2]
						field_map['symbol'] = symbol
					if (td_count == 2):
						time = parse_value(td)
						if (time.find('After') != -1):
							time = 'C'
						elif (time.find('Before') != -1):
							time = 'O'
						else:
							time = '?'
									
						field_map['time'] = time
					if (td_count == 4):
						expected = parse_value(td)
						field_map['expected_eps'] = expected
					if (td_count == 5):		
						actual = parse_value(td)
						field_map['actual_eps'] = actual
							
					# get next <td>	
					[td, rem_tr] = parse_tag(rem_tr, "td")	
			
				earnings_list.append(field_map)
				# get the next <tr> in the remainder of the table body
				[tr, rem_body] = parse_tag(rem_body, "tr")
		
		# next <table in> the remainder of the doc
		[table, rem_doc] = parse_tag(rem_doc, "table")
	
	return earnings_list	
		
if __name__ == '__main__':		
	if (len(sys.argv) == 1):
		print "Use morningstar.py earnings [date], with date format YYYY-MM-DD"
	else:
		if (sys.argv[1] == 'earnings' or sys.argv[1] == 'e'):
			date_string = sys.argv[2]
			earnings_list = get_earnings_for_date(date_string)
			for earnings in earnings_list:
				print earnings
				
				