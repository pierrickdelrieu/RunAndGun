import importlib
import pygame as pg

from .elements import *


class World:
    level_id: int

    def __init__(self):
        self.tile_width = 64
        self.tile_height = 64

        self.size_tiles_x_world = 28
        self.size_tiles_y_world = 14

        self.screen_width = self.tile_width * self.size_tiles_x_world
        self.screen_height = self.tile_height * self.size_tiles_y_world

        self.level = []

        self.tiles = {
            0: Empty(self.tile_height, self.tile_width),
            1: Dirt(self.tile_height, self.tile_width),
            2: Grass(self.tile_height, self.tile_width),
            3: Wall(self.tile_height, self.tile_width),
            4: Box(self.tile_height, self.tile_width),
        }

    def load_map(self, level_id):
        self.level_id = level_id
        self.level = importlib.import_module(f"resources.levels.{self.level_id}")

    def save_map(self):
        background = pg.Surface(self.screen_size())
        background.blit(pg.image.load(f"resources/sprites/sky.png").convert_alpha(), (0, 0))

        x_max = int(self.screen_width / self.tile_width)
        y_max = int(self.screen_height / self.tile_height)

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * self.tile_width
                y = i * self.tile_height
                item = self.level.layouts[i][j]

                background.blit(
                    self.tiles[item].render((x, y)),
                    (x, y)
                )

        pg.image.save(background, f"resources/levels/{self.level_id}.png")

    def screen_size(self):
        size = (self.tile_width * self.size_tiles_x_world, self.tile_height * self.size_tiles_y_world)
        return size
