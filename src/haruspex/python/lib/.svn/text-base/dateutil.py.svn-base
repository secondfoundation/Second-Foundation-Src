import datetime

def next_weekday(date):
	next = next_day(date)
	# monday-friday is day 0-4
	while (next.weekday() > 4):
		next = next_day(next)
	return next	
		
def prev_weekday(date):
	prev = prev_day(date)
	while (prev.weekday() > 4):
		prev = prev_day(prev)
	return prev	
		
def next_day(date):
	return date + datetime.timedelta(1)
	
def prev_day(date):
	return date + datetime.timedelta(-1)
	
def to_string(date):
	return str(date.year) + "-" + str(pad(date.month)) + "-" + str(pad(date.day))	
	
def create_date(date_string):
	return datetime.date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10]))
	
def pad(x):
	if (x < 10):
		return '0' + str(x)
	else:
		return x	