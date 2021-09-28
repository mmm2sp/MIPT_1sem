import pygame
import pygame.draw as dr

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

dr.rect(screen, (255, 0, 255), (100, 100, 200, 200))
dr.rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
dr.polygon(screen, (255, 255, 0), [(100,100), (200,50),
                               (300,100), (100,100)])
dr.polygon(screen, (0, 0, 255), [(100,100), (200,50),
                               (300,100), (100,100)], 5)
dr.circle(screen, (0, 255, 0), (200, 175), 50)
dr.circle(screen, (255, 255, 255), (200, 175), 50, 5)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
