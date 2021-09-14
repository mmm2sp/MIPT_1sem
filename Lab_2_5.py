import turtle as trt
trt.shape('turtle')

N = 4
num = 10
for l in range (10, 10 * num + 1, 10):
    trt.penup()
    trt.goto(- l / 2, - l / 2)
    trt.pendown()
    for i in range (N):
        trt.forward(l)
        trt.left(360 / N)
