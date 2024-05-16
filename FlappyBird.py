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

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        #handle animation
        self.counter += 1
        flapCooldown = 5

        if self.counter > flapCooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

birdGroup = pygame.sprite.Group()

flappy = Bird(100, screenHeight/2)

birdGroup.add(flappy)

run = True
while(run):

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0, -150))

    #draw bird
    birdGroup.draw(screen)
    birdGroup.update()

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
