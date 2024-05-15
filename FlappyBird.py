import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screenWidth = 480
screenHeight = 600

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Flappy Bird")

#game variables
groundScroll = 0
scrollSpeed = 4

#load images
bg = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")

run = True
while(run):

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0, -150))

    #draw and scroll ground
    screen.blit(ground, (groundScroll, 500))
    groundScroll -= scrollSpeed
    if abs(groundScroll) > 35:
        groundScroll = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    pygame.display.update()

pygame.quit()
