

'''

'''

'''
	priotities:
		build "food/sales"
		build "supp/sales"		
'''

import soy.databases.supp.sales.build as build_supp_DB
import soy.databases.supp.sales.build as build_supp_sales_table

import soy.databases.food.sales.build as build_food_DB
import soy.databases.food.sales.build as build_foods_sales_table
			
def superbly ():
	build_supp_DB.superbly ()
	build_supp_sales_table.superbly ()	

	build_food_DB.superbly ()
	build_foods_sales_table.superbly ()	

