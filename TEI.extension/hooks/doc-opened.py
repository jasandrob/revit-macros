

"""
doc opened hook. Will save the job info to a csv and then update current using editdoc_python3.py
"""


import os
import csv
import subprocess
import io
import traceback

# import datetime
# from datetime import datetime as dd
import time

import pyrevit
from pyrevit import revit
from pyrevit import script
from pyrevit import forms


import Autodesk.Revit.DB as DB

#imports local functions from TEI/TEI.extension/lib
from settings import debug_mode
import functions as fun
from functions import print_info, trace_print, failer, day






"""
HERE IS CODE FOR MAKING THE POPUP LIST SELECTOR
items = ['1', '2', '3']
a = forms.SelectFromList.show(items, button_name='Select Item')
print(a)
"""



def tei_path():
    """
    Returns the directory path TEI.extension. Useful so file path does not have to be coded for each user, use relative paths instead.
    Needs to be defined in each script because our imported functions cannot use pyrevit modules.
    """

    script_path = pyrevit.script.get_script_path()

    #uncomment this code in script file instead of a hook
    # script_path = os.path.dirname(os.path.dirname(script_path))   

    return os.path.dirname(script_path)


def find_spath():
    """
    returns the directory path of the workshared document in the Master server
    """

    homepath = os.path.expanduser('~')
    doc = __eventargs__.Document
    # # when using in a tab button
    # doc = __revit__.ActiveUIDocument.Document

    rsn_paths = {'C://Users' : homepath}
    server_path = revit.serverutils.get_server_path(doc, rsn_paths)

    return server_path



def jobfind(path):
    """
    takes the server path of a job and returns [pathlist, job number, job details] as a list
    """


    #splits the path into a list of directories
    pathlist = path.split('\\')

    #hopefully the 3rd to last file has the job number
    jobparse = pathlist[-3]
    jobdeets = jobparse.split("-")

    jobnum = "-".join(jobdeets[:2])
    job_deet = "-".join(jobdeets[2:])
        


    return [pathlist, jobnum, job_deet]



def run_cpython(info, te_path):
    """
    will run the cpython code. This is necessary because the libraries for openpyxl cannot run on IronPython
    """

    #this is the path to where the cpython script is stored
    pathToScript = os.path.join(te_path, 'lib', 'editdoc_python3.py')
    
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
    
 
 
def popup_dialog(string, te_path):
    """
    Takes the string given from editdoc_python3.py and creates a popup dialog to notify user that the job has been recorded
    """
    
    split = string.splitlines()
    
    #city_info and description are the last two lines sent from editdoc
    info = split[-2:]
    
    
    if str(info[-1]) != 'ERROR':
        msg = info[0] + " - " + info[1]
        
        path_to_icon = os.path.join(te_path, 'bin', 'tei.png')
        forms.toast(msg, title="Added Job to Current as:", appid=' ', icon=path_to_icon)
        
    else:
        msg = "Could not add job to current"
        
        path_to_icon = os.path.join(te_path, 'bin', 'tei.png')
        forms.toast(msg, title="ERROR", appid=' ', icon=path_to_icon)
 
  

	
def main(): 

    if debug_mode:
        print("DEBUG MODE ON")


    dir = tei_path()
    start = time.time()
    
    #will send an error popup if job is not recorded, also records traceback
    msg = ''
    trace = []
    
    try:
        te_path = tei_path()
        s_path = find_spath()
        jobinfo = jobfind(s_path)
        
    except Exception as error:
        err_msg = "Could not find job directory                              "
        msg = msg + err_msg
        fun.report_error(dir)
        

    try:
        output = run_cpython(jobinfo[1:], te_path)
        popup_dialog(output, te_path)
        
    except:
        err_msg = "Could not paste job to current            "
        msg = msg + err_msg
        fun.report_error(dir)
       
       
    if len(msg) > 0:
        path_to_icon = os.path.join(te_path, 'bin', 'tei.png')
        forms.toast(msg, title="Job not recorded", appid=' ', icon=path_to_icon)
        
        


   
    end = time.time() - start
    print_info("Finished in " + str(end) + " seconds")

if __name__ == "__main__":
	main()