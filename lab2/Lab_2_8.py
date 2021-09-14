import turtle as trt
import numpy as np
trt.shape('turtle')
trt.speed(10)

delt = 5
n = 7
for a in range (delt, n * 4 * delt + 1, delt):
    trt.forward(a)
    trt.left(90)
