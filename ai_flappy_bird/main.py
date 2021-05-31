
#check out gitpod
import pygame
pygame.init()
import neat
import time
import os
import random

WIN_WIDTH = 450 #caps for constant is convention
WIN_HEIGHT = 700 #my laptop is not large enough

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("ai_flappy_bird\imgs\\bird1.png")), pygame.transform.scale2x(pygame.image.load("ai_flappy_bird\imgs\\bird2.png")), pygame.transform.scale2x(pygame.image.load("ai_flappy_bird\imgs\\bird3.png"))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("ai_flappy_bird\imgs\\pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("ai_flappy_bird\imgs\\base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("ai_flappy_bird\imgs\\bg.png"))

class Bird():
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 #how much the bird is going to tilt (bird tilts when going up or down)
    ROTATION_VEL = 20 #how much rotate on each frame
    ANIMATION_TIME = 5 #how long each bird animation is shown

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 #starts looking flat
        self.tick_count = 0
        self.vel = 0
        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5 #negative vel goes up (this number is arbitrary but should work with other vals picked)
        self.tick_count = 0
        self.height = self.y #tracks where the jump started

    def move(self):
        self.tick_count += 1 #this is going to be called every frame, so counting frames since last jump
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2 #tells us, based on our birds current velocity, how much we're moving up or down. tick count represents "seconds", or how much time we've been moving down (acceleration?)

        if d >= 16:
            d = 16
        elif d < 0:
            d -= 2 #makes the jump smoother?

        self.y += d

        if d < 0 or self.y < self.height + 50: #if we are moving upward or above where the jump started
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL
    
    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0] #display for 5 frames
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1] #wings will be level
            self.img_count = self.ANIMATION_TIME*2 #and reseting animation count when it goes back up

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) #code rotates image
        win.blit(rotated_image, new_rect.topleft)
    
    def collision(self):
        return pygame.mask.from_surface(self.img)

def win_draw(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()

def main(): #runs main loop
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        bird.move()
        win_draw(win, bird)
    
    pygame.quit()

main()
