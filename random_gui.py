from tkinter import Tk, Label, Button, Entry, StringVar, END, W, E
from typing import List, Union, Optional
from iterative_pennSAT import IterativePennSAT

Lit = int
Var = int
Clause = List[int]
CNF = List[Clause]
Assignment = List[Optional[bool]]

class PennSAT:

    def __init__(self, master):
        self.master = master
        master.title("penn sat")

        self.action = "enter a cnf"

        self.action_label_text = StringVar()
        self.action_label_text.set(self.action)
        self.action_label = Label(master, textvariable=self.action_label_text)

        self.label = Label(master, text="current action:")

        self.entry = Entry(master)

        self.next_button = Button(master, text="next", command=lambda: self.update("next"))
        self.enter_button = Button(master, text="enter", command=lambda: self.update("enter"))
        self.reset_button = Button(master, text="reset", command=lambda: self.update("reset"))

        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.action_label.grid(row=0, column=1, columnspan=2, sticky=E)

        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        self.next_button.grid(row=2, column=0)
        self.enter_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)

        # PENNSAT?
        # self.solver = iterative_PennSAT(n, self.entry, True)
        



    def update(self, method):
        if method == "reset":
            self.action = "enter a cnf"
        elif method == "enter":
            self.temp_cnf = self.entry.get()
            self.action = "entered: " + self.temp_cnf
            self.parse_input(self.temp_cnf)
            self.solver = IterativePennSAT(self.n, self.cnf, True)

        else: # next
            self.solver.solve()
            self.action = "horrible life"

        self.action_label_text.set(self.action)
        self.entry.delete(0, END)


    def parse_input(self, input):
        output = []
        clauses = input.split(";")
        temp_set = set()
        for clause in clauses:
            clause = clause[1:-1]
            temp = clause.split(",")
            temp_clause = []
            for i in temp:
                temp_clause.append(int(i))
                temp_set.add(i)
            output.append(temp_clause)
        self.cnf = output
        self.n = len(temp_set)


root = Tk()
my_gui = PennSAT(root)
root.mainloop()