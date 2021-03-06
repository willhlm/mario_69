import pygame

class Block(pygame.sprite.Sprite):

    images = {1 : pygame.image.load("sprites/brick.gif"),
            2 : pygame.image.load("sprites/ground.gif"),
            3 : pygame.image.load("sprites/block.gif"),
            4 : pygame.image.load("sprites/block_question.png"),
            5 : pygame.image.load("sprites/block_castle.png"),
            }

    def __init__(self,img,x_pos,y_pos,breakable,item):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect.inflate(0,0)
        self.breakable = breakable
        self.item=item

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]
        self.hitbox = self.rect.inflate(0,0)

class BG_object(pygame.sprite.Sprite):

    images = {0: pygame.image.load("sprites/hill.gif"),
              1: pygame.image.load("sprites/cloud1.gif"),
              2: pygame.image.load("sprites/castle_brick.gif"),
              3: pygame.image.load("sprites/castle_top.gif"),
              4: pygame.image.load("sprites/castle_top2.gif"),
              5: pygame.image.load("sprites/castle_window.gif"),
              6: pygame.image.load("sprites/block_castleBG.png")
              }

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]

class Goal(pygame.sprite.Sprite):

    images = {0: pygame.image.load("sprites/castle_door.gif"),
            1: pygame.image.load("sprites/peach.gif")}

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]
        self.hitbox = self.rect

class Easter_egg(pygame.sprite.Sprite):
    images={0: pygame.image.load("sprites/toad.gif")}
    text={1:'Hey Mario! You know Johan sucks right?',
          2: 'I will grant you the abillity to dress as bowser'}

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect.copy()
        self.letter=1
        self.print=Easter_egg.text

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]
        self.hitbox = self.rect

class Player(pygame.sprite.Sprite):#mario

    images = {0: pygame.image.load("sprites/stand_right.gif"),
            1: pygame.image.load("sprites/stand_left.gif"),
            2: pygame.image.load("sprites/run_right1.gif"),
            3: pygame.image.load("sprites/run_right2.gif"),
            4: pygame.image.load("sprites/run_right3.gif"),
            5: pygame.image.load("sprites/run_left1.gif"),
            6: pygame.image.load("sprites/run_left2.gif"),
            7: pygame.image.load("sprites/run_left3.gif"),
            8: pygame.image.load("sprites/dead.png"),
            9: pygame.image.load("sprites/jump_right.png"),
            10: pygame.image.load("sprites/jump_left.png"),
            }

    IMAGES = {0: pygame.image.load("sprites/stand_right_big.png"),
            1: pygame.image.load("sprites/stand_left_big.png"),
            2: pygame.image.load("sprites/run_right1_big.png"),
            3: pygame.image.load("sprites/run_right2_big.png"),
            4: pygame.image.load("sprites/run_right3_big.png"),
            5: pygame.image.load("sprites/run_left1_big.png"),
            6: pygame.image.load("sprites/run_left2_big.png"),
            7: pygame.image.load("sprites/run_left3_big.png"),
            8: pygame.image.load("sprites/dead.png"),
            9: pygame.image.load("sprites/jump_right_big.png"),
            10: pygame.image.load("sprites/jump_left_big.png"),
            }


    IMAGES_flower = {0: pygame.image.load("sprites/stand_right_flower.gif"),
            1: pygame.image.load("sprites/stand_left_flower.gif"),
            2: pygame.image.load("sprites/run_right1_flower.gif"),
            3: pygame.image.load("sprites/run_right2_flower.gif"),
            4: pygame.image.load("sprites/run_right3_flower.gif"),
            5: pygame.image.load("sprites/run_left1_flower.gif"),
            6: pygame.image.load("sprites/run_left2_flower.gif"),
            7: pygame.image.load("sprites/run_left3_flower.gif"),
            8: pygame.image.load("sprites/dead.png"),
            9: pygame.image.load("sprites/jump_right_flower.gif"),
            10: pygame.image.load("sprites/jump_left_flower.gif"),
            }
    IMAGES_B={0: pygame.image.load("sprites/bowser_right1.gif"),
            1: pygame.image.load("sprites/bowser_left1.gif"),
            2: pygame.image.load("sprites/bowser_right1.gif"),
            3: pygame.image.load("sprites/bowser_right2.gif"),
            4: pygame.image.load("sprites/bowser_right3.gif"),
            5: pygame.image.load("sprites/bowser_left1.gif"),
            6: pygame.image.load("sprites/bowser_left2.gif"),
            7: pygame.image.load("sprites/bowser_left3.gif"),
            8: pygame.image.load("sprites/bowser_left1.gif"),
            9: pygame.image.load("sprites/bowser_right1.gif"),
            10: pygame.image.load("sprites/bowser_left1.gif")}

    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = self.images[0]
        self.dir = 0 # 0 = right, 1 = left
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect.copy()
        self.life=3
        self.dead=False
        self.small=True
        self.hit_timer=30
        self.flower=False
        self.bowser=False

    def update(self,pos):
        self.rect.topleft = [self.rect.topleft[0] + pos[0], self.rect.topleft[1] + pos[1]]
        self.hitbox = self.rect

    def set_img(self,val):
        # 0 = stand right
        # 1 = stand left
        # 2 - 4 = running right
        # 5 - 7 = running left
        if self.bowser==True:
            self.images=Player.IMAGES_B
            self.IMAGES=Player.IMAGES_B
            self.IMAGES_flower=Player.IMAGES_B
        else:
            self.images=Player.images
            self.IMAGES=Player.IMAGES
            self.IMAGES_flower=Player.IMAGES_flower

        if self.small:
            if(val in range(2,4)):
                self.dir = 0
            elif(val in range(5,7)):
                self.dir = 1
            if(val == 0):
                self.image = self.images[self.dir]
            elif(val == 1):
                self.image = self.images[self.dir + 9]
            else:
                self.image = self.images[val]
        elif not self.small and not self.flower:
            if(val in range(2,4)):
                self.dir = 0
            elif(val in range(5,7)):
                self.dir = 1
            if(val == 0):
                self.image = self.IMAGES[self.dir]
            elif(val == 1):
                self.image = self.IMAGES[self.dir + 9]
            else:
                self.image = self.IMAGES[val]
        elif self.flower:
                if(val in range(2,4)):
                    self.dir = 0
                elif(val in range(5,7)):
                    self.dir = 1
                if(val == 0):
                    self.image = self.IMAGES_flower[self.dir]
                elif(val == 1):
                    self.image = self.IMAGES_flower[self.dir + 9]
                else:
                    self.image = self.IMAGES_flower[val]

