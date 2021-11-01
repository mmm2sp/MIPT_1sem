import pygame
import math
from random import randint
from random import random as rnd


class Figure:
    '''
    Класс фигурок
    :param typ: тип объекта: нуль соответствует снаряду, 2 -- шару, 1 -- квадрату
    :param time: время, которое сущесствует этот объект (в проходах цикла)
    :param color: кортеж, задающий цвет объекта в системе RGB
    :param x: абсцисса центра объекта
    :param y: ордината центра объекта
    :param r: радиус объекта (для квадрата -- радиус вписанной окружности)
    :param v_x: скорость объекта в пикселях/1 проход цикла по оси абсцисс
    :param v_y: скорость объекта в пикселях/1 проход цикла по оси ординат
    :param g_y: ускорение объекта в пикселях/(1 проход цикла)**2 по оси ординат
    '''
    
    def __init__(self, time, num):
        '''
        Начальные настройки класса
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: номер объекта в списке фигур
        '''
        self.typ = 0
        self.time = time
        self.color = COLORS[0]
        self.x = 0
        self.y = 0
        self.r = 0
        self.v_x = 0
        self.v_y = 0
        self.g_y = 3 * WIDTH / FPS**2
        self.num = num

    def move(self):
        '''
        Рассчитывает перемещение фигуры, заменяет пойманные на новые
        по истечении времени жизни фигуры.
        Отрисовывает все существующие фигуры
        '''
        
        self.move_count() #Расчет новых параметров объекта
        self.draw() #Отрисовка объекта

    def move_count(self):
        '''
        Отвечает за расчет новых параметров движения объекта, в том числе
        создание новых объектов по истечении времени жизини T_life
        '''

        self.time += 1
        #Создание нового объекта по истечение времени жизни старого
        if (self.time >= T_life) and (self.typ != 0):
            self.new()
        elif self.r != 0:
            self.shift() #Преобразования координат
            self.check_walls() #Отражения от стенок
            self.check_figures() #Столкновения с другими фигурами
            
    def shift(self):
        '''Преобразует координаты'''
        self.x += self.v_x
        self.y += self.v_y
        self.v_y += self.g_y
        
    def check_walls(self):
        '''Проверка столкновения со стенами'''
        if (self.x+self.r) >= WIDTH: self.v_x = -abs(self.v_x)
        if (self.x-self.r) <= 0: self.v_x = abs(self.v_x)
        if (self.y+self.r) >= HEIGHT:  self.v_y = -abs(self.v_y)
        if (self.y-self.r) <= min(SIZE)*0.12: self.v_y = abs(self.v_y)

    def check_figures(self):
        '''Проверка столкновения с фигурами. Для каждого подкласса реализовано отдельно'''
        pass
        
    def kill(self):
        '''"Обнуление" объекта при попадании в него. Начисление очков'''
        self.r = 0
        self.color = COLORS[0]
        global score
        score += self.typ

    def collision(self, delta_v):
        '''
        Перерасчет скоростей при столкновении с другими фигурами
        :param delta_v: изменение скорости (кортеж из двух проекций)
        '''
        self.v_x += delta_v[0]
        self.v_y += delta_v[1]
            
    def check_intersection(self):
        '''Убеждаемся, что созданные параметры объекта не нарушают законы природы'''

        intersection = 1
        count = 0
        while intersection > 0: #Генерим, пока не попадем в свободное место
            self.x = randint(0.1 * WIDTH, 0.9 * WIDTH)
            self.y = randint(min(SIZE)*0.12 + 0.1 * HEIGHT, 0.9 * HEIGHT)
            intersection = -1 #Разумеется, будет пересечение с самим собой
            for fig in figures:
                if fig.r != 0 and abs(self.x - fig.x) <= self.r + fig.r \
                   and abs(self.y - fig.y) <= self.r + fig.r:
                    intersection += 1
            count += 1
            if count >= 100: #Если зашкал по количеству генераций, объект не создаем
                intersection = 0
                self.r = 0
                self.color = COLORS[0]
            
