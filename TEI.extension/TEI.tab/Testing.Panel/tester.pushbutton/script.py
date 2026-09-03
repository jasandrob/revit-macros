"""
tester code to test whatever
"""
#import traceback
import subprocess
import os


import pyrevit
from pyrevit import script

from functions import print_info, report_error

def tei_path():
    """
    Returns the directory path TEI.extension. Useful so file path does not have to be coded for each user, use relative paths instead.
    Needs to be defined in each script because our imported functions cannot use pyrevit modules.
    """

    script_path = pyrevit.script.get_script_path()


    #comment out this code in a hook file instead of a script
    script_path = os.path.dirname(os.path.dirname(script_path))


    return os.path.dirname(script_path)




def main():
    tei = tei_path()
    print(tei)
    
    report_error(tei, error="hi")
    
    
if __name__ == '__main__':
    main()