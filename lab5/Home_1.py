import pygame
import math

def background(color_up, color_down, M):
    '''
    Заполняет окно, размера SIZE двумя цветами
    :param color_up: цвет верхней половины
    :param color_down: цвет нижней половины
    :param M: отнощение высоты верхней половины к нижней
    '''
    pygame.draw.rect(screen, color_up, (0, 0, SIZE[0], SIZE[1]*M))
    pygame.draw.rect(screen, color_down, (0, SIZE[1]*M, SIZE[0], SIZE[1]*(1-M)))



def wall(color, r_c, size):
    '''
    Рисует стену дома
    :param color: цвет стены
    :param r_c: координаты (x_c, y_c) центра стены
    :param size: размеры (width, height) стены
    '''
    x_c = r_c[0]
    y_c = r_c[1]
    width = size[0]
    height = size[1]
    pygame.draw.rect(screen, color, (x_c - width/2, y_c - height/2, width, height))
    pygame.draw.rect(screen, black, (x_c - width/2, y_c - height/2, width, height),
                                     thickness)
def roof(color, r_0, size):
    '''
    Рисует крышу дома
    :param color: цвет крыши
    :param r_0: координаты (x, y) левого верхнего угла стены дома
    :param size: размеры (width, height) крыши
    '''
    x = r_0[0]
    y = r_0[1]
    width = size[0]
    height = size[1]
    pygame.draw.polygon(screen, color, [(x, y), (x + width, y), (x + width*0.5, y - height)])

    pygame.draw.polygon(screen, black, [(x, y), (x + width, y), (x + width*0.5, y - height)],
                        thickness)
    
def window(color, color_frame, r_c, size):
    '''
    Рисует окна дома
    :param color: цвет окна
    :param color_frame: цвет рамы
    :param r_c: координаты (x_c, y_c) центра окна (он же центр стены)
    :param size: размеры (width, height) окна
    '''
    x_c = r_c[0]
    y_c = r_c[1]
    width = size[0]
    height = size[1]
    pygame.draw.rect(screen, color, (x_c - width/2, y_c - height/2, width, height))
    pygame.draw.rect(screen, color_frame, (x_c - width/2, y_c - height/2, width, height), 4)
  

def home(color, x_c, y_c, k):
    '''
    Рисование дома
    :param color: список из четырех цветов по системе RGB для стены, крыши, окна и рамы соответственно
    :param x_c: абсцисса центра стены
    :param y_c: ордината центра стены
    :param k: Отношения размера дома к нормальному (250x200)
    '''
    #Задание размеров стены
    width = 250*k
    height = 200*k

    #Задание отношения характерного размера частей дома по (x, y) к характерному размеру по (x, y) стены
    sc_wall = (1, 1)
    sc_roof = (1, 0.4)
    sc_window = (0.28, 0.3)

    #Задание размеров частей дома
    size_wall = (width * sc_wall[0], height * sc_wall[1])
    size_roof = (width * sc_roof[0], height * sc_roof[1])
    size_window = (width * sc_window[0], height * sc_window[1])

    #Рисование частей дома
    wall(color[0], (x_c, y_c), size_wall)
    roof(color[1], (x_c - size_wall[0]/2, y_c - size_wall[1]/2), size_roof)
    window(color[2], color[3], (x_c, y_c), size_window)

def trunk(color, r_0, size):
    '''
    Рисует ствол дерева
    :param color: цвет ствола
    :param r_0: координаты (x, y) середины (по x) верхнего края ствола
    :param size: размеры (width, height) ствола
    '''
    x = r_0[0]
    y = r_0[1]
    width = size[0]
    height = size[1]
    pygame.draw.rect(screen, color, (x - width/2, y, width, height))


def foliage(color, r_0, r):
    '''
    Рисует листву дерева
    :param color: цвет листвы
    :param r_0: координаты (x, y) середины (по x) верхнего края ствола
    :param r: радиус окружностей в листве
    '''
    x = r_0[0]
    y = r_0[1]
    #Пять кружочков с черной границей
    pygame.draw.circle(screen, color, (x, y - 2.5*r), r)
    pygame.draw.circle(screen, black, (x, y - 2.5*r), r, thickness)

    pygame.draw.circle(screen, color, (x - 1.1*r, y - 2*r), r)
    pygame.draw.circle(screen, black, (x - 1.1*r, y - 2*r), r, thickness)
    
    pygame.draw.circle(screen, color, (x + 1.1*r, y - 2*r), r)
    pygame.draw.circle(screen, black, (x + 1.1*r, y - 2*r), r, thickness)

    pygame.draw.circle(screen, color, (x, y - 1.2*r), r)
    pygame.draw.circle(screen, black, (x, y - 1.2*r), r, thickness)

    pygame.draw.circle(screen, color, (x - 0.8*r, y - 0.2*r), r)
    pygame.draw.circle(screen, black, (x - 0.85*r, y - 0.15*r), r, thickness)

    pygame.draw.circle(screen, color, (x + 0.8*r, y - 0.2*r), r)
    pygame.draw.circle(screen, black, (x + 0.75*r, y - 0.2*r), r, thickness)

