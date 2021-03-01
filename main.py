import pygame, sys, random, tools, entities
from pygame import mixer#sounds
from pygame.locals import *

air_timer = 0
run_timer = 0
moving_right = False
moving_left = False
sprint = False
jump_trigger = False
on_ground = False
horizontal_momentum = 0
vertical_momentum = 0
true_scroll = [0,0]
scroll = [0,0]

mario_bros = pygame.sprite.Group()
blocks = pygame.sprite.Group()
enemies = pygame.sprite.Group()
flower_balls = pygame.sprite.Group()

class GUI():

    BG_surface=pygame.transform.scale(pygame.image.load('sprites/start_meny_2.jpg'),(1000,600))
    BG_cloud=pygame.image.load('sprites/cloud1.gif')
    dead=pygame.transform.scale(pygame.image.load('sprites/dead.png'),(100,100))

    def __init__(self,ESC,click=False):
        self.ESC=ESC
        self.click=click
        self.display_height = 176
        self.display_width = 320
        self.gameover = False

        self.scale = 3
        self.WINDOW_SIZE = (self.display_width*self.scale,self.display_height*self.scale)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE,0,32) # initiate the window
        self.display = pygame.Surface((self.display_width,self.display_height)) # used as the surface for rendering, which is scaled

    def start_menu(self,first=True):#escape botton
        x=[]#placeholder
        y=[]
        for i in range(0,20):
            y.append(random.randint(0,400))
            x.append(random.randint(0,900))

        while self.ESC or first:

            if first:#on boot
                text='Start Game'
            else:#on esc button
                text='Resume Game'

            start_surface=game_font.render(text,True,(255,255,255))#antialias flag
            start_rect=start_surface.get_rect(center=(200,100))#position
            exit_surface=game_font.render('Exit game',True,(255,255,255))#antialias flag
            exit_rect=start_surface.get_rect(center=(200,400))#position

            pygame.draw.rect(game.screen,(255,255,255),start_rect,width=2)
            pygame.draw.rect(game.screen,(255,255,255),exit_rect,width=2)

            if start_rect.collidepoint((pygame.mouse.get_pos())) ==True and self.click==True:
                self.ESC=False
                self.click=False
                first=False
            elif exit_rect.collidepoint((pygame.mouse.get_pos())) ==True and self.click==True:
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.click=True
                if event.type==pygame.MOUSEBUTTONUP:
                    self.click=False

            game.screen.blit(self.BG_surface,(0,0))
            for i in range(0,20):
                x[i]+=0.5
                if x[i]>1000:
                    x[i]=-50
                game.screen.blit(self.BG_cloud,(x[i],y[i]))

            game.screen.blit(start_surface,start_rect)
            game.screen.blit(exit_surface,exit_rect)

            pygame.display.update()

    def game_over_screen(self):
        game.screen.fill((0,0,0))
        go_surface=game_font.render("Game Over",True,(255,255,255))#antialias flag
        go_rect=go_surface.get_rect(center=(450,250))#position
        #pygame.draw.rect(game.screen,(0,0,0),go_rect)
        game.screen.blit(go_surface,go_rect)
        game.screen.blit(self.dead,(400,300))

        while self.gameover:
            pygame.display.update()
            clock.tick(60)


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        game.gameover=False#to exit game over
                        mario.life=3
                        mario.dead=False
                        mario.hitbox.bottom=100
                        game.start_menu()#back to start
                        world.active=True
                        world.world_select()

