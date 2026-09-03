#matches the elevation of two pipes

from pyrevit import revit, forms
from Autodesk.Revit import DB
from Autodesk.Revit.UI.Selection import ObjectType
from System.Collections.Generic import List

doc = revit.doc
uidoc = revit.uidoc

def match_pipe_elevation():
    # Setup override graphics (Red and Thick)
    green = DB.Color(0, 255, 0)
    override_settings = DB.OverrideGraphicSettings()
    override_settings.SetProjectionLineColor(green)
    override_settings.SetProjectionLineWeight(8)
    
    red = DB.Color(255, 0, 0)
    override_settings_t = DB.OverrideGraphicSettings()
    override_settings_t.SetProjectionLineColor(red)
    override_settings_t.SetProjectionLineWeight(8)
    

    source_pipe_id = None

    try:
        # 1. Pick the SOURCE pipe
        try:
            with forms.WarningBar(title="Select the SOURCE pipe"):
                source_ref = uidoc.Selection.PickObject(ObjectType.Element)
            source_pipe = doc.GetElement(source_ref.ElementId)
        except:
            return # User cancelled initial selection

        if not isinstance(source_pipe, DB.Plumbing.Pipe):
            forms.alert("Source must be a pipe!")
            return

        source_pipe_id = source_pipe.Id

        # --- HIGHLIGHT THE SOURCE ---
        t_high = DB.Transaction(doc, "Temp Highlight")
        t_high.Start()
        doc.ActiveView.SetElementOverrides(source_pipe_id, override_settings)
        t_high.Commit()

        # 2. Loop for TARGET pipes
        
        targets = []
        
        while True:
            try:
                # The script stays here until you click a target or hit Enter/Esc
                with forms.WarningBar(title="Select the TARGET pipe(s)"):
                    target_ref = uidoc.Selection.PickObject(ObjectType.Element, "Select TARGET pipe (Enter/Esc to Finish)")
                target_pipe = doc.GetElement(target_ref.ElementId)


                if not isinstance(target_pipe, DB.Plumbing.Pipe):
                    continue # Ignore non-pipe clicks and keep looping

                #start transaction for highlighting pipes
                t_hight = DB.Transaction(doc, "Temp Highlight Target")
                t_hight.Start()
                doc.ActiveView.SetElementOverrides(target_pipe.Id, override_settings_t)
                t_hight.Commit()
                
                targets.append(target_pipe.Id)

                # 3. Calculate and Move
                source_z = source_pipe.Location.Curve.GetEndPoint(0).Z
                target_z = target_pipe.Location.Curve.GetEndPoint(0).Z
                translation_z = source_z - target_z

                # Only move if there is a difference
                if abs(translation_z) > 0.0001:
                    t_move = DB.Transaction(doc, "Match Pipe Elevation")
                    t_move.Start()
                    move_vector = DB.XYZ(0, 0, translation_z)
                    DB.ElementTransformUtils.MoveElement(doc, target_pipe.Id, move_vector)
                    t_move.Commit()

            except:
                # This triggers when the user hits Enter or Esc
                break 

    except Exception as e:
        forms.alert("An unexpected error occurred: {}".format(str(e)))

    finally:
        # --- CLEAN UP ---
        if source_pipe_id:
            t_clean = DB.Transaction(doc, "Clear Highlight")
            t_clean.Start()
            doc.ActiveView.SetElementOverrides(source_pipe_id, DB.OverrideGraphicSettings())
            
            for pipe_id in targets:
                doc.ActiveView.SetElementOverrides(pipe_id, DB.OverrideGraphicSettings())
                
            t_clean.Commit()

if __name__ == "__main__":
    match_pipe_elevation()