class Rect(Figure):
    '''Класс квадратов, наследуемый от Figure'''
    def __init__(self, time, num):
        '''
        Начальные настройки класса
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: номер объекта в списке фигур
        '''
        super().__init__(time, num)
        self.typ = 1

    def new(self):
        '''
        "Создает" (то есть сохраняет информацию) новый квадрат
        произвольного размера в случайном месте
        '''
        self.time = 0
        self.color = COLORS[randint(2, 6)]
        
        self.r = (0.05 + 0.05*rnd())*min(SIZE)
        self.v_x = WIDTH / FPS / (5 + 8*rnd())
        self.v_y = HEIGHT / FPS / (3 + 7*rnd())
        self.g_y = 0

        self.check_intersection()
           
        
    def draw(self):   
        '''Рисует квадрат'''
        pygame.draw.rect(screen, self.color, (self.x - self.r, self.y - self.r,
                                                  2*self.r, 2*self.r))
    

    def check_figures(self):
        '''Проверка столкновения с другими фигурами'''
        for fig in figures[self.num+1::]:
            if fig.r != 0:
                delta_x = self.x - fig.x
                delta_y = self.y - fig.y
                d = self.r + fig.r
                if (abs(delta_x) <= d) and (abs(delta_y) <= d):
                    if fig.typ == 0:
                        self.kill()
                        fig.kill()
                    else: #Определяем, с какой стороны прилетел: сверху или сбоку
                        if abs(delta_x - self.v_x + fig.v_x) > d:
                            check_figures_count(self, fig, 1, 0)
                        elif abs(delta_y - self.v_y + fig.v_y) > d:
                            check_figures_count(self, fig, 0, 1)

class Ball(Figure):
    '''Класс шаров, наследуемый от Figure'''
    def __init__(self, time, num):
        '''
        Начальные настройки класса
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: номер объекта в списке фигур
        '''
        super().__init__(time, num)
        self.typ = 2

    def new(self):
        '''
        "Создает" (то есть сохраняет информацию) новый шар
        произвольного размера в случайном месте
        '''
        self.time = 0
        self.color = COLORS[randint(2, 6)]
        
        self.r = (0.02 + 0.03*rnd())*min(SIZE)
        self.v_x = WIDTH / FPS / (5 + 8*rnd())
        self.v_y = 0
        self.g_y = 3 * WIDTH / FPS**2

        self.check_intersection()

    def draw(self):
        '''Рисует круг'''
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def check_figures(self):
        '''Проверка столкновения с другими фигурами'''
        for fig in figures[self.num+1::]:
            if fig.r != 0:
                if (self.x - fig.x)**2 + (self.y - fig.y)**2 <= (self.r + fig.r)**2:
                    if fig.typ == 0:
                        self.kill()
                        fig.kill()
                    else:
                        check_figures_count(self, fig, 1, 1) #Изменение скоростей

class Bullet(Figure):
    '''Класс пуль, наследуемый от Figure'''
    def __init__(self, time, num):
        '''
        Начальные настройки класса
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: номер объекта в списке фигур
        '''
        super().__init__(time, num)
        self.typ = 0

    def new(self, x, y, v_x, v_y):
        '''
        Создание новой пули в указанном месте
        :param x: абсцисса центра пули
        :param y: ордината центра пули
        :param v_x: скорость пули в пикселях/1 проход цикла по оси абсцисс
        :param v_y: скорость пули в пикселях/1 проход цикла по оси ординат
        '''
        self.color = (0, 0, 0)
        self.r = min(SIZE) / 100
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        
    def draw(self):
        '''Рисует пулю'''
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def check_figures(self):
        '''Проверка столкновения с другими пулями'''
        for fig in figures[self.num+1::]:
            if (self.x - fig.x)**2 + (self.y - fig.y)**2 <= (self.r + fig.r)**2:
                self.kill()
                fig.kill()
        
    def kill(self):
        '''Удаление пули из списка фигур'''
        super().kill()
        if self.r == 0:
            global num_bullet, figures
            num_bullet -= 1
            figures = figures[:self.num:] + figures[self.num+1::]
            for i in range(self.num, len(figures)): #Подстраиваем нумерацию
                figures[i].num = i

