"""
called on by the open popup to make gas form
"""
import sys
import tkinter as tk

from functions import print_info



	
def read_direct():
    """
    reads the job data sent directly from doc-opened.py
    """
    info = sys.argv[1]


    return info
    
    
    
    
    
def code_selector(bool_list):
    """
    Given a list of lists in the following format [[var1 , True, var_str],[var2, False, var_str],[var3, True, var_str],...]
    Will return the ONE var_str that is paired with a False value. Remember that False means the button is pressed.
    """
    for list in bool_list:
        if list[1] == False:
            return list[2]
            
    return None

def handle_click(event):
    print('the button was clicked')







def switch(frame_name, num, is_on, contents=None, root_destroy=None, entry_list=None, forcenum_list=None):
    """
    given the frame and all the frame attributes, will create a switch to collect all the entry data
    
    INPUTS:
        entry_list: a list of the entries you want to record when the SIZE PIPES button is hit, or a single entry
        contents: set to list that you want to return your entry data to
        root_destroy: set to the root that you want to destroy when the button is pressed
        forcenum: a list of booleans associated with an entry list determining whether or not to force each entry to be an int
                    needs to be the same length as entry_list. If it is not set it will automatically force num.
    """
    
    
    on = tk.RAISED
    off = tk.SUNKEN
    
    #determine if on or off
    if is_on[num]:
     
        frame_name.config(relief= off)

                        
        is_on[num] = False
        info = str(is_on)
   
        
        
        
        #if this is the size pipes button
        if contents is not None:
        
        
        
            #variable to check if one of the entries is not a number
            err_nonum = False
            
            #allows you to enter a single entry
            if not isinstance(entry_list, list):
                entry_list = [entry_list]
            
            
            for i, entry_name in enumerate(entry_list):
                user_entry = entry_name.get()
                
                #will default forcenum to true, otherwise will read from the list
                forcenum = True
                if isinstance(forcenum_list, list):
                    forcenum = forcenum_list[i]
                
                #checks that user actually inputted a number and not letters if forcenum is True
                if forcenum:
                    try:
                        user_int = int(user_entry)
                        contents.append(user_int)
                        
                        

                    except:
                        entry_name.delete(0, tk.END)
                        entry_name.insert(0, "Please enter an integer")
                        
                        #pops the button back out
                        frame_name.config(relief = on)
                        is_on[num] = True
                        
                        err_nonum = True
                        
                else:
                    contents.append(user_entry)

              
            #closes the window  
            if (root_destroy is not None) and (err_nonum is False):
                root_destroy.destroy()
            elif err_nonum is True:
                contents.clear()
                
            

        
    else:
        frame_name.config(relief = on)

        is_on[num] = True
        info = str(is_on)
     


def switch_group(this_frame_name, frame_name_group, entry_name, num):
    """
    given the frame and all the frame attributes, will create a switch to collect all the entry data
    
    Will cause the buttons to only one to be able to be selected at a time. Additionally, if a button is
    clicked twice it will be deselected
    
    frame_name_list: a list of tuples of the (frame_name, num) for each of the associated buttons
    is_on: a list of booleans keeping track of whether each button in the group is selected
    """
    on = tk.RAISED
    off = tk.SUNKEN
    
    #determine if onor off based on bool val in frame_name_group
    if frame_name_group[num][1] == True:
    
        #deselects all the buttons
        for frame_info in frame_name_group:
            frame_info[0].config(relief=on)
            frame_info[1] = True
    
        #then selects the clicked button
        this_frame_name.config(relief = off)
        frame_name_group[num][1] = False
        
        # info = str(frame_name_group[num][1])
        # label_name.config(text = info0 + 'i', fg = "green")
    
        
    else:
        info0 = str(frame_name_group[num][1])
        this_frame_name.config(relief= on)
        
                        
        frame_name_group[num][1] = True
        # info = str(frame_name_group[num][1])
        # label_name.config(text = info0 + " " + info + 'l',
                        # fg = "grey")

        print(entry_name.get())
    


