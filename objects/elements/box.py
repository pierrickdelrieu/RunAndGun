import random

from objects.constants import *


class Wall(pg.sprite.Sprite):
    def __init__(self, tile_height: int, tile_width: int):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tile = pg.transform.scale(
            pg.image.load(f"{TILES_PATH}/wall.jpg"),
            (self.tile_width, self.tile_height)
        )

    def render(self, pos):
        self.pos = pos
        return self.tile


class Box(pg.sprite.Sprite):
    def __init__(self, tile_height: int, tile_width: int):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tiles = []
        for i in range(1, 4):
            self.tiles.append(
                pg.transform.scale(
                    pg.image.load(f"{TILES_PATH}/box{i}.png"),
                    (self.tile_width, self.tile_height)
                )
            )

    def render(self, pos):
        self.pos = pos
        return self.tiles[random.randint(0, len(self.tiles) - 1)]
