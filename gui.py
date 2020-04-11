import tkinter
from tkinter import messagebox
from tkinter import *


from solver_phase import *

win = Tk()

top = Frame(win, borderwidth=2, relief="solid")
bottom = Frame(win, borderwidth=2, relief="solid")

top.pack(side="top", expand=True, fill="both")
bottom.pack(side="bottom", expand=True, fill="both")

entries = [Entry(top)]

for entry in entries:
    entry.pack()

def cont():
    #print(w.get())
    for entry in entries:
        nums = entry.get().split(',')
        bigbreak = False
        print(nums)
        for num in nums:
            num = num.lstrip().strip()
            if (not str.isdigit(num)) or num == '':
                bigbreak = True
                break
        if bigbreak:
            break
    else:
        top.pack_forget()
        bottom.pack_forget()

        solver_phase([9], win)
        return

    messagebox.showerror("Error","All boxes must have numbers separated by commas to represent a clause")

def addThing():
    local_entry = Entry(top)
    entries.append(local_entry)
    local_entry.pack()

def removeThing():
    local_entry = entries[-1]
    local_entry.pack_forget()
    entries.pop()

button = Button(bottom, text="Add New Clause", command=addThing)
button.pack()

button = Button(bottom, text="Remove Bottom Clause", command=removeThing)
button.pack()

button = Button(bottom, text="Submit Formula", command=cont)
button.pack()


win.title("PennSAT Visualizer")





























win.mainloop()



