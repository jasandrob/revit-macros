"""
called on by the open popup to make tkinter window
"""
import sys
import tkinter as tk


is_on = [True, True, True]
is_on2 = True
            

	
def read_direct():
    """
    reads the job data sent directly from doc-opened.py
    """
    info = sys.argv[1]


    return info


def handle_click(event):
    print('the button was clicked')



def main():

    global is_on
    
    
    
    window = tk.Tk()
    window.title("Temperature Converter")
    window.configure(background='wheat1')
    
    
    #switch code
    on = tk.RAISED
    off = tk.SUNKEN
    

    
    
    # def switch(hi):
        
        # global is_on
        
        
        # #determine if on or off
        # if is_on:
         
            # frame_d2.config(relief= off)
            # labeld.config(text = "The Switch is Off",
                            # fg = "grey")
                            
            # is_on = False
            # print(entrytext.get())
            
        # else:
            # frame_d2.config(relief = on)
            # labeld.config(text = "The Switch is On", fg = "green")
            # is_on = True
            
            
  
    # # on_button = tk.Button(window, text="click here", relief=on, bd=0, command=switch)
    # # on_button.pack(pady=50)
    
    
    # frame_d = tk.Frame(width=20, bg='wheat1')
    # # label = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
    # labeld = tk.Label(master=frame_d, width=20, height=2, text="I'm in Frame d", anchor='w', bg='wheat1')
    # labeld.pack()
    
    # frame_d2 = tk.Frame(width=20, bg='blue', relief=on, borderwidth=5)
    # # entrytextd = tk.Entry(master=frame_d2, width=20)
    # # entrytextd.pack()

    # frame_d3 = tk.Frame(width=20, bg='wheat1')
    
    # buttond2 = tk.Button(
        # master=frame_d2,
        # text="Click me!",
        # width=8,
        # height=1,
        # bg="blue",
        # fg="yellow",
        # bd=0,
        # command=lambda: switch(10),
    # )
    # buttond2.pack()
    
    
    def switch(frame_name, label_name, num):
    
        global is_on
        
        
        #determine if on or off
        if is_on[num]:
         
            frame_name.config(relief= off)
            label_name.config(text = "The Switch is Off",
                            fg = "grey")
                            
            is_on[num] = False
            print(entrytext.get())
            
        else:
            frame_name.config(relief = on)
            label_name.config(text = "The Switch is On", fg = "green")
            is_on[num] = True
            
            
  
    # on_button = tk.Button(window, text="click here", relief=on, bd=0, command=switch)
    # on_button.pack(pady=50)
    
    
    frame_d = tk.Frame(width=20, bg='wheat1')
    # label = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
    labeld = tk.Label(master=frame_d, width=20, height=2, text="I'm in Frame d", anchor='w', bg='wheat1')
    labeld.pack()
    
    frame_d2 = tk.Frame(width=20, bg='blue', relief=on, borderwidth=5)
    # entrytextd = tk.Entry(master=frame_d2, width=20)
    # entrytextd.pack()

    frame_d3 = tk.Frame(width=20, bg='wheat1')
    
    buttond2 = tk.Button(
        master=frame_d2,
        text="Click me!",
        width=8,
        height=1,
        bg="blue",
        fg="yellow",
        bd=0,
        command=lambda: switch(frame_d2, labeld, 0),
    )
    buttond2.pack()
    
    
    
    
    
    



    #switch2 code
    frame_a1 = tk.Frame(width=20, bg='green', relief=on, borderwidth=5)
    
    
    on = tk.RAISED
    off = tk.SUNKEN
    
    my_label2 = tk.Label(master=frame_a1,
        text = "The Switch is On!",
        fg = 'green',
        font = ("Helvetica", 32))
        
    my_label2.pack(pady = 20)
    
    
    def switch2():
        global is_on2
        
        
        #determine if on or off
        if is_on2:
            frame_a1.config(relief=off)
            my_label2.config(text = "The Switch is Off",
                            fg = "grey")
                            
            is_on2 = False
            
        else:
            frame_a1.config(relief=on)
            my_label2.config(text = "The Switch is On", fg = "green")
            is_on2 = True
      
            
  
    on_button2 = tk.Button(master=frame_a1, text="click here", relief=on, bd=0, command=switch2)
    on_button2.pack(pady=50)



















    #code for rest

    frame_a = tk.Frame(width=20, bg='wheat1')
    # label = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
    label = tk.Label(master=frame_a, width=20, height=2, text="I'm in Frame A", anchor='w', bg='wheat1')
    label.pack(side=tk.LEFT)
    
    
    entrytext = tk.Entry(master=frame_a, width=20)
    entrytext.pack(side=tk.LEFT)
    
    frame_a2 = tk.Frame(bg='wheat1')
    label2 = tk.Label(master=frame_a2, width=20, height=2, text="Frame A2", anchor="w", bg='wheat1')
    label2.pack(side=tk.LEFT)
    
    
    entrytext2 = tk.Entry(master=frame_a2, width=20)
    entrytext2.pack(side=tk.LEFT)

    frame_b = tk.Frame(bg='blue')
    button = tk.Button(
        master=frame_b,
        text="Click me!",
        width=40,
        height=20,
        bg="blue",
        fg="yellow",
    )
    button.pack()
    
    frame_c = tk.Frame(bg='blue')
    labelend = tk.Label(master=frame_c, width=60, bg='blue')
    # relief=tk.SUNKEN
    labelend.pack()
    
    
    

    
    
    
    frame_a1.pack()
    frame_a.pack(fill=tk.X)
    frame_a2.pack(fill=tk.X)
    frame_b.pack(fill=tk.X)
    frame_c.pack(fill=tk.BOTH, expand=True)
    
    
    
    frame_d.pack(side=tk.LEFT)
    frame_d2.pack(side=tk.LEFT)
    frame_d3.pack(side=tk.LEFT)    

    
    #name = entry.get()
    
    button.bind('<Button-1>', handle_click)
    
    window.mainloop()
    
    
    

    
    # window.resizable(width=False, height=False)



		



main()


