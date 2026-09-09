# -*- coding: utf-8 -*-
"""
updates blocks
"""
import os
import re
from pyrevit import revit, forms
from Autodesk.Revit.DB import FilteredElementCollector, CADLinkType, ExternalFileUtils, ModelPathUtils, ImportInstance

def select_blocks():
    doc = revit.doc
    uidoc = revit.uidoc

    # Get the active view/sheet ID
    active_view_id = doc.ActiveView.Id
    
    # Collect all CAD Link Types in the model
    link_types = FilteredElementCollector(doc, active_view_id).OfClass(ImportInstance)

    # Filter links that start with "DP_" or "DM_"
    matching_links = {}
    for link in link_types:
    
        # Get the underlying CAD Link Type
        type_id = link.GetTypeId()
        if type_id != doc.GetElement(type_id).Id.InvalidElementId: # safer check
            link_type = doc.GetElement(type_id)
            if isinstance(link_type, CADLinkType):
            
                if link_type.IsExternalFileReference():
                    cad_link_ref = link_type.GetExternalFileReference().GetPath()
                    cad_link_str = ModelPathUtils.ConvertModelPathToUserVisiblePath(cad_link_ref)
                    name = os.path.basename(cad_link_str)
                    #name = link_type.Name
                    
                    if name.startswith("DP_") or name.startswith("DM_"):
                        # Map name to the instance element so we can select it on the sheet
                        matching_links[name] = link_type, cad_link_str   

    

    if not matching_links:
        forms.alert(
            "No linked DWGs found starting with 'DP_' or 'DM_'.", 
            title="Linked DWGs Selector", 
            warn_icon=True
        )
        return

    # Display a multi-select dialog box using pyRevit forms
    selected_names = forms.SelectFromList.show(
        sorted(matching_links.keys(), key=natural_sort_key),
        multiselect=True,
        title="Select Blocks in Model",
        button_name="Update Blocks"
    )

    # If the user made a selection, update Revit's active selection
    if selected_names:

        selected_links = [matching_links[name][1] for name in selected_names]
        
        # selected_elements = [matching_links[name] for name in selected_names]
        # element_ids = [el.Id for el in selected_elements]
        
        # # Set the selection in the active UI document
        # uidoc.Selection.SetElementIds(element_ids)
        
        # forms.alert(
            # "Successfully selected {} linked DWG(s).".format(len(element_ids)), 
            # title="Done", 
            # exitscript=False
        # )

def check_master():
#creates a list of all the details in the sync revit directory

    sync_path = "S:\MECHANICAL\_CostcoDetails\_SyncRevitDetails"
    
    all_items = os.listdir(sync_path)
    
    #get all dwgs
    dwg_files = [
        f for f in all_items
        if os.path.isfile(os.path.join(sync_path, f)) and f.lower().endswith('.dwg')
    ]
    
    for file in dwg_files:
        print(file)


def natural_sort_key(s):
    # Splits the string into text and integer chunks
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
    
    
def main():
    select_blocks()
    check_master()


if __name__ == "__main__":
    main()