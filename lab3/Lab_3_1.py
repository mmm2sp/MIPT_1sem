import turtle as trt
import random as rnd

trt.speed(10)
trt.color('red')

for i in range(100):
    trt.forward(50*rnd.random())
    trt.left(360*rnd.random())
