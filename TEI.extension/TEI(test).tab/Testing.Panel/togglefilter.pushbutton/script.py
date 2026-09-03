#toggles the vent filter on and off

# -*- coding: utf-8 -*-
__title__ = "Toggle Vent\nFilter"

from Autodesk.Revit.DB import Transaction
from pyrevit import revit, forms

doc = revit.doc
view = revit.active_view

# 1. Get all filter IDs applied to the view
filter_ids = view.GetFilters()
found_filter = False

# 2. Start the transaction properly
with revit.Transaction("Toggle Vent Filter"):
    for f_id in filter_ids:
        filter_elem = doc.GetElement(f_id)
        # Check if 'vent' is in the name (case-insensitive)
        if "vent" in filter_elem.Name.lower():
            found_filter = True
            
            # 3. Perform the toggle inside the 'with' block
            current_visibility = view.GetFilterVisibility(f_id)
            view.SetFilterVisibility(f_id, not current_visibility)

# 4. Feedback if nothing was found
if not found_filter:
    forms.alert("No filter containing 'vent' was found in this view.", title="Filter Not Found")