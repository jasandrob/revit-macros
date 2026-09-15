# -*- coding: utf-8 -*-
"""
updates the path of selected block
"""
import shutil
import os

from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, RevitLinkType, Transaction, CADLinkType
from Autodesk.Revit.DB import ModelPathUtils, ExternalResourceReference, ExternalResourceTypes, PathType
from Autodesk.Revit.UI import Selection
from Autodesk.Revit.Exceptions import OperationCanceledException
from pyrevit import script, forms


import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import OpenFileDialog, DialogResult

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


# 1. Prompt user to select a CAD Link instance in the view
try:
    selected_ref = uidoc.Selection.PickObject(
        Selection.ObjectType.Element, 
        "Select a CAD Link instance to reload."
    )
    selected_element = doc.GetElement(selected_ref)

    #Verify the selected element is a link instance

    selected_element_type = doc.GetElement(selected_element.GetTypeId())
    if not isinstance(selected_element_type, CADLinkType):
        forms.alert("The selected element is not a CAD Link instance.", exitscript=True)
        
    #Get the underlying RevitLinkType
    link_type_id = selected_element.GetTypeId()
    link_type = doc.GetElement(link_type_id)



except OperationCanceledException:
    # User canceled selection
    script.exit()
except Exception as e:
    # An error occurred during selection
    forms.alert("An unexpected error occurred:\n{}".format(str(e)), title="Selection Error")
    script.exit()

# 2. Open a file dialog to choose the new Revit file path
file_dialog = OpenFileDialog()
file_dialog.Filter = "Revit Files (*.dwg)|*.dwg"
file_dialog.Title = "Select New Revit File Path for Link"

if file_dialog.ShowDialog() == DialogResult.OK:
    new_filepath = file_dialog.FileName
    
    # 3. Load the link from the new path within a transaction
    try:
        
        # Convert string path to ModelPath
        model_path = ModelPathUtils.ConvertUserVisiblePathToModelPath(new_filepath)
        
        # Wrap the model path into an ExternalResourceReference
        ext_ref = ExternalResourceReference.CreateLocalResource(
            doc, 
            ExternalResourceTypes.BuiltInExternalResourceTypes.RevitLink, 
            model_path, 
            PathType.Absolute
        )
        
        t = Transaction(doc, "Reload Link from New Path")
        t.Start()
        
        # Reload the link type from the new location
        link_type.LoadFrom(ext_ref)
        
        t.Commit()
        
        forms.alert("Successfully reloaded link from:\n{}".format(new_filepath), title="Success")
        
    except Exception as e:
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
        forms.alert("Failed to reload link. Error:\n{}".format(str(e)), title="Error")
else:
    script.exit()