#! python3

"""
called on by the record + edit function to run python3 code. Edits Current.xlsm with the active job data. Will output anything that is printed in this file.
"""
import os
import sys
# import datetime

import xlwings as xw

import settings
from functions import day, trace_print, failer



def read_tei_jobs(target):
    """
    with a known job number in the format 00-000, will return info about the job using the job list
    """
    #finds the year of the job to access the sheet with that year
    year = '20' + target.split("-")[0]

    filename = 'K:\Job-Logs2010\Tei-Jobs.xlsm'
    wb = xw.Book(filename, read_only=True)
    sheet = wb.sheets[year]
    
    
    # limit range to 1500, might need to be changed in future
    for i, row in enumerate(sheet.range("A1:E1500").value):

            
        try:
            fullnum = row[0]
            num = fullnum.split(".")[0]

            #returns job info if the job number matches
            if num.strip() == target.strip():
            
                return[row[1], row[2], row[3], row[4]]
                
        except:
            # some colums dont have values and it breaks
            pass

        if i == 1500:
            print("Could not find job in tei-jobs.xlsm")
            

	
def read_direct():
    """
    reads the job data sent directly from doc-opened.py
    """
    info = sys.argv[1]
    
    info_list = info.strip('][').split(', ')
    info_1 = info_list[0].strip('\'')
    info_2 = info_list[1].strip('\'')
    
    n_info = [info_1, info_2]
    
    
    return n_info



def edit(jobdata, weekday):
    """
    edits the time sheet with the new job information

    inputs:
		jobdata: a list of lists with the job information
		    day: the day of the week as a string 

    """

    filename = 'P:\\Timesheet\\Daily\\Current.xlsm'
    wb = xw.Book(filename)
    sheet = wb.sheets[weekday]

	#edits the next available row in the excel sheet
    iter = 0

    #checks if there is any data in the csv file
    if len(jobdata) > 0:
        jobnum = jobdata[0]
        
        #gets job info from the info function
        [owner, location, state, description] = read_tei_jobs(str(jobnum))
    
        city_info = owner +  ' - ' + location + ', ' + state
        workcode = str(settings.work_code)

     
        for i in range(20):
            print_info("working..")
            cell = "D" + str(iter + 4)
            cell2 = "E" + str(iter + 4)
            cell3 = "F" + str(iter + 4)
            cell4 = "G" + str(iter + 4)
            cell7 = "J" + str(iter + 4)
            cell9 = "L" + str(iter + 4)
        
            #checks if the job is already recorded
            if sheet[cell].value == jobnum:
                print_info("job already recorded")
                #sheet[cell7].value = 10
        
                break

            #adds data to next empty row if job is not already recorded
            if sheet[cell].value == None:
                sheet[cell].value = jobnum
                sheet[cell2].value = city_info
                sheet[cell3].value = workcode
                sheet[cell4].value = description
                break
            
            iter += 1
                    
    else:
        print_info("Error: no data in csv file")
    
    return city_info, description

# def day():
	# """
	# returns the day of the week as a string
	# """
	# today = datetime.date.today()
	# weekday_name = today.strftime('%A')

	# return str(weekday_name)
    
    
def print_info(info, override=False):
    """
    will print info if debug mode is turned on
    """
    if settings.debug_mode or override:
        print(info)


def main():



    try:
        jobdata = read_direct()
        
        date_info = day()
        weekday = date_info[0]
        print_info(weekday)
        print_info(jobdata)
        [city_info, description] = edit(jobdata, weekday)
        
        #sends these two back to doc-opened.py to be used for popup
        print(city_info)
        print(description)

    except:
        trace_print()
    #except Exception as e:
    #   print("Error pasting job to current: " + str(e))


		



main()


