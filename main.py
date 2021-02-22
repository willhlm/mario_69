import pygame, sys, random, tools, entities
from pygame import mixer#sounds
from pygame.locals import *

vertical_momentum = 0
horizontal_momentum = 0
air_timer = 0
moving_right = False
moving_left = False

def player_move(player, block):

    global vertical_momentum
    global horizontal_momentum

    if(pygame.sprite.spritecollide(player,block,False)):
        vertical_momentum = 0
    else:
        vertical_momentum = 3

    if(moving_right and player.rect.topleft[0] < 304):
        horizontal_momentum = 2
    elif(moving_left and player.rect.topleft[0] > 0):
        horizontal_momentum = -2
    else:
        horizontal_momentum = 0

    return horizontal_momentum, vertical_momentum

pygame.init()
clock = pygame.time.Clock()

display_height = 176
display_width = 320
pygame.display.set_caption('Pygame Platformer')
scale = 3
WINDOW_SIZE = (display_width*scale,display_height*scale)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((display_width,display_height)) # used as the surface for rendering, which is scaled


mario = entities.Player(50,100)
mario_bros = pygame.sprite.Group()
mario_bros.add(mario)

blocks, enemies = tools.load_level("levels/level1")


while True:#Game loop
    display.fill((120,180,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.QUIT()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    mario_bros.update(player_move(mario,blocks))

    mario_bros.draw(display)
    blocks.draw(display)
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)

class overworld():#level selection stuff
    pass

class level():#level
    pass

class items():#shrooms
    pass