class Gun:
    '''
    Класс Пушка
    :param color: кортеж, задающий цвет объекта в системе RGB
    :param width: толщина ствола пушки
    :param length: длина ствола пушки
    :param x: абсцисса центра объекта
    :param y: ордината центра объекта
    :param fire_power: мощность выстрела от 10 до 100 
    :param fire: True / False идет ли подготовка к выстрелу (нажата ли кнопка)
    :param angle: угол поворота дула от горизонтали в радианах
    :param coords: список из координат углов ствола
    '''
    def __init__(self):
        '''
        Начальные настройки класса
        '''
        self.color = COLORS[-1]
        self.width = min(SIZE) / 50
        self.length = min(SIZE) / 20
        self.x = self.width / 2
        self.y = HEIGHT / 2
        self.fire_power = 10
        self.fire = False
        self.angle = 0
        self.coords = []

    def fire_start(self, event):
        '''
        Начало подготовки к стрельбе при нажатии кнопки мыши
        :param event: обрабатываемое событие
        '''
        self.fire = True

    def fire_end(self, event):
        '''
        Выстрел мячом. Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        :param event: обрабатываемое событие
        '''
        global num_bullet, figures
        new_bullet = Bullet(0, NUM_RECTS+NUM_BALLS+num_bullet)
        num_bullet += 1
        new_bullet.new(self.x, self.y, self.fire_power * math.cos(self.angle),
                       self.fire_power * math.sin(self.angle))
        figures.append(new_bullet)
        self.fire = False
        self.fire_power = 10
        
    def targetting(self, event):
        '''
        Прицеливание. Зависит от положения мыши.
        :param event: обрабатываемое событие
        '''
        if event.pos[0] > self.x:
            self.angle = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
        else: self.angle = math.pi / 2
        
    def move(self):
        '''
        Рассчитывает перемещение пушки и рисует ее
        '''
        self.coords = turn(-self.angle, [(self.x, self.y), (self.x, self.y - self.width / 2),
                          (self.x + self.length, self.y - self.width / 2),
                          (self.x + self.length, self.y + self.width / 2),
                          (self.x, self.y + self.width / 2)])
        self.draw()
        self.power_up()
        self.length = min(SIZE) / 20 * self.fire_power**0.2

    def draw(self):
        '''
        Рисуем повернутый прямоугольник
        '''
        pygame.draw.polygon(screen, self.color, self.coords[1::])

    def power_up(self):
        '''Увеличение мощности с течением времени'''
        if self.fire:
            if self.fire_power < 100:
                self.fire_power += 1
            self.color = COLORS[1]
        else:
            self.color = COLORS[-1]
            self.fire_power = 10
            

def const_colors():
    '''
    Задаем основные цвета, используемые в программе.
    Функция возвращает список из 7 цветов:
    черный, красный, синий, желтый, зеленый, маджента, цвет морской волны
    '''
    
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    black = (0, 0, 0)
    colors = [white, red, blue, yellow, green, magenta, cyan, black]
    return colors

def turn(angle, spisok):
    '''
    Возвращает поверутый на angle радиан список относительно нулевой точки списка
    :param angle: угол, на который поворачиваем относительно нулевой точки списка
    :param spisok: исходный список. Возвращает преобразованный
    '''
    r_0 = spisok[0]
    for i in range(len(spisok)):
        x = spisok[i][0] - r_0[0]
        y = spisok[i][1] - r_0[1]
        spisok[i] = (r_0[0] + x*math.cos(angle) + y*math.sin(angle),
                     r_0[1] - x*math.sin(angle) + y*math.cos(angle))
    return spisok

def begin():
    '''Задание начальных параметров для игры'''
    global TIME, score, num_bullet, gun, figures
    
    TIME = 0 #Игра продоолжается, пока TIME < T * FPS
    score = 0 #Набранный счет
    num_bullet = 0 #Количество отрисовываемых пуль
    gun = Gun()
    figures = [] #Список объектов класса Figures

    for i in range(NUM_RECTS):
        figures.append(Rect(T_life * (i+1) / NUM_RECTS, i))
    for i in range(NUM_BALLS):
        figures.append(Ball(T_life * (i+1) / NUM_BALLS, i + NUM_RECTS))

def screen_update(score):
    '''
    Рассчитывает перемещения объектов, заменяет пойманные на новые
    по истечении времени жизни объекта.
    Отрисовывает новое изображение на экране
    :param score: набранный счет
    '''
    screen.fill(COLORS[0]) #Экран в белый
    for fig in figures:
        fig.move() #Расчет новых параметров объекта и его отрисовка
    gun.move()
    menu(score)
    pygame.display.update()

