import tkinter
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk

from iterative_pennSAT import IterativePennSAT

from tree import display_tree


# https://stackoverflow.com/questions/46522200/how-to-make-two-split-up-screen-canvas-inside-the-python-tkinter-window

#for

flowchart_images = []


def create_images():
    load = Image.open("flowchart copy.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchart2.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchart3.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchart4.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchart5.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchart6.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchartSAT.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))
    load = Image.open("flowchartUNSAT.jpg")
    render = ImageTk.PhotoImage(load)
    flowchart_images.append((load,render))

# load = Image.open("download.png")
# render = ImageTk.PhotoImage(load)




def solver_phase(max, cnf, win):
    # win.grid_rowconfigure(1, weight=1)
    # win.grid_columnconfigure(1, weight=1)
    create_images()

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
    top_right.grid(row=0, column=2)

    top_middle = Frame(win, width=500, height=150, background="blue")
    top_middle.grid(row=0, column=1)
    bottom_middle = Frame(win, width=500, height=150, background="blue")
    bottom_middle.grid(row=1, column=1)

    bottom_left = Frame(win, width=500, height=150, background="green")
    bottom_left.grid(row=1, column=0)
    bottom_right = Frame(win, width=500, height=150, background="yellow")
    bottom_right.grid(row=1, column=2)
    # #
    # # # top_left
    # # # top_right
    # # # bottom_left
    # # # bottom_right
    # #
    
    #
    #
    print(max, cnf)
    solver = IterativePennSAT(max, cnf, True)



    # label.pack()

    ass_stack_label = Label(top_left, text="Assignment Stack Stuff")
    ass_stack_label.pack()

    text = StringVar()
    text.set('Level 0: ' + str(solver.assignment_stack[1:]) + '\n')
    label = Label(top_left,textvariable=text)
    label.pack()

    tree_label = Label(bottom_left, text="Tree Stuff")
    tree_label.pack()
    


    decision_stack_text = StringVar()
    decision_stack_text.set('Decision Stack: ' + str(solver.decision_stack) + '\n')
    decisions_label = Label(bottom_left,textvariable=decision_stack_text)
    decisions_label.pack()

    tree_canvas = Canvas(bottom_left, width = 200, height = 200,bg="white")
    tree_canvas.pack()

    


    cnf_label = Label(bottom_middle, text=f"CNF:{solver.cnf}\n Var Ordering {solver.var_ordering}")
    cnf_label.pack()


    flowchart_label = Label(top_right, text="Flowchart")
    flowchart_label.pack()


    # image = Image.open("brian.png")
    # image_Pack = Label(bottom_left, image = image)
    # image_Pack.pack()


    img = Label(top_right, image=flowchart_images[0][1])
    # img.image = render
    img.pack()

    # canvas = Canvas(bottom_left, width = 1600, height = 250)
    #
    #
    # canvas.pack(fill = BOTH, expand = True)
    # photo = PhotoImage(file = 'tenor.gif')
    # canvas.create_image(55, 55, image=photo)

    # photo = PhotoImage('logo192.pbm')
    # l = Label(bottom_left, text="hoho", image=photo)
    # #l.image = photo
    # l.pack()
    watching_text = StringVar()
    # watchy_string = ''
    # i = 1
    # for clauses_list in solver.clauses_watching:
    #     string += f''
    watching_text.set(f'Im watching {solver.clauses_watching[0]}')
    watching_label = Label(top_middle,textvariable=watching_text)
    watching_label.pack()

    UP_text = StringVar()
    UP_text.set(f'Propagation Queue: {solver.propagation_queue}')
    UP_label = Label(top_middle,textvariable=UP_text)
    UP_label.pack()


    # load = Image.open("brian.png")
    # load.resize((50, 50), Image.ANTIALIAS)
    # render = ImageTk.PhotoImage(load)
    # img = Label(bottom_left, image=render)
    # img.image = render
    # img.pack()

    # ass_stack = Label()
    # ass_stack["text"] = solver.assignment_stack
    # ass_stack.pack()

    def start():
        button.configure(text = "Continue")


        img.configure(image=flowchart_images[1][1])
        # img.image = flowchart_images[1][1]

        solution = solver.solve()

        print('watchy', solver.clauses_watching)
        watching_text.set(f'Im watching {solver.clauses_watching[0]}')

        display_tree(tree_canvas, solver.assignment_stack, solver.decision_stack, solver.var_ordering, 200, 200)

        decision_stack_text.set('Decision Stack: ' + str(solver.decision_stack) + '\n')

        UP_text.set(f'Propagation Queue: {solver.propagation_queue}')

        print('FUK', f'switch: {solver.switch}, in_loop:{solver.in_loop}, next:{solver.next}, check_l0 {solver.check_level_0}, all_set {solver.check_all_set}, unit {solver.check_unit_prop}')
        print('--------------\n', solution, '--------------\n')

        if (solution == 'SAT'):
            button.pack_forget()
            img.configure(image=flowchart_images[6][1])
            Label(bottom_right, text="SAT!").pack()
            #Button(bottom_right, text="exit", command=).pack()
        elif (solution == 'UNSAT'):
            button.pack_forget()
            img.configure(image=flowchart_images[7][1])
            Label(bottom_right, text="UNSAT!").pack()
            #Button(bottom_right, text="exit", command=win.destroy()).pack()
        # elif (solution == 'checked for 0'):
        #     img.configure(image=flowchart_images[5][1])
        # elif (solver.next == 3 and solver.in_loop == 3 and solver.switch == 1 and not solver.check_unit_prop):
        #     img.configure(image=flowchart_images[3][1])
        # elif (solver.next == 3 and solver.in_loop == 3 and solver.switch == -1 and not solver.check_level_0):
        #     print('really ninja')
        #     img.configure(image=flowchart_images[4][1])
        # elif (solver.check_all_set):
        #     img.configure(image=flowchart_images[1][1])
        # elif (solution is None and solver.next == 3 and solver.in_loop == 1 and solver.switch == -1 and solver.check_all_set):
        #     img.configure(image=flowchart_images[1][1])
        # elif (solution is None and solver.next == 3 and solver.in_loop == 1 and solver.switch == 1 ):
        #     img.configure(image=flowchart_images[2][1])
        # elif (solver.next == 3 and solver.in_loop == 1 and solver.switch == 1):
        #     img.configure(image=flowchart_images[5][1])
        # elif (solver.next == 3 and solver.in_loop == 2):
        #     img.configure(image=flowchart_images[4][1])
        #
        # elif (solver.next == 3 and solver.in_loop == 3 and solver.check_unit_prop):
        #     img.configure(image=flowchart_images[4][1])

        # elif (solution == 'image2'):
        #     img.configure(image=flowchart_images[1][1])
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
        # elif (solution == 'image5'):
        #     img.configure(image=flowchart_images[5][1])
        # elif (solution == 'image6'):
        #     img.configure(image=flowchart_images[5][1])

        # elif (solution == 'checked for 0'):
        #     img.configure(image=flowchart_images[5][1])
        # elif (solution == 'checked for 0'):
        #     img.configure(image=flowchart_images[5][1])

        print('wh')
        print(str(solver.assignment_stack))
       # text.set('FUCK')

        string = ''
        ass_stack_copy = solver.assignment_stack.copy()
        ass_stack_copy.reverse()
        i= len(ass_stack_copy)-1
        for assignment in ass_stack_copy:
            assignment = assignment[1:]
            string += f'Level {i}: {assignment} \n'
            i-=1

        print(string)
        text.set(string)

    control_label = Label(bottom_right, text="Controls")
    control_label.pack()
    button = Button(bottom_right, text="start", command=start)
    button.pack()


