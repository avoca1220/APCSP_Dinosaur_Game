import os
import pygame as pg

CAPTION = "Test Program"
SCREEN_SIZE = (1420, 800)
BACKGROUND_COLOR = (40, 40, 40)
TRANSPARENT = (0, 0, 0, 0)

clock = pg.time.Clock()            


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
        self.must_jump = False

    def jump(self):
        
        if self.ypos > self.jump_height and self.going_down == False:
            
            if self.jump_timer < 10:
                self.jump_timer += 1
            elif self.jump_timer == 10:
                self.jump_timer = 1
            if self.jump_timer % 2 == 1:
                self.ypos -= 5
            print self.jump_timer

                
        if self.ypos == self.jump_height and self.going_down == False:
            self.going_down = True
            
        if self.going_down == True and self.ypos < 400:
            if self.jump_timer < 10:
                self.jump_timer += 1
            elif self.jump_timer == 10:
                self.jump_timer = 1
            if self.jump_timer % 2 == 1:
                self.ypos += 5
            print self.jump_timer


        if self.going_down == True and self.ypos == 400:
            self.going_down = False


    def move(self):
        
        if self.input_control.SPACE == True:
            self.jump()
        
        if self.input_control.SPACE == False and self.ypos < 400:
            if self.jump_timer < 10:
                self.jump_timer += 1
            elif self.jump_timer == 10:
                self.jump_timer = 1
            if self.jump_timer % 2 == 1:
                self.ypos += 5
            print self.jump_timer

def main():
    clock.tick(120)
    pg.init()
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SCREEN_SIZE)
    controls = Control()
    #Player gets input through 'controls'
    player = Player(controls)
        
    while True:

        screen.fill((0, 0, 0))
        controls.get_input()
        player.move()
        pg.draw.rect(screen, (100, 100, 100), pg.Rect(player.xpos, player.ypos, 80, 160))
        pg.display.flip()
        
        if controls.UP == True:
            pass
            #print "UP"
        if controls.DOWN == True:
            pass
            #print "DOWN"
        if controls.RIGHT == True:
            pass
            #print "RIGHT"
        if controls.LEFT == True:
            pass
            #print "LEFT"
        

main()
