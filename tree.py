import tkinter
from tkinter import messagebox
from tkinter import *
import math

# class Tree:
#     def __init__(self, win):
#         self.width = win.width
#         self.height = win.height
#         self.canvas = Canvas(win, 
#         width = self.width, height = self.height,bg="white")
#         self.canvas.pack()

#         self.decision_stack = decision_stack


#         self.angleFactor = math.pi/5
#         self.sizeFactor = 0.58


#size_factor = 0.58

printed = []

def get_to_print(assignment_stack, decision_stack, var_ordering):
    counter = 0
    get_to_print = []
    nums_added = []

    for index, layer in enumerate(assignment_stack):

        if counter < len(decision_stack) and layer[decision_stack[counter]] is not None and decision_stack[counter] not in nums_added:
            nums_added.append(decision_stack[counter])
            get_to_print.append((decision_stack[counter], not layer[decision_stack[counter]], " (decision)"))
            counter+=1
        for var_no, variable in enumerate(layer):
            if variable is not None:
                if var_no in decision_stack or var_no in nums_added:
                    continue
                if index == 0:
                    get_to_print.append((var_no, not variable, " (initial UP)"))
                    nums_added.append(var_no)
                else:
                    get_to_print.append((var_no, not variable, " (UP)"))
                    nums_added.append(var_no)

    # if get_to_print == []:
    #     get_to_print.append((var_ordering[0], None, " (first in var ordering)"))
    for item in var_ordering:
        # for (var_no, variable, text) in get_to_print:
        #     if item == var_no:
        #         break
        # else:
        #     get_to_print.append((item, None, " (next)"))
        #     break
        if item not in nums_added:
            get_to_print.append((item, None, " (next)"))
            break

    return(get_to_print)

def draw_line(canvas, number,x1,y1, x2, y2, is_left):
    if is_left:
        canvas.create_line(x1,y1, x2,y2, tags = "line", fill='#f11')  
        #canvas.create_text(x2, y2, font="Purisa", text=str(number))
    else:
        canvas.create_line(x1,y1, x2,y2, tags = "line", fill='#1f1')  
        
        

def display_tree(canvas, assignment_stack, decision_stack, var_ordering, width, height):
    canvas.delete("line")
    canvas.delete("var_text")
    # depth = -1
    # first = None
    # for index, var in enumerate(assignment_stack[-1]):
    #     print(var, index)
    #     if var is not None:
    #         if first is None:
    #             first = index
    #         depth += 1

    # if depth == -1:
    #     first = var_ordering[0]
    
    
    # if assignment_stack[-1][first] is None:
    #     return
    
    to_print = get_to_print(assignment_stack, decision_stack, var_ordering)
    print(to_print)
    canvas.create_text(width/2, height/10, anchor=W, font="Purisa", text=str(to_print[0][0]) + str(to_print[0][2]), tag="var_text")
    depth = len(to_print)-2

    if to_print[0][1] is True:
        paint_branch(canvas,  to_print[1:], depth, width/ 2, height/10, height/4, -math.pi/4, True)
    elif to_print[0][1] is False:
        paint_branch(canvas,  to_print[1:], depth, width/ 2, height/10, height/4, math.pi + math.pi/4, False)
    elif to_print[0][1] is None:
        paint_branch(canvas,  to_print[1:], depth, width/ 2, height/10, height/4, math.pi + math.pi/4, None)

def paint_branch(canvas, to_print, depth, x1, y1, length, angle, is_left):
    x2 = x1 + int(math.cos(angle) * length)
    y2 = y1 - int(math.sin(angle) * length)
    if is_left is not None:
        draw_line(canvas, 4, x1,y1, x2,y2, is_left)

    if depth >= 0:
        depth -= 1
        x2 = x1 + int(math.cos(angle) * length)
        y2 = y1 - int(math.sin(angle) * length)

        print(x1, x2, y1, y2)

        # Draw the line
        # if not (is_first):
        print(is_left)
        
        #else:
            
        # else:
        #     angle = angle + self.angleFactor
        # printed_copy1 = printed.copy()
        # printed_copy2 = printed.copy()
        (variable, sign, reason) = to_print[0]

        if is_left is not None:
            draw_line(canvas, 4, x1,y1, x2,y2, is_left)



        print(variable, sign, sign == True)
        canvas.create_text(x2, y2, font="Purisa", text=str(variable) + str(reason), tag="var_text")
        if sign == True:
            print('yes')
            paint_branch(canvas,  to_print[1:], depth, x2, y2, length * .75, -math.pi/4, sign)
        else:
            print('no')
            paint_branch(canvas,  to_print[1:], depth, x2, y2, length * .75, math.pi + math.pi/4 , sign)        
       
        # Draw the left branch
        
        # Draw the right branch
        


# win = Tk()


# canvas = Canvas(win, width=200, height=200)
# canvas.pack()

# display_tree(canvas, 200, 200)

# win.mainloop()