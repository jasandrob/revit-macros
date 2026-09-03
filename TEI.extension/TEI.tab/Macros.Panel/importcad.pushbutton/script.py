# -*- coding: utf-8 -*-
"""
link cad code
"""

import os, clr
from pyrevit import revit, DB, forms
from Autodesk.Revit.DB import DWGImportOptions, ImportPlacement, Transaction, TransactionGroup, ElementId

doc = revit.doc
uidoc = revit.uidoc

# 1. Ensure the active view is a Sheet
active_view = doc.ActiveView
if not isinstance(active_view, DB.ViewSheet):
    forms.alert("Please open the target Sheet before running this script.", exitscript=True)

# 2. Prompt user to select multiple DWG files from a directory
dwg_files = forms.pick_file(
    file_ext='dwg',
    multi_file=True,
    title='Select DWG Files to link'
)

if not dwg_files:
    forms.alert("No DWG files selected.", exitscript=True)

# 3. Configure DWG link Options
# You can adjust placement, units, colors, etc., based on your standards
link_options = DWGImportOptions()
link_options.Placement = ImportPlacement.Centered
#link_options.AutoSelectViews = True
# If you want them linked (not linked), set Link = False
link_options.ColorMode = DB.ImportColorMode.Preserved

# 4. Execute the Import inside a Transaction Group
success_count = 0
for dwg_path in dwg_files:
    file_name = os.path.basename(dwg_path)
    
    with Transaction(doc, "Link " + file_name) as t:
        t.Start()
        try:
            # This signature matches DWGImportOptions precisely
            link_result = doc.Link(dwg_path, link_options, active_view)
            
            if link_result: # doc.Import returns a boolean directly when out param is passed in IronPython
                t.Commit()
                success_count += 1
            else:
                t.RollBack()
                print("Failed to link: {}".format(file_name))
        except Exception as e:
            t.RollBack()
            print("Error linking {}: {}".format(file_name, str(e)))

# 5. Summary Notification
forms.alert(
    "Successfully linked {} of {} DWG file(s) onto sheet: {}".format(
        success_count, len(dwg_files), active_view.SheetNumber
    ),
    title="Batch DWG Link Complete",
    warn_icon=False
)