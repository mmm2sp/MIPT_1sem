import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 400))

#фон
dr.rect(screen, (170, 238, 255), (0, 0, 500, 200))
dr.rect(screen, (55, 200, 113), (0, 200, 500, 200))

#Паренек
dr.ellipse(screen, (167, 147, 172), (125, 115, 78, 150))
dr.circle(screen, (244, 227, 215), (165, 100), 28)
dr.line(screen, (0, 0, 0), (188, 136), (245, 212))
dr.line(screen, (0, 0, 0), (140, 135), (74, 218))

"""
rect(screen, (0, 0, 0), (150, 250, 100, 20))
circle(screen, (255, 0, 0), (155, 179), 20)
circle(screen, (0, 0, 0), (155, 179), 20, width=1)
circle(screen, (0, 0, 0), (155, 179), 9)
circle(screen, (255, 0, 0), (245, 179), 17)
circle(screen, (0, 0, 0), (245, 179), 17, width=1)
circle(screen, (0, 0, 0), (245, 179), 8)
polygon(screen, (0, 0, 0), [(100,100), (180,170), (173,178), (93,108)])
polygon(screen, (0, 0, 0), [(300,140), (222,167), (222 - 3,167 - 3*78/27), (300 - 3,140 - 3*78/27)])
"""

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
