
'''
	python3 insurance.py shows/essential_nutrients/land/measures/sums/status/status_1.py
'''

import apoplast.shows.essential_nutrients.land.measures.sums as land_measures_sums
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land

def check_1 ():
	land = build_essential_nutrients_land.eloquently ()
	land_measures_sums.calc (
		land = land
	)

	return;
	
	
checks = {
	'check 1': check_1 
}