# -*- coding: utf-8 -*-
"""
code to plus/subtract gas
"""
# import sys
# import subprocess
# import os


from pyrevit import revit, DB, forms
# from pyrevit import forms\


# from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
from Autodesk.Revit.DB import BuiltInParameter
#from Autodesk.Revit.UI.Selection import ObjectType
import Autodesk.Revit.DB.Plumbing as Plumb

# import pyrevit
# from pyrevit import script

# import create_gas_object
# import gas_calc
# from functions import print_info


def select(user_input):
    
    if user_input is not None:
        try:
            # Attempt to convert to float or int
            numeric_value = int(user_input)
            
            
            
            # Proceed with updating the selection
            selection = revit.get_selection()

            if not selection:
                message = "No pipes selected. Please select pipes in the model."
                selection = revit.pick_elements(message)

            sel_pipes = [el for el in selection if isinstance(el, Plumb.Pipe)]
            pipe_info_lists = get_pipe_comment(sel_pipes)
            
            if sel_pipes:
                with revit.Transaction("Update Pipe Comment"):
                    for p_list in pipe_info_lists:
                        cur_comment = p_list[2]
                        if cur_comment:
                            param = p_list[0].get_Parameter(DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
                            if param and not param.IsReadOnly:
                                
                                new_MBH = int(cur_comment) + numeric_value
                                new_MBH_formatted = "{:,}".format(new_MBH)
                                new_comment = "(" + str(new_MBH_formatted) + " MBH)"
                                param.Set(new_comment)
                forms.toast("Successfully updated {} pipes?".format(len(pipe_info_lists)), title="Update Complete")
            else:
                forms.alert("No pipes selected.", title="Warning")
            
        except ValueError:
            forms.alert("Please enter a valid numeric value.", title="Invalid Input")


def query():
    # 1. Ask the user for input
    user_input = forms.ask_for_string(
        prompt="Enter a numeric value for the comment:",
        title="Set Pipe Comment",
        default="0"
    )
    
    return user_input

    
def get_pipe_comment(sel_pipes):
#given a list of pipe elements, return a list with the pipe info [id, size, comment] of all the pipes
    pipe_info_lists = []

    for i in sel_pipes:
        commentsParameter = i.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
        comments = commentsParameter.AsString()
        
        #list for pipe_id, pipe_size, pipe_comment
        p_info_list = (i, i.Diameter, destring(comments))
    
        #remove the values that have non-gas comment
        if isinstance(p_info_list[2], int):
            pipe_info_lists.append(p_info_list)
        
        
    return pipe_info_lists


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

def main():
    user_input =  query()
    select(user_input)
    
    
if __name__ == '__main__':
    main()
