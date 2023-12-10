

'''

'''

#
#	Essential Nutrients: land
#
import apoplast.shows.essential_nutrients.land.add_measured_ingredient as add_measured_ingredient
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import apoplast.shows.essential_nutrients.land.measures.sums as land_measures_sums
import apoplast.shows.essential_nutrients.land.calculate_portions as calculate_portions
	
#
#	Essential Nutrients: grove
#
import apoplast.shows.essential_nutrients.grove.seek as grove_seek
import apoplast.shows.essential_nutrients.grove.seek_count as seek_grove_count
import apoplast.shows.essential_nutrients.grove.has_uniters as has_uniters

#
#	Essential Nutrients: assertions
#
import apoplast.shows.essential_nutrients.assertions.one as essentials_nutrients_assertions_one

	
import json	


def eloquently (
	measured_ingredients_list = [],
	identity = {},
	records = 1
):	
	land = build_essential_nutrients_land.eloquently ()
	grove = land ["grove"]
	natures = land ["natures"]
		
	natures.append ({
		"amount": "1",
		"identity": identity
	})	
	
	for measured_ingredient in measured_ingredients_list:
		if (records >= 1):
			if ("name" in measured_ingredient):
				print ("measured_ingredient", measured_ingredient ['name'])
			else:
				print ("A name was not found in", measured_ingredient)
		
	
		added = add_measured_ingredient.beautifully (
			#
			#	This is a reference to the land.
			#
			land = land,
			
			amount = 1,
			source = identity,
			measured_ingredient = measured_ingredient
		)
		
		assert (added == True), measured_ingredient
		
	'''
		priorities:
			[ ] calculate the essential nutrients sums.
	'''
	land_measures_sums.calc (
		land = land
	)
	
	'''
		After the measure sums have been calculated,
		the portions can be calculated from the sums.
	'''
	calculate_portions.illustriously (
		land = land
	)	
		
		
	'''
		description:
			This makes sure that the story 2 and above "essentials",
			have a uniter that has "natures".
			
			That is make sure if "added, sugars" is listed,
			that "sugars, total" is listed.
		
		example:
			sugars, total	<- make sure that this exists, if "added sugars" is added.
				added, sugars
	'''
	has_uniters.check (grove)
	
	
	
	
	'''
		This asserts that the number of nutrients in the grove is greater than or
		equal to the number of nutrients in the measured ingredients list.
	'''
	grove_count = seek_grove_count.beautifully (grove)
	assert (grove_count >= len (measured_ingredients_list)), [
		grove_count,
		len (measured_ingredients_list)
	]
	
	'''
		priorities:
		
			[ ]	Could or should assert that there are len (measured_ingredients_list)
				number of grove ingredients with 1 "nature".
	'''
	
		
	
	
	'''
		assertions
	'''
	essentials_nutrients_assertions_one.sweetly (
		essentials_nutrients = land
	)	
	
	return land;