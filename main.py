import pygame, sys, random, tools, entities
from pygame import mixer#sounds
from pygame.locals import *

air_timer = 0
run_timer = 0
moving_right = False
moving_left = False
jump_trigger = False
on_ground = False
horizontal_momentum = 0
vertical_momentum = 0
true_scroll = [0,0]
scroll = [0,0]

mario_bros = pygame.sprite.Group()
blocks = pygame.sprite.Group()
enemies = pygame.sprite.Group()

#def check_block_col(player,block)

class GUI():
    def __init__(self,ESC,click=False):
        self.ESC=ESC
        self.click=click
        self.display_height = 176
        self.display_width = 320
        self.dead = False

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

    def game_over_screen(self):
        # this shit is crashing the program
        while self.dead:
            game.screen.fill((0,0,0))
            go_surface=game_font.render("Game Over",True,(255,255,255))#antialias flag
            go_rect=go_surface.get_rect(center=(200,100))#position
            pygame.draw.rect(game.screen,(0,0,0),go_rect)
            game.screen.blit(go_surface,go_rect)
            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        game.dead=False
                        mario.life=4
                        game.start_menu()#back to start
                        world.active=True
                        world.world_select()

class overworld():#level selection stuff
    def __init__(self,active,click=False):
        #super().__init__(ESC,click=False)
        self.active=active
        self.click=click

    @staticmethod
    def draw_map(int):
        level_surface=game_font.render('level'+str(int),True,(255,255,255))#antialias flag
        level_rect=level_surface.get_rect(center=(200,100*int))#position
        return level_surface,level_rect

    def world_select(self):
        while self.active:
            game.screen.fill((0,0,0))

            for i in range(1,3):
                level_surface,level_rect=overworld.draw_map(i)
                pygame.draw.rect(game.screen,(255,0,0),level_rect)
                game.screen.blit(level_surface,level_rect)

                if level_rect.collidepoint((pygame.mouse.get_pos())) ==True and self.click==True:
                    self.active=False
                    self.click=False
                    map.select_level(i)
                    self.level=i

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

            pygame.display.update()

class level():#level
    def __init__(self):
        self.level='level'
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def select_level(self,level):
        self.blocks, self.enemies = tools.load_level("levels/"+self.level+str(level))

class items():#shrooms
    pass

def re_spawn():#restart the whole level
    global moving_right
    global moving_left

    moving_right=False
    moving_left=False
    mario.rect.topleft=[255,82]
    mario.hitbox=mario.rect
    mario.update
    map.blocks=[]
    map.select_level(world.level)

def check_death(player,enemies):
    death = False
    if (player.hitbox.bottom > 192):
        death = True
        return death

    enemy = pygame.sprite.spritecollideany(player,enemies,collided)
    if enemy:
        if ((player.rect.right - enemy.rect.left > 0) or (player.rect.left - enemy.rect.right < 0)):
            death = True
            return death
    return death


#rollback function to be used with spritecollideany() below
def collided(sprite, other):
    return sprite.hitbox.colliderect(other.hitbox)
    #return sprite.hitbox.bottom == other.hitbox.top or sprite.hitbox.colliderect(other.hitbox)

