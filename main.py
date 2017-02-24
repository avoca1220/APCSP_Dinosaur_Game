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



continue_game = True

class Ground(object):
    def __init__(self):
        self.ground_image = pg.image.load('Assets/tile.png')
        self.ground_image = pg.transform.scale(self.ground_image, (80, 80))
        self.spike_image = pg.image.load('Assets/spike.png')
        self.offset = 0
        self.offset_interval = 1
        self.spike_offset = 0
        self.spike_map = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,]
        
    def display(self):
        if self.control.paused == False:
            if self.offset < 80:
                self.offset += self.offset_interval
            if self.offset == 80:
                self.offset = 0

            if self.spike_offset < (len(self.spike_map) * 80):
                self.spike_offset += 1
            if self.spike_offset == (len(self.spike_map) * 80):
                self.spike_offset = 0
            
        for i in range(19):
            if (i * 80 - self.offset) < 400:
                screen.blit(self.ground_image, ((i * 80 - self.offset), 560 - ((i * 80 - self.offset) - 400)))

            else:
                screen.blit(self.ground_image, ((i * 80 - self.offset), 560))

        for i in range(len(self.spike_map)):
            if self.spike_map[i] == 1:
                if (i * 80 - self.spike_offset) < 400:
                    screen.blit(self.spike_image, ((i * 80 - self.spike_offset), 480 - ((i * 80 - self.spike_offset) - 400)))
                else:
                    screen.blit(self.spike_image, ((i * 80 - self.spike_offset), 480))
        

            
            


    
class Control(object):
    
    def __init__(self, display):
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.SPACE = False
        self.display = display
        self.paused = False
        self.space_released = False
        
    def get_input(self):
        for event in pg.event.get():
            
            if event.type == pg.KEYDOWN:
                
                if event.key == 32:
                    self.SPACE = True

                    
            if event.type == pg.KEYUP:
                if event.key == 32:
                    self.SPACE = False
                    
    def reset(self):
        self.display.offset = 0
        self.display.spike_offset = 0
        self.display.paused = False
        self.display.space_released = False
        self.paused = False
        self.space_released = False
        self.player.dead = False

    def pause(self):
        
        self.paused = True

        if self.SPACE == False:
            self.space_released = True

        if self.SPACE == True and self.space_released == True:
            self.reset()

class Player(object):
    def __init__(self, control, environment):
        self.xpos = 500
        self.ypos = 400
        self.jump_height = 200
        self.control = control
        self.environment = environment
        self.going_down = False
        self.jump_timer = 1
        self.space_was_released = True
        self.must_fall = False
        self.jump_interval = 10
        self.value = 1
        self.sprite = pg.image.load('Assets\chrome-trex-dinosaur-armed.png')
        self.sprite = pg.transform.scale(self.sprite, (100, 107))

        self.explosion = pg.image.load('Assets\explosion.png')
        self.explosion = pg.transform.scale(self.explosion, (400, 200))

        self.font = pg.font.SysFont("monospace", 30)
        self.gameover = self.font.render("GAME OVER", 1, (255, 50, 50))

        self.dead = False

    def jump(self):

        if self.control.paused == False:
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
        if self.control.paused == False:
            if self.control.SPACE == True:
                self.jump()

            
            
            if self.control.SPACE == False and self.ypos < 400:

                self.going_down = True
                
                if self.jump_timer < 10:
                    self.jump_timer += 1
                elif self.jump_timer == 10:
                    self.jump_timer = 1
                if self.jump_timer % 8 == 1:
                    self.ypos += self.jump_interval

    def display(self):
        if self.dead == False:
            screen.blit(self.sprite, (self.xpos, self.ypos + 53))

        if self.dead == True:
            screen.blit(self.explosion, (self.xpos - 150, self.ypos - 30))

    def kill(self):
        self.dead = True
        screen.blit(self.gameover, (600, 100))
        self.control.pause()

    def check_if_dead(self):
        pixel_right = screen.get_at((self.xpos + 80, self.ypos + 107))

        pixel_middle = screen.get_at((self.xpos + 40, self.ypos + 107))

        pixel_left = screen.get_at((self.xpos, self.ypos + 107))
        
        if pixel_right == (116, 114, 114, 255) or pixel_left == (116, 114, 114, 255) or pixel_middle == (116, 114, 114, 225):
            self.kill()
        




def main():
    clock.tick(120)
    #Player gets input through 'controls'
    brick = Ground()
    controls = Control(brick)
    brick.control = controls
    player = Player(controls, brick)
    controls.player = player
        
    while continue_game == True:

        screen.fill((255, 255, 255))
        brick.display()
        controls.get_input()
        player.move()
        player.check_if_dead()
        player.display()
        pg.display.flip()

        

main()
