def load_level(path):

    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))

    print(game_map)
    return game_map
