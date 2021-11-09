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
        
        self.draw() #Отрисовка объекта
        self.move_count() #Расчет новых параметров объекта
        
    def move_count(self):
        '''
        Отвечает за расчет новых параметров движения объекта, в том числе
        создание новых объектов по истечении времени жизини T_life
        '''

        self.time += 1
        #Создание нового объекта по истечение времени жизни старого
        if (self.time >= T_life) and (self.typ >= 0):
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
        '''"Обнуление" объекта при попадании в него'''
        self.r = 0
        self.color = COLORS[-1]

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
                self.color = COLORS[-1]
            
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
                    if fig.typ <= 0:
                        self.kill(fig.typ)
                        fig.kill(fig.typ)
                    else: #Определяем, с какой стороны прилетел: сверху или сбоку
                        if abs(delta_x - self.v_x + fig.v_x) > d:
                            check_figures_count(self, fig, 1, 0)
                        elif abs(delta_y - self.v_y + fig.v_y) > d:
                            check_figures_count(self, fig, 0, 1)
                            
    def kill(self, k):
        '''
        Создание бомбочки
        :param k: тип убившего объекта
        '''
        super().kill()
        if k == 0:
            global bombs
            new_bomb = Bomb(0, len(bombs))
            new_bomb.new(self.x, self.y)
            bombs.append(new_bomb)
        

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
                    if fig.typ <= 0:
                        self.kill(fig.typ)
                        fig.kill(fig.typ)
                    else:
                        check_figures_count(self, fig, 1, 1) #Изменение скоростей
    
    def kill(self, k):
        '''
        Создание бомбочки
        :param k: тип убившего объекта
        '''
        super().kill()
        if k == 0:
            global bombs
            new_bomb = Bomb(0, len(bombs))
            new_bomb.new(self.x, self.y)
            bombs.append(new_bomb)


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
        self.color = COLORS[0]
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
                self.kill(self.typ)
                fig.kill(self.typ)
        
    def kill(self, k):
        '''
        Удаление пули из списка фигур
        :param k: тип убившего объекта
        '''
        super().kill()
        global figures
        figures = figures[:self.num:] + figures[self.num+1::]
        for i in range(self.num, len(figures)): #Подстраиваем нумерацию
            figures[i].num = i

class Laser(Figure):
    '''Класс пуль, наследуемый от Figure'''
    def __init__(self, time, num):
        '''
        Начальные настройки класса
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: номер объекта в списке фигур
        '''
        super().__init__(time, num)
        self.typ = -1

    def new(self, x, y, v_x, v_y):
        '''
        Создание новой пули в указанном месте
        :param x: абсцисса центра пули
        :param y: ордината центра пули
        :param v_x: скорость пули в пикселях/1 проход цикла по оси абсцисс
        :param v_y: скорость пули в пикселях/1 проход цикла по оси ординат
        '''
        self.color = COLORS[1]
        self.r = min(SIZE) / 100
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.g_y = 0
        
    def draw(self):
        '''Рисует пулю'''
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def check_figures(self):
        '''Проверка столкновения с другими пулями'''
        for fig in figures[self.num+1::]:
            if (self.x - fig.x)**2 + (self.y - fig.y)**2 <= (self.r + fig.r)**2:
                fig.kill(self.typ)
    def check_walls(self):
        '''Проверка столкновения со стенами'''
        if (self.x+self.r) >= WIDTH or (self.x-self.r) <= 0 or (self.y+self.r) >= HEIGHT or \
           (self.y-self.r) <= min(SIZE)*0.12:
            self.kill(self.typ)
        
    def kill(self, k):
        '''
        Удаление пули из списка фигур
        :param k: тип убившего объекта
        '''
        super().kill()
        global figures
        figures = figures[:self.num:] + figures[self.num+1::]
        for i in range(self.num, len(figures)): #Подстраиваем нумерацию
            figures[i].num = i

