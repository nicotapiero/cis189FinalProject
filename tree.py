import tkinter
from tkinter import messagebox
from tkinter import *
import math
from iterative_pennSAT import Node


def draw_line(canvas, number, x1, y1, x2, y2, is_left):
    if is_left:
        canvas.create_line(x1, y1, x2, y2, tags="line", fill='#f11')
    else:
        canvas.create_line(x1, y1, x2, y2, tags="line", fill='#1f1')


def draw_branch(canvas, node, x1, y1, length, curr_direction, curr_leaf):
    x2_right = x1 + int(math.cos(- math.pi / 3) * length)
    y2_right = y1 - int(math.sin(- math.pi / 3) * length)

    x2_left = x1 + int(math.cos(math.pi + math.pi/3) * length)
    y2_left = y1 - int(math.sin(math.pi + math.pi/3) * length)

    if node is None:
        return

    if node.text == 'CONFLICT':
        canvas.create_text(x1, y1, font="Purisa",
                           text=str(node.text), tag="var_text")
        return

    canvas.create_text(x1, y1, font="Purisa", text=str(
        node.decision_var) + " " + str(node.text), tag="var_text")

    if node == curr_leaf:
        if curr_direction == 'Right':
            draw_line(canvas, 4, x1, y1, x2_right, y2_right, True)
        elif curr_direction == 'Left':
            draw_line(canvas, 4, x1, y1, x2_left, y2_left, False)

    if node.left is not None:
        if node.left.text == 'CONFLICT':
            canvas.create_line(x1, y1, x1, y1+length,
                               tags="line", fill='purple')
        else:
            draw_line(canvas, 4, x1, y1, x2_left, y2_left, False)
    draw_branch(canvas, node.left, x2_left, y2_left,
                length, curr_direction, curr_leaf)
    if node.right is not None:
        if node.right.text == 'CONFLICT':
            canvas.create_line(x1, y1, x1, y1+length,
                               tags="line", fill='purple')
        else:
            draw_line(canvas, 4, x1, y1, x2_right, y2_right, True)
    draw_branch(canvas, node.right, x2_right, y2_right,
                length, curr_direction, curr_leaf)


def draw_tree(canvas, tree_info, curr_direction, width, height, curr_leaf):
    root = tree_info.left
    canvas.delete("line")
    canvas.delete("var_text")
    draw_branch(canvas, root, width/2, height/10,
                height/9, curr_direction, curr_leaf)
