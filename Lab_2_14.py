import turtle as trt
import numpy as np
trt.shape('turtle')
trt.speed(10)

N = 11
R = 100
trt.penup()
trt.left(90 - 360 / N)
trt.forward(R)
trt.left(180 - 90 / N)
trt.pendown()
for i in range(N):
    trt.forward(2 * R * np.cos(0.5 * np.pi / N))
    trt.left(180 - 180 / N)
