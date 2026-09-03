#closes all section views

from pyrevit import revit, forms
from Autodesk.Revit import DB
import sys


# Initialize
uidoc = revit.uidoc
doc = revit.doc


def close_all_sections():
    open_views = uidoc.GetOpenUIViews()
    closed_count = 0
    active_view_id = uidoc.ActiveView.Id


    for ui_view in open_views:
        view_id = ui_view.ViewId
        view_el = doc.GetElement(view_id)

        # Ensure it's a section and NOT the active window
        if view_el.ViewType == DB.ViewType.Section:
            if view_id == active_view_id:
                continue
                
            ui_view.Close()
            closed_count += 1


    if closed_count > 0:
        # Simplified toast for better compatibility
        #forms.toast("Closed {} section views.".format(closed_count))
        pass
    else:
        forms.alert("No open section views found.")
        sys.exit()


if __name__ == "__main__":
    close_all_sections()