class overworld():#level selection stuff
    castle_pos=800

    def __init__(self,active,click=False):
        #super().__init__(ESC,click=False)
        self.active=active
        self.click=click

    @staticmethod
    def draw_map(int):

        if map.level>int+1:#complete castle
            level_surface=pygame.transform.scale(pygame.image.load('sprites/overworld_complete'+'.png'),(200,200))
            level_rect=level_surface.get_rect(midbottom=(200+int*300,520))#position
        else:#new castle
            if overworld.castle_pos<520:
                overworld.castle_pos=520
            level_surface=pygame.transform.scale(pygame.image.load('sprites/overworld_castle_'+str(int+1)+'.png'),(200,200))
            level_rect=level_surface.get_rect(midbottom=(200+int*300,overworld.castle_pos))#position
            overworld.castle_pos-=1
        return level_surface,level_rect


    def world_select(self):
        x=[]#placeholder
        y=[]
        for i in range(0,20):
            y.append(random.randint(0,400))
            x.append(random.randint(0,900))

        while self.active:
            game.screen.blit(GUI.BG_surface,(0,0))

            for i in range(0,20):
                x[i]+=1
                if x[i]>1000:
                    x[i]=-50
                game.screen.blit(GUI.BG_cloud,(x[i],y[i]))

            for i in range(0,map.level):
                level_surface,level_rect=overworld.draw_map(i)

                text_surface=game_font.render('Level '+str(i+1),True,(255,255,255))#antialias flag
                text_rect=text_surface.get_rect(center=(200+i*300,500))#position

                game.screen.blit(level_surface,level_rect)
                game.screen.blit(text_surface,text_rect)

                if level_rect.collidepoint((pygame.mouse.get_pos())) ==True and self.click==True:
                    self.active=False
                    self.click=False
                    map.select_level(i+1)
                    self.level=i+1


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
        self.level=1
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bg_objects = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.clear = False
        self.items=pygame.sprite.Group()
        self.bg_color=(92,148,252)

    def select_level(self,level):
        self.cur_level=level
        self.blocks, self.enemies, self.bg_objects, self.goals ,self.items= tools.load_level("levels/level"+str(level))

def re_spawn():#restart the whole level
    global vertical_momentum
    global horizontal_momentum

    vert_momentum = 0
    horizontal_momentum = 0

    mario.rect.topleft=[55,82]
    mario.hitbox=mario.rect
    mario.dead=False
    #mario.update([255,82])
    map.blocks=[]

    map.select_level(world.level)

def check_goal(player,goals):
    global vertical_momentum
    global horizontal_momentum
    global moving_left
    global moving_right

    goal = pygame.sprite.spritecollideany(player,goals,collided)
    if goal:
        if abs(player.rect.right - goal.rect.right) < 5:
            vertical_momentum = 0
            horizontal_momentum = 0
            moving_left = False
            moving_right = False
            map.clear = True
            if map.level==map.cur_level:
                map.level+=1
                overworld.castle_pos=800
            if map.level>=3:
                map.level=3
            goal_animation()

def check_death(player,enemies,flower_balls):
    if (mario.hitbox.bottom > 192):
        mario.dead = True
        mario.life-=1
        death_animation()
        mario.small=True
        mario.flower=False
        update_hitbox()


    #bowser balls
    ball_list = [i for i in flower_balls.sprites() if i.type==2]#bowser ball
    if ball_list:
        for i in ball_list:
            if i.rect.colliderect(player.rect):
                if player.small and player.hit_timer>30:#small
                    mario.life-=1
                    mario.dead = True
                    death_animation()
                elif not player.small and not player.flower and player.hit_timer>30:
                    player.small=True
                    player.hit_timer=0
                    start_timer()
                    update_hitbox()
                elif player.flower:
                    player.flower=False
                    player.hit_timer=0
                    start_timer()

    enemy = pygame.sprite.spritecollideany(player,enemies,collided)
    if enemy and player.small and player.hit_timer>30 and enemy.no_kill>30:
        if ((player.rect.right - enemy.rect.left > 0) and enemy.alive==True or (player.rect.left - enemy.rect.right < 0) and enemy.alive==True):
            mario.dead = True
            mario.life-=1
            player.hit_timer=0
            start_timer()
            death_animation()

    if enemy and not player.small and not player.flower and player.hit_timer>30 and enemy.no_kill>30:#shrrom
        if ((player.rect.right - enemy.rect.left > 0) and enemy.alive==True or (player.rect.left - enemy.rect.right < 0) and enemy.alive==True):
            player.hit_timer=0
            mario.small=True
            start_timer()
            update_hitbox()

    if enemy and player.flower and enemy.no_kill>30:#flower
        if ((player.rect.right - enemy.rect.left > 0) and enemy.alive==True or (player.rect.left - enemy.rect.right < 0) and enemy.alive==True):
            player.hit_timer=0
            mario.flower=False
            start_timer()

#rollback function to be used with spritecollideany() below
def collided(sprite, other):
    if (sprite == other):
        return False
    else:
        return sprite.hitbox.colliderect(other.hitbox)
    #return sprite.hitbox.bottom == other.hitbox.top or sprite.hitbox.colliderect(other.hitbox)
def start_timer():
    mario.hit_timer+=1

