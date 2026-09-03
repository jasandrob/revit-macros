"""
opens the autocad master files
"""
import os
from pyrevit import forms


#HERE IS CODE FOR MAKING THE POPUP LIST SELECTOR
year = "2025"

path = "S:\\MECHANICAL\\_CostcoDrawing\\Master " + year
m_files = os.listdir(path)


#finds available dwgs in master folder
dwgs = []
for file in m_files:
    if "_000" in file and '.dwg' in file:
        dwgs.append(file)
        
selection = forms.SelectFromList.show(dwgs, title='Open Master ' + year +' DWG in AutoCAD', button_name='Select Item')





if selection != None:
    new_path = os.path.join(path, selection)
    os.startfile(new_path)

