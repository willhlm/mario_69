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
    bg_objects = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    items=pygame.sprite.Group()

    x = 0
    for column in game_map:
        y = 0
        for tile in column:
            if(tile == '2'):
                new_block = entities.Block(2,x*16,y*16,False,0)
                blocks.add(new_block)
            elif(tile == '1'):
                new_block = entities.Block(1,x*16,y*16,True,0)
                blocks.add(new_block)
            elif(tile == '3'):
                new_block = entities.Block(3,x*16,y*16,False,0)
                blocks.add(new_block)
            elif(tile=='4'):
                gumba = entities.Gumba(1,x*16,y*16)
                enemies.add(gumba)
            elif(tile=='5'):
                turtle = entities.Turtle(2,x*16,y*16,False)
                enemies.add(turtle)
            elif(tile=='6'):
                turtle = entities.Turtle(2,x*16,y*16,True)
                enemies.add(turtle)
            elif(tile=='a'):
                new_bg_obj = entities.BG_object(0,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='b'):
                new_bg_obj = entities.BG_object(1,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='7'):
                new_item = entities.items(1,x*16,y*16)
                items.add(new_item)
            elif(tile=='8'):
                new_block = entities.Block(4,x*16,y*16,False,1)
                blocks.add(new_block)
            elif(tile=='9'):
                new_block = entities.Block(4,x*16,y*16,False,2)
                blocks.add(new_block)
            elif(tile=='p'):
                new_block = entities.Block(4,x*16,y*16,False,3)#flower block
                blocks.add(new_block)
            elif(tile=='s'):
                new_block = entities.Block(5,x*16,y*16,False,0)#flower block
                blocks.add(new_block)
            elif(tile=='j'):
                new_bg_obj = entities.BG_object(6,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='m'):
                bowser = entities.Bowser(2,x*16,y*16)
                enemies.add(bowser)

            #next 5 are for the castle
            elif(tile=='c'):
                new_bg_obj = entities.BG_object(2,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='d'):
                new_bg_obj = entities.BG_object(3,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='e'):
                new_bg_obj = entities.BG_object(4,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='f'):
                new_bg_obj = entities.BG_object(5,x*16,y*16)
                bg_objects.add(new_bg_obj)
            elif(tile=='g'):
                new_goal = entities.Goal(x*16,y*16)
                goals.add(new_goal)

            y += 1
        x+= 1

    return blocks, enemies, bg_objects, goals, items
