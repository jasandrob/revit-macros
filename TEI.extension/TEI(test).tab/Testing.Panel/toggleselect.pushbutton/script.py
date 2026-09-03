#toggles on/off selection toggles

# -*- coding: utf-8 -*-
from pyrevit import revit, forms, HOST_APP
from Autodesk.Revit.UI import RevitCommandId, PostableCommand

uiapp = HOST_APP.uiapp

# List of Command Names for the Selection Toggles
# These are the internal Revit strings for those buttons
commands = [
    "ID_SETTINGS_SELECT_LINKS",
    "ID_SETTINGS_SELECT_UNDERLAYS",
    "ID_SETTINGS_SELECT_PINNED"
]

try:
    for cmd_str in commands:
        cmd_id = RevitCommandId.LookupCommandId(cmd_str)
        if cmd_id:
            uiapp.PostCommand(cmd_id)
    
    forms.toast("Selection Toggles Cycled")

except Exception as e:
    print("Command Error: {}".format(str(e)))
    forms.alert("Final attempt failed. Revit 2026 internal IDs may have changed.")