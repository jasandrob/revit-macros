"""
General functions to reuse throughout code
"""

import os
import traceback
import datetime

from Autodesk.Revit.UI.Events import TaskDialogShowingEventArgs

from settings import debug_mode


def day():
    """
    returns the day of the week, date, and current time as a list of strings
    """
    today = datetime.date.today()
    weekday_name = today.strftime('%A')

    date_value = today.strftime("%m_%d_%y")
    
    
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return weekday_name, date_value, current_time


def failer():
    """
    run this function that intentionally fails to cause an error
    """
    print(1 + 'i')


def handle_cad_dialog(sender, args):
    """Event handler to catch the paper/model space prompt and auto-select Yes."""
    if isinstance(args, TaskDialogShowingEventArgs):
        # Look for keywords related to the paper/model space prompt in the dialog message
        message_text = args.Message.lower()
        if "paper space" in message_text or "model space" in message_text:
            # Override result with '1', which corresponds to clicking 'Yes'
            args.OverrideResult(1)


def print_info(info):
    """
    will print info if debug mode is set to true
    """
    if debug_mode:
        print(info)
        
 
def report_error(directory, error=None):
    """
    saves the most recent error into a txt file with a timestamp, given the TEI/TEI.extension directory
    """
    date_info = day()

    if error is None:
        error = trace_print()
    

    #add date to filename
    name = 'errorlog' + date_info[1] + '.txt'
    path1 = os.path.join('errorlogs', name)
    
    #create timestamp
    header = date_info[1] + ' ' + date_info[2]
    msg = [header, error, "----------------------------"]
    
    
    path = os.path.join(directory, 'bin', 'errorlogs')


    to_txt(name, path, msg)


def report_problem(directory, message):
    """
    saves a message into the error txt file, given the TEI/TEI.extension directory
    """


def to_txt(filename, directory, message):
    """
    turns a list of strings into a message that will be saved to a txt file in the given path
    """
    try:
        
        path = os.path.join(directory, filename)

        with open(path, 'a') as f:
        
            if isinstance(message, basestring):
                f.write(message)
            else:
                for string in message:
                    f.write(str(string) + '\n')
            
            f.close()
    except:
        print_info('COULD NOT RECORD MESSAGE TO TXT FILE')
        trace_print() 
    
    
def trace_print():
    """
    will print error message if debug mode is set to true
    """
    trace = traceback.format_exc()
    if debug_mode:
        print("----------------------------")
        print(trace)
        print("----------------------------")
        
    return trace