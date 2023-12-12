



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

ut_number = "7"

import homeostasis

import time
import unittest
class CONSISTENCY (unittest.TestCase):
	def test_1 (THIS):
		import pathlib
		from os.path import dirname, join, normpath

		THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()
		stasis = normpath (join (THIS_FOLDER, f"stasis/{ ut_number }"))


		scan = homeostasis.start (
			glob_string = stasis + '/**/guarantee_*.py',
			
			simultaneous = True,
			
			relative_path = stasis,
			module_paths = [
				normpath (join (stasis, "modules"))
			]
		)
		status = scan ['status']
		paths = status ["paths"]
		
		import json
		print (f"Unit test suite { ut_number } status found:", json.dumps (status ["stats"], indent = 4))
		assert (len (paths) == 1)
				
		assert (status ["stats"]["alarms"] == 0)
		assert (status ["stats"]["empty"] == 0)
		assert (status ["stats"]["checks"]["passes"] == 1)
		assert (status ["stats"]["checks"]["alarms"] == 1)

