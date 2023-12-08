




'''
	import soy.databases.supp.sales.build as build_supp_DB
	build_supp_DB.superbly ()
'''


import soy.connect as connect

def superbly ():
	[ r, c ] = connect.it ()
	
	r.db_create ('supp').run (c)
	assert ("supp"	in r.db_list ().run (c))

