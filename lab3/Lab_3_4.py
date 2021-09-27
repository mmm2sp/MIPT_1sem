import turtle as trt

def start_position():
    trt.speed(10)
    trt.penup()
    trt.goto(x, y)
    trt.pendown()
    trt.goto(-x, y)
    trt.goto(x, y)
    trt.shape('circle')
    trt.color('blue')

dt = 0.02 # Промежуток времени
k = 0.8 #Коэффициент отражения
#  Далее -- начальные параметры
v_x = 20.0
v_y = 40.0
a_y = -10.0
x = -300.0
y = 0.0

start_position()
for i in range(2000):
    x += v_x*dt
    y += v_y*dt + a_y*dt**2/2
    v_y += a_y*dt
    if y <= 0 and v_y < 0:
        v_y = -k*v_y
        v_x = k*v_x
    trt.goto(x,y)
    
