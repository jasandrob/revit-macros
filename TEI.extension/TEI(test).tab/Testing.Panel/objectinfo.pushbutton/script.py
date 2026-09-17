
"""
object info code
"""

from pyrevit import revit
from pyrevit import DB, forms

# import Autodesk
from Autodesk.Revit.DB import FilteredElementCollector, CADLinkType, ExternalFileUtils, ModelPathUtils, Group
from Autodesk.Revit.UI import Selection

doc = __revit__.ActiveUIDocument.Document
uidoc = revit.uidoc
active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel


    
# DB.ScheduleSheetInstance.Create(doc, 
# forms.select_sheets()
# sel = __revit__.ActiveUIDocument.Selection

sel = uidoc.Selection
pickedref = sel.PickObject(Selection.ObjectType.Element, "Please select a group")
elem = doc.GetElement(pickedref)
loc = elem.Location
#xyz = XYZ(10,20,30)
id = elem.Id

print("CATEGORY: {}".format(elem.Category.Name))
print("ELEMENT: {}".format(elem))
print("ID: {}".format(id))

if isinstance(elem, Group):
    group = elem
    grouptype = group.GroupType

    
    print("Group Name: " + str(group.Name))



def get_link_path():

    # Get the underlying CAD Link Type
    type_id = elem.GetTypeId()
    if type_id != doc.GetElement(type_id).Id.InvalidElementId: # safer check
        link_type = doc.GetElement(type_id)
        if isinstance(link_type, CADLinkType):
        
            if link_type.IsExternalFileReference():
                cad_link_ref = link_type.GetExternalFileReference().GetPath()
                cad_link_str = ModelPathUtils.ConvertModelPathToUserVisiblePath(cad_link_ref)
                print("LINK PATH: {}".format(cad_link_str))

get_link_path()
# #code for revit task dialog
# maindialog = Autodesk.Revit.UI.TaskDialog("hello revit")
# maindialog.MainInstruction = "Helloooo"
# maindialog.MainContent = "This sample shows how to use a REvit task dialog to communicate with the user."
# maindialog.Show()


