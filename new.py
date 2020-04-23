import tkinter
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

from iterative_pennSAT import IterativePennSAT

from tree import display_tree

win = Tk()

#
# left_frame = Frame(win, width=500, height=150, background="black").pack(side="left", fill=BOTH)
# right_frame = Frame(win, width=500, height=150, background="black").pack(side="right", fill=BOTH)

# top_left = Frame(win, width=500, height=150, background="red").pack(fill="both", expand=True, padx=20, pady=20)
# top_right = Frame(win, width=500, height=150, background="blue").pack(fill="both", expand=True, padx=20, pady=20)
# bottom_left = Frame(win, width=500, height=150, background="green").pack(fill="both", expand=True, padx=20, pady=20)
# bottom_right = Frame(win, width=500, height=150, background="yellow").pack(fill="both", expand=True, padx=20, pady=20)

left = Frame(win, width=500, height = 300, background="white")
left.grid(row=0, column=0)

middle = Frame(win, width=700, height = 300, background="white")
middle.grid(row=0, column=1)

right = Frame(win, width=500, height = 300, background="white")
right.grid(row=0, column=2)


top_left = Frame(left, width=500, height=150, background="red")
top_left.pack()

top_right = Frame(right, width=500, height=150, background="blue")
top_right.pack()

# top_middle = Frame(, width=500, height=150, background="blue")
# top_middle.grid(row=0, column=1)
# bottom_middle = Frame(win, width=500, height=150, background="blue")
# bottom_middle.grid(row=1, column=1)

bottom_left = Frame(left, width=500, height=150, background="green")
bottom_left.pack()

bottom_right = Frame(right, width=500, height=150, background="yellow")
bottom_right.pack()

win.mainloop()