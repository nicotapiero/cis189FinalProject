import tkinter
from tkinter import messagebox
from tkinter import *
from pennSAT import *


# https://stackoverflow.com/questions/46522200/how-to-make-two-split-up-screen-canvas-inside-the-python-tkinter-window



def solver_phase(cnf, win):
    text = StringVar()
    solver = PennSAT(3, [[1], [-2, -2], [-1, -2, -3], [-1, 3]], True)

    text.set(str(solver.assignment_stack))
    label = Label(win, textvariable=text)

    label.pack()

    ass_stack = Label()
    ass_stack["text"] = solver.assignment_stack
    ass_stack.pack()

    def start():
        solver.start()
        print('wh')
        print(str(solver.assignment_stack))
       # text.set('FUCK')

        text.set(str(solver.assignment_stack))

    button = Button(text="start", command=start)
    button.pack()
