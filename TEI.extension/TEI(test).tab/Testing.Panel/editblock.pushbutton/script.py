# -*- coding: utf-8 -*-
"""
opens selected block in autocad
"""

import os, sys
from pathlib import Path

from Autodesk.Revit.DB import CADLinkType, ImportInstance, ModelPathUtils, ExternalFileUtils
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Exceptions import OperationCanceledException
from pyrevit import forms, script

# Get current document and UIDocument
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get current selection
selected_ids = uidoc.Selection.GetElementIds()

# If nothing is selected, prompt the user to pick one interactively
if not selected_ids:
    try:

        picked_ref = uidoc.Selection.PickObject(ObjectType.Element, "Please select a CAD link in the view.")
        if picked_ref:

            selected_ids = [picked_ref.ElementId]
    except OperationCanceledException:
        # User pressed ESC to cancel the prompt
        script.exit()


cad_link_type = None

# Loop through selection to find a CAD link type or instance
for elem_id in selected_ids:
    elem = doc.GetElement(elem_id)
    
    # If user selected the instance in the drawing area
    if isinstance(elem, ImportInstance):
        type_elem = doc.GetElement(elem.GetTypeId())
        if isinstance(type_elem, CADLinkType):
            cad_link_type = type_elem
            break
            
    # If user selected the type directly (e.g. from Project Browser)
    elif isinstance(elem, CADLinkType):
        cad_link_type = elem
        break

if not cad_link_type:
    forms.alert("The selected element is not a linked CAD file. Please select a valid CAD link.", exitscript=True)

# Verify if it is actually linked (not just imported)
if not cad_link_type.IsExternalFileReference():
    forms.alert("The selected CAD file is 'Imported' rather than 'Linked'. Import instances do not reference an external file path.", exitscript=True)


#safety check to ensure selected linked file is in the same directory folder as the workshared model
def confirm_or_exit(message, title="Confirm Action", continue_label="Continue", exit_label="Exit"):
    """Show a dialog with Continue/Exit options; exits script unless user chooses continue."""
    """Show a dialog with Continue/Exit options; exits silently if not continued."""
    choice = forms.alert(
        message,
        title=title,
        options=[continue_label, exit_label],
        exitscript=False,
    )
    if choice != continue_label:
        sys.exit()

if doc.IsWorkshared:
    central_model_path = doc.GetWorksharingCentralModelPath()
    
    # Convert the ModelPath object to a readable string format
    central_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(central_model_path)
    parts = Path(central_path).parts
    
    job_dir = parts[1:4]

    elem_id = elem.GetTypeId()
    elem_type = doc.GetElement(elem_id)
    cad_link_ref = elem_type.GetExternalFileReference().GetPath()
    cad_link_str = ModelPathUtils.ConvertModelPathToUserVisiblePath(cad_link_ref)
    
    block_name = os.path.basename(cad_link_str)
    parts_blk_path = Path(cad_link_str).parts
    if parts_blk_path[1:4] != job_dir:
        confirm_or_exit(
            "This CAD link is referenced outside of this job's directory:\n\n {}\n\nDo you want to continue?".format(cad_link_str),
            title="Edit CAD Link",
            continue_label="Continue",
            exit_label="Exit",
        )
    

# Retrieve file path and open in AutoCAD
try:
    ext_ref = cad_link_type.GetExternalFileReference()
    if ext_ref:
        model_path = ext_ref.GetPath()
        file_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(model_path)
        
        if os.path.exists(file_path):
            
            
            #checks we are not on master
            master_path = "S:\\MECHANICAL\_CostcoDetails"
            p = Path(file_path).parts
            if Path(*p[0:3]) != Path(master_path):
                
                # Opens the file with its default registered application (AutoCAD for .dwg)
                os.startfile(file_path)
                forms.toaster.send_toast("Opening CAD file...", title="pyRevit")                
                    
                
            else:
                forms.alert(
                    msg="The selected block is linked to the MASTER directory. Blocks should be linked to a folder in the job's directory.",
                    sub_msg="{}".format(file_path), 
                    title="Master Block Selected - Error")
            

        else:
            forms.alert("The file path could not be found on disk", title="File Not Found")
    else:
        forms.alert("Could not retrieve the external file reference for this CAD link.", title="Error")

except Exception as e:
    forms.alert("Failed to open CAD link.\n\nError: {}".format(str(e)), title="Error")