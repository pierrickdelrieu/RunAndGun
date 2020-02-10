import pygame as pg
import random


class Grass(pg.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tiles = []
        for i in range(1, 7):
            self.tiles.append(
                pg.transform.scale(
                    pg.image.load(f"resources/sprites/grass{i}.png"),
                    (self.tile_width, self.tile_height)
                )
            )

    def render(self, pos):
        self.pos = pos
        return self.tiles[random.randint(0, len(self.tiles) - 1)]
