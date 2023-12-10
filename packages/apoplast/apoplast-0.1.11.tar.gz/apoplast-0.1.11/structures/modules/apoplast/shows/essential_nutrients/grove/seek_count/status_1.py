




'''
	python3 insurance.py shows/essential_nutrients/grove/seek_count/status_1.py
'''





import json

def check_1 ():
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
	
	import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
	grove = grove_nurture.beautifully (
		essentials_DB_list = essentials_DB_list
	)

	import apoplast.shows.essential_nutrients.grove.seek_count as seek_grove_count
	count = seek_grove_count.beautifully (grove)
	
	assert (count == 45)
	print ("count:", count)
	
checks = {
	'check 1': check_1
}