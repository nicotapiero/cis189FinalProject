import tkinter
from tkinter import messagebox
from tkinter import *
from pennSAT import *


# https://stackoverflow.com/questions/46522200/how-to-make-two-split-up-screen-canvas-inside-the-python-tkinter-window



def solver_phase(max, cnf, win):
    # win.grid_rowconfigure(1, weight=1)
    # win.grid_columnconfigure(1, weight=1)

    #
    # left_frame = Frame(win, width=500, height=150, background="black").pack(side="left", fill=BOTH)
    # right_frame = Frame(win, width=500, height=150, background="black").pack(side="right", fill=BOTH)

    # top_left = Frame(win, width=500, height=150, background="red").pack(fill="both", expand=True, padx=20, pady=20)
    # top_right = Frame(win, width=500, height=150, background="blue").pack(fill="both", expand=True, padx=20, pady=20)
    # bottom_left = Frame(win, width=500, height=150, background="green").pack(fill="both", expand=True, padx=20, pady=20)
    # bottom_right = Frame(win, width=500, height=150, background="yellow").pack(fill="both", expand=True, padx=20, pady=20)

    top_left = Frame(win, width=500, height=150, background="red")
    top_left.grid(row=0, column=0)
    top_right = Frame(win, width=500, height=150, background="blue")
    top_right.grid(row=1, column=0)
    bottom_left = Frame(win, width=500, height=150, background="green")
    bottom_left.grid(row=0, column=1)
    bottom_right = Frame(win, width=500, height=150, background="yellow")
    bottom_right.grid(row=1, column=1)
    # #
    # # # top_left
    # # # top_right
    # # # bottom_left
    # # # bottom_right
    # #
    text = StringVar()
    #
    #
    print(max, cnf)
    solver = PennSAT(max, cnf, True)



    # label.pack()

    ass_stack_label = Label(top_left, text="Assignment Stack Stuff")
    ass_stack_label.pack()

    text.set(str(solver.assignment_stack))
    label = Label(top_left,textvariable=text)
    label.pack()

    tree_label = Label(bottom_left, text="Tree Stuff")
    tree_label.pack()
    flowchart_label = Label(top_right, text="Flowchart")
    flowchart_label.pack()

    # ass_stack = Label()
    # ass_stack["text"] = solver.assignment_stack
    # ass_stack.pack()

    def start():
        solver.start()
        print('wh')
        print(str(solver.assignment_stack))
       # text.set('FUCK')

        text.set(str(solver.assignment_stack))

    control_label = Label(bottom_right, text="Controls")
    control_label.pack()
    button = Button(bottom_right, text="start", command=start)
    button.pack()
