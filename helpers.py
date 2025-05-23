import random
import turtle
import math
from turtle import *

setup(600, 600)

t = Turtle()

turtle.colormode(255)
center_thickness = 15
t.width(center_thickness)
t.speed(-1)

move_amt = 18

first_color = (253, 206, 255)
last_color = (110, 255, 249)

def get_thickness(x, y, center_amount):
    max_dist = math.dist((0, 0), (300, 300))  # ≈ 424.26
    dist = math.dist((0, 0), (x, y))
    t = 1 - dist / max_dist  # scales from 1 at center to 0 at far corner
    return 1 + (center_amount - 1) * t  # interpolates from 1 to center_amount

def get_color(x, y, first_color, last_color):
    u = (x + 300) / 600
    v = (y + 300) / 600
    t = (u + v) / 2  # blend factor
    r = int((1 - t) * first_color[0] + t * last_color[0])
    g = int((1 - t) * first_color[1] + t * last_color[1])
    b = int((1 - t) * first_color[2] + t * last_color[2])
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return (r, g, b)

def forward():
    t.forward(move_amt)

def back():
    t.left(180)
    t.forward(move_amt)

def left():
    t.left(90)
    t.forward(move_amt)

def right():
    t.right(90)
    t.forward(move_amt)

def choose_direction():
    directions = [forward, left, right, back]
    random.choice(directions)()

if __name__ == "__main__":
    for i in range(1000):
        x, y = t.pos()
        if abs(x) > 280 or abs(y) > 280:
            t.penup()
            t.goto(0,0)
            t.pendown()
            x, y = t.pos()
        t.width(get_thickness(x, y, center_thickness))
        t.color(get_color(x, y, first_color, last_color))
        choose_direction()
    turtle.done()