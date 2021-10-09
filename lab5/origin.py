import pygame
import math

pygame.init()

FPS = 30

screen = pygame.display.set_mode((1000, 800))

#фон
pygame.draw.rect(screen, (204, 255, 255), (0, 0, 1000, 400))
pygame.draw.rect(screen, (51, 204, 51), (0, 400, 1000, 400))

def home(x, y, k): #k-коэффициент подобия
    # дом
    pygame.draw.rect(screen, (153, 102, 0), (x, y, 250*k, 200*k))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 250*k, 200*k), 2)
    # крыша
    pygame.draw.polygon(screen, (255, 0, 102), [(x, y), (x + 250*k, y),
                                                (x + 125*k, y - 80*k)])

    pygame.draw.polygon(screen, (0, 0, 0), [(x, y), (x + 250 * k, y),
                                                (x + 125 * k, y - 80*k)], 2)

    # окно
    pygame.draw.rect(screen, (0, 204, 204), (x + 90*k, y + 70*k, 70*k, 60*k))
    pygame.draw.rect(screen, (0, 204, 204), (x + 90*k, y + 70*k, 70*k, 60*k), 2)

def cloud(x, y, k):
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 50*k, 2)

    pygame.draw.circle(screen, (255, 255, 255), (x + 50*k, y), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 50*k, y), 50*k, 2)

    pygame.draw.circle(screen, (255, 255, 255), (x + 100*k, y), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 100*k, y), 50*k, 2)

    pygame.draw.circle(screen, (255, 255, 255), (x + 150*k, y), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 150*k, y), 50*k, 2)

    pygame.draw.circle(screen, (255, 255, 255), (x + 100*k, y - 40*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 100*k, y - 40*k), 50*k, 2)

    pygame.draw.circle(screen, (255, 255, 255), (x + 50*k, y - 40*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 50*k, y - 40*k), 50*k, 2)

def tree(x, y, k):
    # дерево

    pygame.draw.rect(screen, (51, 0, 0), (x, y, k*30, k*180))

    # листва

    pygame.draw.circle(screen, (0, 102, 51), (x, y - 130*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x, y - 130*k), 50*k, 2)

    pygame.draw.circle(screen, (0, 102, 51), (x - 60*k, y - 90*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x - 60*k, y - 90*k), 50*k, 2)

    pygame.draw.circle(screen, (0, 102, 51), (x + 60*k, y - 90*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 60*k, y - 90*k), 50*k, 2)

    pygame.draw.circle(screen, (0, 102, 51), (x, y - 60*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x, y - 60*k), 50*k, 2)

    pygame.draw.circle(screen, (0, 102, 51), (x - 40*k, y - 10*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x - 40*k, y - 10*k), 50*k, 2)

    pygame.draw.circle(screen, (0, 102, 51), (x + 50*k, y - 15*k), 50*k)
    pygame.draw.circle(screen, (0, 0, 0), (x + 50*k, y - 15*k), 50*k, 2)

def sun(x, y):
    da = 2 * math.pi / 25
    a = 0
    for i in range(25):  # triangle

        pygame.draw.polygon(screen, (255, 204, 204), [(x + 70 - (1 - math.cos(a)) * 70, y - 70 * math.sin(a)),
                                                      (x + 70 - (1 - math.cos(a + da)) * 70, y - 70 * math.sin(a + da)),
                                                      (x + 75 - (1 - math.cos(a + da / 2)) * 75,
                                                       y - 75 * math.sin(a + da / 2))])

        pygame.draw.polygon(screen, (0, 0, 0), [(x + 70 - (1 - math.cos(a)) * 70, y - 70 * math.sin(a)),
                                                (x + 70 - (1 - math.cos(a + da)) * 70, y - 70 * math.sin(a + da)),
                                                (x + 75 - (1 - math.cos(a + da / 2)) * 75,
                                                 y - 75 * math.sin(a + da / 2))], 3)
        a = a + da
    pygame.draw.circle(screen, (255, 204, 204), (x, y), 71)

home(150, 430, 1)
tree(495, 460, 1)

home(600, 430, 0.7)
tree(850, 440, 0.7)

cloud(250, 100, 1)
cloud(550, 150, 0.7)
cloud(800, 100, 1)

sun(80, 100)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()