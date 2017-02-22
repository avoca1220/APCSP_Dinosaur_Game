import os
import pygame as pg
import random

CAPTION = "Dinosaur Game"
SCREEN_SIZE = (1420, 800)
BACKGROUND_COLOR = (40, 40, 40)
TRANSPARENT = (0, 0, 0, 0)

pg.init()
pg.display.set_caption(CAPTION)
screen = pg.display.set_mode(SCREEN_SIZE)

clock = pg.time.Clock()            

class Ground(object):
    def __init__(self):
        self.ground_image = pg.image.load('Assets/tile.png')
        self.ground_image = pg.transform.scale(self.ground_image, (80, 80))
        self.spike_image = pg.image.load('Assets/spike.png')
        self.spike_image = pg.transform.scale(self.spike_image, (80, 80))
        self.offset = 0
        self.offset_interval = 1
        self.ground_array = {}

    def display(self):
        if self.offset < 80:
            self.offset += self.offset_interval
        if self.offset == 80:
            self.offset = 0
        for i in range(19):
            if (i * 80 - self.offset) < 80:
                screen.blit(self.ground_image, ((i * 80 - self.offset), 560 - ((i * 80 - self.offset)- 80)))

            else:
                screen.blit(self.ground_image, ((i * 80 - self.offset), 560))

            
            


    
class Control(object):
    
    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.SPACE = False
        
    def get_input(self):
        for event in pg.event.get():
            
            if event.type == pg.KEYDOWN:
                
                if event.key == 32:
                    self.SPACE = True

                    
            if event.type == pg.KEYUP:
                if event.key == 32:
                    self.SPACE = False

class Player(object):
    def __init__(self, input_control):
        self.xpos = 500
        self.ypos = 400
        self.jump_height = 200
        self.input_control = input_control
        self.going_down = False
        self.jump_timer = 1
        self.space_was_released = True
        self.must_fall = False
        self.jump_interval = 10
        self.value = 1
        self.sprite = pg.image.load('Assets\chrome-trex-dinosaur.png')
        self.sprite = pg.transform.scale(self.sprite, (100, 107))

    def jump(self):


        if self.ypos > self.jump_height and self.going_down == False:
                
            if self.jump_timer < 10:
                self.jump_timer += 1
            elif self.jump_timer == 10:
                self.jump_timer = 1
            if self.jump_timer % 8 == 1:
                self.ypos -= self.jump_interval

            

                    
        if self.ypos == self.jump_height and self.going_down == False:
            self.going_down = True
                
        if self.going_down == True and self.ypos < 400:
            if self.jump_timer < 10:
                self.jump_timer += 1
            elif self.jump_timer == 10:
                self.jump_timer = 1
            if self.jump_timer % 8 == 1:
                self.ypos += self.jump_interval
            


        if self.going_down == True and self.ypos == 400:
            self.going_down = False

            


    def move(self):
        if self.input_control.SPACE == True:
            self.jump()

        
        
        if self.input_control.SPACE == False and self.ypos < 400:

            self.going_down = True
            
            if self.jump_timer < 10:
                self.jump_timer += 1
            elif self.jump_timer == 10:
                self.jump_timer = 1
            if self.jump_timer % 8 == 1:
                self.ypos += self.jump_interval

    def display(self):
        screen.blit(self.sprite, (self.xpos, self.ypos + 53))




def main():
    clock.tick(120)
    controls = Control()
    #Player gets input through 'controls'
    player = Player(controls)
    brick = Ground()
        
    while True:

        screen.fill((255, 255, 255))
        brick.display()
        controls.get_input()
        player.move()
        player.display()
        pg.display.flip()

        

main()
