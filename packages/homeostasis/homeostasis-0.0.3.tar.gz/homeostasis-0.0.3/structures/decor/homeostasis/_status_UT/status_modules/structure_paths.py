

import pathlib
from os.path import dirname, join, normpath

def find ():
	this_folder = pathlib.Path (__file__).parent.resolve ()
	structure = normpath (join (this_folder, "../../../../../structures"))

	return [
		normpath (join (structure, "decor")),
		normpath (join (structure, "decor_pip"))
	]
	

def add (paths):
	import pathlib
	this_folder = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	for path in paths:
		sys.path.insert (0, normpath (join (this_folder, path)))