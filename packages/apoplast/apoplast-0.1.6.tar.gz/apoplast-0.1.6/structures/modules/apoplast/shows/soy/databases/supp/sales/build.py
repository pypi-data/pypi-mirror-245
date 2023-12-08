




'''
	import soy.databases.supp.sales.build as build_supp_sales_table
	build_supp_sales_table.superbly ()
'''

import soy.connect as connect

def superbly ():
	primary_key = "primary_key"
	table = "sales"
	db = "supp"

	[ r, c ] = connect.it ()
	
	proceeds = r.db (db).table_create (
		table,
		primary_key = primary_key
	).run (c)
	
	assert (table in r.db (db).table_list ().run (c))
	assert (primary_key == r.db (db).table (table).config (c) ["primary_key"])


