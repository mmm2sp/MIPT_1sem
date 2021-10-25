import pygame
from random import randint
from random import random as rnd

class rectballs:
    '''
    Класс фигурок
    :param typ: тип объекта: нуль соответствует шару, 1 -- квадрату
    :param time: время, которое сущесствует этот объект (в проходах цикла)
    :param color: кортеж, задающий цвет объекта в системе RGB
    :param x: абсцисса центра объекта
    :param y: ордината центра объекта
    :param r: радиус объекта (для квадрата -- радиус вписанной окружности)
    :param v_x: скорость объекта в пикселях/1 проход цикла по оси абсцисс
    :param v_y: скорость объекта в пикселях/1 проход цикла по оси ординат
    :param g_y: ускорение объекта в пикселях/(1 проход цикла)**2 по оси ординат
    '''
    
    def __init__(self, typ, time, num):
        '''
        Начальные настройки класса
        :param typ: тип объекта: нуль соответствует шару, 1 -- квадрату
        :param time: время, которое сущесствует этот объект (в проходах цикла)
        :param num: гомер объекта в списке фигур
        '''
        self.typ = typ
        self.time = time
        self.color = COLORS[0]
        self.x = 0
        self.y = 0
        self.r = 0
        self.v_x = 0
        self.v_y = 0
        self.g_y = 0
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
        #Создание нового объекта по истечение времени жизни старого, если его поймали
        if self.r == 0:
            if self.time >= T_life:
                self.new()
        else:
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
        if (self.y-self.r) <= 0: self.v_y = abs(self.v_y)

    def check_figures(self):
        '''Проверка столкновения с другими фигурами'''
        for i in range(self.num + 1, NUM_BALLS + NUM_RECTS):
            if figures[i].r != 0:
                delta_x = self.x - figures[i].x
                delta_y = self.y - figures[i].y
                d = self.r + figures[i].r
                if figures[i].typ == 0: #Если следующая (и эта) фигура -- шар
                    if delta_x**2 + delta_y**2 <= d**2:
                        check_figures_count(self, figures[i], 1, 1) #Изменение скоростей
                else: #Если хотя бы одна -- квадрат
                    if (abs(delta_x) <= d) and (abs(delta_y) <= d):
                        if abs(delta_x - self.v_x + figures[i].v_x) > d:
                            check_figures_count(self, figures[i], 1, 0)
                        elif abs(delta_y - self.v_y + figures[i].v_y) > d:
                            check_figures_count(self, figures[i], 0, 1)

    def collision(self, delta_v):
        '''
        Перерасчет скоростей при столкновении с другими фигурами
        :param delta_v: изменение скорости (кортеж из двух проекций)
        '''
        self.v_x += delta_v[0]
        self.v_y += delta_v[1]

    def new(self):
        '''
        "Создает" (то есть сохраняет информацию) новый объект
        произвольного размера в случайном месте
        '''
        self.time = 0
        self.color = COLORS[randint(1, 6)]
        
        if self.typ == 0: #Для шара
            self.r = (0.02 + 0.03*rnd())*min(SIZE)
            self.v_x = WIDTH / FPS / (5 + 8*rnd())
            self.v_y = 0
            self.g_y = 3 * WIDTH / FPS**2
            
        else: #Для квадрата
            self.r = (0.05 + 0.05*rnd())*min(SIZE)
            self.v_x = WIDTH / FPS / (5 + 8*rnd())
            self.v_y = HEIGHT / FPS / (3 + 7*rnd())
            self.g_y = 0

        intersection = True
        count = 0
        while intersection == True: #Генерим, пока не попадем в свободное место
            self.x = randint(0.1 * WIDTH, 0.9 * WIDTH)
            self.y = randint(0.1 * HEIGHT, 0.9 * HEIGHT)
            intersection = self.check_intersection()
            count += 1
            if count >= 100: #Если зашкал по количеству генераций, объект не создаем
                intersection = False
                self.r = 0
                self.color = COLORS[0]
            
    def check_intersection(self):
        '''Убеждаемся, что созданные параметры объекта не нарушают законы природы'''
        intersection = False
        for i in range(NUM_BALLS + NUM_RECTS):
            if (figures[i].r != 0) and (i != self.num):
                delta_x = self.x - figures[i].x
                delta_y = self.y - figures[i].y
                d = self.r + figures[i].r
                if (abs(delta_x) <= d) and (abs(delta_y) <= d):
                    intersection = True
        return intersection

    def draw(self):   
        '''Рисует объект'''
        if self.typ == 0:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        else:
            pygame.draw.rect(screen, self.color, (self.x - self.r, self.y - self.r,
                                                  2*self.r, 2*self.r))

    def click_check(self, button, pos_mouse):
        '''
        Проверяет, попали ли кликом в один из объектов
        :param pos_mouse: кортеж из двух координат положения мыши
        :param button: номер кнопки мыши
        '''
        points = 0
        #Если попали в шар левой кнопкой
        if (self.typ == 0) and (button == 1) and (((pos_mouse[0] - self.x)**2 +
                                                   (pos_mouse[1] - self.y)**2) < self.r**2):
            self.color = COLORS[0] #Цвет шара черный
            self.r = 0 #Радиус шара нулевой
            points += 2
            
        #Если попали в квадрат правой кнопкой
        if (self.typ == 1) and (button == 3) and (abs(pos_mouse[0] - self.x) < self.r) \
           and (abs(pos_mouse[1] - self.y) < self.r):
            self.color = COLORS[0] #Цвет квадрата черный
            self.r = 0 #Полусторона квадрата нулевая
            points += 1
        return points


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