def create_entry(var_list, text, rownum, endtext='PSI'):
    """
    will define a line for adding an entry box
    
    inputs:
        var_list: a list of NONE with length 3 or 4, the frames/entry variables will be saved to it
        
    creates:
        var_list = [frame, label_name, entry_name]
    """
    on = tk.RAISED
    off = tk.SUNKEN
    
    
    var_list[0] = tk.Frame(width=20, bg='wheat1')
    var_list[0].grid(row=rownum, sticky="ew")
    # create the widgets for fr_equiv_pipe_len
    var_list[1] = tk.Label(master=var_list[0], width=20, height=2, text=text, anchor='w', bg='wheat1')
    var_list[2] = tk.Entry(master=var_list[0], width=20, relief=off, borderwidth=4)
    # layout the widgets for fr_equiv_pipe_len
    var_list[1].grid(row=0, column=0, padx = 5)
    var_list[2].grid(row=0, column=2)
    
    
    #will add psi end text if len of var_list is 4
    if len(var_list) == 4:
        var_list[3] = tk.Label(master=var_list[0], width=20, height=2, text=endtext, anchor='w', bg='wheat1')
        var_list[3].grid(row=0, column=3, padx = 5)
        


def create_button(var_list, text, rownum, is_on, is_on_num, contents=None, root=None, entry=None, forcenum=None):
    """
    will create a clickable button
    inputs:
        var_list: a list of NONE with length 5, the frames/entry variables will be saved to it
        width: the width of the button
        
        root: the root. If given a value will turn into a button that closes the root window.
        
    creates:
        var_list = [frame, left_padding, button_frame, right_padding, button_name]
    """
    on = tk.RAISED
    off = tk.SUNKEN
    
    width = len(text) * 4
    size = 410
    padding = (410-width)/2
    
    var_list[0] = tk.Frame(bg='gray2', width=410) 
    var_list[0].grid(row=rownum, sticky="nsew")
    var_list[0].grid_rowconfigure(0, weight=1)
    var_list[0].grid_columnconfigure(1, weight=1)
    #creates an empty frame before and after the size pipes button
    var_list[1] = tk.Frame(var_list[0],width=padding, bg='wheat1')
    var_list[2] = tk.Frame(var_list[0], width=width, bg='blue', relief=on, borderwidth=5)
    var_list[3] = tk.Frame(var_list[0], width=padding, bg='wheat1')
    
    var_list[1].grid(row=0, column=0, sticky="ns")
    var_list[2].grid(row=0, column=1, sticky="nsew")
    var_list[3].grid(row=0, column=2, sticky="ns")


    #create the SIZE PIPES button
    var_list[4] = tk.Button(
        master=var_list[2],
        text=text,
        width=len(text)-1,
        height=1,
        bg="blue",
        fg="yellow",
        bd=0,
        command=lambda: switch(var_list[2], 1, is_on, contents, root, entry, forcenum),
    )
    #layout the button
    var_list[4].grid(row=0, columnspan=3)