class Bomb(Figure):
    '''Класс бомб, наследуемый от Figure'''
    def __init__(self, time, num):
        '''
        Начальные настройки класса
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: номер объекта в списке фигур
        '''
        super().__init__(time, num)
        self.typ = -2
        
    def new(self, x, y):
        '''
        Создание новой бомбы в указанном месте
        :param x: абсцисса центра бомбы
        :param y: ордината центра бомбы
        '''
        self.color = COLORS[1]
        self.r = min(SIZE) / 100
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        
    def draw(self):
        '''Рисует бомбу'''
        pygame.draw.rect(screen, self.color, (self.x - self.r, self.y - self.r,
                                                  2*self.r, 2*self.r))
    
    def check_figures(self):
        '''Проверка столкновения с фигурами'''
        for fig in figures:
            if fig.r != 0 and abs(self.x - fig.x) <= self.r + fig.r and \
               abs(self.y - fig.y) <= self.r + fig.r:
                fig.kill(self.typ)
    
    def check_walls(self):
        '''Взаимодействие с границами экрана. Снизу - удаляем'''
        super().check_walls()
        if self.y >= figures[0].y:
            self.kill(self.typ)
    
    def kill(self, k):
        '''
        Удаление бомбы из списка фигур
        :param k: тип убившего объекта
        '''
        super().kill()
        global bombs
        bombs = bombs[:self.num:] + bombs[self.num+1::]
        for i in range(self.num, len(bombs)): #Подстраиваем нумерацию
            bombs[i].num = i    


class Gun():
    '''
    Класс Пушка
    :param main_color: кортеж, задающий цвет танка в системе RGB
    :param color: кортеж, задающий цвет дула в системе RGB
    :param num: номер объекта
    :param fire_mode: 0/1/2 = не стреляем, стреляем пулями или лазером
    :param fire_power: мощность выстрела от 10 до 100
    :param hp: количество жизней у танка
    :param width: толщина ствола пушки
    :param length: длина ствола пушки
    :param r: полусторона основания танка
    :param x: абсцисса центра объекта
    :param y: ордината центра объекта
    :param angle: угол поворота дула от горизонтали в радианах
    :param v_x: скорость по оси абсцисс в пикселах на 1 FPS
    :param omega: угловая скорость дула пушки
    :param coords: список из координат угловых тояек ствола
    '''
    def __init__(self, color, x, num):
        '''
        Начальные настройки класса
        '''
        self.main_color = color
        self.color = COLORS[0]
        self.num = num
        self.fire_mode = 0
        self.fire_power = 10
        self.hp = 10
        self.width = min(SIZE) / 50
        self.length = min(SIZE) / 20
        self.r = self.width
        self.x = x
        self.y = HEIGHT - self.width
        self.angle = math.pi / 2
        self.v_x = 0
        self.omega = 0
        self.coords = []

    def fire_start(self, fire_mode):
        '''
        Начало подготовки к стрельбе при нажатии кнопки мыши
        :param fire_mode: вид снаряда (1 - обычный, 2 - лазер)
        '''
        self.fire_mode = fire_mode
        self.color = COLORS[1]

    def fire_end(self):
        '''
        Выстрел мячом. Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        '''
        global figures
        if self.fire_mode == 1:
            new_bullet = Bullet(0, len(figures))
        elif self.fire_mode == 2:
            new_bullet = Laser(0, len(figures))
        x = (self.coords[2][0] + self.coords[3][0])*0.5
        y = (self.coords[2][1] + self.coords[3][1])*0.5
        new_bullet.new(x, y, self.fire_power * math.cos(self.angle) * min(SIZE) * 0.1 / FPS,
                       -self.fire_power * math.sin(self.angle) * min(SIZE) * 0.1 / FPS)
        figures.append(new_bullet)
        
        self.fire_mode = 0
        self.fire_power = 10
        self.color = COLORS[0]
        
    def shift_start(self, k):
        '''
        начало движения
        :param k: отвечает за направление движения лево/право ~ -1/+1
        '''
        self.v_x = k * WIDTH / 10 / FPS

    def shift_end(self):
        '''Окончание движения'''
        self.v_x = 0

    def turn_start(self, k):
        '''
        начало движения
        :param k: отвечает за направление движения лево/право ~ -1/+1
        '''
        self.omega = k * math.pi / FPS / 2

    def turn_end(self):
        '''Окончание движения'''
        self.omega = 0
        
    def check_walls(self):
        '''Проверка столкновения со стенами и вторым танком'''
        if self.x >= WIDTH - self.r:
            self.v_x = 0
            self.x = WIDTH - self.r
        if self.x <= self.r:
            self.v_x = 0
            self.x = self.r
        if self.num == 0:
            if figures[1].x - self.x <= 2*self.r:
                self.v_x = 0
                figures[1].v_x = 0
                self.x = figures[1].x - 2*self.r - 1  

    def check_angle(self):
        '''Проверка направления дула в верхнюю часть'''
        if self.angle >= math.pi:
            self.omega = 0
            self.angle = math.pi
        if self.angle <= 0:
            self.omega = 0
            self.angle = 0

    def move(self):
        '''
        Рассчитывает перемещение танка и рисует его
        '''
        
        if self.fire_mode != 0 and self.fire_power < 100:
            self.fire_power += 1
            
        self.length = min(SIZE) / 20 * self.fire_power**0.1
        self.x += self.v_x
        self.angle += self.omega

        self.check_walls()
        self.check_angle()
        self.check_figures()
        
        self.coords = turn(self.angle, [(self.x, self.y), (self.x, self.y - self.width / 2),
                          (self.x + self.length, self.y - self.width / 2),
                          (self.x + self.length, self.y + self.width / 2),
                          (self.x, self.y + self.width / 2)])
        self.draw()

    def draw(self):
        '''
        Рисуем повернутый прямоугольник и основание танка
        '''
        pygame.draw.rect(screen, self.main_color, (self.x - self.width, HEIGHT - 2*self.width,
                                                  2*self.width, 2*self.width))
        pygame.draw.polygon(screen, self.color, self.coords[1::])

    def kill(self, k):
        '''
        Убираем hp
        :param k: тип убившего объекта
        '''
        self.hp -= 1
        if self.hp <= 0:
            self.hp = 0
            global finished
            finished = True
        

    def check_figures(self):
        '''Проверка столкновения с другими фигурами'''
        for fig in figures[2::]:
            if fig.r != 0:
                delta_x = self.x - fig.x
                delta_y = self.y - fig.y
                d = self.r + fig.r
                if (abs(delta_x) <= d) and (abs(delta_y) <= d):
                    if (fig.typ == 0 and fig.time > FPS / 5) or fig.typ == -2:
                        fig.kill(fig.typ)
                        self.kill(fig.typ)
                    elif fig.typ > 0: #Определяем, с какой стороны прилетел: сверху или сбоку
                        if abs(delta_x - self.v_x + fig.v_x) > d:
                            fig.collision((-2*fig.v_x, 0))
                        elif abs(delta_y + fig.v_y) > d:
                            fig.collision((0, -2*fig.v_y))

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
    white = (255, 255, 255)
    colors = [black, red, blue, yellow, green, magenta, cyan, white]
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

