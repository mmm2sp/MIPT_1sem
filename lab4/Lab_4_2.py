import pygame
import pygame.draw as dr
import numpy as np

#Изменение СК: гомотетия относительно нулевой точки -> сдвиг ->
# -> поворот против часовой стрелки относительно нулевой точки
def motion(k, null, angle, spisok):
    spisok = gomotet(k, spisok)
    spisok = shift(null, spisok)
    spisok = turn(angle, spisok)
    return spisok

def turn(angle, spisok):
    angle = angle*np.pi/180
    r_0 = spisok[0]
    for i in range(len(spisok)):
        x = spisok[i][0] - r_0[0]
        y = spisok[i][1] - r_0[1]
        spisok[i] = (r_0[0] + x*np.cos(angle) + y*np.sin(angle),
                     r_0[1] - x*np.sin(angle) + y*np.cos(angle))
    return spisok

def shift(null, spisok):
    for i in range(len(spisok)):
        spisok[i] = (null[0] + spisok[i][0], null[1] + spisok[i][1])
    return spisok

def gomotet(k, spisok):
    r_0 = spisok[0]
    for i in range(len(spisok)):
        spisok[i] = (r_0[0] + k*(spisok[i][0] - r_0[0]),
                     r_0[1] + k*(spisok[i][1] - r_0[1]))
    return spisok


#Рисуем мороженое. Параметры: радиус шариков, нахлест шариков, координаты основания рожка,
#поворот против часовой стрелки относительно вертикали       
def icecream(R, delt, nul, phi):
    d = delt / R
    coord_cr = [(0, 0), (-1+d/8, 4*(-2**0.5 / 2) - 1 + d), (1-d/8, 4*(-2**0.5 / 2) - 1 + d),
             (0, 4*(-2**0.5 / 2) - 3 + 2*d)]
    coord_tr = [(0, 0), (-0.5, -2**0.5 / 2), (0.5, -2**0.5 / 2)]
    coord_tr = motion(4*R, nul, phi, coord_tr)
    coord_cr = motion(R, nul, phi, coord_cr)
    dr.polygon(screen, (255, 204, 0), coord_tr)
    dr.circle(screen, (85, 0, 0), coord_cr[1], R)
    dr.circle(screen, (255, 0, 0), coord_cr[2], R)
    dr.circle(screen, (255, 255, 255), coord_cr[3], R)
pygame.init()

#Рисуем шарик в форме сердечка на нити. Параметры: сторона треугольника, характеризующего сердечко, длина нити, координаты начала нити,
#поворот против часовой стрелки относительно вертикали
def balloon(a_tr, length, nul, phi):
    l = length/a_tr
    coord = [(0, 0), (0, -l)]
    for t in np.arange(0, 2 * np.pi, 2 * np.pi/100):
        coord.append((0.5*np.sin(t)**3, -(13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t) + 17)/32 - l))
    coord = motion(a_tr, nul, phi, coord)
    dr.line(screen, (0, 0, 0), coord[0], coord[1])
    dr.polygon(screen, (255, 0, 0), coord[2::])

        
pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 400))

#фон
dr.rect(screen, (170, 238, 255), (0, 0, 500, 200))
dr.rect(screen, (55, 200, 113), (0, 200, 500, 200))

#Паренек
dr.line(screen, (0, 0, 0), (152, 260), (114, 357))
dr.line(screen, (0, 0, 0), (114, 357), (94, 359))
dr.ellipse(screen, (167, 147, 172), (125, 115, 78, 150))
dr.circle(screen, (244, 227, 215), (165, 100), 28)
dr.line(screen, (0, 0, 0), (183, 252), (193, 353))
dr.line(screen, (0, 0, 0), (193, 353), (215, 355))
dr.line(screen, (0, 0, 0), (188, 136), (245, 212))
dr.line(screen, (0, 0, 0), (140, 135), (79, 212))

icecream(13, 7, (80, 215), 30)

#Девочка
dr.line(screen, (0, 0, 0), (323, 264), (323, 350))
dr.line(screen, (0, 0, 0), (300, 350), (323, 350))
dr.line(screen, (0, 0, 0), (355, 264), (355, 350))
dr.line(screen, (0, 0, 0), (376, 352), (355, 350))
dr.polygon(screen, (255, 85, 221), [(286, 264), (396, 264), (341, 119)])
dr.circle(screen, (244, 227, 215), (341, 103), 28)
dr.line(screen, (0, 0, 0), (331, 137), (241, 211))
dr.line(screen, (0, 0, 0), (348, 136), (382, 164))
dr.line(screen, (0, 0, 0), (424, 141), (382, 164))

balloon(52, 75, (420, 158), -15)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
