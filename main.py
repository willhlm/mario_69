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

class GUI():
    def __init__(self,ESC,click=False):
        self.ESC=ESC
        self.click=click
        self.display_height = 176
        self.display_width = 320

        self.scale = 3
        self.WINDOW_SIZE = (self.display_width*self.scale,self.display_height*self.scale)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,0,32) # initiate the window
        self.display = pygame.Surface((self.display_width,self.display_height)) # used as the surface for rendering, which is scaled

    def start_menu(self,first=True):#escape botton
        while self.ESC or first:

            game.screen.fill((0,0,0))
            if first:#on boot
                text='Start Game'
            else:#on esc button
                text='Resume Game'

            start_surface=game_font.render(text,True,(255,255,255))#antialias flag
            start_rect=start_surface.get_rect(center=(200,100))#position

            pygame.draw.rect(game.screen,(255,0,0),start_rect)

            if start_rect.collidepoint((pygame.mouse.get_pos())) ==True and self.click==True:
                self.ESC=False
                self.click=False
                first=False

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.click=True
                if event.type==pygame.MOUSEBUTTONUP:
                    self.click=False
            game.screen.blit(start_surface,start_rect)
            pygame.display.update()

class overworld():#level selection stuff
    def __init__(self,active,click=False):
        #super().__init__(ESC,click=False)
        self.active=active
        self.click=click

    def world_select(self):
        while self.active:
            game.screen.fill((0,0,0))
            level1_surface=game_font.render('level1',True,(255,255,255))#antialias flag
            level1_rect=level1_surface.get_rect(center=(200,100))#position

            level2_surface=game_font.render('level2',True,(255,255,255))#antialias flag
            level2_rect=level1_surface.get_rect(center=(200,300))#position

            pygame.draw.rect(game.screen,(255,0,0),level1_rect)
            pygame.draw.rect(game.screen,(255,0,0),level2_rect)

            if level1_rect.collidepoint((pygame.mouse.get_pos())) ==True and self.click==True:
                self.active=False
                self.click=False

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.click=True
                if event.type==pygame.MOUSEBUTTONUP:
                    self.click=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        game.ESC=True
                        game.start_menu(False)

            game.screen.blit(level1_surface,level1_rect)
            game.screen.blit(level2_surface,level2_rect)

            pygame.display.update()

class level():#level
    def __init__(self,level):
        self.level='level'
        self.surface=game_font.render(self.level,True,(255,255,255))#antialias flag
        self.rect=self.surface.get_rect(center=(200,100))#position

class items():#shrooms
    pass

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

    if(x > 0):
        mario.set_img(0)
    elif(x < 0):
        mario.set_img(1)

    air_timer += 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Pygame Platformer')

game_font=pygame.font.Font('freesansbold.ttf',40)


mario = entities.Player(55,82)
mario_bros = pygame.sprite.Group()
mario_bros.add(mario)

blocks, enemies = tools.load_level("levels/level1")


game=GUI(False)#The escape botton flag
game.start_menu()#Start with start game menu
world=overworld(True)#flag to open after start game menu

while True:#Game loop
    game.display.fill((120,180,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if air_timer < 10:
                    vertical_momentum = -5
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key==pygame.K_ESCAPE:
                game.ESC=True

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False


    game.start_menu(False)
    world.world_select()

    move_player(mario,blocks)

    blocks.draw(game.display)
    mario_bros.draw(game.display)


    game.screen.blit(pygame.transform.scale(game.display,game.WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(120)
