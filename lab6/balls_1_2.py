import pygame
from random import randint

def const_colors():
    '''
    Задаем основные цвета, используемые в программе.
    Функция возвращает список из 7 цветов:
    черный, красный, синий, желтый, зеленый, маджента, цвет морской волны
    '''
    
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    colors = [black, red, blue, yellow, green, magenta, cyan]
    return colors

def new_obj(typ):
    '''
    "Создает" (то есть сохраняет информацию) новый объект произвольного размера в случайном месте
    Возвращает цвет, координаты, радиус объекта, компоненты
    его скорости по х и у и время, которое объект уже существует (нуль)
    '''
    
    color = COLORS[randint(1, 6)]
    x = randint(0.1 * WIDTH, 0.9 * WIDTH)
    y = randint(0.1 * HEIGHT, 0.9 * HEIGHT)
    
    if typ == 0: #Для шара
        r = randint(0.02 * min(SIZE), 0.05 * min(SIZE))
        v_x = WIDTH / randint(4, 10) / FPS
        v_y = 0
        g_y = 0.7
        
    else: #Для квадрата
        r = randint(0.05 * min(SIZE), 0.1 * min(SIZE)) #Полусторона
        v_x = WIDTH / randint(2, 7) / FPS
        v_y = HEIGHT / randint(1, 4) / FPS
        g_y = 0
        
    return [color, x, y, r, v_x, v_y, g_y, 0, typ]



def obj(params):
    '''
    Рисует объект
    :param params: параметры объекта (цвет, координаты x и y, радиус (или полуширина),
    компоненты его скорости по х и у и время, которое шар уже существует)
    '''
    
    color, x, y, r = params[:4:]
    typ = params[-1]
    if typ == 0:
        pygame.draw.circle(screen, color, (x, y), r)
    else:
        pygame.draw.rect(screen, color, (x - r, y - r, 2*r, 2*r))                         


def move_count(params):
    '''
    Отвечает за расчет новых параметров движения объекта, в том числе
    создание новых шаров по истечении времени жизини T_life
    :param params: параметры объекта (цвет, координаты x и y, радиус,
    компоненты его скорости по х и у и время, которое шар уже существует)
    Возвращает преобразованные параметры объекта
    '''

    color, x, y, r, v_x, v_y, g_y, t, typ = params #Распаковка параметров
    
    #Создание нового объекта по истечение времени жизни старого, если его поймали
    if (t >= T_life) and (r == 0):
        params = new_obj(typ)
    else:
        #Преобразования координат
        x += v_x
        y += v_y
        v_y += g_y
        t += 1
            
        #Отражения от стенок
        if (x+r) >= WIDTH: v_x = -abs(v_x)
        if (x-r <= 0): v_x = abs(v_x)
        if (y+r) >= HEIGHT:  v_y = -abs(v_y)
        if (y-r <= 0):  v_y = abs(v_y)
            
        params = [color, x, y, r, v_x, v_y, g_y, t, typ]
       
    return params

def move():
    '''
    Рассчитывает перемещения объектов, заменяет пойманные на новые
    по истечении времени жизни объекта.
    Отрисовывает все существующие объекты
    Возвращает измененный список информации про все объекты
    '''
    
    screen.fill(COLORS[0]) #Экран в черный
    
    for i in range(NUM_BALLS + NUM_RECTS): # Для каждого объекта
        objs[i] = move_count(objs[i]) #Расчет новых параметров объекта
        obj(objs[i]) #Отрисовка i-го объекта
        
    pygame.display.update()
    return objs

def button_down(pos_mouse, button):
    '''
    Обрабатывает нажатие кнопки мыши
    :param pos_mouse: кортеж из двух координат положения мыши
    :param button: номер кнопки мыши
    Возвращает обновленную информацию об объектах и количество набранных баллов
    '''
    
    points = 0
    for i in range(NUM_BALLS):
        x, y, r = objs[i][1:4:]
        if (button == 1) and (((pos_mouse[0] - x)**2 + (pos_mouse[1] - y)**2) < r**2): #Если попали в шар левой кнопкой
            objs[i][0] = COLORS[0] #Цвет шара черный
            objs[i][3] = 0 #Радиус шара нулевой
            points += 2
            
    for i in range(NUM_BALLS, NUM_BALLS + NUM_RECTS):
        x, y, a_2 = objs[i][1:4:]
        if (button == 3) and (abs(pos_mouse[0] - x) < a_2) and (abs(pos_mouse[1] - y) < a_2): #Если попали в квадрат правой кнопкой
            objs[i][0] = COLORS[0] #Цвет квадрата черный
            objs[i][3] = 0 #Полусторона квадрата нулевая
            points += 1
            
    return objs, points

def end(score):
    '''
    Нормализация счета на Т = 100с. Запись результата в файл и вывод в консоль
    :param score: счет в данной игре
    '''
    fin_score = int(score * 100 / T)
    print("Время вышло. Ваш результат:", fin_score)
    with open('Rating.txt', 'a') as file:
        file.write(str(fin_score) + ' ' + NAME + '\n')


NAME = input("Введите ваше имя:  ")
print(NAME, "добро пожаловать в игру. Ваша задача нажать на наибольшее число фигур.")
print("На круги нужно нажимать левой кнопкой мыши, за них дается по два баллу.")
print("На квадраты -- правой, за них дается по одному баллу.")
T_life = int(input("Введите желаемый период регенерации объектов (в секундах):  "))
print("Результат (счет) в игре обратно пропорционален ее продолжительности.")
T = int(input("Введите желаемую длительность игры в секундах:  "))
NUM_BALLS = 5 #Наибольшее число шаров, одновременно присутствующих на экране
NUM_RECTS = 3 #Наибольшее число квадратов, одновременно присутствующих на экране

FPS = 30
SIZE = WIDTH, HEIGHT = 500, 500 #Размер окошка
screen = pygame.display.set_mode(SIZE)
T_life *= FPS #Перерасчет времени жизни в количество проходов цикла
COLORS = const_colors()
TIME = 0 #Игра продоолжается, пока TIME < T * FPS
score = 0 #Набранный счет
objs = []
'''
objs -- список списков, описывающих объект. objs[i] = [color, x, y, r, v_x, v_y, g_y, t, typ]
:param color: кортеж, задающий цвет объекта в системе RGB
:param x: абсцисса центра объекта
:param y: ордината центра объекта
:param r: радиус объекта (для квадрата -- радиус вписанной окружности)
:param v_x: скорость объекта в пикселях/1 проход цикла по оси абсцисс
:param v_y: скорость объекта в пикселях/1 проход цикла по оси ординат
:param g_y: ускорение объекта в пикселях/(1 проход цикла)**2 по оси ординат
:param t: время, которое сущесствует этот объект (в проходах цикла)
:param typ: тип объекта: нуль соответствует шару, 1 -- квадрату
'''

for i in range(NUM_BALLS):
    objs.append([COLORS[0], 0, 0, 0, 0, 0, 0, T_life * (i+1) / NUM_BALLS, 0])
for i in range(NUM_RECTS):
    objs.append([COLORS[0], 0, 0, 0, 0, 0, 0, T_life * (i+1) / NUM_BALLS, 1])

    
pygame.init()
clock = pygame.time.Clock()
finished = False
    
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            objs, delt = button_down(event.pos, event.button)
            score += delt

    objs = move() #Прорисовка сдвинутых объектов
    
    TIME+=1
    if TIME == T*FPS: #Завершение игры при окончании времени
        finished = True

end(score)#Сохранение результатов игры в файл и вывод в консоль
pygame.quit()