def move_player(mario, blocks,enemies,dead):

    global vertical_momentum
    global horizontal_momentum
    global air_timer
    global run_timer

    run_timer += 0.05

    x,y=0,0
    if(moving_right):
        if(horizontal_momentum < 0.7):
            horizontal_momentum += 0.1
        else:
            horizontal_momentum += 0.2
        if(horizontal_momentum > 2):
            horizontal_momentum = 2
        mario.set_img((int)(2 + horizontal_momentum * run_timer % 3))
    if(moving_left):
        if(horizontal_momentum > -0.7):
            horizontal_momentum -= 0.1
        else:
            horizontal_momentum -= 0.2
        if(horizontal_momentum < -2):
            horizontal_momentum = -2
        mario.set_img((int)(5 + horizontal_momentum * run_timer % 3))
    if not moving_left and not moving_right:
        if horizontal_momentum < -1:
            horizontal_momentum += 0.1
        elif horizontal_momentum > 1:
            horizontal_momentum -= 0.1
        else:
            horizontal_momentum = 0
            run_timer = 0
            mario.set_img(0)

    vertical_momentum += 0.2
    if(vertical_momentum > 4):
        vertical_momentum = 4

    x=horizontal_momentum
    y=vertical_momentum

    mario.update([x-scroll[0],0])
    col_block = pygame.sprite.spritecollideany(mario,blocks,collided)
    if(col_block):
        if x > 0:
            mario.rect.right = col_block.hitbox.left
        elif x < 0:
            mario.rect.left = col_block.hitbox.right

    mario.update([0,y-scroll[1]])
    col_block = pygame.sprite.spritecollideany(mario,blocks,collided)
    if(col_block and not dead):
        if y < 0:
            mario.rect.top = col_block.hitbox.bottom
            air_timer = 0
            vertical_momentum = 0
            if (col_block.breakable):
                blocks.remove(col_block)
        elif y > 0:
            mario.rect.bottom = col_block.hitbox.top
            air_timer = 0
            vertical_momentum = 0


    #collision between groups
    enemies.update(0,0.2,False)
    for enemy in enemies:
        col_block = pygame.sprite.spritecollideany(enemy,blocks,collided)
        if col_block:
            enemy.rect.bottom = col_block.hitbox.top
            enemy.vert_momentum = 0


    enemies.update(0,0,False)
    for enemy in enemies:
        col_block = pygame.sprite.spritecollideany(enemy,blocks,collided)
        if col_block:
            if enemy.dir > 0:
                enemy.rect.right = col_block.hitbox.left - 2
            elif enemy.dir < 0:
                enemy.rect.left = col_block.hitbox.right + 2
            enemy.dir *= -1


    air_timer += 1

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Pygame Platformer')

game_font=pygame.font.Font('freesansbold.ttf',40)

mario = entities.Player(55,82)
mario_bros = pygame.sprite.Group()
mario_bros.add(mario)
real_dead = False

map=level()

game=GUI(False)#The escape botton flag
game.start_menu()#Start with start game menu
world=overworld(True)#flag to open after start game menu

def enemy_AI(enemies,blocks):
    gumba_list = [i for i in map.enemies.sprites() if i.enemy_type==1]
    #turtle_list = [i for i in map.enemies.sprites() if i.enemy_type==2]
    for i in gumba_list:
        #i.vel[0]=piece_mob.dir-scroll[0]
        pass
        #print(i.vel[0])


while True:#Game loop
    game.display.fill((120,180,255))

    scroll[0] += mario.rect.center[0] - scroll[0] - 100
    #scroll[1] += mario.rect.center[1] - scroll[1] - 100
    map.blocks.update(-scroll[0],-scroll[1])
    map.blocks.draw(game.display)
    map.enemies.update(-scroll[0],0, True)

    dead = False
    if not real_dead:
        dead = check_death(mario,map.enemies)
    if(dead):
        real_dead = True
        vertical_momentum = -5
        moving_right = False
        moving_left = False
    if(real_dead and mario.rect.bottom > 230):
        break
    elif(real_dead):
        mario_bros.update([0,vertical_momentum])
        vertical_momentum += 0.1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if air_timer < 10:
                    vertical_momentum = -5
            if event.key == K_RIGHT:
                if not real_dead or dead:
                    moving_right = True
            if event.key == K_LEFT:
                if not real_dead or dead:
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
    move_player(mario,map.blocks,map.enemies,real_dead)

    #move_player(mario,map.blocks)

    #map.blocks.draw(game.display)
    mario_bros.draw(game.display)
    map.enemies.draw(game.display)


    #enemy_AI(map.enemies,map.blocks)

    game.screen.blit(pygame.transform.scale(game.display,game.WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)

game.dead = True
game.game_over_screen()
