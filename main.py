import pygame, sys, random, tools, entities
from pygame import mixer#sounds

pygame.init()
clock = pygame.time.Clock()

display_height = 176
display_width = 320
pygame.display.set_caption('Pygame Platformer')
WINDOW_SIZE = (display_width*2,display_height*2)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((display_width,display_height)) # used as the surface for rendering, which is scaled


mario = entities.Player(50,100)
mario_bros = pygame.sprite.Group()
mario_bros.add(mario)

blocks, enemies = tools.load_level("levels/level1")

display.fill((120,180,255))
while True:#Game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            sys.exit()

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