def create_nonstandard_popup(code=None, max_pressure=None):
    """
    creates the nonstandard gas popup
    
    will return:
        the new gas code(str)
        inlet pressure(int)
        outlet pressure(int)
        if LPG was selected
    """
    is_on = [True, True]
    on = tk.RAISED
    off = tk.SUNKEN
    
    
    window = tk.Tk()
    window.title("Non-standard")
    window.configure(background='wheat1')
    #window.resizable(width=False, height=False)
    window.geometry('{}x{}'.format(460,400))


    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    
    
    fr_options_grid = tk.Frame(width=20, bg='wheat1',highlightbackground="black", highlightthickness=1)
    fr_options_grid.grid(row=0,sticky='nsew')
    
    #creates the entries
    #var_list = [frame, label_name, entry_name, end_text]    
    var_entry1 = [None, None, None]
    var_entry2 = [None, None, None, None] 
    var_entry3 = [None, None, None, None]
    
    create_entry(var_entry1, "Enter Gas Code", 1)
    create_entry(var_entry2, "Enter Inlet Pressure", 2)
    create_entry(var_entry3, "Enter Outlet Pressure", 3)
    
    entry_list = [var_entry1, var_entry2, var_entry3]
    entry_name_list = [x[2] for x in entry_list]

    #CREATES THE LPG BUTTON
    #def create_button(var_list, text, rownum, is_on, is_on_num, contents=None, root=None, entry=None):
    #var_list2 = [frame, left_padding, button_frame, right_padding, button_name]
    var_list2 = [None, None, None, None, None]
    create_button(var_list2, "Select for LPG",  4, is_on, 1)



    fr_button_grid = tk.Frame(window, bg='gray2', width=410) 
    fr_button_grid.grid(row=5, sticky="nsew")
    fr_button_grid.grid_rowconfigure(0, weight=1)
    fr_button_grid.grid_columnconfigure(1, weight=1)
    #creates an empty frame before and after the size pipes button
    frame_b_blank1 = tk.Frame(fr_button_grid,width=195, bg='wheat1')
    frame_b_button = tk.Frame(fr_button_grid, width=20, bg='blue', relief=on, borderwidth=5)
    frame_b_blank2 = tk.Frame(fr_button_grid, width=195, bg='wheat1')
    
    frame_b_blank1.grid(row=0, column=0, sticky="ns")
    frame_b_button.grid(row=0, column=1, sticky="nsew")
    frame_b_blank2.grid(row=0, column=2, sticky="ns")


    #extracts the entry data when the size pipes button is pressed
    contents = []
    

    
    #create the SIZE PIPES button
    buttond2 = tk.Button(
        master=frame_b_button,
        text="Size Pipes",
        width=8,
        height=1,
        bg="blue",
        fg="yellow",
        bd=0,
        command=lambda: switch(frame_b_button, 0, is_on, contents, window, entry_name_list, forcenum_list=[False, True, True]),
    )
    #layout the button
    buttond2.grid(row=0, columnspan=3)


    #adds anything that was selected to automatically fill out
    if code is not None:
        var_entry1[2].insert(0, code)
    if max_pressure is not None:
        var_entry2[2].insert(0, max_pressure[0])
        
        
    window.mainloop()
    
    
    

    
    
    #adds LPG info to contents, True if LPG was selected
    if is_on[1] == False:
        contents.append(True)
    else:
        contents.append(False)
    
    return contents

