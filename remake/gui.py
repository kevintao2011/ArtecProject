import datetime
import tkinter as tk

# window = tk.Tk()

# # root window
# window.title('GUI')
# window.geometry("240x100")
# window.resizable(0, 0)

# # configure the grid
# #window.columnconfigure(which col, weight=size)
# window.columnconfigure(0, weight=1)
# window.columnconfigure(1, weight=3)

# greeting = tk.Label(text="Hello, Tkinter") #label 

# robot_label = tk.Label(window,text="ARtec1")
# robot_label.grid(column=0,row=0)

# robot_label = tk.Label(window,text="1")
# robot_label.grid(column=1,row=0)

# # frame1 = tk.Frame()
# # frame1.config()





# # greeting.pack() #pack all thgs

# window.mainloop() #must


def set_label():
    currentTime = datetime.datetime.now()
    label['text'] = currentTime
    root.after(1, set_label)

root = tk.Tk()
label = tk.Label(root, text="placeholder")
label.pack()

set_label()
root.mainloop()

# window.columnconfigure([0, 1, 2], minsize=50, weight=1)


# btn_decrease = tk.Button(master=window, text="-")

# btn_decrease.grid(row=0, column=0, sticky="nsew")


# lbl_value = tk.Label(master=window, text="0")

# lbl_value.grid(row=0, column=1)


# btn_increase = tk.Button(master=window, text="+")

# btn_increase.grid(row=0, column=2, sticky="nsew")


# window.mainloop()