def begin():
    '''Задание начальных параметров для игры'''
    global TIME, bombs, figures
    
    TIME = 0 #Игра продоолжается, пока TIME < T * FPS
    bombs = [] #Список бомб
    
    #Список объектов класса Figure
    figures = [Gun((200, 200, 200), WIDTH/3, 0), Gun((50, 50, 50), WIDTH*2/3, 1)]
    for i in range(NUM_RECTS):
        figures.append(Rect(T_life * (i+1) / NUM_RECTS, i + 2))
    for i in range(NUM_BALLS):
        figures.append(Ball(T_life * (i+1) / NUM_BALLS, i + NUM_RECTS + 2))

def screen_update():
    '''
    Рассчитывает перемещения объектов, заменяет пойманные на новые
    по истечении времени жизни объекта.
    Отрисовывает новое изображение на экране
    '''
    screen.fill(COLORS[-1]) #Экран в белый
    for bomb in bombs:
        bomb.move() #Расчет новых параметров объекта и его отрисовка
    for fig in figures:
        fig.move() #Расчет новых параметров объекта и его отрисовка
    menu()
    pygame.display.update()

def menu():
    '''
    Заполняет информационное поле -- зону меню
    '''
    hp1 = figures[0].hp
    hp2 = figures[1].hp
    text('HP:', (min(SIZE)*0.05, min(SIZE)*0.05))
    text(str(hp1) + ' vs ' + str(hp2), (min(SIZE)*0.05 + 60, min(SIZE)*0.05))
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
    text = text1.render(string, True, COLORS[0])
    screen.blit(text, coords)

