import math

import pygame
import random


class Sky(pygame.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        tile = pygame.image.load('resources/sprites/sky.png')
        self.tile = pygame.transform.scale(tile, (self.tile_width, self.tile_height))

    def render(self, pos):
        self.pos = pos
        return self.tile


class Grass(pygame.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tiles = []
        for i in range(1, 7):
            self.tiles.append(
                pygame.transform.scale(
                    pygame.image.load(f"resources/sprites/grass{i}.png"),
                    (self.tile_width, self.tile_height)
                )
            )

    def render(self, pos):
        self.pos = pos
        return self.tiles[random.randint(0, len(self.tiles) - 1)]


class Dirt(pygame.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tiles = []
        for i in range(1, 4):
            self.tiles.append(
                pygame.transform.scale(
                    pygame.image.load(f"resources/sprites/dirt{i}.png"),
                    (self.tile_width, self.tile_height)
                )
            )

    def render(self, pos):
        self.pos = pos
        return self.tiles[random.randint(0, len(self.tiles) - 1)]


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tile = pygame.transform.scale(
            pygame.image.load(f"resources/sprites/wall.jpg"),
            (self.tile_width, self.tile_height)
        )

    def render(self, pos):
        self.pos = pos
        return self.tile


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.tiles = []
        for i in range(1, 4):
            self.tiles.append(
                pygame.transform.scale(
                    pygame.image.load(f"resources/sprites/box{i}.png"),
                    (self.tile_width, self.tile_height)
                )
            )

    def render(self, pos):
        self.pos = pos
        return self.tiles[random.randint(0, len(self.tiles) - 1)]


class Player(pygame.sprite.Sprite):
    def __init__(self, tile_height, tile_width):
        super().__init__()
        self.pos = (0, 0)

        self.tile_height = tile_height
        self.tile_width = tile_width

        self.angle = 0
        self.power = 0

        bow = pygame.image.load('resources/sprites/bow.png')
        self.powers = []

        for x in range(0, 420, 70):
            for y in range(0, 360, 90):
                self.powers.append(
                    pygame.transform.scale(
                        bow.subsurface(x, y, 70, 90),
                        (self.tile_width, self.tile_height)
                    )
                )

    def render(self, pos):
        self.pos = pos
        self.rotate()
        return pygame.transform.rotate(self.powers[self.power], self.angle)

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.angle = angle
