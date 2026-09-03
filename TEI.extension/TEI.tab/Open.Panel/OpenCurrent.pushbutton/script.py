#! python3
"""
script for open current pushnbutton
"""



import os

fileclosed = False
#this will detected if file is opened
try:
    os.rename("P:\\Timesheet\\Daily\\Current.xlsm", "P:\\Timesheet\\Daily\\Current.xlsm")
    fileclosed = True
except:
    print("Current is already open")


if fileclosed:
    path = "P:\\Timesheet\\Daily\\Current.xlsm"
    os.startfile(path)




"""
import subprocess
import sys
import appopener

try:
	open('excel')
except:
	print('did not work')



#subprocess.Popen("P:\\Timesheet\\Daily\\Current.xlsm")
"""