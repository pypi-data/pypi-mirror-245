


'''
import soy.databases.food.sales.indexes as build_foods_sales_indexes
build_foods_sales_indexes.superbly ()
'''

import soy.connect as connect
	
def superbly ():
	[ r, c ] = connect.it ()

	foods_table = r.db ('foods').table ("sales");

	foods_table.index_create (
		"nature_name",
		r.row ["struct_2"] ["product"] ["name"]
	).run (c)
	
	foods_table.index_wait ().run (c);