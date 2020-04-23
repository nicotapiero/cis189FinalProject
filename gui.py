import tkinter
from tkinter import messagebox
from tkinter import *


from solver_phase import *

from random import random

def R(n, m):
    """Generate a random formula in the family R(n,m), with no empty clauses."""
    # Fill in here
    cnf = []
    for j in range(m):
        clause = []
        for i in range(1, n+1):
            rng = random()
            if rng < (1/3):
                clause.append(i)
            elif rng < (2/3):
                clause.append(-1 * i)
        if (len(clause) > 0):
            cnf.append(clause)

    return cnf

random_cnf = R(3, 4)

def generate_cnf():
    random_cnf = R(3,4)
    cnf.set(str(random_cnf))
    return

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
        print(array, 'array')

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

blank_label = Label(bottom, text="\n\n")
blank_label.pack()

button = Button(bottom, text='Generate Random CNF', command=generate_cnf)
button.pack()

cnf = StringVar()
cnf.set(str(random_cnf))
blank_label = Label(bottom, textvariable=cnf)
blank_label.pack()

def submit_random():
    maxes = [max(max(clause), abs(min(clause))) for clause in random_cnf]
    big_num = max(maxes)
    top.pack_forget()
    bottom.pack_forget()
    #print(maxes, big_num, random_cnf)
    solver_phase(big_num, random_cnf, win)
    return

button = Button(bottom, text='Use random CNF', command=submit_random)
button.pack()


win.title("PennSAT Visualizer")



win.mainloop()
