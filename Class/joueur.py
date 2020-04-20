import pygame as pg

from .constants import LARGEUR_TUILE, HAUTEUR_TUILE


class Joueur(pg.sprite.Sprite):
    energy: 100
    life: 100
    speed = 5
    bonds = 10
    images = {}

    is_shooting: bool = False

    def __init__(self, screen_rect, pos: tuple, facing: int, skin):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.image = self.images.get(facing)

        self.rect = self.image.get_rect(
            midbottom=(
                (pos[1] + 1) * LARGEUR_TUILE,
                (pos[0] + 1) * HAUTEUR_TUILE
            )
        )
        self.origtop = self.rect.top
        self.facing = facing

    def move(self, direction, world):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        self.image = self.images.get(self.facing)

        if direction != 0:
            self.energy -= 1

        self.rect.top = self.origtop - (self.rect.left // self.bonds % 2)

    def get_pos(self):
        pos = (self.rect.left, self.rect.top)
        return pos


class Bras(pg.sprite.Sprite):
    angle = 0
    speed = 5
    bonds = 10
    images = {}

    def __init__(self, screen_rect, pos: tuple, facing, skin):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.images = self.images.get(skin)

        self.image = self.images.get(facing).get(self.angle)
        self.rect = self.image.get_rect(
            midbottom=((pos[1] + 1) * LARGEUR_TUILE, (pos[0] + 1) * HAUTEUR_TUILE)
        )
        self.origtop = self.rect.top
        self.facing = facing

    def move(self, direction):
        if direction:
            self.facing = direction

        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        self.image = self.images[self.facing][self.angle]

        self.rect.top = self.origtop - (self.rect.left // self.bonds % 2)

    def rotate(self, angle):
        if angle != 0:
            if 15 > self.angle > -5:
                if angle == -1 and self.angle == -4 or angle == 1 and self.angle == 14:
                    return
                self.angle += angle * 2
                self.image = self.images.get(self.facing).get(self.angle)
                pg.time.wait(100)

    def get_pos(self):
        pos = (self.rect.left, self.rect.top)
        return pos
