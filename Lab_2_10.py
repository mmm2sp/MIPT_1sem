import turtle as trt
import numpy as np
trt.shape('turtle')
trt.speed(10)

def okr (n, r, k):
    for i in range(n):
        trt.forward(2 * r * np.sin(np.pi / n))
        trt.left(k * 360 / n)
    
R = 50
num = 100
N = 3
for i in range (N):
    okr(num, R, 1)
    okr(num, R, -1)
    trt.left(180 / N)
