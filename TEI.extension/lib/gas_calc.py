
"""
calculates the gas equation given the selected values
"""
import traceback


from pyrevit import revit
from pyrevit import DB, forms, script

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType

output = script.get_output()







doc = __revit__.ActiveUIDocument.Document
uidoc = revit.uidoc
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel


sel = uidoc.Selection

def convert_to_ft(feet, inches):
    """
    takes a measurement in feet and inches and automatically converts to a decimal in feet
    """
    
    tot_ft = feet + inches * 0.0833
    
    return tot_ft
   
    
def gas_eq(d, var, ver, code, LPG=False, non_standard=False):
    """
    creates the gas equation based on the user input
    
    
    inputs:
        d: the diameter of pipe used in the calculation
        var: list of the other variables used in this equation
        ver: a string, either 'WC' or 'PSI'
        code: a string, either 'UPC','IPC', or None
        LPG: a boolean representing whether LPG is selected
        
    output:
        q: the allowable gas load in MBH for the pipe size and code
    """
    p1 = var[0]
    p2 = var[1]
    Y = var[2]
    Cr = var[3]
    L = var[4]
    
    
    DH = 0.5
    code = code.upper()
    #chooses the equation to use based on code selected
    #first if statement will run also for a nonstandard selection
    if (ver == 'PSI' and code == 'IPC') or (ver == 'PSI' and code!='IPC' and code!='UPC'):
        q = (18.93 * d * (((p1**2 - p2**2) * Y / (Cr * L)) **0.206)) ** (1 / 0.381)
    
    elif ver == 'PSI' and code == 'UPC':
        q = 2237 * d ** 2.623 * ((p1 ** 2 - p2 ** 2) * Y / (Cr * L)) ** 0.541
        
        
    elif ver == 'WC' and code == 'IPC':
        q = (19.17 * d * ((DH / (Cr * L)) ** 0.206)) ** (1 / 0.381)
        
    elif ver == 'WC' and code == 'UPC':
        q = (19.17 * d * ((DH / (Cr * L)) ** 0.206)) ** (1 / 0.381)
        
        
    #adds the LPG multiplier
    if LPG == 'True':
        q = q * 2.5
        
    return q
    
    
    
    
def size_gas(pressure_code, max_pressure, max_length,  pressure_min=None, LPG=False):



    #sets the default min pressure based on user selection
    if pressure_min is None:
        if max_pressure == '5 psi':
            pressure_min = 1.5
        elif max_pressure == '7"W.C.':
            pressure_min = 6.5
        elif max_pressure == '2 psi':
            pressure_min = 1.0

    #will inform equation whether to use PSI or WC
    if max_pressure == '7"W.C.':
        ver = "WC"
    else: 
    #(max_pressure == '5 psi' or max_pressure == "2 psi") or (max_pressure is unidentified):
        ver = "PSI"
    


    pipe_equiv = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0]
    pipe_true_diam = [0.622, 0.824, 1.049, 1.38, 1.61, 2.067, 2.469, 3.068, 4.026, 6.065, 7.981]
    pipe_sizes = ['1/2"', '3/4"', '1"', '1-1/4"', '1-1/2"', '2"', '2-1/2"', '3"', '4"', '6"', '8"']
    
    
    

    
    
    #cr=1.2462 if LPG
    if LPG is False or LPG == 'False':
        Cr = 0.6094
        Y = 0.9992
    elif LPG == 'True':
        Cr = 1.2462
        Y = 0.991
    
    
    #solve for pipe_loads
    pipe_loads = ['XXX', 'XXX', 'XXX', 'XXXX', 'XXXX', 'XXXX', 'XXXX', 'XXXX', 'XXXXX', 'XXXXX', 'XXXXXX']
    chart_loads = ['XXX', 'XXX', 'XXX', 'XXXX', 'XXXX', 'XXXX', 'XXXX', 'XXXX', 'XXXXX', 'XXXXX', 'XXXXXX']
    

    #CALCULATE GAS TABLE
    p1 = float(max_pressure[0]) + 14.7
    p2 = float(pressure_min) + 14.7
    L = float(max_length)
    
    vars = [p1, p2, Y, Cr, L]
    
    for i in range(len(pipe_loads)):
    

        # gas_eq(d, vars, ver, code, LPG=False)
        q_calc = gas_eq(pipe_true_diam[i], vars, ver, pressure_code)
        #q_calc = (18.93 * pipe_true_diam[i] * (((p1**2 - p2**2) * Y / (Cr * L)) **0.206)) ** (1 / 0.381)
        
        #add a 10% F.S.
        pipe_loads[i] = int(round(0.9*q_calc))
        
        #chart will show 5% F.S. BUT NOT ON THE W.C. ONE FOR SOME REASON
        if ver == 'PSI':
            chart_loads[i] = int(round(0.95*q_calc))
        elif ver == 'WC':
            chart_loads[i] = pipe_loads[i]
        
        #print(0.95*q_calc)

    #creates a copy of the chart loads list to use later
    chart_loads_no_comma = list(chart_loads)
    
    #this code adds commas to the chart loads for readability
    for i in range(len(chart_loads)):
        num_len = len(str(chart_loads[i]))
        comma_sep = '{:,d}'.format(chart_loads[i])

        chart_loads[i] = comma_sep
    
    

    #creates a readable list of the gas size chart
    list1 = []
    for i in range(len(chart_loads)):
        list1.append([pipe_sizes[i], chart_loads[i]])
    output.print_table(list1, columns=["PIPE SIZE (" +pressure_code.upper() +")", "MAX LOAD (MBH)"], title="GAS SIZE CHART (PRESSURE DROP TO " + str(pressure_min) + ")")
    
    #returns the size list to use to edit the drawing
    size_list = []
    for i in range(len(chart_loads)):
        size_list.append([pipe_equiv[i]/12, int(chart_loads_no_comma[i])])
    
    return(size_list)   



if __name__ == "__main__":
    size_gas('XX', 'TO XXX', 'XXXX')

#import traceback
# try:
    # hu = fasdfasd
# except Exception, err:
    # pass

# print(traceback.format_exc())
    