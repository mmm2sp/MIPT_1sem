import turtle as trt
import random as rnd

def start():
    trt.speed(100)
    trt.penup()
    trt.goto(-0.5 * length, -0.5 * length)
    trt.pendown()
    trt.goto(-0.5 * length, 0.5 * length)
    trt.goto(0.5 * length, 0.5 * length)
    trt.goto(0.5 * length, -0.5 * length)
    trt.goto(-0.5 * length, -0.5 * length)
    trt.penup()
    trt.goto(0, 0)
    trt.ht()

number_of_turtles = 20
steps_of_time_number = 500
length = 390
step = 2

start()

pool = [trt.Turtle(shape='circle') for i in range(number_of_turtles)]
for unit in pool:
    unit.penup()
    unit.speed(0)
    unit.goto(rnd.randint(-0.5 * length, 0.5 * length), rnd.randint(-0.5 * length, 0.5 * length))
    unit.left(rnd.randint(-180, 180))
    unit.turtlesize(0.3)


for i in range(steps_of_time_number):
    for unit in pool:
        pos = unit.position()
        angle = unit.heading()
        if(pos[0] > length*0.5) and (angle < 90 and angle > 0 or angle > 270 and angle < 360):
            unit.setheading(180 - 2*angle)
        if(pos[0] < -length*0.5) and (angle > 90 and angle < 270):
            unit.setheading(180 - 2*angle)
        if(pos[1] > length*0.5) and (angle > 0 and angle < 180):
            unit.setheading(360 - angle)
        if(pos[1] < -length*0.5) and (angle > 180 and angle < 360):
            unit.setheading(360 - angle)
        unit.forward(step)
