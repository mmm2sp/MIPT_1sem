import turtle as trt
trt.shape('turtle')

n = 12
l = 50
for i in range (n):
    trt.forward(l)
    trt.stamp()
    trt.left(180)
    trt.forward(l)
    trt.left(180 + 360 / n)
