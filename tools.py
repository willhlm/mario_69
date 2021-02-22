import pygame, entities

ground_img = "sprites/ground.gif"

def load_level(path):

    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))

    blocks = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    x = 0
    for column in game_map:
        y = 0
        for tile in column:
            if(tile == '2'):
                new_block = entities.Block(ground_img,x*16,y*16)
                blocks.add(new_block)
            y += 1
        x+= 1

    return blocks, enemies
