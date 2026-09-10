# -*- coding: utf-8 -*-
"""
updates blocks
"""
import os
import re
from pathlib import Path
from pyrevit import revit, forms
from Autodesk.Revit.DB import FilteredElementCollector, CADLinkType, ExternalFileUtils, ModelPathUtils, ImportInstance

doc = revit.doc


def select_blocks():
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
    selected_links = None
    if selected_names:

        selected_links = [matching_links[name] for name in selected_names]
        
        # selected_elements = [matching_links[name] for name in selected_names]
        # element_ids = [el.Id for el in selected_elements]
        
        # # Set the selection in the active UI document
        # uidoc.Selection.SetElementIds(element_ids)
        
        # forms.alert(
            # "Successfully selected {} linked DWG(s).".format(len(element_ids)), 
            # title="Done", 
            # exitscript=False
        # )
    return selected_links
    
    

def check_master(sync_path):
#creates a list of all the details in the sync revit directory, 

    #path for master revit details and checks if it exsits
    if not os.path.exists(sync_path):
        forms.alert(
            "The directory does not exist:\n{}".format(sync_path), 
            title="Path Not Found", 
            warn_icon=True
        )
        return None  # Exit the function early

    
    
    all_items = os.listdir(sync_path)
    
    #get all dwgs
    dwg_files = [
        f for f in all_items
        if os.path.isfile(os.path.join(sync_path, f)) and f.lower().endswith('.dwg')
    ]
    
    
    #checks for dwg files
    if not dwg_files:
        forms.alert(
            "The sync directory {} exists, but contains no .dwg files.".format(sync_path), 
            title="No DWG Files Found", 
            warn_icon=True
        )
        return None  # Exit the function early
    
    
    master_set = set(dwg_files)
    
    
    return master_set


def compare(selected_blocks, master_set,sync_path):
    #compares a list and checks if the set items are contained within the list
    
    #safety check to ensure linked files are in the same directory folder as the workshared model
    if doc.IsWorkshared:
        central_model_path = doc.GetWorksharingCentralModelPath()
        
        # Convert the ModelPath object to a readable string format
        central_path = ModelPathUtils.ConvertModelPathToUserVisiblePath(central_model_path)
        print(central_path)
        parts = Path(central_path).parts
        
        job_dir = parts[1:4]
        
    else:
        #since our safety check uses the workshared location exit the script if it is not workshared
        forms.alert("Model is not workshared",title="Error updating",exitscript=True)


    not_found = []
    for block in selected_blocks:
        
        block_name = os.path.basename(block[1])
        
        print(job_dir)
        print(Path(block[1]).parts[1:4])
        #checks if the block is in the job directory
        if Path(block[1]).parts[1:4] == job_dir:
            if block_name in master_set:
                print(block_name)
            else:
                not_found.append(block_name)
        else:
            #ends the script if block is not in the job directory
            forms.alert(
                'Block "{}" is not saved in the job directory "{}". Please relink block to this directory and try again'.format(block_name,central_path),
                title="Error updating",
                exitscript=True)
    
    #error message if non-master blocks selected
    if(len(not_found)) > 0:        
        not_found = "\n".join(not_found)
        forms.alert(
            "Some selected blocks could not be found: {}".format(not_found),
            title="Non-master blocks selected"
        )
   

def natural_sort_key(s):
    # Splits the string into text and integer chunks
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]
    
    
def main():
    sync_path = "S:\MECHANICAL\_CostcoDetails\_SyncRevitDetails"

    selected_blocks = select_blocks()
    
    if selected_blocks:
        master_set = check_master(sync_path)
        compare(selected_blocks, master_set, sync_path)
    

if __name__ == "__main__":
    main()