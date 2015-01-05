# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 10:06:01 2015

@author: benjamin

Standalone Level Editor for platform games

generates a list of entity blocks for use in my two player platformer (could work with other games?)
"""

import pygame, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WIN_CAPTION = 'Level Editor'

save_name = raw_input('enter file name:')
BLOCK_SIZE = int(raw_input('block size:'))
WIN_WIDTH = 640#int(raw_input('size of window\'s width in pixels:'))
WIN_HEIGHT = 480#int(raw_input('size of window\'s height in pixels:'))


assert WIN_WIDTH % BLOCK_SIZE == 0, 'window width must be equal to a multiple of blocksize'
assert WIN_HEIGHT % BLOCK_SIZE == 0, 'window height must be equal to a multiple of blocksize' 

#Init Colours
#            R    G    B
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
BLUE     = (  0,   0, 255)
PURPLE   = (122,  15, 128)
CYAN     = (  0, 255, 255)
NAVYBLUE = ( 60,  60, 100)
GRAY     = (100, 100, 100)

BGCOLOUR = NAVYBLUE

block_list = []

class Block:
    def __init__(self, x, y, size, block_type):
        self.x = x
        self.y = y
        self.size = size      
        self.block_type = block_type

        self.rect = Rect(self.x, self.y, self.size, self.size) 
        
        if self.block_type == 'block':
            self.colour = BLACK
        elif self.block_type == 'p1_spawn':
            self.colour = BLUE
        elif self.block_type == 'p2_spawn':
            self.colour = PURPLE
        elif self.block_type == 'exit':
            self.colour = CYAN
        elif self.block_type == 'button':
            self.colour = WHITE
        elif self.block_type == 'door':
            self.colour = GRAY


def get_level_logic():
    #do all the logic of the buttons and switches - what they do etc
    return 'logic for stuff goes here'

def main():
    global FPSCLOCK, DISPLAYSURF

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(WIN_CAPTION)
    FPSCLOCK = pygame.time.Clock()

    x = 0
    y = 0
    wall_list = []
    block_list = []

    while True: #main game loop
        DISPLAYSURF.fill(BGCOLOUR)
        
        mouse_rect = pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE)

        for event in pygame.event.get(): 
            #event handling loop
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    x +=- BLOCK_SIZE
                    
                elif event.key == K_RIGHT:
                    x += BLOCK_SIZE
                    
                elif event.key == K_DOWN:
                    y += BLOCK_SIZE
            
                elif event.key == K_UP:
                    y +=- BLOCK_SIZE
                    
                elif event.key == K_z:
                    #make block                    
                    _block = Block(x,y,BLOCK_SIZE, 'block')
                    block_list.append(_block)
                    
                elif event.key == K_x:
                    #delete block
                    for _i_num, _i in enumerate(block_list):
                        if mouse_rect.colliderect(_i.rect):
                            del block_list[_i_num]
                            
                elif event.key == K_DELETE:
                    #clears list - i dont think the objects are cleared from memory however.
                    block_list = []
                    
                    
                elif event.key == K_1:
                    #player 1 spawnpoint
                    _block = Block(x,y,BLOCK_SIZE, 'p1_spawn')
                    block_list.append(_block)
                    
                elif event.key == K_2:
                    #player 1 spawnpoint
                    _block = Block(x,y,BLOCK_SIZE, 'p2_spawn')
                    block_list.append(_block)
                
                elif event.key == K_3:
                    _block = Block(x,y,BLOCK_SIZE, 'exit')
                    block_list.append(_block)
                
                elif event.key == K_4:
                    _block = Block(x,y,BLOCK_SIZE, 'button')
                    block_list.append(_block) 
                    
                elif event.key == K_5:
                    _block = Block(x,y,BLOCK_SIZE, 'door')
                    block_list.append(_block)
                    
                elif event.key == K_RETURN:
                    #output to file
                    for _i in block_list:
                        wall_list.append((_i.x,_i.y,BLOCK_SIZE,_i.block_type)) #list of blocks that will be transferred to main program
                        
                    output = open(save_name,'w')
                    output.write(str(wall_list)+'\n')
                    output.write(get_level_logic())
                    print 'outputted to file: ', wall_list
                    output.close()
                    wall_list = []
                    
                
                    
        #draw a cursor square
        pygame.draw.rect(DISPLAYSURF, BLACK,mouse_rect,1)
        
        #draw line for ground level
        pygame.draw.rect(DISPLAYSURF, (80, 80, 120), (0,WIN_HEIGHT-192,WIN_WIDTH,BLOCK_SIZE),1)
        
        #draw blocks
        for _i in block_list:
            pygame.draw.rect(DISPLAYSURF, _i.colour, _i.rect)
          
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()

if __name__=='__main__':
    main()
