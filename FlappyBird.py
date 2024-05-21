import pygame
from pygame.locals import *
import random

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
flying = False
gameOver = False
pipeGap = 150
pipeFrequency = 1500 #miliseconds
lastPipe = pygame.time.get_ticks() - pipeFrequency

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
        self.vel = 0
        self.clicked = False


    def update(self):
        if flying == True:
            #handle gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 500:
                self.rect.y += int(self.vel)

        if gameOver == False:
            #handle jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handle animation
            self.counter += 1
            flapCooldown = 5

            if self.counter > flapCooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #handle rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipeGap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipeGap/2)]

    def update(self):
        self.rect.x -= scrollSpeed
        if self.rect.right < 0:
            self.kill()
        

birdGroup = pygame.sprite.Group()
pipeGroup = pygame.sprite.Group()

flappy = Bird(100, screenHeight/2)

birdGroup.add(flappy)

run = True
while(run):

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0, -150))

    birdGroup.draw(screen)
    birdGroup.update()

    pipeGroup.draw(screen)

    #draw ground
    screen.blit(ground, (groundScroll, 500))

    #look for collisions
    if pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False) or flappy.rect.top < 0:
        gameOver = True

    #check if game over
    if flappy.rect.bottom >= 500:
        gameOver = True
        flying = False

    if gameOver == False and flying == True:
        #generate pipes
        timeNow = pygame.time.get_ticks()
        if timeNow - lastPipe > pipeFrequency:
            pipeHeight = random.randint(-100, 100)
            bottomPipe = Pipe(screenWidth, screenHeight/2 + pipeHeight, 1)
            topPipe = Pipe(screenWidth, screenHeight/2 + pipeHeight, -1)
            pipeGroup.add(bottomPipe)
            pipeGroup.add(topPipe)
            lastPipe = timeNow

        #draw and scroll ground
        groundScroll -= scrollSpeed
        if abs(groundScroll) > 35:
            groundScroll = 0
        
        pipeGroup.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
            flying = True

    pygame.display.update()

pygame.quit()
