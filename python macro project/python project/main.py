import pygame
from sys import exit
pygame.init()
board=pygame.image.load("snake.png")
bt=pygame.transform.scale(board,(800,800))
screen=pygame.display.set_mode((1000,800))
clock=pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if (event.type==pygame.QUIT):
            pygame.quit()
            exit()
    screen.blit(bt,(200,0))
    pygame.display.update()
    clock.tick(60)
