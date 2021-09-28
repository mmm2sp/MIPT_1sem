import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

dr.rect(screen, (200, 200, 200), (0, 0, 400, 400))
dr.circle(screen, (255, 255, 0), (200, 200), 100)
dr.circle(screen, (0, 0, 0), (200, 200), 100, width=1)
dr.rect(screen, (0, 0, 0), (150, 250, 100, 20))
dr.circle(screen, (255, 0, 0), (155, 179), 20)
dr.circle(screen, (0, 0, 0), (155, 179), 20, width=1)
dr.circle(screen, (0, 0, 0), (155, 179), 9)
dr.circle(screen, (255, 0, 0), (245, 179), 17)
dr.circle(screen, (0, 0, 0), (245, 179), 17, width=1)
dr.circle(screen, (0, 0, 0), (245, 179), 8)
dr.polygon(screen, (0, 0, 0), [(100,100), (180,170), (173,178), (93,108)])
dr.polygon(screen, (0, 0, 0), [(300,140), (222,167), (222 - 3,167 - 3*78/27),
                               (300 - 3,140 - 3*78/27)])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
