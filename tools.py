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
                new_block = entities.Block(2,x*16,y*16,False)
                blocks.add(new_block)
            elif(tile == '1'):
                new_block = entities.Block(1,x*16,y*16,True)
                blocks.add(new_block)
            elif(tile == '3'):
                new_block = entities.Block(3,x*16,y*16,False)
                blocks.add(new_block)
            elif(tile=='4'):
                gumba = entities.Enemy(1,x*16,y*16)
                enemies.add(gumba)
            elif(tile=='5'):
                turtle = entities.Enemy(2,x*16,y*16)
                enemies.add(turtle)
            y += 1
        x+= 1

    return blocks, enemies
