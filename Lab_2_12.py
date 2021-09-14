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
    
R_max = 50
R_min = 7
num = 50
N = 5
trt.penup()
trt.goto(-250, 0)
trt.left(90)
trt.pendown()
for i in range (N - 1):
    duga(num, R_max)
    duga(num, R_min)
duga(num, R_max)
