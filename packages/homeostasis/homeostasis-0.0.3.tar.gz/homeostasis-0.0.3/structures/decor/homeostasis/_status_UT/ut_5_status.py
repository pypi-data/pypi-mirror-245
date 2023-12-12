



'''
	https://docs.python.org/3/library/unittest.html#module-unittest
'''

'''
	python -m unittest ut_5_status.py

	python -m unittest *status.py
'''

import pathlib
from os.path import dirname, join, normpath

import status_modules.structure_paths as structure_paths
structure_paths.add (structure_paths.find ())

import homeostasis

import time
import unittest
class consistency (unittest.TestCase):
	def test_1 (THIS):
		import pathlib
		THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

		from os.path import dirname, join, normpath
		stasis = normpath (join (THIS_FOLDER, "stasis/5"))

		print ("SEARCHING:", stasis)

		SCAN = homeostasis.start (
			glob_string = stasis + '/**/*_health.py',
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
		assert (len (paths) == 1)
				
		assert (status ["stats"]["alarms"] == 0)
		assert (status ["stats"]["empty"] == 0)
		assert (status ["stats"]["checks"]["passes"] == 1)
		assert (status ["stats"]["checks"]["alarms"] == 0)

