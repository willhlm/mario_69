import pygame

class Block(pygame.sprite.Sprite):

    images = {1 : pygame.image.load("sprites/brick.gif"),
            2 : pygame.image.load("sprites/ground.gif"),
            3 : pygame.image.load("sprites/block.gif"),
            }

    def __init__(self,img,x_pos,y_pos,breakable):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect.inflate(0,0)
        self.breakable = breakable

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]
        self.hitbox = self.rect.inflate(0,0)

class BG_object(pygame.sprite.Sprite):

    images = {0: pygame.image.load("sprites/hill.gif"),
              1: pygame.image.load("sprites/cloud1.gif"),
              2: pygame.image.load("sprites/castle_brick.gif"),
              3: pygame.image.load("sprites/castle_top.gif"),
              4: pygame.image.load("sprites/castle_top2.gif"),
              5: pygame.image.load("sprites/castle_window.gif")
              }

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]

class Goal(pygame.sprite.Sprite):

    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load("sprites/castle_door.gif")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect

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

    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = self.images[0]
        self.dir = 0 # 0 = right, 1 = left
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect.copy()
        self.life=3
        self.dead=False

    def update(self,pos):
        self.rect.topleft = [self.rect.topleft[0] + pos[0], self.rect.topleft[1] + pos[1]]
        self.hitbox = self.rect

    def set_img(self,val):
        # 0 = stand right
        # 1 = stand left
        # 2 - 4 = running right
        # 5 - 7 = running left
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
        self.alive=True
        self.dead_time=0

    def set_img(self,img):
        self.image = self.images[img]

class Turtle(Enemy):
    images={1:pygame.image.load("sprites/turtle_1.gif"),
            2:pygame.image.load("sprites/turtle_2.gif"),
            3:pygame.image.load("sprites/turtle_3.gif"),
            4:pygame.image.load("sprites/turtle_4.gif")}

    def __init__(self,img,x_pos,y_pos):
        super().__init__(img,x_pos,y_pos)
        self.frame=1
        self.alive=True
        self.dead_time=0

    def set_img(self,img):
        if self.dir>0:
            self.image=self.images[img]
        else:
            self.image=self.images[img+2]
