# -*- coding: utf-8 -*-
"""
updates blocks
"""
import os
from pyrevit import revit, forms
from Autodesk.Revit.DB import FilteredElementCollector, CADLinkType, ExternalFileUtils, ModelPathUtils, ImportInstance

def main():
    doc = revit.doc
    uidoc = revit.uidoc

    # Get the active view/sheet ID
    active_view_id = doc.ActiveView.Id
    
    # Collect all CAD Link Types in the model
    #link_types = FilteredElementCollector(doc).OfClass(CADLinkType)
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
                        matching_links[name] = link_type   

    
    
        # #get the file path/name as a string
        # cad_link_ref = link.GetExternalFileReference().GetPath()
        # cad_link_str = ModelPathUtils.ConvertModelPathToUserVisiblePath(cad_link_ref)
        # name = os.path.basename(cad_link_str)

        # if name.startswith("DP_") or name.startswith("DM_"):
            # matching_links[name] = link

    if not matching_links:
        forms.alert(
            "No linked DWGs found starting with 'DP_' or 'DM_'.", 
            title="Linked DWGs Selector", 
            warn_icon=True
        )
        return

    # Display a multi-select dialog box using pyRevit forms
    selected_names = forms.SelectFromList.show(
        sorted(matching_links.keys()),
        multiselect=True,
        title="Select Linked DWGs (DP_ / DM_)",
        button_name="Select in Model"
    )

    # If the user made a selection, update Revit's active selection
    if selected_names:
        selected_elements = [matching_links[name] for name in selected_names]
        element_ids = [el.Id for el in selected_elements]
        
        # Set the selection in the active UI document
        uidoc.Selection.SetElementIds(element_ids)
        
        forms.alert(
            "Successfully selected {} linked DWG(s).".format(len(element_ids)), 
            title="Done", 
            exitscript=False
        )

if __name__ == "__main__":
    main()