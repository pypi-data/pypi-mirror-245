



'''
	priorities, plan:
		
		This should be for accessing the list of essential 
		nutrients, and the nutrients that they are comprised of.
		
		There could be another access point (like a rethinkdb weave
		access point) for accessing a network weave.
'''

'''
	#
	#	Accessing the core DB:
	#
	import apoplast.shows.essential_nutrients.DB.access as access
	essentials_DB = access.DB ()
'''

'''
	#
	#	Accessing a static DB for consistency purposes, etc.
	#
	import pathlib
	from os.path import dirname, join, normpath
	this_directory = pathlib.Path (__file__).parent.resolve ()	

	import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list
	import apoplast.shows.essential_nutrients.DB.access as access
	essentials_DB_list = essentials_list.retrieve (
		essentials_DB = access.DB (
			normpath (join (this_directory, "essentials.JSON"))
		)
	)
'''

'''
	#
	#	Not sure what this does exactly...
	#

	#
	#	Accessing another DB (replica, etc.):
	#
	import apoplast.shows.essential_nutrients.DB.access as access
	import apoplast.shows.essential_nutrients.DB.path as essentials_DB_path
	essentials_DB = access.DB (
		path = essentials_DB_path.find ()
	)
'''

from tinydb import TinyDB, Query
import apoplast.shows.essential_nutrients.DB.path as essentials_DB_path
	
def DB (
	path = essentials_DB_path.find (),
	sort_keys = True
):
	DB = TinyDB (
		path, 
		sort_keys = sort_keys
	)
	
	return DB;