def check_figures_count(fig_1, fig_2, k_x, k_y):
    '''
    Рассчитывает столкновения с другими фигурами
    :param fig_1: фигура №1 класса Figure
    :param fig_2: фигура №2 класса Figure
    :param k_x: параметр, принимающий значение нуль или один, отвечающий за обнуление delta_v_x
    :param k_y: параметр, принимающий значение нуль или один, отвечающий за обнуление delta_v_y
    '''
    m_1 = fig_1.r**2
    m_2 = fig_2.r**2
    mu = m_1 * m_2 / (m_1 + m_2)
    v_rel_x = fig_1.v_x - fig_2.v_x
    v_rel_y = fig_1.v_y - fig_2.v_y
    delta_v_1 = (-v_rel_x * k_x * 2 * mu / m_1, -v_rel_y * k_y * 2 * mu / m_1)
    delta_v_2 = (v_rel_x * k_x * 2 * mu / m_2, v_rel_y * k_y * 2 * mu / m_2)
    fig_1.collision(delta_v_1)
    fig_2.collision(delta_v_2)

def menu(score):
    '''
    Заполняет информационное поле -- зону меню
    :param score: количество очков
    '''
    text('Score:', (min(SIZE)*0.05, min(SIZE)*0.05))
    text(str(score), (min(SIZE)*0.05 + 120, min(SIZE)*0.05))
    pygame.draw.rect(screen, (220, 220, 220), (min(SIZE)*0.05 + 200, min(SIZE)*0.045,
                                               120, min(SIZE) * 0.055))
    text('Restart', (min(SIZE)*0.05 + 200, min(SIZE)*0.05))

def text(string, coords):
    '''
    Выводит заданный текст в заданном месте экрана
    :param string: строка, которую выводим
    :param coords: кортеж координат начала строки
    '''
    text1 = pygame.font.Font(None, 48)
    text = text1.render(string, True, COLORS[-1])
    screen.blit(text, coords)

def end(score):
    '''
    Нормализация счета на Т = 100с. Запись результата в файл и вывод в консоль
    :param score: счет в данной игре
    '''
    
    fin_score = int(score * 100 / T)
    print("Игра окончена. Ваш результат:", fin_score)
    with open('Rating.txt', 'a') as file:
        file.write(str(fin_score) + ' ' + NAME + '\n')


NAME = input("Введите ваше имя:  ")
print(NAME, "добро пожаловать в игру. Ваша задача уничтожить выстрелом наибольшее число фигур.")
print("Чем дольше вы жмете на кнопку, тем больше исходная скорость снаряда.")
print("За квадратики дается по баллу, за шарики по два")
T_life = int(input("Введите желаемый период регенерации объектов (в секундах):  "))
print("Результат (счет) в игре обратно пропорционален ее продолжительности.")
T = int(input("Введите желаемую длительность игры в секундах:  "))
NUM_BALLS = 4 #Наибольшее число шаров, одновременно присутствующих на экране
NUM_RECTS = 5 #Наибольшее число квадратов, одновременно присутствующих на экране

FPS = 30
SIZE = WIDTH, HEIGHT = 700, 700 #Размер окошка
screen = pygame.display.set_mode(SIZE)
T_life *= FPS #Перерасчет времени жизни в количество проходов цикла
COLORS = const_colors()

begin() #Начальные параметры
    
pygame.init()
clock = pygame.time.Clock()
finished = False
    
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Если курсор вне зоны меню -- выстрел
            if event.pos[1] > min(SIZE)*0.12:
                gun.fire_start(event)
            #Иначе -- обработка нажатия на кнопку
            elif (event.pos[0] > min(SIZE)*0.05 + 200) and (event.pos[0] < min(SIZE)*0.05 + 320) and \
                 (event.pos[1] > min(SIZE)*0.045) and (event.pos[1] < min(SIZE)*0.1):
                end(score) #Сохранение текущего результата 
                begin() #Начало новой игры
        elif event.type == pygame.MOUSEBUTTONUP:
            if gun.fire == True: #Если начали стрелять
                gun.fire_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    screen_update(score) #Прорисовка сдвинутых объектов
    
    TIME+=1
    if TIME == T*FPS: #Завершение игры при окончании времени
        finished = True

end(score)#Сохранение результатов игры в файл и вывод в консоль
pygame.quit()
