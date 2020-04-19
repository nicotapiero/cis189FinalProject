import tkinter
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

win = Tk()



load = Image.open("flowchart copy.jpg")
render = ImageTk.PhotoImage(load)
img = Label(win, image=render)
img.image = render
img.pack()




win.mainloop()