def move_player(mario, blocks,enemies,items,flower_balls):

    global vertical_momentum
    global horizontal_momentum
    global air_timer
    global run_timer
    global sprint

    run_timer += 0.05

    speed_cap = 2
    if sprint:
        speed_cap = 4

    x,y=0,0
    if(moving_right):
        if(horizontal_momentum < 0.7):
            horizontal_momentum += 0.1
        else:
            horizontal_momentum += 0.1
        if (horizontal_momentum > speed_cap + 0.3):
            horizontal_momentum -= 0.2
        elif (horizontal_momentum > speed_cap):
            horizontal_momentum = speed_cap
        mario.set_img((int)(2 + abs(horizontal_momentum) * run_timer % 3))
    if(moving_left):
        if(horizontal_momentum > -0.7):
            horizontal_momentum -= 0.1
        else:
            horizontal_momentum -= 0.1
        if (horizontal_momentum < -1*speed_cap - 0.3):
            horizontal_momentum += 0.2
        elif (horizontal_momentum < -1*speed_cap):
            horizontal_momentum = -1*speed_cap
        mario.set_img((int)(5 + abs(horizontal_momentum) * run_timer % 3))
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

    if(air_timer > 5):
        mario.set_img(1)


    mario.update([x-scroll[0],0])
    col_block = pygame.sprite.spritecollideany(mario,blocks,collided)
    if(col_block):
        if x > 0:
            mario.rect.right = col_block.hitbox.left
            horizontal_momentum /= 2
        elif x < 0:
            mario.rect.left = col_block.hitbox.right
            horizontal_momentum /= 2

    mario.update([0,y-scroll[1]])
    col_block = pygame.sprite.spritecollideany(mario,blocks,collided)
    if(col_block and not mario.dead):
        if y < 0:
            mario.rect.top = col_block.hitbox.bottom
            air_timer = 0
            vertical_momentum = 0
            if (col_block.breakable):
                blocks.remove(col_block)
            elif col_block.item!=0:#make an item
                pos=[col_block.rect.topleft[0], col_block.rect.topleft[1]]
                items.add(entities.items(col_block.item,pos[0],pos[1]))#spawn the item
                col_block.item=False
                col_block.image=col_block.images[3]

        elif y > 0:
            mario.rect.bottom = col_block.hitbox.top
            air_timer = 0
            vertical_momentum = 0

    #stomp
    col_enemy = pygame.sprite.spritecollideany(mario,enemies,collided=None)
    if (col_enemy and not mario.dead):#stomp
        if y>1 and mario.rect.bottom > col_enemy.rect.top:#stomp
            if col_enemy.jump:
                col_enemy.no_kill=1
                col_enemy.jump=False
                vertical_momentum=-2#mario
                mario.hit_timer=0
                start_timer()

            else:
                col_enemy.alive=False
                vertical_momentum=-2#mario

            if col_enemy.enemy_type==-1:#if it is bowser
                col_enemy.life-=1
                if col_enemy.life<=0:
                    col_enemy.kill()


    #collision between groups
    enemies.update(0,0.2,False)
    items.update(0,0.2,False)

    for item in items:
        col_block = pygame.sprite.spritecollideany(item,blocks,collided)
        if col_block:
            item.rect.bottom = col_block.hitbox.top
            item.vert_momentum = 0


    for enemy in enemies:
        col_block = pygame.sprite.spritecollideany(enemy,blocks,collided)
        if col_block:
            enemy.rect.bottom = col_block.hitbox.top
            enemy.vert_momentum = 0

    #ball block collision
    for ball in flower_balls:
        col_block = pygame.sprite.spritecollideany(ball,blocks,collided=None)
        if col_block:
            ball.rect.bottom = col_block.hitbox.top
            ball.vert_momentum = -5
            if ball.rect.top<ball.temp:#kill ball if collide with block from side
                ball.kill()

    #ball enemy collisions
    for ball in flower_balls:
        col_enemy = pygame.sprite.spritecollideany(ball,enemies,collided=None)
        if col_enemy:
            ball.kill()
            if col_enemy.jump:
                col_enemy.jump=False
            else:
                if col_enemy.enemy_type==-1:#bowswer
                    col_enemy.life-=1
                    if col_enemy.life<=0:
                        col_enemy.kill()
                else:
                    col_enemy.kill()



    enemies.update(0,0,False)
    items.update(0,0,False)
    flower_balls.update()

    for item in items:
        col_block = pygame.sprite.spritecollideany(item,blocks,collided)
        if col_block:
            if item.dir > 0:
                item.rect.right = col_block.hitbox.left - 2
            elif item.dir < 0:
                item.rect.left = col_block.hitbox.right + 2
            item.dir *= -1

    for item in items:
        col_block = pygame.sprite.spritecollideany(item,enemies,collided)
        if col_block:
            if item.dir > 0:
                item.rect.right = col_block.hitbox.left - 2
            elif item.dir < 0:
                item.rect.left = col_block.hitbox.right + 2
            item.dir *= -1
            col_block.dir *= -1

    for enemy in enemies:
        col_block = pygame.sprite.spritecollideany(enemy,blocks,collided)
        if col_block:
            if enemy.dir > 0:
                enemy.rect.right = col_block.hitbox.left - 2
            elif enemy.dir < 0:
                enemy.rect.left = col_block.hitbox.right + 2
            enemy.dir *= -1

    for enemy in enemies:
        col_block = pygame.sprite.spritecollideany(enemy,enemies,collided)
        if col_block:
            if enemy.dir > 0:
                enemy.rect.right = col_block.rect.left - 2
            elif enemy.dir < 0:
                enemy.rect.left = col_block.rect.right + 2
            enemy.dir *= -1
            col_block.dir *= -1

    #collision between mario and items
    item = pygame.sprite.spritecollideany(mario,items,collided)
    if item:
        if ((mario.rect.right - item.rect.left > 0) and item.alive==True or (mario.rect.left - item.rect.right < 0) and item.alive==True):

            item.kill()
            if mario.small and item.id==1:#red shrrom
                grow_animation()
                update_hitbox()
            elif item.id==2:#green shrrom
                mario.life+=1
            elif item.id==3:#flower
                mario.flower=True
                if mario.small:
                    grow_animation()
                    update_hitbox()
    air_timer += 1


    ball_list = [i for i in flower_balls.sprites()]
    for i in ball_list:
        i.timer+=1
        i.vert_momentum+=1
        if i.timer>50:
            i.kill()

