import pygame

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

class Enemy(pygame.sprite.Sprite):#mario
    def __init__(self,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load("sprites/stand_right.gif")
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos,y_pos]
