# download and documentation
# http://mysql-python.sourceforge.net/MySQLdb.html
import MySQLdb

def db_execute(statement, db):
	print "Executing SQL: " + statement
	c = db.cursor()
	c.execute(statement)
	c.close()
	db.commit()
	
def db_get(query, db, rows=0):
	print "Executing SQL: " + query
	
	c = db.cursor()
	c.execute(query)
	
	res = ()
	if (rows == 0):
		res = c.fetchall()
	else:	
		res = c.fetchn(rows)
		
	c.close()
	db.commit()	
	
	return res
		
def insert_dict(dict, column_map, table, db):
	field_names = ""
	values = ""
	first = True
	for key, value in dict.items():
		if (column_map != None):
			if (key not in column_map):
				continue
			column_name = column_map[key]
		else:
			column_name = key	

		if (first):
			first = False
		else:	
			field_names += ","
			values += ","

		field_names += column_name
		try:
			float(value)
		except:
			value = '"' + value + '"'

		values += str(value)

	insert = "insert into " + table + " (" + field_names + ") values (" + values + ")"	
	db_execute(insert, db)		
		
def db_connect(user, pw, db_name):
	return MySQLdb.connect(user=user, passwd=pw, db=db_name)		