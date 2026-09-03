# -*- coding: utf-8 -*-
from pyrevit import revit, DB

uidoc = revit.uidoc
doc = revit.doc
selection = revit.get_selection()

filled_regions = [el for el in selection if isinstance(el, DB.FilledRegion)]

if not filled_regions:
    print("No Filled Regions selected.")
else:
    with revit.Transaction("Update Text Inside Regions"):
        for region in filled_regions:
            # 1. Get Data
            area_val = region.get_Parameter(DB.BuiltInParameter.HOST_AREA_COMPUTED).AsDouble()
            area_text = "{:.0f} SF".format(area_val)
            
            bbox = region.get_BoundingBox(doc.ActiveView)
            center = (bbox.Min + bbox.Max) / 2
            
            # 2. Get all text in the current view
            all_text_in_view = DB.FilteredElementCollector(doc, doc.ActiveView.Id)\
                                 .OfClass(DB.TextNote)\
                                 .ToElements()
            
            target_note = None
            min_dist = float('inf')

            for note in all_text_in_view:
                # 3. Check if the text's XY position is inside the region's XY box
                note_pos = note.Coord
                
                is_inside_x = bbox.Min.X <= note_pos.X <= bbox.Max.X
                is_inside_y = bbox.Min.Y <= note_pos.Y <= bbox.Max.Y
                
                if is_inside_x and is_inside_y:
                    # Calculate 2D distance (Ignoring Z)
                    dist = ((center.X - note_pos.X)**2 + (center.Y - note_pos.Y)**2)**0.5
                    
                    if dist < min_dist:
                        min_dist = dist
                        target_note = note
            
            # 4. Update or Create
            if target_note:
                target_note.Text = area_text
            else:
                DB.TextNote.Create(
                    doc, 
                    doc.ActiveView.Id, 
                    center, 
                    area_text, 
                    doc.GetDefaultElementTypeId(DB.ElementTypeGroup.TextNoteType)
                )

    print("Success: Processed {} regions using 2D boundary check.".format(len(filled_regions)))