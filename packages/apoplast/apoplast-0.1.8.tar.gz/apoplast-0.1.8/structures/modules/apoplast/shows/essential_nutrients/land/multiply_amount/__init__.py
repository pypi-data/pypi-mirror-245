


'''
	import apoplast.shows.essential_nutrients.land.multiply_amount as multiply_land_amount
	multiply_land_amount.smoothly (
		land = land
	)
'''

'''
	Description:
		This multiplies the amount of all the ingredient measures.
		
		This multiplies the amount of all the land measures.
				
			course 1: 	This multiplies the land measures times the amount
		
			course 2: 	This aggregates the nutrient measures times into
						an empty land measures object.
						
			equality check between "course 1" and "course 2"
'''

#
import apoplast.shows.essential_nutrients.land.build.measures as build_land_measures
#
import apoplast.shows.essential_nutrients.grove.seek as grove_seek
#
import apoplast.shows.essential_nutrients.measures.merge as merge_measures
import apoplast.shows.essential_nutrients.measures.multiply as multiply_measures
#


import copy
from fractions import Fraction
import json


'''
	course 2
'''
import apoplast.shows.essential_nutrients.land.measures.sums as land_measures_sums
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
def calculate_from_land_sum (land):
	new_land = build_essential_nutrients_land.eloquently ()
	new_land ["grove"] = copy.deepcopy (land ["grove"]);
	land_measures_sums.calc (
		land = new_land
	)

	return new_land


def multiply_the_grove (land, amount):
	grove = land ["grove"]
	
	original_land_measures = land ["measures"]
	multiply_measures.effortlessly (
		amount = amount,
		measures = land ["measures"]
	)
	
	def for_each (entry):
		nonlocal amount;
	
		natures = entry ["natures"]
		if (len (natures) == 1):		
			entry ["natures"] [0] ["amount"] = str (Fraction (amount));
			multiply_measures.effortlessly (
				amount = amount,
				measures = entry ["measures"]
			)
			
			measures_to_merge = copy.deepcopy (entry ["measures"]);
			if ("biological activity" in measures_to_merge):
				del measures_to_merge ["biological activity"]
			
							
		elif (len (natures) == 0):
			pass;
			
		else:
			print (json.dumps (natures, indent = 4))
			raise Exception ("A nature was found that had more than one.")

		return False		

	grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
	
	
	'''
		This calculates the measurements based on going throug the nutrients
		again from a land copy.
	'''
	new_land_measures = calculate_from_land_sum (copy.deepcopy (land)) ["measures"]
	assert (
		new_land_measures == 
		original_land_measures
	), [{
		"natures": land ["natures"],
		"new": new_land_measures,
		"original": original_land_measures
	}]
	

def smoothly (land, amount):
	#print (json.dumps (land, indent = 4))
	#print ("amount:", amount)

	multiply_the_grove (land, amount)

	return;