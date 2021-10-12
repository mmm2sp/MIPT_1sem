import pygame
import pygame.draw as dr
from random import randint

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
    
    color = COLORS[randint(1, 6)]
    x = randint(0.1 * WIDTH, 0.9 * WIDTH)
    y = randint(0.1 * HEIGHT, 0.9 * HEIGHT)
    r = randint(0.02 * min(SIZE), 0.1 * min(SIZE))
    v_x = WIDTH / randint(2, 10) / FPS
    v_y = HEIGHT / randint(2, 10) / FPS
    
    ball(color, x, y, r)
    
    return (color, x, y, r, v_x, v_y)

def ball(color, x, y, r):
    '''
    Рисует шарик
    :param color: цвет шара по системе RGB
    :param x: абсцисса центра шара
    :param y: ордината центра шара
    :param r: радиус шара
    '''
    
    dr.circle(screen, color, (x, y), r)
    

def move(coords):
    '''
    Перемещает шарик
    :param coords: список из цвета, абсциссы, ординаты, радиуса шара
    и его скоростей по х и у
    '''
    
    color, x, y, r, v_x, v_y = coords
    
    x += v_x
    y += v_y
    if ((x+r) >= WIDTH) or (x-r <= 0):
        v_x = -v_x
    if ((y+r) >= HEIGHT) or (y-r <= 0):
        v_y = -v_y

    ball(color, x, y, r)
    return [color, x, y, r, v_x, v_y]

def button_down(pos_mouse, ball):
    '''
    Обрабатывает нажатие левой кнопки мыши
    :param pos_mouse: кортеж из двух координат положения мыши
    :param ball: список из абсциссы, ординаты и радиуса шарика
    '''
    k = 0
    if ((pos_mouse[0]-ball[0]) ** 2 + (pos_mouse[1]-ball[1]) ** 2) <= ball[2] ** 2:
        k = 1
    return k


pygame.init()

NAME = input("Введите ваше имя:  ")
print(NAME, "добро пожаловать в игру. ")
NUM = float(input("Введите желаемое количество шариков в секунду:  "))
print("Результат (счет) в игре обратно пропорционален ее продолжительности")
T = int(input("Введите желаемую длительность игры в секундах:  "))

FPS = 30
SIZE = WIDTH, HEIGHT = 500, 500 #Размер окошка
screen = pygame.display.set_mode(SIZE)
    
COLORS = const_colors()

clock = pygame.time.Clock()
finished = False
TIME = 0 #Игра продоолжается, пока TIME < T * FPS
counter = 0 #Создаем счетчик, чтобы создавать шарик не при каждом обновлении экрана
coords = [(0, 0, 0), 0, 0, 0, 0, 0] #Список из абсциссы, ординаты, радиуса шарика и его цвета
score = 0 #Переменная отвечает за количество пойманных шариков

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        #Обработка нажатия на левую кнопку мыши
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            score += button_down(event.pos, coords[1:4:])
            counter = 0
            
    if counter == 0:# Создаем новый шарик, если старый уже давно бегает
        coords = new_ball()
       
    screen.fill(COLORS[0]) #Экран в черный
    coords = move(coords) #Прорисовка сдвинутого шара
    pygame.display.update()
    
    counter+=1 #Прошел 1 тик
    if counter > (FPS // NUM): #Если тиков достаточно -- обнуляем счетчик.
        counter = 0 #В следующий раз появится шарик)
        
    TIME+=1
    if TIME == T*FPS: #Завершение игры при окончании времени
        finished = True
        
score = int(score * 100 / T) #Нормализация счета. Далее -- запись в файл
with open('output.txt', 'a') as file:
    st = str(score) + ' ' + NAME + '\n'
    file.write(str(score) + ' ' + NAME + '\n')
pygame.quit()
