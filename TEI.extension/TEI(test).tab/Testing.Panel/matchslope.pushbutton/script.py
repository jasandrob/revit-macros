#matches the projected slope of two sloped pipes

from pyrevit import revit, forms
from Autodesk.Revit import DB
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
import sys

doc = revit.doc
uidoc = revit.uidoc

# Selection Filter to keep things clean
class PipeFilter(ISelectionFilter):
    def AllowElement(self, elem):
        return isinstance(elem, DB.Plumbing.Pipe)
    def AllowReference(self, ref, pt): return True

def match_sloped_pipes():
    pipe_filter = PipeFilter()
    
    try:
        # 1. Pick Source
        with forms.WarningBar(title="Select the SLOPED SOURCE pipe"):
            source_ref = uidoc.Selection.PickObject(ObjectType.Element, pipe_filter)
            source_pipe = doc.GetElement(source_ref.ElementId)

        # Get Source Geometry
        source_curve = source_pipe.Location.Curve
        p0 = source_curve.GetEndPoint(0)
        p1 = source_curve.GetEndPoint(1)
        
        # 2. Loop for Targets
        while True:
            try:
                with forms.WarningBar(title="Select TARGET pipe to align (Esc/Enter to finish)"):
                    target_ref = uidoc.Selection.PickObject(ObjectType.Element, pipe_filter)
                    target_pipe = doc.GetElement(target_ref.ElementId)

                target_curve = target_pipe.Location.Curve
                t_start = target_curve.GetEndPoint(0)

                # --- MATH: PROJECT ELEVATION ---
                # We project the target's start point onto the infinite line of the source
                # This finds the "Correct" Z at that specific XY location
                
                # Vector of source pipe
                v = p1 - p0
                # Vector from source start to target start
                w = t_start - p0
                
                # Project w onto the horizontal direction of v to find the relative distance along the slope
                # Note: We use 2D (XY) math if we want to match based on "Stationing"
                v_xy = DB.XYZ(v.X, v.Y, 0)
                w_xy = DB.XYZ(w.X, w.Y, 0)
                
                if v_xy.IsZeroLength():
                    continue # Avoid vertical pipe math errors
                
                # Factor of how far along the source line the target point sits
                dot_prod = w_xy.DotProduct(v_xy)
                v_sq_len = v_xy.DotProduct(v_xy)
                parameter = dot_prod / v_sq_len
                
                # Calculate the projected Z on the source line
                projected_z = p0.Z + (parameter * v.Z)
                
                # How much do we need to move the target?
                translation_z = projected_z - t_start.Z

                # 3. Execute Move
                if abs(translation_z) > 0.0001:
                    t = DB.Transaction(doc, "Match Sloped Elevation")
                    t.Start()
                    move_vec = DB.XYZ(0, 0, translation_z)
                    DB.ElementTransformUtils.MoveElement(doc, target_pipe.Id, move_vec)
                    t.Commit()

            except Exception:
                # User cancelled (Esc/Enter)
                break

    except Exception as e:
        forms.alert("Error: {}".format(str(e)))




if __name__ == "__main__":
    match_sloped_pipes()