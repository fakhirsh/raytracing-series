WIDTH = 800
HEIGHT = 800

print(f"P3\n{WIDTH} {HEIGHT}\n255")

TILE_SIZE = 100
for h in range(1,HEIGHT):
    for w in range(WIDTH):
        tile_x = w // TILE_SIZE
        tile_y = h // TILE_SIZE

        if (tile_x + tile_y) % 2 == 0:
            color = "255 0 0"
        else:
            color = "255 255 255"
        
        print(color)