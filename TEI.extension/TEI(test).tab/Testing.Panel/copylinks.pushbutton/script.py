# -*- coding: utf-8 -*-
"""
copies linked cad from one project to another
"""

from pyrevit import revit, DB, forms


uidoc = revit.uidoc
dest_doc = revit.doc

# 1. Pick a source project from currently open documents
open_docs = [d for d in revit.docs if not d.IsFamilyDocument and d.Title != dest_doc.Title]
if not open_docs:
    forms.alert("Open the source Revit project first, then run this tool.", exitscript=True)

doc_map = {d.Title: d for d in open_docs}
picked_title = forms.SelectFromList.show(sorted(doc_map.keys()), title="Select Source Project")
if not picked_title:
    forms.alert("No source project selected.", exitscript=True)

source_doc = doc_map[picked_title]

# 2. Collect CAD instances and identify external CAD links
instances = DB.FilteredElementCollector(source_doc).OfClass(DB.ImportInstance).ToElements()
link_entries = []


for inst in instances:
    cad_type = source_doc.GetElement(inst.GetTypeId())
    if isinstance(cad_type, DB.CADLinkType) and cad_type.IsExternalFileReference():
        ext_ref = cad_type.GetExternalFileReference()
        if ext_ref:
            # Resolve path (handles local/network paths; cloud/BIM 360 may need special handling)
            model_path = ext_ref.GetPath()
            user_path = DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(model_path)
            if user_path:
                link_entries.append((cad_type.Category.Name, user_path, inst))

if not link_entries:
    forms.alert("No external CAD links found in '{}'.".format(source_doc.Title), exitscript=True)

# 3. Link into the destination document
linked_count = 0
with DB.Transaction(dest_doc, "Copy CAD Links from Project") as t:
    t.Start()
    for name, path, _inst in link_entries:
        try:
            opts = DB.DWGImportOptions()
            opts.Placement = DB.ImportPlacement.Origin
            opts.ThisViewOnly = False
            #opts.ColorMode = DB.ImportColorMode.PreserveColors

            
            # Optional: set placement/units/colors on CADLinkOptions as needed
            dest_doc.Link(path, opts, dest_doc.ActiveView)
            linked_count += 1
        except Exception as ex:
            print("Failed to link '{}' ({}): {}".format(name, path, ex))
    t.Commit()

forms.alert("Linked {} CAD file(s) into '{}'.".format(linked_count, dest_doc.Title))