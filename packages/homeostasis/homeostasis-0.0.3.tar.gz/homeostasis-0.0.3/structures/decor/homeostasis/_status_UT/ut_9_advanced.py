



'''
	https://docs.python.org/3/library/unittest.html#module-unittest
'''

'''
	python -m unittest ut_9_status.py
	python -m unittest *status.py
'''

import pathlib
from os.path import dirname, join, normpath

import status_modules.structure_paths as structure_paths
structure_paths.add (structure_paths.find ())

ut_number = "9"

import homeostasis
import homeostasis.db as homeostasis_db
	
import time
import unittest
class consistency (unittest.TestCase):
	def test_1 (this):
		import pathlib
		from os.path import dirname, join, normpath

		this_folder = pathlib.Path (__file__).parent.resolve ()
		stasis = normpath (join (this_folder, f"stasis/{ ut_number }"))
		dynamics = normpath (join (this_folder, f"dynamics/{ ut_number }"))

		records_1 = homeostasis_db.records (
			db_directory = normpath (join (dynamics, f"status_db"))
		)

		scan = homeostasis.start (
			glob_string = stasis + '/**/guarantee_*.py',
			simultaneous = True,
			relative_path = stasis,
			module_paths = [
				normpath (join (stasis, "modules"))
			],
			db_directory = normpath (join (dynamics, f"status_db")),
			
			
			before = normpath (join (stasis, "before.py")),
			after = normpath (join (stasis, "after.py"))
		)
		status = scan ["status"]
		paths = status ["paths"]
		
		'''
		import json
		print (
			f"Unit test suite { ut_number } status found:", 
			json.dumps (status ["stats"], indent = 4)
		)
		'''
		
		assert (len (paths) == 1)
		
		def check_status (status):
			assert (status ["stats"]["alarms"] == 0)
			assert (status ["stats"]["empty"] == 0)
			assert (status ["stats"]["checks"]["passes"] == 500)
			assert (status ["stats"]["checks"]["alarms"] == 0)

		
		check_status (scan ["status"])

		records_2 = homeostasis_db.records (
			db_directory = normpath (join (dynamics, f"status_db"))
		)
		assert (len (records_2) == (len (records_1) + 1))
		
		last_record = homeostasis_db.last_record (
			db_directory = normpath (join (dynamics, f"status_db"))
		)
		check_status (last_record)
