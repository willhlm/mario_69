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

class Player(pygame.sprite.Sprite):#mario

    images = {0: pygame.image.load("sprites/stand_right.gif"),
            1: pygame.image.load("sprites/stand_left.gif"),
            2: pygame.image.load("sprites/run_right1.gif"),
            3: pygame.image.load("sprites/run_right2.gif"),
            4: pygame.image.load("sprites/run_right3.gif"),
            5: pygame.image.load("sprites/run_left1.gif"),
            6: pygame.image.load("sprites/run_left2.gif"),
            7: pygame.image.load("sprites/run_left3.gif"),
            }

    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = self.images[0]
        self.dir = 0 # 0 = right, 1 = left
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect

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
        else:
            self.image = self.images[val]

class Enemy(pygame.sprite.Sprite):
    images={1:pygame.image.load("sprites/gumba_1.gif"),
            2:pygame.image.load("sprites/turtle_1.gif")}#5
    vel = 1

    def __init__(self,img,x_pos,y_pos):
        super().__init__()
        self.image = self.images[img]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.enemy_type = img
        self.dir = 1 # -1 left, 1 right
        self.vert_momentum = 0
        self.hitbox = self.rect

    def update(self,x_pos,y_pos):

        if y_pos == 0:
            self.update_x(x_pos)
        elif x_pos == 0:
            self.vert_momentum += y_pos
            self.update_y(y_pos)

    def update_x(self,x_pos):
        self.rect.topleft = [self.rect.topleft[0] + (self.vel * self.dir) + x_pos, self.rect.topleft[1]]
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
