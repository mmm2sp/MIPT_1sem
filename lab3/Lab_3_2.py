import turtle as trt

def commands(index):
    for i in str(index):
        draw(numbers[int(i)])

def draw(params):
    trt.penup()
    for move, turn in params[0]:
        trt.left(90 * turn)
        trt.forward(A * move)
        
    trt.pendown()
    for move, turn in params[1]:
        trt.left(90 * turn)
        trt.forward(A * move)
        
    trt.penup()
    for move, turn in params[2]:
        trt.left(90 * turn)
        trt.forward(A * move)

def start_position():
    trt.speed(10)
    trt.color('blue')
    trt.penup()
    trt.goto(-300, 0)

A = 40 # Длина короткой стороны цифры
k = 0.5 #Отношение расстояния между цифрами к ширине цифры

'''index[i] - списк кортежей,состоящий из последовательности движений и поворотов
с поднятым пером, чтобы прийти в стартовое для данной цифры положение,
опущенным пером для рисования самой цифры, а затем - с поднятым, чтобы попасть
в верхний левый угол новой цифры. Движение задается в единицах А, повороты -
в единицах прямого угла. Сначала выполняется поворот, а затем уже движение
[((движения), (повороты), ((движения), (повороты)), ((движения), (повороты))]'''
numbers = [[((0, 0), (0, 0)), ((2, -1), (1, 1), (2, 1), (1, 1)), ((1+k, 2), (0, 0))], #0
         [((1, -1), (0, 0)), ((2**0.5, 1.5), (2, -1.5)), ((2, 2), (k, -1))], #1
         [((0, 0), (0, 0)), ((1, 0), (1, -1), (2**0.5, -0.5), (1, 1.5)), ((2, 1), (k, -1))], #2
         [((0, 0), (0, 0)), ((1, 0), (2**0.5, -1.5), (1, 1.5), (2**0.5, -1.5)),
          ((2, -1.5), (1+k, -1))], #3
         [((0, 0), (0, 0)), ((1, -1), (1, 1), (1, -1), (2, 2)), ((k, -1), (0, 0))], #4
         [((1, 0), (0, 0)), ((1, 2), (1, 1), (1, 1), (1, -1), (1, -1)), ((2, -1), (1+k, -1))], #5
         [((1, 0), (0, 0)), ((2**0.5, -1.5), (1, 0.5), (1, 1), (1, 1), (1, 1)), ((1, -1), (1+k, -1))], #6
         [((0, 0), (0, 0)), ((1,0), (2**0.5, -1.5), (1,0.5)), ((2, 2), (1+k, -1))], #7
         [((0, 0), (0, 0)), ((2, -1), (1, 1), (2, 1), (1, 1), (1, 1), (1, 1)), ((1, 1), (k, -1))], #8
         [((2, -1), (0, 0)), ((2**0.5, 1.5), (1, 0.5), (1, 1), (1, 1), (1, 1)), ((1, 1), (k, -1))]] #9                                                                      #8, 9

start_position()
commands(141700)
