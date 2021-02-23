import pygame, sys, random, tools, entities
from pygame import mixer#sounds
from pygame.locals import *

air_timer = 0
moving_right = False
moving_left = False
jump_trigger = False
on_ground = False
vertical_momentum = 0

#def check_block_col(player,block)

#rollback function to be used with spritecollideany() below
def collided(sprite, other):
    return sprite.hitbox.colliderect(other.hitbox)
    #return sprite.hitbox.bottom == other.hitbox.top or sprite.hitbox.colliderect(other.hitbox)

def move_player(mario, blocks):

    global vertical_momentum
    global air_timer

    x,y=0,0
    if(moving_left):
        x -= 2
    if(moving_right):
        x += 2
    vertical_momentum += 0.2
    if(vertical_momentum > 4):
        vertical_momentum = 4
    y=vertical_momentum

    mario.update([x,0])
    col_block = pygame.sprite.spritecollideany(mario,blocks,collided)
    if(col_block):
        if x > 0:
            mario.rect.right = col_block.hitbox.left
        elif x < 0:
            mario.rect.left = col_block.hitbox.right

    mario.update([0,y])
    col_block = pygame.sprite.spritecollideany(mario,blocks,collided)
    if(col_block):
        if y < 0:
            mario.rect.top = col_block.hitbox.bottom
            air_timer = 0
            vertical_momentum = 0
        elif y > 0:
            mario.rect.bottom = col_block.hitbox.top
            air_timer = 0
            vertical_momentum = 0

    air_timer += 1


pygame.init()
clock = pygame.time.Clock()

display_height = 176
display_width = 320
pygame.display.set_caption('Pygame Platformer')
scale = 3
WINDOW_SIZE = (display_width*scale,display_height*scale)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((display_width,display_height)) # used as the surface for rendering, which is scaled


mario = entities.Player(55,82)
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
            if event.key == K_SPACE:
                if air_timer < 10:
                    vertical_momentum = -5
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    move_player(mario,blocks)

    blocks.draw(display)
    mario_bros.draw(display)
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(120)

class overworld():#level selection stuff
    pass

class level():#level
    pass

class items():#shrooms
    pass