def update_hitbox():
    if mario.small:#insert small mario hitbox
        mario.image = mario.images[0]
        mario.rect = mario.image.get_rect(midbottom=mario.rect.midbottom)
    else:#insert large mario hitbox
        mario.image = mario.IMAGES[0]
        mario.rect = mario.image.get_rect(midbottom=mario.rect.midbottom)

def grow_animation():
    j=0
    Frame=[True,False]
    global horizontal_momentum
    global vertical_momentum
    vertical_momentum=0
    horizontal_momentum=0
    for i in range(6):
        if j>1:
            j=0
        mario.set_img(j)
        pygame.time.wait(150)
        mario.small=Frame[j]
        draw()
        j+=1#wink

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Pygame Platformer')

game_font=pygame.font.Font('freesansbold.ttf',40)

mario = entities.Player(55,82)
mario_bros = pygame.sprite.Group()
mario_bros.add(mario)

map=level()

game=GUI(False)#The escape botton flag
game.start_menu()#Start with start game menu
world=overworld(True)#flag to open after start game menu

def enemy_animation(enemies):
    gumba_list = [i for i in map.enemies.sprites() if i.enemy_type==1]
    turtle_list = [i for i in map.enemies.sprites() if i.enemy_type==2]
    bowser=[i for i in map.enemies.sprites() if i.enemy_type==-1]

    if bowser:#if not empty
        bowser[0].set_img(bowser[0].frame//10+1)
        bowser[0].frame+=1
        if bowser[0].frame>18:
            bowser[0].frame=0

        if random.randint(0,100)<2:
            bowser[0].dir*=-1#5% chance to change dir

            flower_balls.add(entities.projectile(2,bowser[0].rect.center[0]-50,bowser[0].rect.center[1]))#spawn the item
            ball_list = [i for i in flower_balls.sprites() if i.type==2]
            for i in ball_list:
                i.vert_momentum=0


    for i in gumba_list:
        if i.alive:
            if i.frame>=20:
                i.frame=0
            i.set_img(i.frame//10+1)
            i.frame+=1
        elif i.alive==False:
            i.set_img(3)
            i.dead_time+=1
            i.hitbox=[0,0]
            i.vel=0
            i.rect.bottom += 3
            if i.dead_time>20:
                i.kill()

    for i in turtle_list:
        if i.no_kill>0:
            i.no_kill+=1
        if i.jump:#jumping
            i.vert+=1
            i.hop()
            if i.vert>3:
                i.vert=-3

        if i.alive:
            if i.frame>=20:
                i.frame=0
            i.set_img(i.frame//10+1)
            i.frame+=1
        elif i.alive==False:
            #i.set_img(3)
            i.dead_time+=1
            i.vel=0
            if i.dead_time>10:
                i.kill()

def death_animation():
    global moving_right
    global moving_left

    dead_ani = -5
    moving_right = False
    moving_left = False
    mario.set_img(8)

    while mario.rect.bottom<230:
        draw()
        mario_bros.update([0,dead_ani])
        dead_ani += 0.2

        pygame.time.wait(10)

    re_spawn()

def goal_animation():
    if map.cur_level!=3:
        flag_surface=pygame.image.load('sprites/castleflag_complete.png')
        i=0

        mario.set_img(0)
        pygame.display.update()
        pygame.time.wait(300)

        #remove mario
        while i<20:
            flag_rect=flag_surface.get_rect(center=(320,200-i))#position
            i+=1
            pygame.time.wait(50)

            #draw except mario
            game.display.fill(map.bg_color)
            map.bg_objects.draw(game.display)
            map.blocks.draw(game.display)
            map.goals.draw(game.display)
            map.enemies.draw(game.display)
            map.items.draw(game.display)
            game.screen.blit(pygame.transform.scale(game.display,game.WINDOW_SIZE),(0,0))
            game.screen.blit(flag_surface,flag_rect)
            pygame.display.update()
        pygame.time.wait(500)

    elif map.cur_level==3:
        pygame.time.wait(500)
        text='Oh mario you are the best. Now let us close this game, so that I can give you a BJ!'
        j=0
        h=0
        for i in text:

            pygame.time.wait(50)

            if i=='.' or i==',':
                h+=40
                j=0

            text_surface=game_font.render(i,True,(255,255,255))#antialias flag
            text_rect=text_surface.get_rect(center=(100+j,100+h))#position

            game.screen.blit(text_surface,text_rect)

            pygame.display.update()
            j+=25
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

def shoot_balls():
    if len(flower_balls)<2:
        flower_balls.add(entities.projectile(1,mario.rect.center[0],mario.rect.center[1]))#spawn the item
        ball_list = [i for i in flower_balls.sprites() if i.type==1]
        for i in ball_list:
            if i.dir==-2 and mario.dir==1:
                i.dir=-1
            elif i.dir==-2 and mario.dir==0:
                i.dir=1

def life_display():#fix
        score_surface=game_font.render(f'Life: {mario.life}',True,(255,255,255))#antialias flag
        score_rect=score_surface.get_rect(center=(100,50))
        game.screen.blit(score_surface,score_rect)

def draw():
    if map.cur_level==3:
        map.bg_color=(0,0,0)
    game.display.fill(map.bg_color)
    map.bg_objects.draw(game.display)
    map.blocks.draw(game.display)
    map.goals.draw(game.display)
    mario_bros.draw(game.display)
    map.enemies.draw(game.display)
    map.items.draw(game.display)
    flower_balls.draw(game.display)
    game.screen.blit(pygame.transform.scale(game.display,game.WINDOW_SIZE),(0,0))
    life_display()
    pygame.display.update()

while True:#Game loop
    scroll[0] += mario.rect.center[0] - scroll[0] - 100
    #scroll[1] += mario.rect.center[1] - scroll[1] - 100
    map.blocks.update(-scroll[0],-scroll[1])
    map.bg_objects.update(-scroll[0],-scroll[1])
    map.goals.update(-scroll[0],-scroll[1])
    map.enemies.update(-scroll[0],0, True)
    map.items.update(-scroll[0],-scroll[1],True)

    check_death(mario, map.enemies,flower_balls)
    check_goal(mario, map.goals)

    if map.clear:
        map.clear = False
        world.active=True
        #game.gameover=True
        world.world_select()

    if mario.life<=0:
        game.gameover=True
        game.game_over_screen()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if air_timer < 10:
                    if sprint:
                        vertical_momentum = -5
                    else:
                        vertical_momentum = -4.2
            if event.key == K_RIGHT and not mario.dead:
                moving_right = True
            if event.key == K_LEFT and not mario.dead:
                moving_left = True
            if event.key == K_LSHIFT:
                sprint = True
            if event.key==pygame.K_ESCAPE:
                game.ESC=True
            if event.key==pygame.K_f and mario.flower:
                shoot_balls()

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_LSHIFT:
                sprint = False



    game.start_menu(False)
    world.world_select()

    move_player(mario,map.blocks,map.enemies,map.items,flower_balls)
    enemy_animation(map.enemies)
    if mario.hit_timer!=0:
        start_timer()

    draw()
    clock.tick(60)
