

'''
	import apoplast.shows.soy.system.climate as soy_climate
	soy_climate.prepare ()
'''

import copy
import lymphatic.system.climate as ly_system_climate

def prepare (parameters):
	ports = parameters ["ports"]

	print ("ports:", ports)

	ly_system_climate.change ("ports", ports)
	climate ["ports"] = ports
	
climate = {
	"ports": {}
}

def change (field, plant):
	#global CLIMATE;
	climate [ field ] = plant


def find (field):
	return copy.deepcopy (climate) [ field ]