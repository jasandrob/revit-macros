
"""
object info code
"""

from pyrevit import revit
from pyrevit import DB, forms

import Autodesk
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = revit.uidoc
active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel


    
# DB.ScheduleSheetInstance.Create(doc, 
# forms.select_sheets()
# sel = __revit__.ActiveUIDocument.Selection

sel = uidoc.Selection
pickedref = sel.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element, "Please select a group")
elem = doc.GetElement(pickedref)
loc = elem.Location
#xyz = XYZ(10,20,30)
id = elem.Id

print(elem.Category)
print(elem)
print("ID " + str(id))

if isinstance(elem, Autodesk.Revit.DB.Group):
    group = elem
    grouptype = group.GroupType

    
    print("Group Name: " + str(group.Name))
    

# #code for revit task dialog
# maindialog = Autodesk.Revit.UI.TaskDialog("hello revit")
# maindialog.MainInstruction = "Helloooo"
# maindialog.MainContent = "This sample shows how to use a REvit task dialog to communicate with the user."
# maindialog.Show()


