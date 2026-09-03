"""
code to edit gas
"""
import sys
import subprocess
import os


from pyrevit import revit
from pyrevit import DB, forms\


from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction




import pyrevit
from pyrevit import script

import create_gas_object
import gas_calc
from functions import print_info





doc = __revit__.ActiveUIDocument.Document
uidoc = revit.uidoc
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel


test_list = [[1.0/12, 100],
              [1.5/12, 200],
              [2.0/12, 300],
              [2.5/12, 400],
              [3.0/12, 55500]]




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



def get_pipe_sizes():
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
        # create_gas_object.main(gas_info[1], gas_info[2], gas_info[4], pressure_min=gas_info[3], LPG=gas_info[5])
        size_list = gas_calc.size_gas(gas_info[1], gas_info[2], gas_info[4], gas_info[3], gas_info[5])
    else:
        # create_gas_object.main(gas_info[1], gas_info[2], gas_info[3])
        size_list = gas_calc.size_gas(gas_info[1], gas_info[2], gas_info[3])

    #returns a list with rows of [pipe_size, associated load]
    return size_list



def getPipes():
#gets the elements of all pipes in the current view
    collector = FilteredElementCollector(doc, active_view.Id)
    collector.OfCategory(BuiltInCategory.OST_PipeCurves)
    pipesInView = collector.ToElements()

    return pipesInView



def destring(string):
    #will convert gas comment to number, even with commas

    #do not return anything if its a different kind of comment
    try:
        if string[-4:] == "MBH)":

            num_string = string[1:-5]
            num_string_comma = num_string.replace(',', '')
            #turn into int
            num = int(num_string_comma)
            return num
        else:
            return None
        
    except:
        return None
    

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    #compare floating-point numbers
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def compare(g_list, pipe_info_lists):
#compares pipe info list to gas size to determine required size

    pipe_info_lists_r = []

    for p_info_list in pipe_info_lists:
        
        changed = False
        for i in g_list:
            
            if (i[1] >= p_info_list[2]) or isclose(i[1],p_info_list[2]):
                
                #returns the pipe element and new diameter
                pipe_info_lists_r.append([p_info_list[0], i[0], p_info_list[2]])
                changed = True
                break
        
        if changed is False:
            print("error sizing gas")
            return None
        
    return pipe_info_lists_r

        

def get_pipe_info(pipesInView):
#given the elements of the pipes in the view, return a list with the pipe info [id, size, comment] of all the pipes
    pipe_info_lists = []

    for i in pipesInView:
        commentsParameter = i.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
        comments = commentsParameter.AsString()
        
        #list for pipe_id, pipe_size, pipe_comment
        p_info_list = (i, i.Diameter, destring(comments))
    
        #remove the values that have non-gas comment
        if isinstance(p_info_list[2], int):
            pipe_info_lists.append(p_info_list)
        
        
    return pipe_info_lists
        
def change_pipe_size(pipe_element_list):
    """
    pipe_element_list: a 3d list with rows as follows [pipe_element, diameter, comment_text]
    """


    t = Transaction(doc, "Change pipe diameter")
    t.Start()
    
    print_info(pipe_element_list)
    for [pipe, diameter, text] in pipe_element_list:
        
        diameterParam = pipe.Parameter[BuiltInParameter.RBS_PIPE_DIAMETER_PARAM]
        
        if (diameterParam != None and diameterParam.IsReadOnly == False):
            newDiameterInFeet = diameter
            diameterParam.Set(newDiameterInFeet)
   

        
    t.Commit()


def pipe_edit(size_list):
    """
    uses the given list to edit the pipe sizes
    """
    pipesInView = getPipes()
    pipe_info_lists = get_pipe_info(pipesInView)
    sized_pipes_list = compare(size_list, pipe_info_lists)


    change_pipe_size(sized_pipes_list)



def main():
    # size_list = get_pipe_sizes()
    # pipe_edit(size_list)
    
    
if __name__ == '__main__':
    main()
