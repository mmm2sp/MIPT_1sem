import turtle as trt
import numpy as np
trt.shape('turtle')
trt.speed(10)

def duga (n, r):
    trt.right(90 / n)
    for i in range(n):
        trt.forward(2 * r * np.sin(0.5 * np.pi / n))
        trt.right(180 / n)
    trt.left(90 / n)
    
def okr (n, r):
    trt.right(90 / n)
    for i in range(n):
        trt.forward(2 * r * np.sin(np.pi / n))
        trt.left(360 / n)
    trt.left(90 / n)

num = 30

trt.left(90)
trt.penup()
trt.goto(50, 0)
trt.pendown()

trt.begin_fill()
okr(2 * num, 50)
trt.color("yellow")
trt.end_fill()
trt.color("black")

#Левый глаз
trt.penup()
trt.goto(-20, 40)
trt.left(90)
trt.pendown()

trt.begin_fill()
okr(2 * num, 10)
trt.color("blue")
trt.end_fill()
trt.color("black")

#Правый глаз
trt.penup()
trt.goto(10, 30)
trt.left(90)
trt.pendown()

trt.begin_fill()
okr(2 * num, 10)
trt.color("blue")
trt.end_fill()
trt.color("black")

#Нос
trt.penup()
trt.goto(0, 7)
trt.width(8)
trt.pendown()

trt.forward(14)

#Улыбка
trt.penup()
trt.goto(20, -10)
trt.color("red")
trt.pendown()

trt.color("red")
duga(2 * num, 20)
