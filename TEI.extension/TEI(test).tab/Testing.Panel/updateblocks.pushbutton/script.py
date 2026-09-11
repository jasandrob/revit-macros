# -*- coding: utf-8 -*-
"""
updates blocks
"""

import os
import shutil
import re

from pathlib import Path
from pyrevit import revit, forms, script
from Autodesk.Revit.DB import FilteredElementCollector, CADLinkType, ExternalFileUtils, ModelPathUtils, ImportInstance, Transaction

from functions import handle_cad_dialog



doc = revit.doc
uiapp = revit.HOST_APP.uiapp


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
        parts = Path(central_path).parts
        
        job_dir = parts[1:4]
        
    else:
        #since our safety check uses the workshared location exit the script if it is not workshared
        forms.alert("Model is not workshared",title="Error updating",exitscript=True)


    not_found = []
    link_list = []
    name_list = []
    for [block_type,block_path] in selected_blocks:
        
        block_name = os.path.basename(block_path)
        parts_blk_path = Path(block_path).parts

        #checks if the block is in the job directory
        if parts_blk_path[1:4] == job_dir:
            if block_name in master_set:
                
                master_blk_path = os.path.join(sync_path, block_name)
                replace_success = replace_file(master_blk_path, str(Path(*parts_blk_path[:-1])))
                    
                if replace_success:
                    link_list.append(block_type)
                    name_list.append(block_name)
            else:
                not_found.append(block_name)
        else:
            #ends the script if block is not in the job directory
            forms.alert(
                'Block "{}" is not saved in the job directory "{}". \nPlease relink block to this directory and try again'.format(block_name,central_path),
                title="Error updating",
                exitscript=True)
    
    #error message if non-master blocks selected
    if(len(not_found)) > 0:        
        not_found = "\n".join(not_found)
        forms.alert(
            "Some selected blocks could not be found: {} \n \nPlease rename block to one in the master directory and try again ".format(not_found),
            title="Non-master blocks selected"
        )
   
    if len(link_list) > 0:
        reload(link_list)
        
        name_list= "\n".join(name_list)
        forms.alert(
            "Sucessfully updated {} blocks: \n{}".format(len(link_list), name_list),
            title="Updated blocks",
            warn_icon=False
        )        
    


def natural_sort_key(s):
    # Splits the string into text and integer chunks
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def replace_file(source_path, destination_folder):
    """
    Safely copies a file from source_path to destination_folder,
    replacing it if it already exists.
    """
    
    # 1. Safety Check: Verify the source file actually exists
    if not os.path.isfile(source_path):
        forms.alert("Source block not found:\n{}".format(source_path), title="Error")
        return False
        
    # 2. Safety Check: Verify the destination folder exists
    if not os.path.isdir(destination_folder):
        forms.alert("Destination directory does not exist:\n{}".format(destination_folder), title="Error")
        return False
        
    # Extract the file name to build the full destination file path
    file_name = os.path.basename(source_path)
    destination_file_path = os.path.join(destination_folder, file_name)
    
    # 3. Safety Check: Attempt the copy inside a try/except block 
    # (Catches file-in-use locks, permission denials, or network drops)
    try:
        # shutil.copy2 copies the file AND preserves its original metadata/timestamps
        shutil.copy2(source_path, destination_file_path)
        
        return True
        
    except Exception as e:
        forms.alert("Error: Could not copy file '{}'. Reason: {}".format(file_name, str(e)), title="Error")
        return False    
 
 
 
 
def reload(link_list):
    #reloads all the links in the given list
    
    # 1. Subscribe to the event handler before starting the transaction
    uiapp.DialogBoxShowing += handle_cad_dialog
    
    try:
        with Transaction(doc, "Reload Selected CAD Blocks") as t:
            t.Start()
                
            for link in link_list:
                # Reload from its stored path
                link.Reload()
            
            t.Commit()
            

    except Exception as e:
        forms.alert("Failed to reload CAD link.\n\nError: {}".format(str(e)), title="Error")

    finally:
        # 2. Crucial: Always unsubscribe from the event in a 'finally' block 
        # to prevent it from affecting other standard Revit pop-ups later.
        uiapp.DialogBoxShowing -= handle_cad_dialog

# def handle_cad_dialog(sender, args):
    # """Event handler to catch the paper/model space prompt and auto-select Yes."""
    # if isinstance(args, TaskDialogShowingEventArgs):
        # # Look for keywords related to the paper/model space prompt in the dialog message
        # message_text = args.Message.lower()
        # if "paper space" in message_text or "model space" in message_text:
            # # Override result with '1', which corresponds to clicking 'Yes'
            # args.OverrideResult(1)



def main():
    sync_path = "S:\MECHANICAL\_CostcoDetails\_SyncRevitDetails"

    selected_blocks = select_blocks()
    
    if selected_blocks:
        master_set = check_master(sync_path)
        compare(selected_blocks, master_set, sync_path)
    

if __name__ == "__main__":
    main()