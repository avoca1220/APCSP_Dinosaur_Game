#Importing libraries that will be necessary
import os
import pygame as pg
import random

#Creating varibles to define the traits of the window
CAPTION = "Dinosaur Game"
SCREEN_SIZE = (1420, 800)
BACKGROUND_COLOR = (40, 40, 40)
TRANSPARENT = (0, 0, 0, 0)

#Beginning the program and assigning it a name
pg.init()
pg.display.set_caption(CAPTION)
screen = pg.display.set_mode(SCREEN_SIZE)

#Setting up an object to control the framerates
clock = pg.time.Clock()


#A variable that determines whether or not the game should continue to run
continue_game = True

#The class that controls the ground and spikes, and coordinates their movements.
class Ground(object):
    def __init__(self):
        #Loading the various images to be used for the ground and spikes
        self.ground_image = pg.image.load('Assets/tile.png')
        self.ground_image = pg.transform.scale(self.ground_image, (80, 80))
        self.spike_image = pg.image.load('Assets/spike.png')

        #How far left the ground has moved
        self.offset = 0

        #How quickly the round should move
        self.offset_interval = 1

        #How far the spikes have moved
        self.spike_offset = 0

        #A map of the game in regards to the spikes--a '1' means that there will be a spike in that space, while a '0' means that there will not.
        self.spike_map = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,0,1,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,]

    #The method that moves and displays the ground and spikes
    def display(self):

        #Move only if the game isn't paused
        if self.control.paused == False:

            #Moving the ground
            #If the ground has been moved under eighty pixels to the left, move it one to the right.
            if self.offset < 80:
                self.offset += self.offset_interval

            #If it has been moved eighty pixels to the left, move it back to zero. This makes it look like the
                #entire ground is moving, but really it moves a little bit and resets.
            if self.offset == 80:
                self.offset = 0

            #If the map of spikes hasn't been moved so far to the left that it isn't even on the screen, move
                #it one pixel to the left.
            if self.spike_offset < (len(self.spike_map) * 80):
                self.spike_offset += 1

            #If the map of spikes has been moved so far to the left that it isn't even on the screen, loop it
                #over again.
            if self.spike_offset == (len(self.spike_map) * 80):
                self.spike_offset = 0

        #Print nineteen bricks for the ground
        for i in range(19):

            #If it is far enough to the left, make the brick actually move downwards.
            if (i * 80 - self.offset) < 400:
                screen.blit(self.ground_image, ((i * 80 - self.offset), 560 - ((i * 80 - self.offset) - 400)))

            #Otherwise, let it be of the same Y-position.
            else:
                screen.blit(self.ground_image, ((i * 80 - self.offset), 560))

        #Print each spike (most will be too fat to the right to be seen).
        for i in range(len(self.spike_map)):

            #If there is a one in that spot in the spike map, put a spike on the screen.
            if self.spike_map[i] == 1:

                #If the spike is far enough to the left, make it actually move down.
                if (i * 80 - self.spike_offset) < 400:
                    screen.blit(self.spike_image, ((i * 80 - self.spike_offset), 480 - ((i * 80 - self.spike_offset) - 400)))

                #Otherwise, let it be of the same Y-position.
                else:
                    screen.blit(self.spike_image, ((i * 80 - self.spike_offset), 480))
        

            
            


#The class that gets user input and manages features of the game such as pausing and resetting
class Control(object):
    
    def __init__(self, display):

        #The boolean variables for several of the keyboard buttons
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.SPACE = False

        #A way to reference the ground class (or, specifically, th 'brick' object, which is the
            #instantion of the ground class.)
        self.display = display

        #A boolean variable descriing whether or not the game is currently paused
        self.paused = False

        #A variable represening whether of not the space bar has been released (so that the user can't just hold down
            #space and skip the 'game over' scene)
        self.space_released = False

    #The method that gets the user's input
    def get_input(self):
        for event in pg.event.get():

            #If the event is a key being pressed...
            if event.type == pg.KEYDOWN:

                #...and if the key is space...
                if event.key == 32:

                    #...update the space bar's boolean variable.
                    self.SPACE = True

            #If the event is a key being released...
            if event.type == pg.KEYUP:

                #...and if the ket is space...
                if event.key == 32:

                    #...upda the space bar's boolean variable.
                    self.SPACE = False

    #The method that resets the game
    def reset(self):
        #Move the ground back to its original position
        self.display.offset = 0

        #Move the spike map to its original position
        self.display.spike_offset = 0

        #Un-pause the game
        self.display.paused = False

        #Reset the varible that represents whether or not the user has let go of the space bar
        self.display.space_released = False

        #Second variable that does the exact same thing (I'm too tired to edit it out)
        self.paused = False

        #Also a second variable that does the exact smae thing, and that I'm too tired to edit out.
        self.space_released = False

        #Makes the player not dead
        self.player.dead = False

    #Method that pauses all activity in the game, specifically for the 'game over' screen
    def pause(self):

        #Updates the variable representing whether or not the game is paused
        self.paused = True

        #If the user lets go of the space bar, the space released variable is True.
        if self.SPACE == False:
            self.space_released = True

        #If the user has let go of the space bar since the 'game over' screen occured, and is currently pressing the space bar, reset the game.
        if self.SPACE == True and self.space_released == True:
            self.reset()


