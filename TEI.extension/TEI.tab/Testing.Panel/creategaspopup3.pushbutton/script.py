"""
create popup form 3
"""
#import traceback
import subprocess
import os


import pyrevit
from pyrevit import script

import create_gas_object
from functions import print_info


# import Autodesk
# from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB.Structure import StructuralType


def tei_path():
    """
    Returns the directory path TEI.extension. Useful so file path does not have to be coded for each user, use relative paths instead.
    Needs to be defined in each script because our imported functions cannot use pyrevit modules.
    """

    script_path = pyrevit.script.get_script_path()


    #comment out this code in a hook file instead of a script
    script_path = os.path.dirname(os.path.dirname(script_path))


    return os.path.dirname(script_path)




def run_cpython(info, te_path):
    """
    will run the cpython code. This is necessary because the libraries for openpyxl cannot run on IronPython
    """

    #this is the path to where the cpython script is stored
    pathToScript = os.path.join(te_path, 'lib', 'gas_form3.py')
    
    #message sends the job info to editdoc_python3
    message = str(info)
    cmd = ['python', pathToScript, message]

    # Create the subprocess startup info object This prevents the black terminal window from popping up when running hte subprocess
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Run the command and capture the output
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startup_info)

    output, error = process.communicate()
    print_info(error)
    print_info(output)
    return output






# doc = __revit__.ActiveUIDocument.Document
# uidoc = revit.uidoc
# app = __revit__.Application

# active_view = doc.ActiveView
# active_level = doc.ActiveView.GenLevel



#sel = uidoc.Selection



def main():
    path = tei_path()
    info = 'hi'
    
    #output = '[code, max_pressure, max_length, standard?, LPG?]'
    output = run_cpython(info, path)

    #since output of run_cypython is a string of a list, need to parse it back into a python list here
    stripped = output.strip('][').split(', ')
    gas_info = []
    for i in range(len(stripped)):
        gas_info.append(stripped[i].strip("\'"))
    
    
    #if the nonstandard option is selected
    if gas_info[0] == 'NON-STANDARD':
        print('NONSTANDARD')

        #def main(pressure_code, max_pressure, max_length,  pressure_min=None, LPG=False):
        create_gas_object.main(gas_info[1], gas_info[2], gas_info[4], pressure_min=gas_info[3], LPG=gas_info[5])
    else:
        create_gas_object.main(gas_info[1], gas_info[2], gas_info[3])

    #creates the mini chart
    create_gas_object.main(gas_info[1], '7"W.C.', 100)
    
    
if __name__ == '__main__':
    main()