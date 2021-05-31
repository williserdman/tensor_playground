
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
FONT = pygame.font.SysFont('comicsans', 50)

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
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe():
    GAP = 200 #space in between pipes
    VEL = 5 #pipes are actually going to be moving toward bird

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0 #where the top of the pipe is going to be drawn
        self.bottom = 0 #where the bottom of the pipe is going to be drawn
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collision(self, bird): #using pygame masks read documentation if interested
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y)) #how far away the top corners are from each other?
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) #tells uf the point of overlap between bird mask and bottom pipe
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False

class Base(): #is a class because it's going to be moving?
    VEL = 5 #same as pipe
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def win_draw(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes: #can be more than one pipe on the sceen at a time
        pipe.draw(win)

    text = FONT.render("Score: " + str(score), 1, (0, 0, 0)) #1 for anti aliasing on?
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main(): #runs main loop
    BASE_HEIGHT = 650
    PIPE_HEIGHT = 600
    BIRD_X = 200
    BIRD_Y = 300
    bird = Bird(BIRD_X, BIRD_Y)
    base = Base(BASE_HEIGHT) 
    pipes = [Pipe(PIPE_HEIGHT)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #bird.move()
        base.move()
        rem = [] #list of pipes to be removes
        add_pipe = False
        for pipe in pipes:

            if pipe.collision(bird):
                print("hit")

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(PIPE_HEIGHT))
        
        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= BASE_HEIGHT:
            print("floor")

        win_draw(win, bird, pipes, base, score)
    
    pygame.quit()

main()
