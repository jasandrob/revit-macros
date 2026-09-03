# -*- coding: utf-8 -*-
"""
changes the pm on mechanical/plumbing sheets
"""

from pyrevit import revit, forms
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

doc = revit.doc

# Target parameter name
param_name = "Drawn By"

# Prompt user for the new value via pyRevit's text input form
new_value = forms.ask_for_string(
    default='',
    prompt='Enter the new value for "Drawn By" (Mech/Plumbing only):',
    title='Batch Update Mechanical Sheets'
)

if new_value:
    # Collect all title blocks placed on sheets in the project
    title_blocks = FilteredElementCollector(doc)\
                    .OfCategory(BuiltInCategory.OST_TitleBlocks)\
                    .WhereElementIsNotElementType()\
                    .ToElements()

    updated_count = 0

    # Start a Revit transaction to apply changes
    with Transaction(doc, "Batch Update Drawn By for M Sheets") as t:
        t.Start()
        
        for tb in title_blocks:
            # Get the sheet element that the title block belongs to
            sheet_id = tb.OwnerViewId
            if sheet_id:
                sheet = doc.GetElement(sheet_id)
                if sheet:
                    sheet_number = sheet.SheetNumber
                    
                    # Check if the sheet number starts with "M" or "P" (case-insensitive)
                    if (sheet_number.upper().startswith("M")) or (sheet_number.upper().startswith("P")):
                        param = tb.LookupParameter(param_name)
                        if param and not param.IsReadOnly:
                            param.Set(str(new_value))
                            updated_count += 1
                
        t.Commit()

    forms.alert("Successfully updated 'Drawn By' to '{}' on {} matching title blocks.".format(new_value, updated_count),title="PM change Complete", warn_icon=False)
else:
    forms.alert("Operation cancelled by user.")