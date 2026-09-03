"""
called on by the open popup to make gas form
"""
import sys
import tkinter as tk


is_on = [True, True, True]
is_on2 = True
            
on = tk.RAISED
off = tk.SUNKEN
	
def read_direct():
    """
    reads the job data sent directly from doc-opened.py
    """
    info = sys.argv[1]


    return info


def handle_click(event):
    print('the button was clicked')


def switch(frame_name, label_name, entry_name, entry_name2, entry_name3, num):
    """
    given the frame and all the frame attributes, will create a switch to collect all the entry data
    """
    global is_on
    
    on = tk.RAISED
    off = tk.SUNKEN
    
    #determine if on or off
    if is_on[num]:
     
        frame_name.config(relief= off)
        label_name.config(text = "The Switch is Off",
                        fg = "grey")
                        
        is_on[num] = False
        print(entry_name.get(), entry_name2.get(), entry_name3.get())
        
    else:
        frame_name.config(relief = on)
        label_name.config(text = "The Switch is On", fg = "green")
        is_on[num] = True

def main():

    global is_on
    
    
    
    window = tk.Tk()
    window.title("Temperature Converter")
    window.configure(background='wheat1')
    
    
    # #switch code
    on = tk.RAISED
    off = tk.SUNKEN
    

           
    
    
    frame_d = tk.Frame(width=20, bg='wheat1')
    # label = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
    labeld = tk.Label(master=frame_d, width=20, height=2, text="I'm in Frame d", anchor='w', bg='wheat1')
    labeld.pack()
    
    frame_d2 = tk.Frame(width=20, bg='blue', relief=on, borderwidth=5)
    # entrytextd = tk.Entry(master=frame_d2, width=20)
    # entrytextd.pack()

    frame_d3 = tk.Frame(width=20, bg='wheat1')
    


    #entry creator
 
        # frame_name = tk.Frame(width=20, bg='wheat1')
        # label_name = tk.Label(master=frame_name, width=20, height=2, text="Pressure (PSI)", anchor='w', bg='wheat1')
        # label_name.pack(side=tk.LEFT)

        # entrytext_name = tk.Entry(master=frame_name, width=20)
        # entrytext_name.pack(side=tk.LEFT)



    #code for rest

    frame_a = tk.Frame(width=20, bg='wheat1')
    # label = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
    label = tk.Label(master=frame_a, width=20, height=2, text="Pressure (PSI)", anchor='w', bg='wheat1')
    label.pack(side=tk.LEFT)
    
    
    entrytext = tk.Entry(master=frame_a, width=20)
    entrytext.pack(side=tk.LEFT)
    
    
    frame_a2 = tk.Frame(bg='wheat1')
    label2 = tk.Label(master=frame_a2, width=20, height=2, text="Pressure Drop", anchor="w", bg='wheat1')
    label2.pack(side=tk.LEFT)
    
    entrytext2 = tk.Entry(master=frame_a2, width=20)
    entrytext2.pack(side=tk.LEFT)
    
    
    frame_a3 = tk.Frame(width=20, bg='wheat1')
    label_3 = tk.Label(master=frame_a3, width=20, height=2, text="Max Length (FT)", anchor='w', bg='wheat1')
    label_3.pack(side=tk.LEFT)

    entrytext3 = tk.Entry(master=frame_a3, width=20)
    entrytext3.pack(side=tk.LEFT)
    
    
    
    buttond2 = tk.Button(
        master=frame_d2,
        text="Click me!",
        width=8,
        height=1,
        bg="blue",
        fg="yellow",
        bd=0,
        command=lambda: switch(frame_d2, labeld, entrytext, entrytext2, entrytext3, 0),
    )
    buttond2.pack()
    
    
    
    frame_e = tk.Frame(width=20, bg='wheat1')
    label_4 = tk.Label(master=frame_e, width=20, height=2, text="pipe capacitites 90% of true values in higih and low gas sizing charts for additional safety factor",
                       anchor='w', bg='wheat1')
    label_4.pack()
    


    # frame_b = tk.Frame(bg='blue')
    # button = tk.Button(
        # master=frame_b,
        # text="Click me!",
        # width=40,
        # height=20,
        # bg="blue",
        # fg="yellow",
    # )
    # button.pack()
    
    frame_c = tk.Frame(bg='blue')
    labelend = tk.Label(master=frame_c, width=60, bg='blue')
    # relief=tk.SUNKEN
    labelend.pack()
    
    
    

    
    
   
    frame_a.pack(fill=tk.X)
    frame_a2.pack(fill=tk.X)
    frame_a3.pack(fill=tk.X)
    #will break anchor if remove fill=tk.X
    
    #frame_b.pack(fill=tk.X)
    # frame_c.pack(fill=tk.BOTH, expand=True)
    frame_c.pack(side=tk.LEFT)
    
    
    
    frame_d.pack()
    frame_d2.pack()
    frame_d3.pack()    

    frame_e.pack(fill=tk.X)
    

    
    # button.bind('<Button-1>', handle_click)
    
    window.mainloop()
    
    
    

    
    # window.resizable(width=False, height=False)



		



main()


