




'''
	import soy.databases.food.sales.build as build_foods_sales_table
	build_foods_sales_table.superbly ()
'''

import soy.connect as connect

def superbly ():
	DB = "food"	
	table = "sales"
	primary_key = "emblem"

	[ r, c ] = connect.it ()
	
	proceeds = r.db (DB).table_create (
		table,
		primary_key = primary_key
	).run (c)
	
	assert (table in r.db (DB).table_list ().run (c))
	assert (primary_key == r.db (DB).table (table).config (c) ["primary_key"])