def tree(color, x, y, k):
    '''
    Рисование дерева
    :param color: список из двух цветов по системе RGB для ствола и листвы соответственно
    :param x: абсцисса центра кроны (сиридины ствола)
    :param y: ордината центра кроны (верха ствола)
    :param k: Отношения размера дома к нормальному (ствол 30x180, окружности радиусом 50)
    '''
    size_trunk = (k*30, k*180)
    r = 50*k
    
    trunk(color[0], (x, y), size_trunk)
    foliage(color[1], (x, y), r)
   
def cloud(color, x_c, y_c, k):
    '''
    Рисование облака
    :param color: цвет по системе RGB облака
    :param x_c: абсцисса центра облака
    :param y_c: ордината центра облака
    :param k: Отношение размера облака к стандартному (250x140)
    '''
    r = 50*k
    #Шесть кружочков с черной границей
    pygame.draw.circle(screen, color, (x_c - 1.5*r, y_c + 0.4*r), r)
    pygame.draw.circle(screen, black, (x_c - 1.5*r, y_c + 0.4*r), r, thickness)

    pygame.draw.circle(screen, color, (x_c - 0.5*r, y_c + 0.4*r), r)
    pygame.draw.circle(screen, black, (x_c - 0.5*r, y_c + 0.4*r), r, thickness)

    pygame.draw.circle(screen, color, (x_c + 0.5*r, y_c + 0.4*r), r)
    pygame.draw.circle(screen, black, (x_c + 0.5*r, y_c + 0.4*r), r, thickness)

    pygame.draw.circle(screen, color, (x_c + 1.5*r, y_c + 0.4*r), r)
    pygame.draw.circle(screen, black, (x_c + 1.5*r, y_c + 0.4*r), r, thickness)

    pygame.draw.circle(screen, color, (x_c - 0.5*r, y_c - 0.4*r), r)
    pygame.draw.circle(screen, black, (x_c - 0.5*r, y_c - 0.4*r), r, thickness)

    pygame.draw.circle(screen, color, (x_c + 0.5*r, y_c - 0.4*r), r)
    pygame.draw.circle(screen, black, (x_c + 0.5*r, y_c - 0.4*r), r, thickness)

def sun(color, x, y, k):
    '''
    Рисование солнца
    :param color: цвет по системе RGB солнца
    :param x: абсцисса центра солнца
    :param y: ордината центра солнца
    :param k: отношение радиуса солнца к стандартному (77)
    '''
    r = 70 * k #Внутренний радиус солнца
    N = 25 #Количество треугольников на периметре солнца
    
    dr = r / 50 #Добавка к радиусу, чтобы внутренние стороны треугольников не были видны
    delta_r = r / 10 #Высота треугольников
    R = r + delta_r #Внешний радиус (с учетом треугольников)
    da = 2 * math.pi / N
    a = 0
    for i in range(N):  # Треугольники по периметру солнца
        
        pygame.draw.polygon(screen, color, [(x + r - (1 - math.cos(a)) * r, y - r * math.sin(a)),
                                                      (x + r - (1 - math.cos(a + da)) * r, y - r * math.sin(a + da)),
                                                      (x + R - (1 - math.cos(a + da / 2)) * R,
                                                       y - R * math.sin(a + da / 2))])
        
        pygame.draw.polygon(screen, black, [(x + r - (1 - math.cos(a)) * r, y - r * math.sin(a)),
                                                      (x + r - (1 - math.cos(a + da)) * r, y - r * math.sin(a + da)),
                                                      (x + R - (1 - math.cos(a + da / 2)) * R,
                                                       y - R * math.sin(a + da / 2))], thickness)

        a = a + da
        
    pygame.draw.circle(screen, color, (x, y), r+dr) # Само солнце

def draw():
    '''
    Рисование всех объектов. Масштабный фактор sc отвечает за
    корректное оттображение при изменении размеров окошка
    '''
    sc = X_SIZE/1000
    
    background(color_sky, color_grass, 0.5)

    home(color_home, 200*sc, 530*sc, sc)
    tree(color_tree, 450*sc, 450*sc, sc)

    home(color_home, 700*sc, 500*sc, 0.7*sc)
    tree(color_tree, 900*sc, 440*sc, 0.7*sc)

    cloud(color_cloud, 325*sc, 80*sc, sc)
    cloud(color_cloud, 600*sc, 135*sc, 0.7*sc)
    cloud(color_cloud, 875*sc, 80*sc, sc)
    sun(color_sun, 80*sc, 100*sc, sc)



pygame.init()

FPS = 30 #Частота обновления кадра
X_SIZE = 700 #Ширина картинки
Y_X = 0.8 #Отношение высоты картинки к ширине. КАТЕГОРИЧЕСКИ НЕ РЕКОМЕНДОВАНО МЕНЯТЬ
SIZE = (X_SIZE, int(X_SIZE*Y_X)) #Размеры (x, y) картинки.
screen = pygame.display.set_mode(SIZE)
black = (0, 0, 0)
thickness = 2

#Задаем все цвета
color_sky = (204, 255, 255)
color_grass = (51, 204, 51)
color_wall = (153, 102, 0)
color_roof = (255, 0, 102)
color_window = (0, 204, 204)
color_frame = (193, 142, 0)
color_trunk = (51, 0, 0)
color_foliage = (0, 102, 51)
color_cloud = (255, 255, 255)
color_sun = (255, 204, 204)
color_home = [color_wall, color_roof, color_window, color_frame]
color_tree = [color_trunk, color_foliage]

draw() #Рисование всех объектов

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
