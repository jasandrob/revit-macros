# -*- coding: utf-8 -*-
"""
fixes the fitting scale
"""

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
from pyrevit import script, forms

doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView

# Collect all pipe fittings visible in the active view
fittings = FilteredElementCollector(doc, view.Id)\
            .OfCategory(BuiltInCategory.OST_PipeFitting)\
            .WhereElementIsNotElementType()\
            .ToElements()

count = 0
count_unchecked = 0

# Start a Revit transaction to modify element parameters
t = Transaction(doc, "Uncheck Use Annotation Scale for Transition Fittings")
t.Start()

for fitting in fittings:
    # Get element name and type name in lowercase for case-insensitive matching
    #elem_name = fitting.Name.ToLower() if fitting.Name else ""
    type_elem = doc.GetElement(fitting.GetTypeId())
    type_name = type_elem.FamilyName.ToLower() if type_elem and type_elem.FamilyName else ""
    
    # Check if "transition" is in the name or type name
    if "transition" in type_name or "reducer" in type_name:
        # Look up the "Use Annotation Scale" parameter
        param = fitting.LookupParameter("Use Annotation Scale")
        count += 1
        if param and not param.IsReadOnly:
            # Set the parameter value to 0 (False / Unchecked)
            if param.AsInteger() != 0:
                param.Set(0)
                count_unchecked += 1

t.Commit()

# Notify user of completion
if count_unchecked > 0:
    forms.alert("Successfully unchecked 'Use Annotation Scale' for {}/{} transition fitting(s).".format(count_unchecked,count), title="Completed",warn_icon=False)
else:
    forms.alert("Unchecked 'Use Annotation Scale' for {}/{} transition fitting(s).".format(count_unchecked,count), title="Completed")