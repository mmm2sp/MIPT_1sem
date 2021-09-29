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


def man(size, r_0):
    #Левая нога
    dr.line(screen, (0, 0, 0), (r_0[0] - 15*size, r_0[1] + 160*size),
            (r_0[0] - 50*size, r_0[1] + 257*size))
    dr.line(screen, (0, 0, 0), (r_0[0] - 50*size, r_0[1] + 257*size),
            (r_0[0] - 70*size, r_0[1] + 260*size))
    #Туловище и голова
    dr.ellipse(screen, (167, 147, 172), (r_0[0] - 40*size, r_0[1] + 15*size, 80*size, 150*size))
    dr.circle(screen, (244, 227, 215), r_0, 28*size)
    #Правая нога
    dr.line(screen, (0, 0, 0), (r_0[0] + 20*size, r_0[1] + 150*size),
            (r_0[0] + 30*size, r_0[1] + 250*size))
    dr.line(screen, (0, 0, 0), (r_0[0] + 30*size, r_0[1] + 250*size),
            (r_0[0] + 50*size, r_0[1] + 255*size))
    #Руки
    dr.line(screen, (0, 0, 0), (r_0[0] + 25*size, r_0[1] + 35*size),
            (r_0[0] + 80*size, r_0[1] + 110*size))
    dr.line(screen, (0, 0, 0), (r_0[0] - 25*size, r_0[1] + 35*size),
            (r_0[0] - 80*size, r_0[1] + 110*size))

def woman(size, r_0, k):
    #Левая нога
    dr.line(screen, (0, 0, 0), (r_0[0] - 18*size*k, r_0[1] + 164*size),
            (r_0[0] - 18*size*k, r_0[1] + 250*size))
    dr.line(screen, (0, 0, 0), (r_0[0] - 40*size*k, r_0[1] + 250*size),
            (r_0[0] - 18*size*k, r_0[1] + 250*size))
    #Правая нога
    dr.line(screen, (0, 0, 0), (r_0[0] + 14*size*k, r_0[1] + 164*size),
            (r_0[0] + 14*size*k, r_0[1] + 250*size))
    dr.line(screen, (0, 0, 0), (r_0[0] + 35*size*k, r_0[1] + 252*size),
            (r_0[0] + 14*size*k, r_0[1] + 250*size))
    #Туловище и голова
    dr.polygon(screen, (255, 85, 221), [(r_0[0] - 55*size*k, r_0[1] + 164*size),
                                        (r_0[0] + 55*size*k, r_0[1] + 164*size),
                                        (r_0[0], r_0[1] + 20*size)])
    dr.circle(screen, (244, 227, 215), r_0, 28*size)
    #Левая рука
    dr.line(screen, (0, 0, 0), (r_0[0] - 5*size*k, r_0[1] + 35*size),
            (r_0[0] - 95*size*k, r_0[1] + 110*size))
    #Правая рука
    dr.line(screen, (0, 0, 0), (r_0[0] + 5*size*k, r_0[1] + 35*size),
            (r_0[0] + 40*size*k, r_0[1] + 65*size))
    dr.line(screen, (0, 0, 0), (r_0[0] + 82*size*k, r_0[1] + 45*size),
            (r_0[0] + 40*size*k, r_0[1] + 65*size))

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
X_SIZE = 800
N = 4 #Количество людей на картинке

SIZE = (X_SIZE, int(X_SIZE*0.8))
sgn = 1
k = 2/N*SIZE[0]/500
r_0 = (SIZE[0]*(0.5-0.064*N), SIZE[1]*(1-1/N)/2)

screen = pygame.display.set_mode(SIZE)
#фон
dr.rect(screen, (170, 238, 255), (0, 0, SIZE[0], 0.5*SIZE[1]))
dr.rect(screen, (55, 200, 113), (0, 0.5*SIZE[1], SIZE[0], 0.5*SIZE[1]))
#герои
balloon(52*k, 75*k, (r_0[0] - 80*k, r_0[1] + 115*k), 15)
man(k, r_0)
woman(k, (r_0[0] + 175*k, r_0[1]), sgn)
dr.line(screen, (0, 0, 0), (r_0[0] + 257*k, r_0[1] + 45*k),
            (r_0[0] + 257*k, r_0[1] - 90*k))
icecream(26*k, 14*k, (r_0[0] + 257*k, r_0[1] - 90*k), -3)
woman(k, (r_0[0] + 175*k + 165*k, r_0[1]), -sgn)
man(k, (r_0[0] + (175*2 + 165)*k, r_0[1]))
icecream(13*k, 7*k, (r_0[0] + (175*2 + 165 + 80)*k, r_0[1] + 115*k), -30)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