def button_down():
    '''Обработка нажатия'''
    if pygame.key.get_pressed()[pygame.K_s]:
       figures[0].fire_start(1) #Пулей
    if pygame.key.get_pressed()[pygame.K_w]:
       figures[0].fire_start(2) #Лазером
    if pygame.key.get_pressed()[pygame.K_a]:
       figures[0].shift_start(-1) #Влево
    if pygame.key.get_pressed()[pygame.K_d]:
       figures[0].shift_start(1) #Вправо
    if pygame.key.get_pressed()[pygame.K_q]:
       figures[0].turn_start(1) #Дуло левее
    if pygame.key.get_pressed()[pygame.K_e]:
       figures[0].turn_start(-1) #Дуло правее

    if pygame.key.get_pressed()[pygame.K_k]:
       figures[1].fire_start(1) #Пулей
    if pygame.key.get_pressed()[pygame.K_i]:
       figures[1].fire_start(2) #Лазером
    if pygame.key.get_pressed()[pygame.K_j]:
       figures[1].shift_start(-1) #Влево
    if pygame.key.get_pressed()[pygame.K_l]:
       figures[1].shift_start(1) #Вправо
    if pygame.key.get_pressed()[pygame.K_u]:
       figures[1].turn_start(1) #Дуло левее
    if pygame.key.get_pressed()[pygame.K_o]:
       figures[1].turn_start(-1) #Дуло правее

def button_up():
    '''Обработка отпускания'''
    if figures[0].fire_mode != 0 and not pygame.key.get_pressed()[pygame.K_s] and \
       not pygame.key.get_pressed()[pygame.K_w]:
            figures[0].fire_end() #Выстрел
    if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
       figures[0].shift_end() #Не двигать танк
    if not pygame.key.get_pressed()[pygame.K_q] and not pygame.key.get_pressed()[pygame.K_e]:
       figures[0].turn_end() #Не вертеть дуло

    if figures[1].fire_mode != 0 and not pygame.key.get_pressed()[pygame.K_k] and \
       not pygame.key.get_pressed()[pygame.K_i]:
            figures[1].fire_end() #Выстрел
    if not pygame.key.get_pressed()[pygame.K_j] and not pygame.key.get_pressed()[pygame.K_l]:
       figures[1].shift_end() #Не двигать танк
    if not pygame.key.get_pressed()[pygame.K_u] and not pygame.key.get_pressed()[pygame.K_o]:
       figures[1].turn_end() #Не вертеть дуло


T_life = 10
T = 100
NUM_BALLS = 2 #Наибольшее число шаров, одновременно присутствующих на экране
NUM_RECTS = 3 #Наибольшее число квадратов, одновременно присутствующих на экране
FPS = 30
SIZE = WIDTH, HEIGHT = 700, 700 #Размер окошка
screen = pygame.display.set_mode(SIZE)
T_life *= FPS #Перерасчет времени жизни в количество проходов цикла
T *= FPS #Перерасчет времени в количество проходов цикла
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
        elif event.type == pygame.KEYDOWN:
            button_down()
        elif event.type == pygame.KEYUP:
            button_up()  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #Если курсор в зоне меню -- обработка нажатия
            if (event.pos[0] > min(SIZE)*0.05 + 200) and (event.pos[0] < min(SIZE)*0.05 + 320) and \
            (event.pos[1] > min(SIZE)*0.045) and (event.pos[1] < min(SIZE)*0.1):
                begin() #Начало новой игры
                
    screen_update() #Прорисовка сдвинутых объектов
    
    TIME+=1
    if TIME == T: #Завершение игры при окончании времени
        finished = True

if figures[0].hp > 0:
    if figures[1].hp > 0:
        print('Время вышло. Ничья. HP1:HP2 = ', figures[0].hp, ':', figures[1].hp)
    else:
        print('Игрок 1 победил')
else:
    if figures[1].hp > 0:
        print('Игрок 2 победил')
    else:
        print('Вот это да! Ничья. HP1:HP2 = 0:0. Еще разок?!')
pygame.quit()
