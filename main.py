# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 17:43:19 2014

@author: benjamin

simple single player,two character puzzle platform game.

currently: designing levels
timeline:
1 -  stripping all old code
2 -  cleaning it all up, optimising
3 -  creating two players
4 - designing levels
5 - making/programming levels
6 - story, graphics
7 - animation


to do/to fix:
-find way to make all worlds their own file
-fix walls not stopping player moving when it is not their turn
-make players collide with eachother (important)
-make active player have an arrow above its head
-fix players being outside game window

"""

import pygame, sys, ast
from pygame.locals import *

FPS = 60 # frames per second, the general speed of the program

BLOCK_SIZE = 32

WIN_WIDTH = 640 # size of window's width in pixels
WIN_HEIGHT = 480 # size of windows' height in pixels
WIN_CAPTION = 'Platformer Test'

assert WIN_WIDTH % BLOCK_SIZE == 0, 'window width must be equal to a multiple of blocksize'
assert WIN_HEIGHT % BLOCK_SIZE == 0, 'window height must be equal to a multiple of blocksize'

#Init Colours
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (122,  15, 128)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

BGCOLOUR = NAVYBLUE

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

block_list = []
entity_list = pygame.sprite.Group()


class Base_Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Base_Entity):
    def __init__(self, x, y, size, move_speed, jump_speed, colour):
        Base_Entity.__init__(self)
        self.max_gravity = 15
        self.jump_speed = jump_speed
        self.gravity_speed = 0.7

        self.x_vel = 0
        self.y_vel = 0

        self.move_speed = move_speed
        self.alive = True
        self.size = size

        self.on_ground = False
        self.x_collide = False #if colliding with a block to the left or right
        self.current = False


        self.image = pygame.Surface((self.size, self.size))
        self.image.convert()
        self.image.fill(colour)
        self.rect = pygame.Rect(x,y,self.size,self.size)

    def update(self):
        if not self.on_ground:
            if self.y_vel < self.max_gravity:
                self.y_vel += self.gravity_speed
        self.move()
        #increment in x direction
        self.rect.left += self.x_vel
        #do x-axis collisions
        self.collision(self.x_vel,0)
        # increment in y direction
        self.rect.top += self.y_vel
        # assuming we're in the air
        self.on_ground = False
        # assuming we'r not colliding with an object:
        self.x_collide = False
        # do y-axis collisions
        self.collision(0, self.y_vel)
        
        #do room collisions
        if self.rect.topleft[0] < 0:
            self.rect.left = 0 #treat left side as a barrier
            
        elif self.rect.topleft[1] > WIN_HEIGHT:
            self.death() #kill player if outside room
            
        elif self.rect.topright[0]>WIN_WIDTH: #treat right side as a barrier
            self.rect.right = WIN_WIDTH


    def jump(self):
        """Fly, you fools"""
        if self.on_ground:
            self.y_vel -= self.jump_speed

    def collision(self, x_vel, y_vel):
        for _i in block_list:
            if pygame.sprite.collide_rect(self, _i):
                if x_vel > 0:
                    self.rect.right = _i.rect.left
                    self.x_collide = True
                if x_vel < 0:
                    self.rect.left = _i.rect.right
                    self.x_collide = True
                if y_vel > 0:
                    self.rect.bottom = _i.rect.top
                    self.on_ground = True
                    self.y_vel = 0
                if y_vel < 0:
                    self.rect.top = _i.rect.bottom
                    self.y_vel = 0

    def move(self):
        if self.current == True:
            if MOVE_LEFT:
                self.x_vel =- self.move_speed
            if MOVE_RIGHT:
                self.x_vel = self.move_speed
            if not (MOVE_LEFT or MOVE_RIGHT):
                self.x_vel = 0

            if MOVE_UP:
                self.jump()
        else:
            self.x_vel = 0

    def death(self):
        #die
        self.rect.bottomleft = world.p1_spawn
        self.x_vel = 0
        self.y_vel = 0



class Block(Base_Entity):
    def __init__(self, x, y, size):
        Base_Entity.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.Surface((self.size, self.size))
        self.image.convert()
        self.image.fill(BLACK   )
        self.rect = Rect(self.x, self.y, self.size, self.size)

    def update(self):
        pass
    
class Exit(Block):
    def __init__(self,x, y, size):
        Block.__init__(self,x, y, size)
        self.image.fill(CYAN)
    
    def update(self):
        if self.rect.colliderect(player1.rect) and self.rect.colliderect(player2.rect):
            world.advance_level()
            
class Button(Block):
    def __init__(self, x, y, size):
        Block.__init__(self,x ,y, size)
        self.y += self.size/4*3
        self.image = pygame.Surface((self.size, self.size/4))
        self.image.fill(WHITE)
        self.rect = Rect(self.x, self.y, self.size, self.size/4)
        
        
class Door(Block):
    def __init__(self, x, y, size):
        #linked to button
        Block.__init__(self,x,y,size)
        self.image.fill(GRAY)
        self.open = False
         
        

class World:
    """worldgen, spawning and score handler"""
    def __init__(self):
        self.block_size = BLOCK_SIZE
        self.blocks_x = WIN_WIDTH / self.block_size
        self.blocks_y = WIN_HEIGHT / self.block_size

        #load hardcoded world and convert to objects
        #self.world = self.load_world()
        #self.create_world(self.world)

        self.p1_spawn = [0,0]
        self.p2_spawn = [0,0]
        
        self.current_level = 3
        
        #import world from text file
        self.import_world('level{0}'.format(str(self.current_level)))

        self.create_interval = 100
        self.create = 0
        

    def terminate(self):
        #to do: put save game in here
        pygame.quit()
        sys.exit()

    def import_world(self, filename):
        _file = open(filename,'r') #open level.txt
        _file_text = _file.readlines()
        _file.close()
        _file_level_code = ast.literal_eval(_file_text[0]) #convert string of lists into list
       
        if len(_file_text) > 1:
            _file_logic = _file_text[1] #get logic for file if it has it

        #create blocks from imported text
        for _i in _file_level_code:
            if _i[3] == 'block':
                _block = Block(_i[0], _i[1], _i[2])
                block_list.append(_block)
                entity_list.add(_block)
                
            elif _i[3] == 'p1_spawn':
                self.p1_spawn = [_i[0],_i[1]]
                
            elif _i[3] == 'p2_spawn':
                self.p2_spawn = [_i[0],_i[1]] 
                
            elif _i[3] == 'exit':
                _block = Exit(_i[0], _i[1], _i[2])
                entity_list.add(_block)
                
            elif _i[3] == 'button':
                _block = Button(_i[0], _i[1], _i[2])
                entity_list.add(_block)
                block_list.append(_block)
            
            elif _i[3] == 'door':
                _block = Door(_i[0], _i[1], _i[2])
                entity_list.add(_block)  
                block_list.append(_block)
                
        #create player 1
        global player1, player2
        
        player1 = Player(self.p1_spawn[0],self.p1_spawn[1], 32, 4, 10, BLUE)
        entity_list.add(player1)
        
        #create player 2
        player2 = Player(self.p2_spawn[0],self.p2_spawn[1], 48, 3, 9, PURPLE)
        entity_list.add(player2)
                
    def advance_level(self):
        #go to next level.
        
        entity_list.empty()
        self.current_level += 1        
        self.import_world('level{0}'.format(str(self.current_level)))
        
        

def switch_player(player):
    if player == 'player1':
        return 'player2'
    elif player == 'player2':
        return 'player1'

def main():
    global FPSCLOCK, DISPLAYSURF, player, world, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, current_player

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(WIN_CAPTION)
    FPSCLOCK = pygame.time.Clock()
    
    world = World()
    
    current_player = 'player1'


    MOVE_LEFT = False
    MOVE_RIGHT = False
    MOVE_UP = False

    while True: #main game loop
        DISPLAYSURF.fill(BGCOLOUR)

        for event in pygame.event.get(): #event handling loop
            if event.type == QUIT:
                world.terminate()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    MOVE_LEFT = True
                    MOVE_RIGHT = False
                elif event.key == K_RIGHT:
                    MOVE_RIGHT = True
                    MOVE_LEFT = False
                elif event.key == K_UP:
                    MOVE_UP = True
                elif event.key == K_SPACE:
                    current_player = switch_player(current_player)

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    MOVE_LEFT = False
                if event.key == K_RIGHT:
                    MOVE_RIGHT = False
                if event.key == K_UP:
                    MOVE_UP = False

        #switch players
        if current_player == 'player1':
            player1.current = True
            player2.current = False
        elif current_player == 'player2':
            player1.current = False
            player2.current = True

        #update all entities
        for _i in entity_list:
            _i.update()

        entity_list.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
