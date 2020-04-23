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
    array = []
    biggest_num = 1
    for entry in entries:
        nums = entry.get().split(',')
        bigbreak = False
        print(nums)
        smaller_array = []
        for num in nums:
            num = num.lstrip().strip()

            try:
                my_int = int(num)
                smaller_array.append(my_int)
                if abs(my_int) > biggest_num:
                    biggest_num = abs(my_int)
            except:
                bigbreak = True
                break
            # if (not str.isdigit(num)) or num == '':
            #     bigbreak = True
            #     break
        if bigbreak:
            break
        else:
            array.append(smaller_array)
    else:
        top.pack_forget()
        bottom.pack_forget()

        maxnum = 1
        # for entry in entries:
        #     nums = entry.get().split(',')
        #     print(nums)
        print(array)

        solver_phase(biggest_num, array, win)
        return

    messagebox.showerror("Error","All boxes must have numbers separated by commas to represent a clause")

def addThing():
    local_entry = Entry(top)
    entries.append(local_entry)
    local_entry.pack()

def removeThing():
    if len(entries) > 1:
        local_entry = entries[-1]
        local_entry.pack_forget()
        entries.pop()
    else:
        messagebox.showerror("Error","You must have at least one clause, so you cannot remove the last box")


button = Button(bottom, text="Add New Clause", command=addThing)
button.pack()

button = Button(bottom, text="Remove Bottom Clause", command=removeThing)
button.pack()

button = Button(bottom, text="Submit Formula", command=cont)
button.pack()


win.title("PennSAT Visualizer")





























win.mainloop()