def create_gas_popup():
        # #switch code
    on = tk.RAISED
    off = tk.SUNKEN
    
    
    #create the window
    window = tk.Tk()
    window.title("Size Gas Pipes")
    window.configure(background='wheat1')
    #window.resizable(width=False, height=False)
    window.geometry('{}x{}'.format(460,400))
    

    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)


    
    # # create all of the main containers
    fr_options_grid = tk.Frame(width=20, bg='wheat1',highlightbackground="black", highlightthickness=1)
    fr_sel_non_standard = tk.Frame(width=20, bg='wheat1', highlightbackground="black", highlightthickness=1, relief=on, borderwidth=4)
    fr_equiv_pipe_len = tk.Frame(width=20, bg='wheat1')
    fr_txt_abv_button = tk.Frame(width=20, bg='wheat1')
 
    fr_button_grid = tk.Frame(window, bg='gray2', width=410)
 
    fr_end_txt = tk.Frame(width=20, bg='wheat1')
    

    # # layout all of the main containers
    fr_options_grid.grid(row=0,sticky='nsew')
    fr_sel_non_standard.grid(row=1, sticky='ew')
    fr_equiv_pipe_len.grid(row=2, sticky="ew")
    fr_txt_abv_button.grid(row=3, sticky="ew")
    fr_button_grid.grid(row=4, sticky="nsew")
    fr_end_txt.grid(row=5, sticky="ew") 
    

    #layout the options grid
    fr_options_grid.grid_rowconfigure(0, weight=1)
    fr_options_grid.grid_columnconfigure(1, weight=1)


    # # layout the button grid
    fr_button_grid.grid_rowconfigure(0, weight=1)
    fr_button_grid.grid_columnconfigure(1, weight=1)




    


    # create the widgets for fr_equiv_pipe_len
    label_3 = tk.Label(master=fr_equiv_pipe_len, width=20, height=2, text="Equivalent Pipe Length", anchor='w', bg='wheat1')
    entrytext3 = tk.Entry(master=fr_equiv_pipe_len, width=20, relief=off, borderwidth=4)
    # layout the widgets for fr_equiv_pipe_len
    label_3.grid(row=0, column=0, padx = 5)
    entrytext3.grid(row=0, column=2)








    #create the option selection for code and pressure
    #create the mini frames for the options grid
    fr_sel_code = tk.Frame(fr_options_grid, bg='wheat1',highlightbackground="black", highlightthickness=1)
    fr_sel_p = tk.Frame(fr_options_grid, bg='wheat1',highlightbackground="black", highlightthickness=1)
    
    fr_sel_code.grid(row=0, column=0, sticky='nsew', padx=(110,20), pady=20)
    fr_sel_p.grid(row=0, column=1, sticky='w', padx=20, pady=20)


    #create the code selection box
    sel_code_title = tk.Label(master=fr_sel_code, width=0, height=1, text="   Select Code   ", bg='wheat1')
    sel_code_UPC = tk.Frame(fr_sel_code, bg='wheat1', relief=on, borderwidth=4)
    sel_code_IPC = tk.Frame(fr_sel_code, bg='wheat1', relief=on, borderwidth=4)
    
    sel_code_title.grid(row=0, columnspan=3)
    sel_code_UPC.grid(row=1, columnspan=3, pady=1)
    sel_code_IPC.grid(row=2, columnspan=3, pady=1)
    
    
   


    
    #create the pressure selection box
    sel_p_title = tk.Label(master=fr_sel_p, width=0, height=1, text="   Select Pressure   ", bg='wheat1')
    # sel_p_7WC = tk.Label(master=fr_sel_p, width=0, height=1, text='7" W.C.', bg='wheat1')
    # sel_p_2psi = tk.Label(master=fr_sel_p, width=0, height=1, text="2 psi", bg='wheat1')
    # sel_p_5psi = tk.Label(master=fr_sel_p, width=0, height=1, text="5 psi", bg='wheat1')
    
    sel_p_7WC = tk.Frame(master=fr_sel_p, bg='wheat1', relief=on, borderwidth=4)
    sel_p_2psi = tk.Frame(master=fr_sel_p, bg='wheat1', relief=on, borderwidth=4)
    sel_p_5psi = tk.Frame(master=fr_sel_p, bg='wheat1', relief=on, borderwidth=4)
    
    
    sel_p_title.grid(row=0, columnspan=3)
    sel_p_7WC.grid(row=1, columnspan=3, pady=1)
    sel_p_2psi.grid(row=2, columnspan=3, pady=1)
    sel_p_5psi.grid(row=3, columnspan=3, pady=(1,5))



    #create the variables to track which buttons are depressed
    is_on = [True, True]



    #create the non-standard selection
    # sel_non_standard = tk.Label(master=fr_sel_non_standard, width=0, height=1, text="(Select for non-standard gas code, inlet/outlet pressures, or LPG", bg='wheat1')
    

    non_standard_button = tk.Button(
        master=fr_sel_non_standard,
        text="NON-STANDARD NOT YET IMPLEMENTED",
        #text="Select for non-standard gas code, inlet/outlet pressures, or LPG",
        # width=8,
        height=1,
        bg="wheat1",
        fg="black",
        bd=0,
        command=lambda: switch(fr_sel_non_standard,1, is_on),
    )
    non_standard_button.grid(row=0, columnspan=3, padx = 5)


    #create the button label
    labeld = tk.Label(master=fr_txt_abv_button, width=20, height=2, text="", anchor='w', bg='wheat1')
    labeld.grid(row=0, columnspan=3, padx = 5)
    
    

    #creates an empty frame before and after the size pipes button
    frame_b_blank1 = tk.Frame(fr_button_grid,width=195, bg='wheat1')
    frame_b_button = tk.Frame(fr_button_grid, width=20, bg='blue', relief=on, borderwidth=5)
    frame_b_blank2 = tk.Frame(fr_button_grid, width=195, bg='wheat1')
    
    frame_b_blank1.grid(row=0, column=0, sticky="ns")
    frame_b_button.grid(row=0, column=1, sticky="nsew")
    frame_b_blank2.grid(row=0, column=2, sticky="ns")


    #extracts the entry data when the size pipes button is pressed
    contents = []
    
    
    #create the SIZE PIPES button
    buttond2 = tk.Button(
        master=frame_b_button,
        text="Size Pipes",
        width=8,
        height=1,
        bg="blue",
        fg="yellow",
        bd=0,
        command=lambda: switch(frame_b_button,  0, is_on, contents, window, entrytext3),
    )
    #layout the button
    buttond2.grid(row=0, columnspan=3)

    #create the end text widgets
    end_txt1 = tk.Label(master=fr_end_txt, width=0, height=1, text="*pipe capacitites 90% of true values in high and low gas sizing charts", bg='wheat1')
    end_txt2 = tk.Label(master=fr_end_txt, width=0, height=1, text="for additional safety factor", bg='wheat1')
    #layout the end text widgets
    end_txt1.grid(row=0, columnspan=3, padx = 5)
    end_txt2.grid(row=1, columnspan=3, sticky="w", padx = 5)




    #list of tuples tracking the association of frames and their assigned number
    frame_group_code = [[sel_code_UPC, True, "UPC"], [sel_code_IPC, True, "IPC"]]

    #create the toggleable button UPC
    button_upc = tk.Button(
        master=sel_code_UPC,
        text="UPC",
        width=8,
        height=1,
        bg='wheat1',
        fg="black",
        bd=0,
        command=lambda: switch_group(sel_code_UPC, frame_group_code, entrytext3, 0),
    )
    #layout the button
    button_upc.grid(row=0, columnspan=3)
    
    
    
    #create the toggleable button IPC
    button_ipc = tk.Button(
        master=sel_code_IPC,
        text="IPC",
        width=8,
        height=1,
        bg='wheat1',
        fg="black",
        bd=0,
        command=lambda: switch_group(sel_code_IPC, frame_group_code, entrytext3, 1),
    )
    #layout the button
    button_ipc.grid(row=0, columnspan=3)  


 
    #SETUP THE PRESSURE BUTTONS

    frame_group_pressure = [[sel_p_7WC, True, '7"W.C.'], [sel_p_2psi, True, '2 psi'], [sel_p_5psi, True, '5 psi']]


    button_p_7WC = tk.Button(
        master=sel_p_7WC,
        text='7" W.C.',
        width=8,
        height=1,
        bg='wheat1',
        fg="black",
        bd=0,
        command=lambda: switch_group(sel_p_7WC, frame_group_pressure, entrytext3, 0),
    )
    button_p_7WC.grid(row=0, columnspan=3)


    button_p_2psi = tk.Button(
        master=sel_p_2psi,
        text='2psi',
        width=8,
        height=1,
        bg='wheat1',
        fg="black",
        bd=0,
        command=lambda: switch_group(sel_p_2psi, frame_group_pressure, entrytext3, 1),
    )
    button_p_2psi.grid(row=0, columnspan=3)

    button_p_5psi = tk.Button(
        master=sel_p_5psi,
        text='5psi',
        width=8,
        height=1,
        bg='wheat1',
        fg="black",
        bd=0,
        command=lambda: switch_group(sel_p_5psi, frame_group_pressure, entrytext3, 2),
    )
    button_p_5psi.grid(row=0, columnspan=3)
    


    
    window.mainloop()

    code = code_selector(frame_group_code)
    pressure = code_selector(frame_group_pressure)
    
    #to prevent error if x out of tkinter window
    if len(contents) > 0:
        contents = contents[0]
    
    return [is_on[1],code, pressure, contents]



def main():

    #create the gas popup and save the selections to a variable
    #gas_data = [nonstandard?, code, max_pressure, pipe_length]
    gas_data = create_gas_popup()


    #create the non-standard popup if it was selected
    if gas_data[0] == False:

        #will not transfer max_pressure if 7"W.C. is selected to reduce confusion
        if gas_data[2] == '7"W.C.':
            max_pressure = None
        else:
            print(gas_data[1])
            max_pressure = gas_data[2]
            
            
        #CREATES THE NONSTANDARD POPUP
        #non_std data = [code, inlet pressure, outlet pressure, LPG?]
        nonstd_data = create_nonstandard_popup(gas_data[1], max_pressure)
        pressure = str(nonstd_data[1]) + " PSI"
        
        #output = [nonstandard, code,   inlet pressure, outlet pressure, pipe_length, LPG?, '']
        output = ['NON-STANDARD',nonstd_data[0], pressure, nonstd_data[2], gas_data[3],  nonstd_data[3], '']
        
        #when printed this goes to the run_cpython function
        print(output)
        
    else:
        gas_data[0] = 'STANDARD'
        
        #LPG = False
        gas_data.extend([False, ''])
        print(gas_data)



if __name__ == "__main__":
    main()


