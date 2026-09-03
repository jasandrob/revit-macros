
"""
script that will create an error
"""

import os

import pyrevit
from pyrevit import script

import functions as fun
from functions import failer, day, trace_print, print_info


day_info = day()


def tei_path():
	"""
	returns the directory path TEI.extension\TEI.tab\Testing.Panel. Useful so file path does not have to be coded for each user, use relative paths instead
	"""

	script_path = pyrevit.script.get_script_path()
	return os.path.dirname(script_path)



try:
    failer()
except:
    directory = os.path.dirname(os.path.dirname(tei_path()))
    fun.report_error(directory)



