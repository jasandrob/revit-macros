# -*- coding: utf-8 -*-
"""
reload linked cad code
"""

import os
from Autodesk.Revit.DB import CADLinkType, ImportInstance, ModelPathUtils
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

# Retrieve file path and open in AutoCAD
try:
    ext_ref = cad_link_type.GetExternalFileReference()
    if ext_ref:
        model_path = ext_ref.GetPath()
        file_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(model_path)
        
        if os.path.exists(file_path):
            # Opens the file with its default registered application (AutoCAD for .dwg)
            os.startfile(file_path)
            forms.toaster.send_toast("Opening CAD file...", title="pyRevit")
        else:
            forms.alert("The file path could not be found on disk:\n\n{}".format(file_path), title="File Not Found")
    else:
        forms.alert("Could not retrieve the external file reference for this CAD link.", title="Error")

except Exception as e:
    forms.alert("Failed to open CAD link.\n\nError: {}".format(str(e)), title="Error")