import turtle as trt
import numpy as np
trt.shape('turtle')
trt.speed(10)

k = 10
d_phi = 1
n = 3
for phi in range (0, 3 * 360, d_phi):
    trt.forward(k * d_phi * (2 * np.pi / 360) * (1 + (phi * 2 * np.pi / 360) ** 2) ** 0.5)
    trt.left(d_phi)
