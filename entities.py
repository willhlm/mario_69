import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self,block_path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(block_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
        self.hitbox = self.rect.inflate(0,0)

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]
        self.hitbox = self.rect.inflate(0,0)

class Player(pygame.sprite.Sprite):#mario

    stand_right = pygame.image.load("sprites/stand_right.gif")
    stand_left = pygame.image.load("sprites/stand_left.gif")

    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = self.stand_right
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
        if(val == 0):
            self.image = self.stand_right
        elif(val == 1):
            self.image = self.stand_left

class Enemy(pygame.sprite.Sprite):#mario
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load("sprites/stand_right.gif")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]

    def update(self,x_pos,y_pos):
        self.rect.topleft = [self.rect.topleft[0] + x_pos, self.rect.topleft[1] + y_pos]
