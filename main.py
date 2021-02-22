import pygame, sys, random, tools
from pygame import mixer#sounds

class Block(pygame.sprite.Sprite):
    def __init__(self,block_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(block_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]

class Player(pygame.sprite.Sprite):#mario
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load("sprites/stand_right.gif")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]


pygame.init()
clock = pygame.time.Clock()

display_height = 176
display_width = 320
pygame.display.set_caption('Pygame Platformer')
WINDOW_SIZE = (display_width*2,display_height*2)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((display_width,display_height)) # used as the surface for rendering, which is scaled


mario = Player(50,100)
mario_bros = pygame.sprite.Group()
mario_bros.add(mario)

level_map = tools.load_level("levels/level1")
blocks = pygame.sprite.Group()
enemies = pygame.sprite.Group()

ground_img_path = "sprites/ground.gif"
x = 0
for column in level_map:
    y = 0
    for tile in column:
        if(tile == '2'):
            new_block = Block(ground_img_path,x*16,y*16)
            blocks.add(new_block)
        y += 1
    x+= 1


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



class enemies():#gumbas
    pass

class items():#shrooms
    pass
