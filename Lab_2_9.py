import turtle as trt
import numpy as np
trt.shape('turtle')
trt.speed(10)

def n_ug (n, r):
    trt.left(180 / n)
    for i in range(n):
        trt.forward(2 * r * np.sin(np.pi / n))
        trt.left(360 / n)
    trt.right(180 / n)
    

N = 10
delt = 5
trt.penup()
trt.forward(delt * (1 + 2 / 6) * 2)
trt.left(90)
for m in range (3, N + 4, 1):
    trt.penup()
    trt.right(90)
    trt.forward(delt * (1 + m / 6) * m - delt * (1 + (m - 1)/ 6) * (m - 1))
    trt.left(90)
    trt.pendown()
    n_ug(m, delt * (1 + m / 6) * m)
