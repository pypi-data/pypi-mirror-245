
'''
	python3 insurance.py clouds/food_USDA/nature/_status/status_1.py
'''

from apoplast.insure.override_print import override_print
import apoplast.insure.equality as equality

import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples
import apoplast.clouds.food_USDA.nature as food_USDA_nature

import json	
	
def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	
	nature = food_USDA_nature.create (walnuts_1882785)
	equality.check (nature ["identity"]["FDC ID"], "1882785")
	
	
	
	
	
checks = {
	'check 1': check_1
}