import importlib

from .elements import *
from .constants import *


class World:
    level_id: int

    def __init__(self):
        self.tile_width = TILE_WIDTH
        self.tile_height = TILE_HEIGHT

        self.size_tiles_x_world = SIZE_X_WORLD
        self.size_tiles_y_world = SIZE_Y_WORLD

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

    def load_map(self, level_id) -> None:
        self.level_id = level_id
        self.level = importlib.import_module(f"resources.levels.{self.level_id}.map")

    def save_map(self) -> None:
        background = pg.Surface(self.screen_size())
        background.blit(
            pg.image.load(f"{TILES_PATH}/sky.jpg").convert_alpha(),
            (0, 0)
        )

        y_max = int(self.screen_height / self.tile_height)
        x_max = int(self.screen_width / self.tile_width)

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * self.tile_width
                y = i * self.tile_height
                item = self.level.layouts[i][j]

                background.blit(
                    self.tiles[item].render((x, y)),
                    (x, y)
                )

        pg.display.update()

        pg.image.save(background, f"resources/levels/{self.level_id}/map.png")

    def screen_size(self) -> tuple:
        size = (self.tile_width * self.size_tiles_x_world, self.tile_height * self.size_tiles_y_world)
        return size

    def hit_box(self) -> list:
        hit_box = []

        y_max = int(self.screen_height / self.tile_height)
        x_max = int(self.screen_width / self.tile_width)

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * self.tile_width
                y = i * self.tile_height
                item = self.level.layouts[i][j]

                if item != 0:
                    hit_box.append((x, y))

        return hit_box
