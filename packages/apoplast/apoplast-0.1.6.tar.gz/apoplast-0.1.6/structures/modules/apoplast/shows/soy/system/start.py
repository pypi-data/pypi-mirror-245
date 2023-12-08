
'''
import apoplast.shows.soy.system.start as soy_start
ly = soy_start.beautifully ()
'''

import pathlib
import lymphatic.system.start as ly_system_start

def beautifully (
	pid_file = ""
):
	ly = ly_system_start.now (
		process = {
			"cwd": pathlib.Path (__file__).parent.resolve ()
		},
		rethinkdb = [
			f"--daemon",
			f"--pid-file { pid_file }"
		],
		#wait = True
	)

	'''
		ly.stop ()
	'''
	return ly;

	