import pygame as pg

from .constants import LARGEUR_TUILE, HAUTEUR_TUILE


class Joueur(pg.sprite.Sprite):
    vitesse = 5
    bonds = 10

    is_shooting: bool = False

    def __init__(self, screen_rect, pos: tuple, textures, regarde: int, peau: int):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.regarde = regarde
        self.images = textures
        self.image = textures.get(self.regarde)

        self.rect = self.image.get_rect(
            midbottom=(
                (pos[0] + 1) * LARGEUR_TUILE,
                (pos[1] + 1) * HAUTEUR_TUILE
            )
        )
        self.energie = 100
        self.vie = 100
        self.origtop = self.rect.top

    def move(self, direction, world):
        if direction:
            self.regarde = direction
        self.rect.move_ip(direction * self.vitesse, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        self.image = self.images.get(self.regarde)

        if direction != 0:
            self.energie -= 1

        self.rect.top = self.origtop - (self.rect.left // self.bonds % 2)

    def get_pos(self):
        pos = (self.rect.left, self.rect.top)
        return pos


class Bras(pg.sprite.Sprite):
    angle = 0
    vitesse = 5
    bonds = 10

    def __init__(self, screen_rect, pos: tuple, textures, regarde: int, peau: int):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.regarde = regarde
        self.images = textures
        self.image = textures.get(self.regarde)

        self.image = self.images.get(regarde).get(self.angle)
        self.rect = self.image.get_rect(
            midbottom=(
                (pos[0] + 1) * LARGEUR_TUILE,
                (pos[1] + 1) * HAUTEUR_TUILE)
        )
        self.origtop = self.rect.top

    def move(self, direction):
        if direction:
            self.regarde = direction

        self.rect.move_ip(direction * self.vitesse, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        self.image = self.images[self.regarde][self.angle]

        self.rect.top = self.origtop - (self.rect.left // self.bonds % 2)

    def rotate(self, angle):
        if angle != 0:
            if 15 > self.angle > -5:
                if angle == -1 and self.angle == -4 or angle == 1 and self.angle == 14:
                    return
                self.angle += angle * 2
                self.image = self.images.get(self.regarde).get(self.angle)
                pg.time.wait(100)

    def get_pos(self):
        pos = (self.rect.left, self.rect.top)
        return pos
