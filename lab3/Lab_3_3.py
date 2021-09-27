import turtle as trt

def imp(s):
    with open(s, 'r') as num:
        numbers = num.readlines()
    for i in range(len(numbers)):
        numbers[i] = numbers[i][0: len(numbers[i])-1:1]
        numbers[i] = numbers[i].split('; ')
        for j in range(len(numbers[i])):
            numbers[i][j] = numbers[i][j].split(', ')
            for h in range(len(numbers[i][j])):
                numbers[i][j][h] = numbers[i][j][h].split(' ')
    return numbers

def commands(index):
    for i in str(index):
        draw(numbers[int(i)])

def draw(params):
    trt.penup()
    for move, turn in params[0]:
        trt.left(90 * eval(turn))
        trt.forward(A * eval(move))
        
    trt.pendown()
    for move, turn in params[1]:
        trt.left(90 * eval(turn))
        trt.forward(A * eval(move))
        
    trt.penup()
    for move, turn in params[2]:
        trt.left(90 * eval(turn))
        trt.forward(A * eval(move))

def start_position():
    trt.speed(10)
    trt.color('blue')
    trt.penup()
    trt.goto(-300, 0)

A = 40 # Длина короткой стороны цифры
k = 0.5 #Отношение расстояния между цифрами к ширине цифры
name = 'Num.txt' #Имя файла со шрифтом

numbers = imp(name)
start_position()
commands(1234567890)
