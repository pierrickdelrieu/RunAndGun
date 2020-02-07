import importlib
import pygame

from tiles import *
from tank import Tank

pygame.init()


class World:
    def __init__(self):
        self.move_speed = 5

        self.tile_width = 64
        self.tile_height = 64

        self.size_tiles_x_world = 30
        self.size_tiles_y_world = 16

        self.screen_width = self.tile_width * self.size_tiles_x_world
        self.screen_height = self.tile_height * self.size_tiles_y_world

        self.level = []

        self.tiles = {
            1: [
                Dirt(self.tile_height, self.tile_width),
                'full', 'floor'
            ],
            2: [
                Grass(self.tile_height, self.tile_width),
                'full', 'floor'
            ],
            3: [
                Wall(self.tile_height, self.tile_width),
                'full', 'wall'
            ],
            4: [
                Box(self.tile_height, self.tile_width),
                'full', 'wall'
            ],
        }

    def load_map(self, level_id):
        self.level = importlib.import_module(f"resources.levels.{level_id}")

    def display_map(self, screen, pos):
        x_max = int(self.screen_width / self.tile_width)
        y_max = int(self.screen_height / self.tile_height)

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * self.tile_width
                y = i * self.tile_height
                item = self.level.layouts[i][j]

                if item == 0:
                    continue

                screen.blit(
                    self.tiles[item][0].render((x, y)),
                    (x, y)
                )

        self.move_player(screen, pos)

        pygame.display.flip()
        pygame.display.update()

        return screen.copy()

    def display_players(self, screen, pos):
        player_a = Tank(screen, self.tile_width)
        player_b = Tank(screen, self.tile_width)

        pos_a = self.level.players.get(1)
        pos_b = self.level.players.get(2)

        pos_a = (self.tile_height * (pos_a[1] + pos[0][0]), self.tile_width * (pos_a[0] + pos[0][1]))
        pos_b = (self.tile_height * (pos_b[1] + pos[1][0]), self.tile_width * (pos_b[0] + pos[1][1]))

        print(pos_a)

        screen.blit(
            player_a.render(),
            (pos_a[0], pos_a[1] + self.tile_height - (self.tile_width * 178) // 489)
        )
        screen.blit(
            pygame.transform.flip(
                player_b.render(),
                True,
                False
            ), (pos_b[0], pos_b[1] + self.tile_height - (self.tile_width * 178) // 489)
        )

        pygame.display.flip()
        pygame.display.update()

        return screen.copy()

    def move_player(self, screen, pos):
        self.display_players(
            screen,
            pos
        )

        pygame.display.flip()
        pygame.display.update()

        return screen.copy()

    def screen_size(self):
        return \
            self.tile_width * self.size_tiles_x_world, \
            self.tile_height * self.size_tiles_y_world