def screen_update():
    '''
    Рассчитывает перемещения объектов, заменяет пойманные на новые
    по истечении времени жизни объекта.
    Отрисовывает новое изображение на экране
    '''
    
    screen.fill(COLORS[0]) #Экран в черный
    for i in range(NUM_BALLS + NUM_RECTS):
        figures[i].move() #Расчет новых параметров объекта и его отрисовка
    pygame.display.update()

def check_figures_count(fig_1, fig_2, k_x, k_y):
    '''
    Рассчитывает столкновения с другими фигурами
    :param fig_1: фигура №1 класса rectballs
    :param fig_2: фигура №2 класса rectballs
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

def button_down(button, pos_mouse):
    '''
    Обрабатывает нажатие кнопки мыши
    :param pos_mouse: кортеж из двух координат положения мыши
    :param button: номер кнопки мыши
    Возвращает количество набранных баллов
    '''
    
    points = 0   
    for i in range(NUM_BALLS + NUM_RECTS):
            points += figures[i].click_check(button, pos_mouse)
    return points

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
NUM_BALLS = 4 #Наибольшее число шаров, одновременно присутствующих на экране
NUM_RECTS = 5 #Наибольшее число квадратов, одновременно присутствующих на экране

FPS = 30
SIZE = WIDTH, HEIGHT = 700, 700 #Размер окошка
screen = pygame.display.set_mode(SIZE)
T_life *= FPS #Перерасчет времени жизни в количество проходов цикла
COLORS = const_colors()
TIME = 0 #Игра продоолжается, пока TIME < T * FPS
score = 0 #Набранный счет
figures = [] #Кортеж объектов класса rectballs


for i in range(NUM_BALLS):
    figures.append(rectballs(0, T_life * (i+1) / NUM_BALLS, i))
for i in range(NUM_RECTS):
    figures.append(rectballs(1, T_life * (i+1) / NUM_RECTS, i + NUM_BALLS))

    
pygame.init()
clock = pygame.time.Clock()
finished = False
    
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            delt = button_down(event.button, event.pos)
            score += delt

    screen_update() #Прорисовка сдвинутых объектов
    
    TIME+=1
    if TIME == T*FPS: #Завершение игры при окончании времени
        finished = True

end(score)#Сохранение результатов игры в файл и вывод в консоль
pygame.quit()
