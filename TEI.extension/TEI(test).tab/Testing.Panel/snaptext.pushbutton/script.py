# -*- coding: utf-8 -*-
"""
snaps midpoint of text to selected point
"""
from pyrevit import revit, DB, UI, forms
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.Exceptions import OperationCanceledException

doc = revit.doc
uidoc = revit.uidoc
view = doc.ActiveView

# Supported target types: Text Notes, Independent Tags, and Spatial Tags (Room, Area, Space)
VALID_TYPES = (DB.TextNote, DB.TextElement)


class TextAndTagFilter(ISelectionFilter):
    """Selection filter restricting picking to text notes and tags only."""

    def AllowElement(self, elem):
        return isinstance(elem, VALID_TYPES)

    def AllowReference(self, ref, point):
        return False


# 1. Retrieve pre-selected elements matching valid types
selection_ids = uidoc.Selection.GetElementIds()
selected_elements = [doc.GetElement(el_id) for el_id in selection_ids]
target_elements = [el for el in selected_elements if isinstance(el, VALID_TYPES)]

# 2. If no valid text or tag is selected, prompt user to pick one
if not target_elements:
    try:
        ref = uidoc.Selection.PickObject(
            ObjectType.Element,
            TextAndTagFilter(),
            "Select a Text Note or Tag to move",
        )
        picked_el = doc.GetElement(ref.ElementId)
        if picked_el:
            target_elements.append(picked_el)
    except OperationCanceledException:
        pass

# 3. Ask user for destination type and get target coordinates
if target_elements:
    try:
        # Prompt user to choose destination mode via pyRevit alert dialog
        mode = forms.alert(
            "Select destination target type:",
            options=["Pick Point", "Pick Text Note / Tag"],
        )

        destination_point = None

        if mode == "Pick Point":
            destination_point = uidoc.Selection.PickPoint(
                "Pick destination point"
            )

        elif mode == "Pick Text Note / Tag":
            dest_ref = uidoc.Selection.PickObject(
                ObjectType.Element,
                TextAndTagFilter(),
                "Select destination Text Note or Tag",
            )
            dest_elem = doc.GetElement(dest_ref.ElementId)
            if dest_elem:
                dest_bbox = dest_elem.get_BoundingBox(view)
                if dest_bbox:
                    # Calculate midpoint of destination text note/tag
                    destination_point = DB.XYZ(
                        (dest_bbox.Min.X + dest_bbox.Max.X) / 2.0,
                        (dest_bbox.Min.Y + dest_bbox.Max.Y) / 2.0,
                        (dest_bbox.Min.Z + dest_bbox.Max.Z) / 2.0,
                    )

        # 4. Move element(s) so source midpoint matches destination point
        if destination_point:
            with revit.Transaction("Snap Text/Tag Midpoint"):
                for elem in target_elements:
                    bbox = elem.get_BoundingBox(view)
                    if bbox:
                        mid_x = (bbox.Min.X + bbox.Max.X) / 2.0
                        mid_y = (bbox.Min.Y + bbox.Max.Y) / 2.0
                        mid_z = (bbox.Min.Z + bbox.Max.Z) / 2.0
                        mid_point = DB.XYZ(mid_x, mid_y, mid_z)

                        # Vector displacement from source midpoint to destination point
                        translation = destination_point - mid_point

                        # Move element
                        DB.ElementTransformUtils.MoveElement(
                            doc, elem.Id, translation
                        )

    except OperationCanceledException:
        pass