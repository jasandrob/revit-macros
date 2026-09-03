"""
called on by the open popup to make gas form
"""
import sys
import tkinter as tk


	
def read_direct():
    """
    reads the job data sent directly from doc-opened.py
    """
    info = sys.argv[1]


    return info


def handle_click(event):
    print('the button was clicked')


def switch(frame_name, label_name, entry_name, num, is_on):
    """
    given the frame and all the frame attributes, will create a switch to collect all the entry data
    """
    
    on = tk.RAISED
    off = tk.SUNKEN
    
    #determine if on or off
    if is_on[num]:
     
        frame_name.config(relief= off)

                        
        is_on[num] = False
        info = str(is_on)
        label_name.config(text = info, fg = "green")        
        print(entry_name.get())
        
    else:
        frame_name.config(relief = on)

        is_on[num] = True
        info = str(is_on)
        label_name.config(text = info, fg = "green")        


def switch_group(this_frame_name, frame_name_list, label_name, entry_name, num, is_on):
    """
    given the frame and all the frame attributes, will create a switch to collect all the entry data
    
    Will cause the buttons to only one to be able to be selected at a time. Additionally, if a button is
    clicked twice it will be deselected
    
    frame_name_list: a list of tuples of the (frame_name, num) for each of the associated buttons
    is_on: a list of booleans keeping track of whether each button in the group is selected
    """
    on = tk.RAISED
    off = tk.SUNKEN
    
    #determine if on or off
    if is_on[num]:
    
        #deselects all the buttons
        for frame, frame_num in frame_name_list:
            frame.config(relief=on)
            is_on[frame_num] = True
    
        #then selects the clicked button
        this_frame_name.config(relief = off)
        is_on[num] = False
        
        info = str(is_on)
        label_name.config(text = info, fg = "green")
    
        
    else:
        this_frame_name.config(relief= on)
        
                        
        is_on[num] = True
        info = str(is_on)
        label_name.config(text = info,
                        fg = "grey")

        print(entry_name.get())
    





def main():

    
    # #switch code
    on = tk.RAISED
    off = tk.SUNKEN
    
    
    #create the window
    window = tk.Tk()
    window.title("Temperature Converter")
    window.configure(background='wheat1')
    #window.resizable(width=False, height=False)
    window.geometry('{}x{}'.format(460,400))
    

    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)


    
    # # create all of the main containers
    fr_options_grid = tk.Frame(width=20, bg='wheat1',highlightbackground="black", highlightthickness=1)
    fr_sel_non_standard = tk.Frame(width=20, bg='wheat1')
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
    entrytext3 = tk.Entry(master=fr_equiv_pipe_len, width=20)
    # layout the widgets for fr_equiv_pipe_len
    label_3.grid(row=0, column=0)
    entrytext3.grid(row=0, column=2)








    #create the option selection for code and pressure
    #create the mini frames for the options grid
    fr_sel_code = tk.Frame(fr_options_grid, bg='wheat1',highlightbackground="black", highlightthickness=1)
    fr_sel_p = tk.Frame(fr_options_grid, bg='wheat1',highlightbackground="black", highlightthickness=1)
    
    fr_sel_code.grid(row=0, column=0, sticky='nsew', padx=(110,20), pady=20)
    fr_sel_p.grid(row=0, column=1, sticky='w', padx=20, pady=20)


    #create the code selection box
    sel_code_title = tk.Label(master=fr_sel_code, width=0, height=1, text="   Select Code   ", bg='wheat1')
    sel_code_UPC = tk.Frame(fr_sel_code, bg='wheat1', relief=on, borderwidth=5)
    sel_code_IPC = tk.Frame(fr_sel_code, bg='wheat1', relief=on, borderwidth=5)
    
    sel_code_title.grid(row=0, columnspan=3)
    sel_code_UPC.grid(row=1, columnspan=3)
    sel_code_IPC.grid(row=2, columnspan=3)
    
    
   


    
    #create the pressure selection box
    sel_p_title = tk.Label(master=fr_sel_p, width=0, height=1, text="   Select Pressure   ", bg='wheat1')
    sel_p_7WC = tk.Label(master=fr_sel_p, width=0, height=1, text='7" W.C.', bg='wheat1')
    sel_p_2psi = tk.Label(master=fr_sel_p, width=0, height=1, text="2 psi", bg='wheat1')
    sel_p_5psi = tk.Label(master=fr_sel_p, width=0, height=1, text="5 psi", bg='wheat1')
    
    
    sel_p_title.grid(row=0, columnspan=3)
    sel_p_7WC.grid(row=1, columnspan=3)
    sel_p_2psi.grid(row=2, columnspan=3)
    sel_p_5psi.grid(row=3, columnspan=3)







    #create the non-standard selection
    sel_non_standard = tk.Label(master=fr_sel_non_standard, width=0, height=1, text="Select for non-standard gas code, inlet/outlet pressures, or LPG", bg='wheat1')
    sel_non_standard.grid(row=0, columnspan=3)


    #create the button label
    labeld = tk.Label(master=fr_txt_abv_button, width=20, height=2, text="I'm in Frame d", anchor='w', bg='wheat1')
    labeld.grid(row=0, columnspan=3)
    
    
    #creates an empty frame before and after the button
    frame_b_blank1 = tk.Frame(fr_button_grid,width=195, bg='wheat1')
    frame_b_button = tk.Frame(fr_button_grid, width=20, bg='blue', relief=on, borderwidth=5)
    frame_b_blank2 = tk.Frame(fr_button_grid, width=195, bg='wheat1')
    
    frame_b_blank1.grid(row=0, column=0, sticky="ns")
    frame_b_button.grid(row=0, column=1, sticky="nsew")
    frame_b_blank2.grid(row=0, column=2, sticky="ns")


    #create the variables to track which buttons are depressed
    is_on = [True, True, True]
    
    
    
    #create the toggleable button
    buttond2 = tk.Button(
        master=frame_b_button,
        text="Size Pipes",
        width=8,
        height=1,
        bg="blue",
        fg="yellow",
        bd=0,
        command=lambda: switch(frame_b_button, labeld, entrytext3, 0, is_on),
    )
    #layout the button
    buttond2.grid(row=0, columnspan=3)

    #create the end text widgets
    end_txt1 = tk.Label(master=fr_end_txt, width=0, height=1, text="*pipe capacitites 90% of true values in high and low gas sizing charts", bg='wheat1')
    end_txt2 = tk.Label(master=fr_end_txt, width=0, height=1, text="for additional safety factor", bg='wheat1')
    #layout the end text widgets
    end_txt1.grid(row=0, columnspan=3)
    end_txt2.grid(row=1, columnspan=3, sticky="w")




    #list of tuples tracking the association of frames and their assigned number
    frame_group1 = [(sel_code_UPC, 1), (sel_code_IPC, 2)]

    #create the toggleable button UPC
    button_upc = tk.Button(
        master=sel_code_UPC,
        text="UPC",
        width=8,
        height=1,
        bg='wheat1',
        fg="black",
        bd=0,
        command=lambda: switch_group(sel_code_UPC, frame_group1, labeld, entrytext3, 1, is_on),
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
        command=lambda: switch_group(sel_code_IPC, frame_group1, labeld, entrytext3, 2, is_on),
    )
    #layout the button
    button_ipc.grid(row=0, columnspan=3)  























    
    window.mainloop()
    
    
    

    
    # window.resizable(width=False, height=False)



		



main()


