"""
settings button script
"""
import os

import pyrevit
from pyrevit import forms
from pyrevit import script

import settings





def tei_path():
    """
    returns the directory path TEI.extension\TEI.tab\Testing.Panel. Useful so file path does not have to be coded for each user, use relative paths instead
    """

    script_path = pyrevit.script.get_script_path()
    dir = os.path.dirname(script_path)
    extension = os.path.dirname(os.path.dirname(dir))

    return extension



def edit_py(directory, filename, setting, change):
    """
    edits the settings in the py file
        setting: str of the setting varible to change
         change: set the given setting variable to (change)
    """

    path = os.path.join(directory, filename)
    
    #check that setting file exists
    if os.path.isfile(path) is False:
        print("Settings file could not be found")
        return None
    
    #reads the current settings
    content = []
    with open(path, 'r') as f:
        content = f.readlines()
        
    #changes the selected setting    
    with open(path, 'w') as f:
        for line in content:
            if setting in line:
                newline = setting + " = " + change
                f.write(newline)
                f.write('\n')
            else:
                f.write(line)
            
        


def main():
    debug_mode = str(settings.debug_mode)
    work_code = str(settings.work_code)


    # if debug_mode == 'True':
        # debug_mode = 'ON'
    # elif debug_mode == 'False':
        # debug_mode = 'OFF'




    #lists the settings in a readable format
    debug = 'DEBUGGING MODE:                               ' + debug_mode
    work  = 'WORK CODE:                                          ' + work_code

    #THESE MUST BE CHANGED TO REFLECT IN THE VARIABLES IN THE SETTINGS FILE
    options = [debug, work]
    setting_vars = ['debug_mode', 'work_code']

    #option dictionary, MUST MATCH SETTING_VARS. not very robust
    optiondict = {
        'debug_mode': ['True', 'False'],
        'work_code' : ["'MDE'", "'EDE'", "''"]
    }
    

    items = [debug, work]

    selection = forms.SelectFromList.show(items, title='Select Setting to Edit', button_name='Change Setting')




    if selection != None:
        
        #will popup the variable selection with the options for the chosen setting
        varpick = None
        for i, option in enumerate(options):
            if option == selection:
                varpick = setting_vars[i]
                optionlist = optiondict[varpick]
    
        selection2 = forms.SelectFromList.show(optionlist, title='Change Setting', button_name='Confirm')
        
        #changes the setting variable to the given setting        
        if selection2 != None:
     
            #gets the setting directory
            extension = tei_path()
            directory = os.path.join(extension, 'lib')
            
            
            change = selection2
            edit_py(directory, 'settings.py', varpick, change)





if __name__ == '__main__':
    main()

