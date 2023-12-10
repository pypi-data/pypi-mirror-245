
'''
	description:
		This should be for calculating the land measures sum of 1 treasure,
		where that 1 treasure only has 1 package.
'''

'''
	import apoplast.shows.essential_nutrients.land.calculate_portions as calculate_portions
	calculate_portions.illustriously (
		land = land
	)
'''
	
from fractions import Fraction
	
def illustriously (
	land = {}
):
	grove = land ['grove']
	land_measures = land ['measures']
	
	for ingredient in grove:
		if (len (ingredient ["natures"]) == 0):
			continue;
		if (len (ingredient ["natures"]) >= 2):
			raise Exception (f"This def is for calculating the sum of a grove with only 1 treasure (food or supp) added")
		
		number_of_packages = Fraction (
			ingredient ["natures"] [ 0 ] ["amount"]
		)
		assert (number_of_packages == 1)

			
	return;