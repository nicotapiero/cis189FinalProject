import tkinter
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from iterative_pennSAT import IterativePennSAT
from tree import draw_tree


flowchart_images = []


def create_images():
    load = Image.open("images/flowchart1.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchart2.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchart3.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchart4.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchart5.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchart6.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchartSAT.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))
    load = Image.open("images/flowchartUNSAT.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load, render))


def solver_phase(max, cnf, win):
    create_images()

    left = Frame(win, width=500, height=400, background="white")
    left.grid(row=0, column=0)

    middle = Frame(win, width=500, height=400, background="white")
    middle.grid(row=0, column=1)

    right = Frame(win, width=500, height=400, background="white")
    right.grid(row=0, column=2)

    top_left = Frame(left, width=500, height=200, background="red")
    top_left.grid(row=0, column=0)

    top_right = Frame(right, width=500, height=200, background="blue")
    top_right.pack()

    bottom_left = Frame(left, width=500, height=200, background="green")
    bottom_left.grid(row=1, column=0)

    bottom_right = Frame(right, width=500, height=200, background="yellow")
    bottom_right.pack()

    solver = IterativePennSAT(max, cnf, True)

    ass_stack_label = Label(top_left, text="Assignment Stack Stuff")
    ass_stack_label.pack()

    text = StringVar()
    text.set('Level 0: ' + str(solver.assignment_stack[1:]) + '\n')
    label = Label(top_left, textvariable=text)
    label.pack()

    tree_label = Label(middle, text="Tree Stuff")
    tree_label.pack()

    decision_stack_text = StringVar()
    decision_stack_text.set('Decision Stack: ' +
                            str(solver.decision_stack) + '\n')
    decisions_label = Label(bottom_left, textvariable=decision_stack_text)
    decisions_label.pack(side=TOP)

    tree_canvas = Canvas(middle, width=500, height=400, bg="snow2")
    tree_canvas.pack()

    flowchart_label = Label(top_right, text="Flowchart")
    flowchart_label.pack()

    img = Label(top_right, image=flowchart_images[0][1])
    img.pack()

    watching_text = StringVar()
    watchy_string = ''

    for i in range(-solver.n, solver.n+1):
        if len(solver.clauses_watching[i]) != 0:
            watchy_string += f'Literal {i} is being watched by {solver.clauses_watching[i]}\n'

    watching_text.set(watchy_string)
    watching_label = Label(bottom_left, textvariable=watching_text)
    watching_label.pack()

    UP_text = StringVar()
    UP_text.set(f'Propagation Queue: {solver.propagation_queue}')
    UP_label = Label(bottom_left, textvariable=UP_text)
    UP_label.pack()

    def start():
        button.configure(text="Continue")

        img.configure(image=flowchart_images[1][1])

        solution = solver.solve()

        watchy_string = ''

        for i in range(-solver.n, solver.n+1):
            if len(solver.clauses_watching[i]) != 0:
                watchy_string += f'Literal {i} is being watched by {solver.clauses_watching[i]}\n'

        watching_text.set(watchy_string)

        draw_tree(tree_canvas, solver.tree_info,
                  solver.curr_direction, 500, 400, solver.curr_child)

        decision_stack_text.set('Decision Stack: ' +
                                str(solver.decision_stack) + '\n')

        UP_text.set(f'Propagation Queue: {solver.propagation_queue}')

        if (solution == 'SAT'):
            button.pack_forget()
            img.configure(image=flowchart_images[6][1])
            Label(bottom_right, text="SAT!\nAssignment:" + str(solver.sat)).pack()
        elif (solution == 'UNSAT'):
            button.pack_forget()
            img.configure(image=flowchart_images[7][1])
            Label(bottom_right, text="UNSAT!").pack()
        elif (solution == 'image2'):
            img.configure(image=flowchart_images[1][1])
        elif (solution == 'image3'):
            img.configure(image=flowchart_images[2][1])
        elif (solution == 'image4'):
            img.configure(image=flowchart_images[3][1])
        elif (solution == 'image5'):
            img.configure(image=flowchart_images[4][1])
        elif (solution == 'image6'):
            img.configure(image=flowchart_images[5][1])

        string = ''
        ass_stack_copy = solver.assignment_stack.copy()
        ass_stack_copy.reverse()
        i = len(ass_stack_copy)-1
        for assignment in ass_stack_copy:
            assignment = assignment[1:]
            string += f'Level {i}: {assignment} \n'
            i -= 1

        text.set(string)

    control_label = Label(bottom_right, text="Controls")
    control_label.pack()

    button = Button(bottom_right, text="start", command=start)
    button.pack()

    cnf_label = Label(
        bottom_right, text=f"\n\nCNF:{solver.cnf}\n Var Ordering {solver.var_ordering}\n\n")
    cnf_label.pack()
