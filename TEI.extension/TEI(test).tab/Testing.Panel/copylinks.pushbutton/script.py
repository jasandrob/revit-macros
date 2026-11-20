# -*- coding: utf-8 -*-
"""
copies linked cad from one project to another
"""

from pyrevit import revit, DB, forms

dest_doc = revit.doc

# 1. Pick source project from open documents
open_docs = [d for d in revit.docs if not d.IsFamilyDocument and d.Title != dest_doc.Title]
if not open_docs:
    forms.alert("Open the source Revit project first.", exitscript=True)

doc_map = {d.Title: d for d in open_docs}
src_title = forms.SelectFromList.show(sorted(doc_map.keys()), title="Select Source Project")
if not src_title:
    forms.alert("No source project selected.", exitscript=True)
source_doc = doc_map[src_title]

# 2. Pick a ViewSheet in the source document
def get_sheet_name(sheet):
    try:
        return sheet.Name
    except Exception:
        return getattr(sheet, "Name", "") or ""

sheets = DB.FilteredElementCollector(source_doc).OfClass(DB.ViewSheet).ToElements()
sheet_map = {
    "{} - {}".format(s.SheetNumber, get_sheet_name(s)): s
    for s in sheets
}
picked_sheet_label = forms.SelectFromList.show(
    sorted(sheet_map.keys()), title="Select Source Sheet"
)
if not picked_sheet_label:
    forms.alert("No sheet selected.", exitscript=True)

target_sheet = sheet_map[picked_sheet_label]

# 3. Collect all View IDs placed on that sheet via Viewports
sheet_view_ids = set([target_sheet.Id])
for vp_id in target_sheet.GetAllViewports():
    vp = source_doc.GetElement(vp_id)
    if vp and vp.ViewId != DB.ElementId.InvalidElementId:
        sheet_view_ids.add(vp.ViewId)



# 4. Filter CAD instances whose OwnerViewId is on the chosen sheet
instances = DB.FilteredElementCollector(source_doc).OfClass(DB.ImportInstance).ToElements()
matched_links = []

for inst in instances:
    if inst.OwnerViewId not in sheet_view_ids:
        continue

    cad_type = source_doc.GetElement(inst.GetTypeId())
    if isinstance(cad_type, DB.CADLinkType) and cad_type.IsExternalFileReference():
        ext_ref = cad_type.GetExternalFileReference()
        if ext_ref:
            user_path = DB.ModelPathUtils.ConvertModelPathToUserVisiblePath(ext_ref.GetPath())
            if user_path:
                try:
                    cad_name = cad_type.Category.Name
                except Exception:
                    cad_name = DB.Element.Name.GetValue(cad_type)
                matched_links.append((cad_name, user_path, inst))

if not matched_links:
    forms.alert("No external CAD links found on views of '{}'.".format(picked_sheet_label), exitscript=True)

# 5. Link matched CAD files into destination document
linked_count = 0
with DB.Transaction(dest_doc, "Copy Sheet CAD Links") as t:
    t.Start()
    for cad_name, path, inst in matched_links:
        opts = DB.DWGImportOptions()
        opts.ThisViewOnly = bool(inst.ViewSpecific)
        opts.Placement = DB.ImportPlacement.Shared

        try:
            ok, link_id = dest_doc.Link(path, opts, dest_doc.ActiveView)
            if ok:
                linked_count += 1
        except Exception as ex:
            print("Failed to link '{}' ({}): {}".format(cad_name, path, ex))
    t.Commit()

forms.alert("Linked {} CAD file(s) from '{}'.".format(linked_count, picked_sheet_label))