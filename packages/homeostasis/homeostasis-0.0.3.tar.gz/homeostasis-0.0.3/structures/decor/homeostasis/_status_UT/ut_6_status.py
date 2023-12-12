



'''
	https://docs.python.org/3/library/unittest.html#module-unittest
'''

'''
	python -m unittest ut_6_status.py
	python -m unittest *status.py
'''

import pathlib
from os.path import dirname, join, normpath


import status_modules.structure_paths as structure_paths
structure_paths.add (structure_paths.find ())



import homeostasis

import time
import unittest
class CONSISTENCY (unittest.TestCase):
	def test_1 (THIS):
		import pathlib
		from os.path import dirname, join, normpath

		THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
		stasis = normpath (join (THIS_FOLDER, "stasis/6"))


		SCAN = homeostasis.start (
			glob_string = stasis + '/**/*_health.py',
			
			simultaneous = True,
			
			relative_path = stasis,
			module_paths = [
				#* FIND_STRUCTURE_paths (),			
				normpath (join (stasis, "MODULES"))
			]
		)
		status = SCAN ['status']
		paths = status ["paths"]
		
		import json
		print ("Unit test suite 6 status found:", json.dumps (status ["stats"], indent = 4))
		assert (len (paths) == 3)
				
		assert (status ["stats"]["alarms"] == 1)
		assert (status ["stats"]["empty"] == 1)
		assert (status ["stats"]["checks"]["passes"] == 7)
		assert (status ["stats"]["checks"]["alarms"] == 1)

