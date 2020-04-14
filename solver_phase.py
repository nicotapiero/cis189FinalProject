import tkinter
from tkinter import messagebox
from tkinter import *
from pennSAT import *


# https://stackoverflow.com/questions/46522200/how-to-make-two-split-up-screen-canvas-inside-the-python-tkinter-window



def solver_phase(max, cnf, win):
    win.grid_rowconfigure(1, weight=1)
    win.grid_columnconfigure(1, weight=1)

    #
    left_frame = Frame(win, width=500, height=150, background="black").pack(side="left", fill=BOTH)
    right_frame = Frame(win, width=500, height=150, background="black").pack(side="right", fill=BOTH)

    top_left = Frame(left_frame, width=500, height=150, background="red").pack(fill="both", expand=True, padx=20, pady=20)
    top_right = Frame(right_frame, width=500, height=150, background="blue").pack(fill="both", expand=True, padx=20, pady=20)
    bottom_left = Frame(left_frame, width=500, height=150, background="green").pack(fill="both", expand=True, padx=20, pady=20)
    bottom_right = Frame(right_frame, width=500, height=150, background="yellow").pack(fill="both", expand=True, padx=20, pady=20)
    #
    # # top_left
    # # top_right
    # # bottom_left
    # # bottom_right
    #
    text = StringVar()


    print(max, cnf)
    solver = PennSAT(max, cnf, True)

    text.set(str(solver.assignment_stack))
    label = Label(textvariable=text).grid(row=0, column=0)

    # label.pack()

    ass_stack_label = Label(top_left, text="Assignment Stack Stff").grid(row=0, column=0)

    tree_label = Label(bottom_right, text="Tree Stuff").grid(row=0, column=0)
    flowchart_label = Label(top_right, text="Flowchart").grid(row=0, column=0)

    # ass_stack = Label()
    # ass_stack["text"] = solver.assignment_stack
    # ass_stack.pack()

    def start():
        solver.start()
        print('wh')
        print(str(solver.assignment_stack))
       # text.set('FUCK')

        text.set(str(solver.assignment_stack))

    control_label = Label(bottom_right, text="Controls").grid(row=0, column=0)
    button = Button(bottom_right, text="start").grid(row=0, column=0)
    # button.pack(side="bottom")
