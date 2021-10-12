import pygame
import pygame.draw as dr
from random import randint
pygame.init()

FPS = 30
SIZE = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(SIZE)

def const_colors():
    '''
    Задаем основные цвета, используемые в программе.
    Функция возвращает список из 7 цветов:
    красного, синего, желтого, зеленого, маджента, цвет морской волны, черный
    '''
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    black = (0, 0, 0)
    colors = [black, red, blue, yellow, green, magenta, cyan]
    return colors

def new_ball():
    '''
    Рисует новый шарик произвольного размера в случайном месте
    Возвращает координаты и радиус шарика
    '''
    x = randint(0.1 * WIDTH, 0.9 * WIDTH)
    y = randint(0.1 * HEIGHT, 0.9 * HEIGHT)
    r = randint(0.02 * min(SIZE), 0.1 * min(SIZE))
    color = COLORS[randint(1, 6)]
    ball(x, y, r, color)
    return (x, y, r, color)

def ball(x, y, r, color):
    '''
    Рисует шарик
    :param x: абсцисса центра шара
    :param y: ордината центра шара
    :param r: радиус шара
    :param color: цвет шара по системе RGB
    '''
    dr.circle(screen, color, (x, y), r)
    

def move(coords, speed):
    '''
    Перемещает шарик
    '''
    x, y, r, color = coords
    v_x, v_y = speed

    x += v_x
    y += v_y
    ball(x, y, r, color)

    if ((x+r) >= WIDTH) or (x-r <= 0):
        v_x = -v_x
    if ((y+r) >= HEIGHT) or (y-r <= 0):
        v_y = -v_y
        
    return [x, y, r, color], [v_x, v_y]

def button_down(pos_mouse, ball):
    '''
    Обрабатывает нажатие левой кнопки мыши
    :param pos_mouse: кортеж из двух координат положения мыши
    :param ball: список из абсциссыб ординаты и радиуса шарика
    '''
    k = 0
    if ((pos_mouse[0]-ball[0]) ** 2 + (pos_mouse[1]-ball[1]) ** 2) <= ball[2] ** 2:
        k = 1
    return k
    
COLORS = const_colors()
NUM = 0.1 #Число генерируемых шариков в секунду
T = 30 #Длительность игры в секундахs
TIME = 0 #Игра продоолжается, пока TIME < T * FPS

clock = pygame.time.Clock()
finished = False
counter = 0 #Создаем счетчик, чтобы создавать шарик не при каждом обновлении экрана
coords = [0, 0, 0, (0, 0, 0)] #Список из абсциссы, ординаты, радиуса шарика и его цвета
score = 0 #Переменная отвечает за количество пойманных шариков
speed = [0.1 * WIDTH / FPS, 0.1 * HEIGHT / FPS] #смещение за 1/FPS секунды

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            score += button_down(event.pos, coords)
            counter = 0
            print(score)
            
    if counter == 0:
        coords = new_ball()
       
    screen.fill(COLORS[0])
    coords, speed = move(coords, speed)

    pygame.display.update()
    
    
    counter+=1 #Прошел 1 тик
    if counter > (FPS // NUM): #Если тиков достаточно -- обнуляем счетчик.
        counter = 0 #В следующий раз появится шарик)
    TIME+=1
    if TIME == T*FPS:
        finished = True

pygame.quit()