class Enemy(pygame.sprite.Sprite):
    vel = 1

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.dir = -1 # -1 left, 1 right
        self.vert_momentum = 0
        self.hitbox = self.rect.copy()
        self.enemy_type=img
        self.jump=False
        self.alive=True
        self.no_kill=40

    def update(self,x_pos,y_pos,scroll):
        if (scroll):
            self.update_scroll(x_pos)
        elif y_pos == 0:
            self.update_x()
        elif x_pos == 0:
            self.vert_momentum += y_pos
            self.update_y(y_pos)

    def update_x(self):
        self.rect.topleft = [self.rect.topleft[0] + (self.vel * self.dir), self.rect.topleft[1]]
        self.hitbox = self.rect

    def update_scroll(self,x_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1]]
        #self.rect.topleft = [self.rect.topleft[0], self.rect.topleft[1]]
        self.hitbox = self.rect

    def update_y(self,y_pos):
        self.rect.topleft = [self.rect.topleft[0], self.rect.topleft[1] + self.vert_momentum]
        self.hitbox = self.rect

    def set_img(self,val):
        # 0 = stand right
        # 1 = stand left
        # 2 - 4 = running right
        # 5 - 7 = running left
        if(val in range(2,4)):
            self.dir = self.images[val]
        elif(val in range(5,7)):
            self.dir = self.images[val]

class Gumba(Enemy):
    images={1:pygame.image.load("sprites/gumba_1.gif"),
            2:pygame.image.load("sprites/gumba_2.gif"),
            3:pygame.image.load("sprites/gumba_3.gif")}

    def __init__(self,img,x_pos,y_pos):
        super().__init__(img,x_pos,y_pos)
        self.frame=1
        self.dead_time=0

    def set_img(self,img):
        self.image = self.images[img]

class Turtle(Enemy):
    vert=-3
    images={1:pygame.image.load("sprites/turtle_1.gif"),
            2:pygame.image.load("sprites/turtle_2.gif"),
            3:pygame.image.load("sprites/turtle_3.gif"),
            4:pygame.image.load("sprites/turtle_4.gif"),
            5:pygame.image.load("sprites/turtle_5.gif"),
            6:pygame.image.load("sprites/turtle_6.gif")}

    def __init__(self,img,x_pos,y_pos,jump):
        super().__init__(img,x_pos,y_pos)
        self.frame=1
        self.dead_time=0
        self.jump=jump
        #self.alive=True

    def set_img(self,img):
        if self.jump:
            if self.dir>0:
                self.image=self.images[5]
            else:
                self.image=self.images[6]
        else:
            if self.dir>0:
                self.image=self.images[img]
            else:
                self.image=self.images[img+2]
    def hop(self):
        self.rect.topleft = [self.rect.topleft[0], self.rect.topleft[1] + Turtle.vert]
        self.hitbox = self.rect

class Bowser(Enemy):
    vel=1

    images={1:pygame.image.load("sprites/bowser_left1.gif"),
            2:pygame.image.load("sprites/bowser_left2.gif"),
            3:pygame.image.load("sprites/bowser_left3.gif"),
            4:pygame.image.load("sprites/bowser_left4.gif")}

    def __init__(self,img,x_pos,y_pos):
        super().__init__(img,x_pos,y_pos)
        self.frame=0
        self.dead_time=0
        self.enemy_type=-1
        self.life=3

    def set_img(self,img):
        self.image = self.images[img]

    def movement(self,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + self.vel*self.dir, self.rect.topleft[1]+y_pos]


class items(Enemy):#shrooms
    images = {1 : pygame.image.load("sprites/item_redmushroom.png"),
            2 : pygame.image.load("sprites/item_greenmushroom.png"),
            3: pygame.image.load("sprites/item_flower.png"),}

    def __init__(self,img,x_pos,y_pos):
        super().__init__(img,x_pos,y_pos)
        self.id=img
        self.image = self.images[img]

class projectile(pygame.sprite.Sprite):
    images={1:pygame.image.load("sprites/item_flowerball.gif"),
            2:pygame.image.load("sprites/bowser_left_projectile.gif")}
    number_of_balls=0
    vel=2

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        #self.hitbox = self.rect.copy()
        self.number_of_balls+=1
        self.timer=0
        self.vert_momentum = 3
        self.hitbox = self.rect.copy()
        self.dir=-2
        self.temp=self.rect.top
        self.type=img

    def update(self):# dir 0 = right, 1 = left
        self.rect.topleft = [self.rect.topleft[0] + self.dir*projectile.vel, self.rect.topleft[1] + self.vert_momentum]