#The class for the player
class Player(object):
    def __init__(self, control, environment):
        #The location of the character on the screen
        self.xpos = 500
        self.ypos = 400

        #The maximum height to which the character may jump
        self.jump_height = 200

        #The manner in which the control class is referenced
        self.control = control

        #The manner in which the 'bricks' instantiation of the ground class is referenced
        self.environment = environment

        #The variable representing whether or not the character must go down after jumping
        self.going_down = False

        #The timer for slowing and controlling the jump
        self.jump_timer = 1

        #The speed at which the character jumps
        self.jump_interval = 10

        #The image used byt he character
        self.sprite = pg.image.load('Assets\chrome-trex-dinosaur-armed.png')
        self.sprite = pg.transform.scale(self.sprite, (100, 107))

        #The image used when the character explodes
        self.explosion = pg.image.load('Assets\explosion.png')
        self.explosion = pg.transform.scale(self.explosion, (400, 200))

        #The font and message used when the character dies and gets the 'game over' screen
        self.font = pg.font.SysFont("monospace", 30)
        self.gameover = self.font.render("GAME OVER", 1, (255, 50, 50))

        #The variable representing whether or not the character is alive
        self.dead = False

    #the method that, wehen called, controls the jump of the character
    def jump(self):

        #If the game is un-paused...
        if self.control.paused == False:

            #If the character is below the limitation fot eh jump height, and it is not going down...
            if self.ypos > self.jump_height and self.going_down == False:

                #If the jump timer is nelow ten, increase it by one.
                if self.jump_timer < 10:
                    self.jump_timer += 1

                #If the jump timer is ten, reset it to one.
                elif self.jump_timer == 10:
                    self.jump_timer = 1

                #If the jump timer is divisible by eight, move the character up by the distance specified. This drastically slows down the jump.
                if self.jump_timer % 8 == 1:
                    self.ypos -= self.jump_interval

                

            #If the characte is at its maximum jumop height and is not going down, make it go down.
            if self.ypos == self.jump_height and self.going_down == False:
                self.going_down = True

            #If the character is going down and has not yet reached the ground, move it down.
            if self.going_down == True and self.ypos < 400:
                if self.jump_timer < 10:
                    self.jump_timer += 1
                elif self.jump_timer == 10:
                    self.jump_timer = 1
                if self.jump_timer % 8 == 1:
                    self.ypos += self.jump_interval
                

            #If the character is going down and has reached the ground, make it stop going down.
            if self.going_down == True and self.ypos == 400:
                self.going_down = False

            

    #The method that calls the jump method and brings the character down
    def move(self):

        #If the game is not paused, and the soace bar id pressed, call the jump method.
        if self.control.paused == False:
            if self.control.SPACE == True:
                self.jump()

            
            #If the spcae bar is not pressed and the character is in the air...
            if self.control.SPACE == False and self.ypos < 400:

                #Change th character's status so that it must go down
                self.going_down = True

                #Move the character downwards
                if self.jump_timer < 10:
                    self.jump_timer += 1
                elif self.jump_timer == 10:
                    self.jump_timer = 1
                if self.jump_timer % 8 == 1:
                    self.ypos += self.jump_interval
                    
    #The method that displays the character
    def display(self):
        
        #If the player hasn't died yet, display the weapons-enthusiast T-Rex (the modifications to the x and y positions were to center the new image and place it on the ground)
        if self.dead == False:
            screen.blit(self.sprite, (self.xpos, self.ypos + 53))

        #If the character has died, replace it with a centered imag of an explosion.
        if self.dead == True:
            screen.blit(self.explosion, (self.xpos - 150, self.ypos - 30))

    #The method that pauses the game, prints the 'game over' message, and changes the character's status to dead.
    def kill(self):
        self.dead = True
        screen.blit(self.gameover, (600, 100))
        self.control.pause()

    #The method that checks to see whether the player should be dead, and kills it accordingly.
    def check_if_dead(self):

        #It starts by getting the color of several pixels adjacent to the character
        pixel_right = screen.get_at((self.xpos + 80, self.ypos + 107))

        pixel_middle = screen.get_at((self.xpos + 40, self.ypos + 107))

        pixel_left = screen.get_at((self.xpos, self.ypos + 107))

        #It then checks to see whether any of said pixels are the colors of the spikes, and kills the player accordingly
        if pixel_right == (116, 114, 114, 255) or pixel_left == (116, 114, 114, 255) or pixel_middle == (116, 114, 114, 225):
            self.kill()
        



#The main function
def main():
    #Uses the clock object to set the framerate
    clock.tick(120)
    
    #Creates the brick object
    brick = Ground()
    
    #Creates the controls object, and references the rick object
    controls = Control(brick)
    
    #References the controls object in the brick object (we couldn't do this earlier, because the controls object did not
        #yet exist).
    brick.control = controls
    
    #Creates the player object adn references the brick object
    player = Player(controls, brick)
    
    #References the player object in the controls object (we couldn't do this earlier, because the controls object did not
        #yet exist).
    controls.player = player

    #The main loop...
    while continue_game == True:

        #Fill the screen with white
        screen.fill((255, 255, 255))

        #display the ground
        brick.display()

        #Get user input
        controls.get_input()

        #Move the player according to the user input
        player.move()

        #See whether or not the character;s new position should kill it
        player.check_if_dead()

        #Display the new character
        player.display()

        #Render the new frame to the window
        pg.display.flip()

        
#Run the game!
main()
