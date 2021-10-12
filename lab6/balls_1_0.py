import pygame
import pygame.draw as dr
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

def new_ball():
    '''
    "Создает" (то есть сохраняет информацию) новый шарик произвольного размера в случайном месте
    Возвращает цвет, координаты, радиус шарика, компоненты
    его скорости по х и у и время, которое шар уже существует (нуль)
    '''
    
    color = COLORS[randint(1, 6)]
    x = randint(0.1 * WIDTH, 0.9 * WIDTH)
    y = randint(0.1 * HEIGHT, 0.9 * HEIGHT)
    r = randint(0.02 * min(SIZE), 0.1 * min(SIZE))
    v_x = WIDTH / randint(2, 10) / FPS
    v_y = HEIGHT / randint(2, 10) / FPS
    return [color, x, y, r, v_x, v_y, 0]

def ball(color, x, y, r):
    '''
    Рисует шарик
    :param color: цвет шара по системе RGB
    :param x: абсцисса центра шара
    :param y: ордината центра шара
    :param r: радиус шара
    '''
    
    dr.circle(screen, color, (x, y), r)
    

def move():
    '''
    Рассчитывает перемещения шаров, заменяет пойманные на новые
    по истечении времени жизни шара.
    Отрисовывает все существующие шары
    Возвращает измененный список информации про все шары
    '''

    screen.fill(COLORS[0]) #Экран в черный
    for i in range(len(balls)):
        color, x, y, r, v_x, v_y, t = balls[i]
        
        #Преобразования координат
        x += v_x
        y += v_y
        t += 1
        
        #Отражения от стенок
        if ((x+r) >= WIDTH) or (x-r <= 0):
            v_x = -v_x
        if ((y+r) >= HEIGHT) or (y-r <= 0):
            v_y = -v_y
            
        #Создание нового шара по истечение времени жизни старого, если его поймали
        if (t >= T_life) and (r == 0):
            balls[i] = new_ball();
        else:
            balls[i] = [color, x, y, r, v_x, v_y, t]
            
        #Отрисовка i-го шара
        ball(color, x, y, r)
        
    pygame.display.update()
    return balls

def button_down(pos_mouse):
    '''
    Обрабатывает нажатие левой кнопки мыши
    :param pos_mouse: кортеж из двух координат положения мыши
    :param balls: список списков "координат" для каждого шара
    '''
    k = 0
    for i in range(len(balls)):
        x, y, r = balls[i][1:4:]
        if ((pos_mouse[0]-x) ** 2 + (pos_mouse[1]-y) ** 2) < r ** 2: #Если попали в шар
            balls[i][0] = COLORS[0] #Цвет шара черный
            balls[i][3] = 0 #Радиус шара нулевой
            k += 1
    return balls, k

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
print(NAME, "добро пожаловать в игру. ")
T_life = int(input("Введите желаемый период регенерации шара (в секундах):  "))
print("Результат (счет) в игре обратно пропорционален ее продолжительности")
T = int(input("Введите желаемую длительность игры в секундах:  "))
NUMBER_OF_BALLS = 5 #Число шаров, одновременно присутствующих на экране

FPS = 30
SIZE = WIDTH, HEIGHT = 500, 500 #Размер окошка
screen = pygame.display.set_mode(SIZE)
T_life *= FPS #Перерасчет времени жизни в количество проходов цикла
COLORS = const_colors()
TIME = 0 #Игра продоолжается, пока TIME < T * FPS
score = 0 #Переменная отвечает за количество пойманных шариков
balls = []
#Список списков из абсциссы, ординаты, радиуса шарика, его цвета,
#двух проекций скорости v_x, v_y и времени жизни

pygame.init()
clock = pygame.time.Clock()
finished = False


'''Первичное заполнение информации о шарах'''
coord = new_ball()#Создаем новый шар
balls.append(coord)
for i in range(NUMBER_OF_BALLS - 1):
    balls.append([COLORS[0], 0, 0, 0, 0, 0, 0]) #Остальных шаров пока нет

'''Основной цикл'''
while not finished:
    clock.tick(FPS)

    '''Создание оставшихся шаров через равные промежутки времени'''
    if TIME <= T_life :
        j = min(TIME // (T_life // NUMBER_OF_BALLS), NUMBER_OF_BALLS - 1)
        if balls[j][3] == 0:
            balls[j] = new_ball()
            
    '''Обработка событий'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        #Обработка нажатия на левую кнопку мыши
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            balls, delt = button_down(event.pos)
            score += delt
       
    balls = move() #Прорисовка сдвинутых шаров
    TIME+=1
    if TIME == T*FPS: #Завершение игры при окончании времени
        finished = True

end(score)#Сохранение результатов игры в файл и вывод в консоль
pygame.quit()
